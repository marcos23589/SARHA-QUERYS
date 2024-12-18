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

# Ingresar numero de liquidacion
numero_liquidacion = int(input("Ingrese el numero de liquidacion: "))

try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv("USUARIO_ORACLE"))
    # EJECUTA LA QUERY PARA OBTENER LIQUIDACION VERTICAL
    embargos_sql = f"""SELECT
el.nro_liquidacion,
    el.cuit,
    c.descripcion,
    cl.periodo_desde,
    cl.cuil,
    el.apellido || ', ' || el.nombre as nombre_completo,
    el.descripcion_escalafon,
    el.descripcion_funcion,
    con.descripcion as convenio,
    cl.cod_concepto,
    cl.descripcion_concepto,
    cl.cod_subconcepto,
    co.remunerativo_recibo,
    cl.descripcion_subconcepto,
    cl.valor


from
    sarha.concepto_liquidacion cl,
    sarha.empleado_liquidacion el,
    sarha.cuit_organismo c,
    sarha.concepto co,
    sarha.convenio con

where
    cl.nro_liquidacion = {numero_liquidacion}
    and el.cuit = c.cuit
    and el.cuil = cl.cuil
    and cl.cod_convenio = con.cod_convenio
    and el.nro_liquidacion = cl.nro_liquidacion
    and el.no_paga is NULL
    and cl.cod_concepto in (select co.cod_concepto from sarha.concepto where co.remunerativo_recibo in (1,2) )
    and cl.valor <> 0

    -- and cl.concepto <> 899
    -- valor 1 conc de pago
    -- valor 2 aportes y descuentos/retenciones personales
    -- valor 3 contrib patronales
    -- valor 4 intermedios (ayudas para calculos)
    -- and not cl.descripcion_concepto LIKE 'INT%'
    -- SIN CONTRIBUCUIONES DEL EMPLEADOR
    -- and not cl.cod_clase_concepto = 16
    -- CONTRIBUCUIONES DEL EMPLEADOR
    -- and cl.cod_clase_concepto = 16

order by
    cl.cuil
"""
    ruta_origen = "SALIDA"
    ruta_destino = "S:/LDDAT/SARHA/REPORTES/"

    # llamamos al modulo borra_directorio(funcion delete_directory)
    borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
    df_vertical = pd.read_sql(embargos_sql, engine)

    df_vertical.to_excel(
        f"SALIDA\\LIQ-VERTICAL-{numero_liquidacion}.xlsx", index=False)

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
