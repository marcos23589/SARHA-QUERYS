import os
import sys
from datetime import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from tkinter import filedialog, Tk, simpledialog  # Importar el diálogo de entrada

sys.path.append(os.path.abspath(".."))
from dotenv import load_dotenv
from modulos import borra_directorio

# Cargar variables de entorno
load_dotenv()

# Ocultar la ventana principal de tkinter
root = Tk()
root.withdraw()

# ESTE PROGRAMA TOMA EL ARCHIVO TXT DE LA LIQUIDACION DE CPE, Y EN BASE A LA LIQUIDACION DE SARHA, COMPARA CON LOS DNI QUE AGENTES COBRAN TITULO EN LOS 2 SISTEMAS.

# Ingresar numero de liquidacion de SAHRA
numero_liquidacion = simpledialog.askinteger("Entrada", "Ingresa el número de liquidación:")

# Verifica si el número de liquidación fue ingresado
if numero_liquidacion is None:
    print("No se ingresó un número de liquidación.")
    sys.exit()  # Termina la ejecución si no se ingresó el número


consulta = f""" 
    SELECT 
        cl.cuil,
        el.NRO_DOCUMENTO as DNI,         
        el.apellido || ', ' || el.nombre as NOMBRE_COMPLETO,         
        cl.descripcion_subconcepto as TITULO,
        el.abreviatura as ORGANISMO
    FROM 
        sarha.concepto_liquidacion cl,
        sarha.empleado_liquidacion el
    where 
        el.nro_liquidacion = cl.nro_liquidacion
        and el.cuil = cl.cuil
        and cl.nro_liquidacion = {numero_liquidacion}
        and cl.cod_concepto = 18
    group by 
        el.nro_liquidacion, cl.cuil, el.apellido, el.nombre, el.abreviatura, cl.descripcion_subconcepto, el.NRO_DOCUMENTO
    """
ruta_origen = "SALIDA"


def carga_df(engine):
    # llamamos al modulo borra_directorio(funcion delete_directory)
    borra_directorio.delete_directory(ruta_origen)

    # CREA EL DATAFRAME DE CON LOS DNI/NOMBRE/ORGANISMO DE LA CONSULTA SQL
    df_vertical = pd.read_sql(consulta, engine)

    # Convertir la columna 'cuil y dni' a int64
    df_vertical["cuil"] = df_vertical["cuil"].astype("int64")
    df_vertical["dni"] = df_vertical["dni"].astype("int64")

    return df_vertical


# SE GUARDA EL EXCEL
def crear_excel(df):
    df_sin_duplicados = df.drop_duplicates(subset='dni', keep='first')
    df = df_sin_duplicados.sort_values(by = 'Organismo SARHA')
    df.to_excel(
        f'./SALIDA/SARHA_CPE_{datetime.now().strftime("%H-%M-%S")}.xlsx', index=False
    )


# cuadro de carga del archivo TXT de CPE
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
    df = pd.read_csv(archivo, sep=";", skipinitialspace=True, encoding="latin-1")

    # ACÁ SE COLOCAN LOS CÓDIGOS DE TITULOS QUE SE DEBEN FILTRAR PARA REALIZAR LA COMPARACION
    df_filtrado = df[df["CODLIQ"].isin([206, 306])]

    # Definir columnas a extraer
    columnas = ["NDOLIQ", "NOMLIQ", "CODLIQ"]

    # Inicializar un DataFrame vacío
    cpe_df = pd.DataFrame()

    # Extraer las columnas del DataFrame filtrado y añadirlas al DataFrame vacío
    for columna in columnas:
        if (
            columna in df_filtrado.columns
        ):  # Verificar si la columna existe en el archivo
            cpe_df[columna] = df_filtrado[
                columna
            ]  # Añadir la columna filtrada al DataFrame
        else:
            print(f"Columna {columna} no encontrada en el archivo.")

    cpe_df = cpe_df.rename(
        columns={"NDOLIQ": "dni", "NOMLIQ": "nombre_completo", "CODLIQ": "titulo"}
    )

    cpe_df["organismo"] = "CPE"
    return cpe_df


try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv("USUARIO_ORACLE"))
    print("conexion exitosa")
    df_sarha = carga_df(engine)
    df_cpe = cargar_archivo()

    busca_duplicados = pd.merge(df_sarha, df_cpe, on="dni", how="inner")
    del busca_duplicados["nombre_completo_y"]

    busca_duplicados = busca_duplicados.rename(
        columns={
            "nombre_completo_x": "agente",
            "titulo_x": "titulo sarha",
            "organismo_x": "Organismo SARHA",
            "titulo_y": "cod titulo cpe",
            "organismo_y": "cpe",
        }
    )
    busca_duplicados = busca_duplicados.sort_values(
        ["cuil", "titulo sarha"], ascending=[True, False]
    )
    crear_excel(busca_duplicados)

except SQLAlchemyError as e:
    print(e)
