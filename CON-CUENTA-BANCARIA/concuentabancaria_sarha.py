import os
import shutil
import sys

import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from modulos import borra_directorio

sys.path.append(os.path.abspath('..'))


# --- Dicccionario con denominaciones estandar para archivos
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

try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(
        "oracle+oracledb://jorellana:R3L4N43@10.2.2.21:1521/SAXE2012")
    # EJECUTA LA QUERY PARA OBTENER LOS EMBARGOS JUDICIALES
    embargos_sql = f"""SELECT DISTINCT
     c.cuit,
     c.descripcion as descripcion,
     cu.cuil,
     el.apellido,
     el.nombre,
     cu.nro_cuenta

 FROM
     sarha.empleado_liquidacion el,
     sarha.cuit_organismo       c,
     sarha.cuenta_empleado cu

 WHERE
     cu.cuil = el.cuil
     AND c.cuit = el.cuit
     AND c.descripcion NOT LIKE 'GCIAS'

 ORDER BY
     c.descripcion, el.apellido, el.nombre

 """
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES/"

    # llamamos al modulo borra_directorio(funcion delete_directory)
    borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
    df_embargos = pd.read_sql(embargos_sql, engine)

    # --- Obtiene organismos únicos para generar los archivos de salida
    organismos = df_embargos['descripcion'].unique()

    for organismo in organismos:
        print(f"Procesado organismo: {organismo}")
        df1 = df_embargos[df_embargos['descripcion'] == organismo]
        df1.to_excel(
            F'./SALIDA/CONCUENTA-{dict_denominaciones.get(organismo)}.xlsx', index=False)

    # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
    ruta_origen = "./SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES"
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
