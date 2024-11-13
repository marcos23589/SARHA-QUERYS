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

# QUERY QUE SE REALIZA PARA CREAR EL DF DE SARHA
consulta = f""" 
    SELECT 
        cl.cuil,
        el.NRO_DOCUMENTO as DNI,         
        el.apellido || ', ' || el.nombre as NOMBRE_COMPLETO,         
        cl.descripcion_subconcepto as TITULO,
        el.abreviatura as ORGANISMO,
        cl.valor_bruto as SARHA
    FROM 
        sarha.concepto_liquidacion cl,
        sarha.empleado_liquidacion el
    where 
        el.nro_liquidacion = cl.nro_liquidacion
        and el.cuil = cl.cuil
        and cl.nro_liquidacion = {numero_liquidacion}
        and cl.cod_concepto = 18
-- estos subconceptos corresponden a TITULO AS SECUNDARIO, TITULO AS TERCIARIO, ETC. 
--        and cl.cod_subconcepto not in (009, 010, 011, 012, 013, 014, 015, 017, 049, 9999)
        and cl.cod_subconcepto not in (9999)
    group by 
        el.nro_liquidacion, cl.cuil, el.apellido, el.nombre, el.abreviatura, cl.descripcion_subconcepto, el.NRO_DOCUMENTO, cl.valor_bruto
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


# FUNCION QUE CREA EL EXCEL
def crear_excel(df):
#    df_sin_duplicados = df.drop_duplicates(subset='dni', keep='first')
#    df = df_sin_duplicados.sort_values(by = 'Organismo SARHA')
    
    df.to_excel(
        f'./SALIDA/SARHA_CPE_{datetime.now().strftime("%H-%M-%S")}.xlsx', index=False
    )


# FUNCION QUE CREA EL CUADRO DE CARGA DEL ARCHIVO TXT DEL CPE
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
    df = pd.read_csv(archivo, sep=";", skipinitialspace=True, encoding="latin-1")

    # ACÁ SE COLOCAN LOS CÓDIGOS DE TITULOS DEL CPE QUE SE DEBEN FILTRAR PARA REALIZAR LA COMPARACION
    df_filtrado = df[df["CODLIQ"].isin([206, 306])]

    # Definir columnas a extraer
    columnas = ["NDOLIQ", "NOMLIQ", "CODLIQ", "IMPLIQ"]

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
        columns={"NDOLIQ": "dni", 
                 "NOMLIQ": "nombre_completo", 
                 "CODLIQ": "titulo", 
                 "IMPLIQ": "CPE"}
    )

    #RETORNA EL DF DEL CPE
    return cpe_df


# FUNCION QUE TOMA LOS VALORES DE BRUTO DE SARHA Y CPE, Y LOS COMPARA PARA RELLENAR LA COLUMNA "MAYOR"
def montos(df):
        # SE ITERA SOBRE TODAS LAS FILAS DEL DF Y SE COMPARAN LOS VALORES DE SARHA Y CPE
        for i in df.index:
            if(df.loc[i, "sarha"] < df.loc[i, "CPE"]):
                df.loc[i, "MAYOR"] = "CPE"
            else:
                df.loc[i, "MAYOR"] = "SARHA"
        
        return df 

# ---------------------------- ACÁ COMIENZA LA EJECUCION DEL PROGRAMA ----------------------------
try:
    # CONECTA CON LA BBDD ORACLE DE SARHA
    engine = sqlalchemy.create_engine(os.getenv("USUARIO_ORACLE"))
    print("conexion exitosa")

    # SE CREA EL DF DE SARHA
    df_sarha = carga_df(engine)

    # SE CREA EL DF DEL ARCHIVO DE CPE
    df_cpe = cargar_archivo()

    # UNE LOS DF 
    df_merge = pd.merge(df_sarha, df_cpe, on="dni", how="inner", validate='many_to_many')
    del df_merge["nombre_completo_y"]

    # SE RENOMBRAN LAS COLUMNAS
    df_merge = df_merge.rename(
        columns={
            "nombre_completo_x": "agente",
            "titulo_x": "titulo sarha",
            "organismo_x": "Organismo SARHA",
            "titulo_y": "cod titulo cpe",
        }
    )

    # SE ORDENA EL DF POR "ORGANISMO"
    df_merge = df_merge.sort_values(
        ["organismo", "cuil"], ascending=[True, True]
    )

    # SE DEFINE DONDE COBRA MAS
    df = montos(df_merge)

    # SE CREA EL EXCEL FINAL
    crear_excel(df)

# SE CAPTURA LA EXCEPCION EN CASO DE ERROR    
except SQLAlchemyError as e:
    print(e)

# ---------------------------- ACÁ FINALIZA LA EJECUCION DEL PROGRAMA ----------------------------