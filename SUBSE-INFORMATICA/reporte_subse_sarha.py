import os
import shutil
import sys
import warnings

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

from modulos import borra_directorio

sys.path.append(os.path.abspath('..'))


warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)


# Cargar variables de entorno
load_dotenv()

# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))


try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv('USUARIO_ORACLE'))
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
 """
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES/"

    # llamamos al modulo borra_directorio(funcion delete_directory)
    # borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
    df_vertical = pd.read_sql(embargos_sql, engine)

    df_vertical.to_excel(
        f'SALIDA\REPORTE-SUBSE-{numero_liquidacion}.xlsx', index=False)

    # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES/"

    # BORRO TODOS LOS ARCHIVOS DE LA CARPETA SALIDA ANTES DE GENERAR UN NUEVO ARCHIVO
    # Obtener la lista de archivos en el directorio
    archivos = os.listdir(ruta_origen)
#    # Iterar sobre la lista de archivos y eliminarlos uno por uno
#    for archivo in archivos:
#     ruta_completa = os.path.join(ruta_origen, archivo)
#    if os.path.isfile(ruta_completa):  # Verificar si es un archivo (no un directorio)
#     os.remove(ruta_completa)

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
