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

# Ingresar Periodo de liquidacion AAAAMM
periodo_liquidacion = int(input('Ingrese periodo de liquidacion AAAAMM: '))

try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv('USUARIO_ORACLE'))

    # DETALLE DE LOS CERTIFICADOS CAMPO PRESTO_SERVICIO 1, 2 y 3
    """
   1 (Certificado)  
   2 (Pendiente de Certificar) 
   3 (No Certificado)
   """
    # EJECUTA LA QUERY PARA OBTENER EL DETALLE DE LOS AGENTES CERTIFICADOS
    certificados_sql = f"""
 SELECT
     ps.periodo,
     ps.cuil,
     el.apellido || ', ' || el.nombre as nombre_completo,
     el.cuit,
     co.descripcion,
     ps.presto_servicio,
     ps.fecha_transaccion

 FROM sarha.prestacion_servicio ps,
      sarha.empleado_liquidacion el,
      sarha.cuit_organismo co

 WHERE PERIODO = '202405'
     AND (ps.PRESTO_SERVICIO = 1 OR ps.PRESTO_SERVICIO = 2 OR ps.PRESTO_SERVICIO = 3)
     and ps.cuil = el.cuil
     and el.cuit = co.cuit

 group by (ps.periodo, ps.cuil, el.apellido, el.nombre, el.cuit, co.descripcion, ps.presto_servicio, ps.fecha_transaccion)
 """
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES/"

    # llamamos al modulo borra_directorio(funcion delete_directory)
    borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE CERTIFICADOS DE LA CONSULTA SQL
    df_vertical = pd.read_sql(certificados_sql, engine)

    # CREA EL EXCEL DE CERTIFICADOS
    df_vertical.to_excel(
        f'./SALIDA/CERTIFICACION-{periodo_liquidacion}.xlsx', index=False)

    # COPIA ARCHIVOS EXCEL A CARPETA REPORTES
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES"

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
