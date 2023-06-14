import pandas as pd
import cx_Oracle
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import openpyxl
import subprocess
import shutil
import os

# CONECTA CON LA VPN DE SARHA
subprocess.call([r"CONECTA_VPN.BAT"])

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine("oracle+cx_oracle://jorellana:R3L4N43@10.2.2.21:1521/SAXE2012")
   # EJECUTA LA QUERY PARA OBTENER LOS EMBARGOS JUDICIALES
   embargos_sql = """SELECT cl.nro_liquidacion, EL.CUIT, CO.DESCRIPCION as ORGANISMO, EL.CUIL, EL.APELLIDO, EL.NOMBRE,  CL.COD_CONCEPTO, CL.COD_SUBCONCEPTO, CP.DESCRIPCION AS DESCRIPCION_CAUSA, O.CAUSA_JUDICIAL, cl.valor
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
    AND CL.nro_liquidacion = 1579 
    AND (CL.COD_CONCEPTO = 481 OR CL.COD_CONCEPTO = 482) 
    AND CL.VALOR < 0
""";
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_embargos = pd.read_sql(embargos_sql, engine)
   
   # MUESTRA TODOS LOS ORGANISMOS QUE EXISTEN EN LOS EMBARGOS
   print(df_embargos['organismo'].unique())
   
   # SEPARA LOS EMBARGOS Y GENERA LOS EXCEL DE CADA ORGANISMO
   cap_df = df_embargos[df_embargos['organismo'] == '(CAP) CONSEJO AGRARIO PROVINCIAL']
   cap_df.to_excel('./SALIDA/EMBARGOS-CAPR.xlsx', index=False)   
   
   mds_df = df_embargos[df_embargos['organismo'] == '(MDS) MINISTERIO DE DESARROLLO SOCIAL']
   mds_df.to_excel('./SALIDA/EMBARGOS-DESA.xlsx', index=False)
   
   mpci_df = df_embargos[df_embargos['organismo'] == '(MPCI) MINISTERIO DE PRODUCCIÓN COMERCIO E INDUSTRIA']
   mpci_df.to_excel('./SALIDA/EMBARGOS-PROD.xlsx', index=False)
   
   mtes_df = df_embargos[df_embargos['organismo'] == '(MTES) MINISTERIO TRABAJO, EMPLEO Y SEG. SOCIAL']
   mtes_df.to_excel('./SALIDA/EMBARGOS-TRAB.xlsx', index=False)
   
   mgo_df = df_embargos[df_embargos['organismo'] == '(MGO) MINISTERIO DE GOBIERNO']
   mgo_df.to_excel('./SALIDA/EMBARGOS-MGOB.xlsx', index=False)
   
   mefi_df = df_embargos[df_embargos['organismo'] == '(MEFI) MINISTERIO DE ECONOMIA, FINANZAS E INFRAESTRUCTURA']
   mefi_df.to_excel('./SALIDA/EMBARGOS-MEFI.xlsx', index=False)
   
   msgg_df = df_embargos[df_embargos['organismo'] == '(MSGG) MINISTERIO SECRETARIA GENERAL DE LA GOBERNACION']
   msgg_df.to_excel('./SALIDA/EMBARGOS-MSGG.xlsx', index=False)
   
   mseg_df = df_embargos[df_embargos['organismo'] == '(MSEG) MINISTERIO DE SEGURIDAD']
   mseg_df.to_excel('./SALIDA/EMBARGOS-SEGU.xlsx', index=False)
   
   csc_df = df_embargos[df_embargos['organismo'] == '(CSC) CASA DE SANTA CRUZ']
   csc_df.to_excel('./SALIDA/EMBARGOS-CASA.xlsx', index=False)
   
   gob_df = df_embargos[df_embargos['organismo'] == '(GOB) GOBERNACIÓN']
   gob_df.to_excel('./SALIDA/EMBARGOS-GOBE.xlsx', index=False)
   
   jgm_df = df_embargos[df_embargos['organismo'] == '(JGM) MINISTERIO JEFATURA DE GABINETE DE MINISTROS']
   jgm_df.to_excel('./SALIDA/EMBARGOS-JGAB.xlsx', index=False)
   
   htd_df = df_embargos[df_embargos['organismo'] == '(HTD) HONORABLE TRIBUNAL DISCIPLINARIO']
   htd_df.to_excel('./SALIDA/EMBARGOS-HTDI.xlsx', index=False)
   
   # TERMINA LA CONEXION DE LA VPN
   subprocess.call([r"DESCONECTA_VPN.BAT"])
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="./SALIDA"
   ruta_destino="S:/LDDAT-SAC/SARHA-SAC/EMBARGOS"
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
except SQLAlchemyError as e:
   print(e)