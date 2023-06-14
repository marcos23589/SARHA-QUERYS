import pandas as pd
import cx_Oracle
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import openpyxl
import subprocess
import shutil
import os

# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

# CONECTA CON LA VPN DE SARHA
subprocess.call([r"LIQ-VERTICAL\CONECTA_VPN.BAT"])

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+cx_oracle://jorellana:R3L4N43@10.2.2.21:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LIQUIDACION VERTICAL
   embargos_sql = f"""SELECT 
	el.nro_liquidacion,
    el.cuit,
    c.descripcion,
    cl.periodo_desde,
    cl.cuil,
    el.apellido,
    el.nombre,
    el.cod_escalafon,
    el.descripcion_escalafon,
    el.cod_funcion,
    el.descripcion_funcion,
    cl.cod_concepto,
    cl.descripcion_concepto,
    cl.cod_subconcepto,
    cl.descripcion_subconcepto,
    cl.valor
    
from 
    sarha.concepto_liquidacion cl,
    sarha.empleado_liquidacion el,
    sarha.cuit_organismo c

where 
    cl.nro_liquidacion = {numero_liquidacion} 
    and el.cuit = c.cuit
    and el.cuil = cl.cuil
    and el.nro_liquidacion = cl.nro_liquidacion
order by
    cl.cuil
""";
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'LIQ-VERTICAL\SALIDA\LIQ-VERTICAL-{numero_liquidacion}.xlsx', index=False)
   
   # TERMINA LA CONEXION DE LA VPN
   subprocess.call([r"LIQ-VERTICAL\DESCONECTA_VPN.BAT"])
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="LIQ-VERTICAL\SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES/"
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
except SQLAlchemyError as e:
   print(e)