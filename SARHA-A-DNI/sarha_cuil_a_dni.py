import os
import shutil
import subprocess
import sys

import openpyxl
import oracledb
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath('..'))
from dotenv import load_dotenv

import modulos
from modulos import borra_directorio

# Cargar variables de entorno
load_dotenv()
# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine(os.getenv('USUARIO_ORACLE'))
   # EJECUTA LA QUERY PARA OBTENER LOS DESCUENTOS DEL 4% y 6,4%
   embargos_sql = f""" 
SELECT substr(cl.cuil, 3, 8) as DNI,
    el.apellido || ', ' || el.nombre as NOMBRE_COMPLETO 
    
FROM 
    sarha.concepto_liquidacion cl,
    sarha.empleado_liquidacion el
where 
    el.nro_liquidacion = cl.nro_liquidacion
    and el.cuil = cl.cuil
    and cl.nro_liquidacion = 13238
group by el.nro_liquidacion, cl.cuil, el.apellido, el.nombre
""";
   ruta_origen="SALIDA"

   # llamamos al modulo borra_directorio(funcion delete_directory) 
   borra_directorio.delete_directory(ruta_origen)
   
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'./SALIDA/SARHA-DNI-{numero_liquidacion}.xlsx', index=False)

   print("Proceso terminado correctamente")   
except SQLAlchemyError as e:
   print(e)