import os
import shutil
import subprocess
import sys

import openpyxl
import oracledb
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath('..'))
from dotenv import load_dotenv

import modulos
from modulos import borra_directorio

# Cargar variables de entorno
load_dotenv()
# Ingresar numero de liquidacion
numero_liquidacion = int(input('Ingrese el numero de liquidacion: '))

try:
   # CONECTA CON LA BBDD ORACLE DE SARHA
   engine = sqlalchemy.create_engine(os.getenv('USUARIO_ORACLE'))
   # EJECUTA LA QUERY PARA OBTENER LOS DESCUENTOS DEL 4% y 6,4%
   ganancias_sql = f"""select EL.NRO_LIQUIDACION, EL.CUIL, EL.APELLIDO, EL.NOMBRE, EL.ABREVIATURA, EL.CUIT, EL.TOTAL_REMUNERACIONES, CL.COD_CONCEPTO, CL.DESCRIPCION_CONCEPTO, CL.VALOR, WEB.FECHA_PRESENTACION_AFIP
    FROM SARHA.EMPLEADO_LIQUIDACION EL
    INNER JOIN SARHA.CONCEPTO_LIQUIDACION CL ON EL.CUIL = CL.CUIL AND CL.NRO_LIQUIDACION = {numero_liquidacion}   --<<<<ACTUALIZAR AL NÚMERO DE LIQUIDACIÓN ANALIZADA
    LEFT JOIN (
    SELECT 
    CUIL, MAX(FECHA_PRESENTACION) FECHA_PRESENTACION_AFIP
    FROM SARHA.GANANCIA_DEDUCCIONES_WEB
    Where
    PERIODO = 2024
    AND ESTADO = 'A '
    GROUP BY CUIL) WEB ON WEB.CUIL = EL.CUIL
    Where
    EL.nro_liquidacion  = {numero_liquidacion}   --<<<<ACTUALIZAR AL NÚMERO DE LIQUIDACIÓN ANALIZADA
    AND CL.COD_CONCEPTO IN (327,332)
    and (EL.NO_PAGA is null or EL.NO_PAGA =2)
    AND CL.VALOR <> 0                            --<<<<PARA QUE TRAIGA A LOS QUE SE LES CALCULA ALGO DE IMPUESTO A LAS GANANCIAS
    --AND EL.TOTAL_REMUNERACIONES <= 3200000       --<<<<PARA QUE TRAIGA A LOS QUE TIENEN SUELDO MENOR AL TOPE 
    --AND WEB.FECHA_PRESENTACION_AFIP IS NOT NULL  --<<<<PARA QUE TRAIGA A LOS QUE HAN PRESENTADO ALGUNA VEZ SIRADIG
    --AND WEB.FECHA_PRESENTACION_AFIP > TO_DATE('01/09/2024 00:00:00', 'DD/MM/YYYY HH24:MI:SS')              --<<<< SI SE QUIERE SABER LAS PRESENTACIONES DE SIRADIG REALIZADAS DESDE CIERTO DIA
    ORDER BY EL.CUIL
    --WEB.FECHA_PRESENTACION_AFIP desc --<<<<ORDENA POR FECHA DE PRESENTACION DE SIRADIG
    """;
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES/"
   
   # llamamos al modulo borra_directorio(funcion delete_directory) 
   
   borra_directorio.delete_directory(ruta_origen)
   # CREA EL DATAFRAME DE EMBARGOS DE LA CONSULTA SQL
   df_vertical = pd.read_sql(ganancias_sql, engine)
       
   df_vertical.to_excel(f'./SALIDA/HABERES-SIRADIG-F572-{numero_liquidacion}.xlsx', index=False)
   
   # COPIA ARCHIVOS EXCEL A CARPETA EMBARGOS
   ruta_origen="SALIDA"
   ruta_destino="S:/LDDAT/SARHA/REPORTES"
    
   #Copio archivos a la carpeta del servidor   
   shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
   print("Proceso terminado correctamente")   
except SQLAlchemyError as e:
   print(e)