import os
import shutil
import sys

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath('..'))
from modulos import borra_directorio

# Cargar variables de entorno
load_dotenv()


contador = 0

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
    '(ISPRO) ISPRO': 'ISPRO',
    '(FDE) FISCALIA DE ESTADO': 'FISC',
    '(POSC) UNIDAD EJECUTORA PORTUARIA DE LA PROV. DE SC': 'POSC',
    '(HTC) TRIBUNAL DE CUENTAS DE LA PROV. DE SC ': 'HTCU'
}


numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv('USUARIO_ORACLE'))
    # EJECUTA LA QUERY PARA OBTENER LOS EMBARGOS JUDICIALES
    embargos_sql = f"""SELECT cl.nro_liquidacion,
    EL.CUIT,
    CO.DESCRIPCION as ORGANISMO,
    EL.CUIL,
    EL.APELLIDO,
    EL.NOMBRE,
    CL.COD_CONCEPTO,
    CL.COD_SUBCONCEPTO,
    CP.DESCRIPCION AS DESCRIPCION_CAUSA,
    O.CAUSA_JUDICIAL,
    cl.valor

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
     AND EL.NO_PAGA IS NULL
 """

    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/EMBARGOS/"

    # llamamos al modulo borra_directorio(funcion delete_directory)
    borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
    df_embargos = pd.read_sql(embargos_sql, engine)

    # --- Obtiene organismos únicos para generar los archivos de salida
    organismos = df_embargos['organismo'].unique()

    for organismo in organismos:
        contador += 1
        print(f"Procesado organismo: {organismo}")
        df1 = df_embargos[df_embargos['organismo'] == organismo]
        df1.to_excel(
            F'./SALIDA/EMBARGOS-SAC-{dict_denominaciones.get(organismo)}.xlsx', index=False)

    # Verifico la cantidad de organismos
    if contador > 0:
        print(f"Cantidad de organismos: {contador}")
    else:
        print("No hay embargos")

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
