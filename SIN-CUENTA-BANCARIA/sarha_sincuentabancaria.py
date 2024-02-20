import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import openpyxl
import subprocess
import shutil
import os
import oracledb


### --- Dicccionario con denominaciones estandar para archivos
dict_denominaciones = {
	'(CAP) CONSEJO AGRARIO PROVINCIAL': 'CAPR',
	'(MDS) MINISTERIO DE DESARROLLO SOCIAL': 'DESA',
	'(MPCI) MINISTERIO DE PRODUCCIÓN COMERCIO E INDUSTRIA': 'PROD',
	'(MTES) MINISTERIO TRABAJO, EMPLEO Y SEG. SOCIAL': 'TRAB',
	'(MGO) MINISTERIO DE GOBIERNO': 'MGOB',
	'(MEFI) MINISTERIO DE ECONOMIA, FINANZAS E INFRAESTRUCTURA': 'MEFI',
	'(MSGG) MINISTERIO SECRETARIA GENERAL DE LA GOBERNACION': 'MSGG',
	'(MSEG) MINISTERIO DE SEGURIDAD': 'SEGU',
	'(CSC) CASA DE SANTA CRUZ': 'CASA',
	'(GOB) GOBERNACIÓN': 'GOBE',
	'(JGM) MINISTERIO JEFATURA DE GABINETE DE MINISTROS': 'JGAB',
	'(HTD) HONORABLE TRIBUNAL DISCIPLINARIO': 'HTDI',
    '(LOAS) LOTERIA DE ACCION SOCIAL DE STA CRUZ': 'LOAS',
    '(MII) MINISTERIO DE LA IGUALDAD E INTEGRACIÓN': 'MIEI',
    '(ICT) INSTITUTO DE CIENCIA, TECNOLOGIA E INNOVACION': 'CYTEC',
    '(ISPRO) ISPRO': 'ISPRO'	
}



#numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

# CONECTA CON LA VPN DE SARHA
conecta = 'rasdial "MEFI-01" "MEFI-01" "JPP33D1"' 
conexion_vpn = subprocess.run(conecta, capture_output=True, text=True)
#subprocess.call([r"CONECTA_VPN.BAT"])

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+oracledb://jorellana:R3L4N43@10.2.2.21:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LOS EMBARGOS JUDICIALES
   embargos_sql = f"""SELECT DISTINCT
    c.cuit,
    c.descripcion as descripcion,
    el.cuil,
    el.apellido,
    el.nombre,
    cu.nro_cuenta

FROM
    sarha.cuit_organismo       c,
    sarha.empleado_liquidacion el    

LEFT JOIN
    sarha.cuenta_empleado cu

ON el.cuil = cu.cuil    

WHERE
    c.cuit = el.cuit AND
    c.descripcion NOT LIKE 'GCIAS' AND
    cu.cuil IS NULL

ORDER BY
    c.cuit, el.apellido, el.nombre
""";
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_embargos = pd.read_sql(embargos_sql, engine)
   
   ### --- Obtiene organismos únicos para generar los archivos de salida
   organismos = df_embargos['descripcion'].unique()
   
   for organismo in organismos:
      print(f"Procesado organismo: {organismo}")
      df1 = df_embargos[df_embargos['descripcion'] == organismo]
      df1.to_excel(F'./SALIDA/SINCUENTA-{dict_denominaciones.get(organismo)}.xlsx', index=False)
   
   # TERMINA LA CONEXION DE LA VPN
   desconecta = 'rasdial "MEFI-01" /DISCONNECT'
   desconexion_vpn = subprocess.run(desconecta, capture_output=True, text=True)
   #subprocess.call([r"DESCONECTA_VPN.BAT"])
   
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="./SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES"
   
   # BORRO TODOS LOS ARCHIVOS DE LA CARPETA SALIDA ANTES DE GENERAR UN NUEVO ARCHIVO
   # Obtener la lista de archivos en el directorio
   archivos = os.listdir(ruta_origen)   
   # Iterar sobre la lista de archivos y eliminarlos uno por uno
   for archivo in archivos:
    ruta_completa = os.path.join(ruta_origen, archivo)
   if os.path.isfile(ruta_completa):  # Verificar si es un archivo (no un directorio)
    os.remove(ruta_completa)
    
   #Copio archivos a la carpeta del servidor   
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")   
except SQLAlchemyError as e:
   print(e)