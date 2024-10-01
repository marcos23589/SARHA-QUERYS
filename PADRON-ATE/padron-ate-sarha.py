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
   # EJECUTA LA QUERY PARA OBTENER LOS AFILIADOS DE ATE CON SU RESPECTIVA LOCALIDAD
   embargos_sql = f"""SELECT * 
FROM (
    SELECT 
        el.cuit,
        co.descripcion,
        cl.cuil,
        el.apellido, 
        el.nombre,
        el.descripcion_sucursal as localidad,
        sum(case when cl.cod_concepto = 488 then cl.valor else 0 end) as CODIGO488,
        sum(case when cl.cod_concepto = 489 then cl.valor else 0 end) as CODIGO489,
        sum(case when cl.cod_concepto = 490 then cl.valor else 0 end) as CODIGO490

    FROM 
        sarha.concepto_liquidacion cl,
        sarha.empleado_liquidacion el,
        sarha.cuit_organismo co,
        sarha.empleado em
    where 
        el.nro_liquidacion = cl.nro_liquidacion
        and em.cuil = el.cuil
        and el.cuil = cl.cuil
        and el.cuit = co.cuit
        and cl.nro_liquidacion = {numero_liquidacion}
        and el.no_paga is null
    
     group by el.cuit, co.descripcion, cl.cuil, el.apellido, el.nombre, el.descripcion_sucursal
     )
WHERE 
    not (CODIGO488 = 0 and CODIGO489 = 0 and CODIGO490 = 0)
""";
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/DESCUENTOS/"
   
   # llamamos al modulo borra_directorio(funcion delete_directory) 
   borra_directorio.delete_directory(ruta_origen)
   
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'./SALIDA/SARHA-PADRON-ATE.xlsx', index=False)
      
   #Copio archivos a la carpeta del servidor   
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")
except SQLAlchemyError as e:
   print(e)