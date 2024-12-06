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

# Crear el motor de SQLAlchemy utilizando la configuración del entorno
engine = sqlalchemy.create_engine(os.getenv('USUARIO_GANANCIAS'))

query = f"""
update SARHA.PARAMETRO_GRAL_CUIT
set valor = '05' -----> cambiar el valor de 02 a 05 cuando haya que acreditar el sac, recordar de volverlo a cambiar a 02 (set valor = '02') luego de realizar la      interfase de acreditación de sac
where COD_PARAMETRO = 'BANCO_SERVICIO_SC' -----> una vez controlado que se haya realizado el cambio correctamente (verificar con la cantidad de registros) , recordar commitear
    """
try:
    with engine.connect() as connection:
       result = connection.execute(sqlalchemy.text(query))
    
    print(f"Registros afectados: {result.rowcount}")
        
        # Confirmar los cambios
    connection.commit()
    print("Transacción realizada con éxito.")

except SQLAlchemyError as e:
    print(f"Ocurrió un error: {e}")