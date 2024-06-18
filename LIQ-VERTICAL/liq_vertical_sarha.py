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
    engine = sqlalchemy.create_engine(os.getenv("USUARIO_ORACLE"))
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
    co.remunerativo_recibo,
    cl.descripcion_subconcepto,
    cl.valor
    
from 
    sarha.concepto_liquidacion cl,
    sarha.empleado_liquidacion el,
    sarha.cuit_organismo c,
    sarha.concepto co

where 
    cl.nro_liquidacion = {numero_liquidacion}
    and el.cuit = c.cuit
    and el.cuil = cl.cuil
    and el.nro_liquidacion = cl.nro_liquidacion
    and el.no_paga is NULL
    -- or el.no_paga = 2
    and cl.cod_concepto in (select co.cod_concepto from sarha.concepto where co.remunerativo_recibo in (1,2) )
    and cl.cod_concepto <> 899
    
    -- valor 1 conc de pago
    -- valor 2 aportes y descuentos/retenciones personales
    -- valor 3 contrib patronales
    -- valor 4 intermedios (ayudas para calculos)
    --
    
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

    df_vertical.to_excel(f"SALIDA\LIQ-VERTICAL-{numero_liquidacion}.xlsx", index=False)

    # Copio archivos a la carpeta del servidor
    shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
    print("Proceso terminado correctamente")
except SQLAlchemyError as e:
    print(e)
