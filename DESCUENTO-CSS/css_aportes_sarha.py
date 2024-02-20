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
   embargos_sql = f"""SELECT 
    el.nro_liquidacion,
    el.cuit,
    co.descripcion,
    cl.cuil,
    el.apellido || ', ' || el.nombre as nombre_completo, 
    sum(case when cl.cod_clase_concepto = 1 and not cl.cod_concepto = 70 and not cl.cod_concepto = 617 then  cl.valor else 0 end) as REMUNERATIVO,
    sum(case when cl.cod_concepto = 322 or cl.cod_concepto = 622 or cl.cod_concepto = 323 or cl.cod_concepto = 623 then cl.valor else 0 end) as RETENCION_CSS

FROM 
    sarha.concepto_liquidacion cl,
    sarha.empleado_liquidacion el,
    sarha.cuit_organismo co
where 
    el.nro_liquidacion = cl.nro_liquidacion
    and el.cuil = cl.cuil
    and el.cuit = co.cuit
    and cl.nro_liquidacion = {numero_liquidacion}
    and el.no_paga is null
group by el.nro_liquidacion, el.cuit, co.descripcion, cl.cuil, el.apellido, el.nombre
""";
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES/"
   
   # llamamos al modulo borra_directorio(funcion delete_directory) 
   
   borra_directorio.delete_directory(ruta_origen)
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'./SALIDA/APORTES-CSS-{numero_liquidacion}.xlsx', index=False)
   
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES"
    
   #Copio archivos a la carpeta del servidor   
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")   
except SQLAlchemyError as e:
   print(e)