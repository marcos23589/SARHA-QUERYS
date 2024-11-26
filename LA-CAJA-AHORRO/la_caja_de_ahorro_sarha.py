import os
import shutil
import sys

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

from modulos import borra_directorio

sys.path.append(os.path.abspath('..'))


# Cargar variables de entorno
load_dotenv()

# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv('USUARIO_ORACLE'))
    # EJECUTA LA QUERY PARA OBTENER LOS DESCUENTOS DEL 4% y 6,4%
    embargos_sql = f"""SELECT *
 FROM (
     SELECT
         el.cuit,
         co.descripcion,
         cl.cuil,
         el.apellido,
         el.nombre,
         em.fecha_nacimiento,
         sum(case when cl.cod_clase_concepto = 1 and not cl.cod_concepto = 70 and not cl.cod_concepto = 617 then  cl.valor else 0 end) as REMUNERATIVO,
         sum(case when cl.cod_concepto = 352 then cl.valor else 0 end) as CODIGO352,
         sum(case when cl.cod_concepto = 353 then cl.valor else 0 end) as CODIGO353,
         sum(case when cl.cod_concepto = 354 then cl.valor else 0 end) as CODIGO354,
         sum(case when cl.cod_concepto = 355 then cl.valor else 0 end) as CODIGO355,
         sum(case when cl.cod_concepto = 356 then cl.valor else 0 end) as CODIGO356
     FROM
         sarha.concepto_liquidacion cl,
         sarha.empleado_liquidacion el,
         sarha.cuit_organismo co,
         sarha.empleado em
     where
         el.nro_liquidacion = cl.nro_liquidacion
         and em.cuil = el.cuil
         and el.cuil = cl.cuil
         and el.cuit = co.cuit
         and cl.nro_liquidacion = {numero_liquidacion}
         and el.no_paga is null

      group by el.cuit, co.descripcion, cl.cuil, el.apellido, el.nombre, em.fecha_nacimiento
      )
 WHERE
     not (CODIGO352 = 0 and CODIGO353 = 0 and CODIGO354 = 0 and CODIGO355 = 0 and CODIGO356 = 0)
 """
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/DESCUENTOS/"

    # llamamos al modulo borra_directorio(funcion delete_directory)
    borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
    df_vertical = pd.read_sql(embargos_sql, engine)

    df_vertical.to_excel(
        f'./SALIDA/SARHA-LA CAJA AHORRO SEGUROS.xlsx', index=False)

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
