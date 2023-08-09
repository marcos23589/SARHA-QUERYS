import pandas as pd
import oracledb
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import openpyxl
import subprocess
import shutil
import os

# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

# # CONECTA CON LA VPN DE SARHA
# conecta = 'rasdial "MEFI-01" "MEFI-01" "JPP33D1"' 
# conexion_vpn = subprocess.run(conecta, capture_output=True, text=True)
# #subprocess.call([r"CONECTA_VPN.BAT"])

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+oracledb://jorellana:R3L4N43@10.0.56.10:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LIQUIDACION VERTICAL
   embargos_sql = f"""SELECT 
el.nro_liquidacion,
    el.cuit,
    c.descripcion,
    cl.periodo_desde,
    cl.cuil,
    el.apellido || ', ' || el.nombre as nombre_completo,
    -- el.cod_escalafon,
    el.descripcion_escalafon,
    -- el.cod_funcion,
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
    and el.no_paga is NULL
    and not cl.descripcion_concepto LIKE 'INT%'	    
    -- SIN CONTRIBUCUIONES DEL EMPLEADOR
    and not cl.cod_clase_concepto = 16
    -- CONTRIBUCUIONES DEL EMPLEADOR
    -- and cl.cod_clase_concepto = 16
    
order by
    cl.cuil
""";
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(embargos_sql, engine)
       
   df_vertical.to_excel(f'SALIDA\LIQ-VERTICAL-{numero_liquidacion}.xlsx', index=False)
   
#    # TERMINA LA CONEXION DE LA VPN
#    desconecta = 'rasdial "MEFI-01" /DISCONNECT'
#    desconexion_vpn = subprocess.run(desconecta, capture_output=True, text=True)
#    #subprocess.call([r"DESCONECTA_VPN.BAT"])
   
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES/"
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")
except SQLAlchemyError as e:
   print(e)