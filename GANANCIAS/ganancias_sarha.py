import os
import shutil
import subprocess
import sys

import openpyxl
import oracledb
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath(".."))
from dotenv import load_dotenv

import modulos
from modulos import borra_directorio

# Cargar variables de entorno
load_dotenv()
# Ingresar numero de liquidacion
numero_liquidacion = int(input("Ingrese el numero de liquidacion: "))

try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv("USUARIO_GANANCIAS"))

    embargos_sql = f"""SELECT 
    el.nro_liquidacion,
    el.cuit,
    co.descripcion,
    cl.cuil,
    el.apellido,
    el.nombre as nombre_completo,
    SUM(
        CASE 
            WHEN cl.cod_clase_concepto = 7 AND (cl.cod_concepto = 8023 OR cl.cod_concepto = 8121 OR cl.cod_concepto = 8770 OR cl.cod_concepto = 8021) 
            THEN cl.valor 
            ELSE 0 
        END
    ) as BRUTO,
    SUM(
        CASE 
            WHEN cl.cod_concepto = 327 
            THEN cl.valor 
            ELSE 0 
        END
    ) as RETENCION_GCIAS
FROM 
    sarha.empleado_liquidacion el
JOIN 
    sarha.concepto_liquidacion cl ON el.nro_liquidacion = cl.nro_liquidacion AND el.cuil = cl.cuil
JOIN 
    sarha.cuit_organismo co ON el.cuit = co.cuit 
WHERE 
    cl.nro_liquidacion = {numero_liquidacion}
    AND el.no_paga IS NULL
GROUP BY 
    el.nro_liquidacion, 
    el.cuit, 
    co.descripcion, 
    cl.cuil, 
    el.apellido, 
    el.nombre
"""
    ruta_origen = "SALIDA"
    ruta_destino = "S:\LDDAT\SARHA\REPORTES"

    # llamamos al modulo borra_directorio(funcion delete_directory)

    borra_directorio.delete_directory(ruta_origen)
    # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
    df_vertical = pd.read_sql(embargos_sql, engine)

    # filtro los cuiles con retenciones en 0
    df_filtrado = df_vertical[(df_vertical["retencion_gcias"] != 0)]

    df_filtrado.to_excel(f"./SALIDA/GANANCIAS-{numero_liquidacion}.xlsx", index=False)

    # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/GANANCIAS"

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
