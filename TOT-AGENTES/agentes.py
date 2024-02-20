import pandas as pd
import oracledb
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import openpyxl
import subprocess
import shutil
import os
import sys
sys.path.append(os.path.abspath('..'))
from modulos import borra_directorio
import modulos

# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+oracledb://jorellana:R3L4N43@10.0.56.10:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LOS DESCUENTOS DEL 4% y 6,4%
   embargos_sql = f"""SELECT O.CUIT, O.DESCRIPCION, E.CUIL, E.APELLIDO, E.NOMBRE 
FROM SARHA.empleado_liquidacion E JOIN SARHA.cuit_organismo O 
ON E.CUIT = O.CUIT  
WHERE NRO_LIQUIDACION = {numero_liquidacion}
""";
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES/"
   
   # llamamos al modulo borra_directorio(funcion delete_directory) 
   borra_directorio.delete_directory(ruta_origen)
   
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'./SALIDA/AGENTES-{numero_liquidacion}.xlsx', index=False)
    
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES"
   
   #Copio archivos a la carpeta del servidor   
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")   
except SQLAlchemyError as e:
   print(e)