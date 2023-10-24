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
   '(ISPRO) ISPRO': 'ISPRO',
   '(FDE) FISCALIA DE ESTADO': 'FDE'
}




numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

# # CONECTA CON LA VPN DE SARHA
# conecta = 'rasdial "MEFI-01" "MEFI-01" "JPP33D1"' 
# conexion_vpn = subprocess.run(conecta, capture_output=True, text=True)
# #subprocess.call([r"CONECTA_VPN.BAT"])

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+oracledb://jorellana:R3L4N43@10.0.56.10:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LOS EMBARGOS JUDICIALES
   embargos_sql = f"""SELECT cl.nro_liquidacion, EL.CUIT, CO.DESCRIPCION as ORGANISMO, EL.CUIL, EL.APELLIDO, EL.NOMBRE,  CL.COD_CONCEPTO, CL.COD_SUBCONCEPTO, CP.DESCRIPCION AS DESCRIPCION_CAUSA, O.CAUSA_JUDICIAL, cl.valor
FROM SARHA.concepto_liquidacion CL,
    SARHA.empleado_liquidacion EL,
    SARHA.cuit_organismo CO,
    SARHA.embargo_concepto EC,
    SARHA.OFICIO O,
    SARHA.CONCEPTO CP

WHERE CL.CUIL = EL.CUIL 
    AND CL.NRO_LIQUIDACION = EL.NRO_LIQUIDACION 
    AND EL.CUIT = CO.CUIT
    AND EC.CUIL = CL.CUIL
    AND CL.COD_CONCEPTO = EC.COD_CONCEPTO
    AND CL.COD_CONCEPTO = CP.COD_CONCEPTO
    AND CL.COD_SUBCONCEPTO = EC.COD_SUBCONCEPTO
    AND EC.COD_OFICIOS = O.COD_OFICIOS
    AND CL.nro_liquidacion = {numero_liquidacion}
    AND (CL.COD_CONCEPTO = 481 OR CL.COD_CONCEPTO = 482) 
    AND CL.VALOR < 0
""";
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_embargos = pd.read_sql(embargos_sql, engine)
   
   ### --- Obtiene organismos únicos para generar los archivos de salida
   organismos = df_embargos['organismo'].unique()
   
   for organismo in organismos:
      print(f"Procesado organismo: {organismo}")
      df1 = df_embargos[df_embargos['organismo'] == organismo]
      df1.to_excel(F'./SALIDA/EMBARGOS-{dict_denominaciones.get(organismo)}.xlsx', index=False)
   
   # # TERMINA LA CONEXION DE LA VPN
   # desconecta = 'rasdial "MEFI-01" /DISCONNECT'
   # desconexion_vpn = subprocess.run(desconecta, capture_output=True, text=True)
   # #subprocess.call([r"DESCONECTA_VPN.BAT"])
   
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="./SALIDA"
   ruta_destino="S:/LDDAT/SARHA/EMBARGOS"
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")   
except SQLAlchemyError as e:
   print(e)