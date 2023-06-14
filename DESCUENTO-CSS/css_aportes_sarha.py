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
subprocess.call([r"DESCUENTO-CSS\CONECTA_VPN.BAT"])

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+cx_oracle://jorellana:R3L4N43@10.2.2.21:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LOS DESCUENTOS DEL 4% y 6,4%
   embargos_sql = f"""SELECT C.NRO_LIQUIDACION, A.CUIT, A.CUIL, A.APELLIDO, A.NOMBRE, A.TOTAL_REMUNERACIONES,  SUM(VALOR) AS DESCUENTO_TOTAL
FROM SARHA.CONCEPTO_LIQUIDACION C 
JOIN SARHA.EMPLEADO_LIQUIDACION A
ON A.CUIL = C.CUIL AND A.NRO_LIQUIDACION = C.NRO_LIQUIDACION 
WHERE A.NRO_LIQUIDACION = {numero_liquidacion} AND (C.COD_CONCEPTO = 322 OR C.COD_CONCEPTO = 622 OR C.COD_CONCEPTO = 323 OR C.COD_CONCEPTO = 623)
group by C.NRO_LIQUIDACION, A.CUIT, A.CUIL, A.APELLIDO, A.NOMBRE, A.TOTAL_REMUNERACIONES
""";
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'DESCUENTO-CSS\SALIDA\APORTES-CSS-{numero_liquidacion}.xlsx', index=False)
   
   # TERMINA LA CONEXION DE LA VPN
   subprocess.call([r"DESCUENTO-CSS\DESCONECTA_VPN.BAT"])
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="DESCUENTO-CSS\SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES"
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
except SQLAlchemyError as e:
   print(e)