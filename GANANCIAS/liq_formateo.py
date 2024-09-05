import datetime
import pandas as pd
from tkinter import filedialog
from pathlib import Path

# si se carga el archivo TXT que sale desde el programa LIQAFIP.COB, es para crear el excel
# si se carga el archivo XLS, es para eliminar los CUILES repetidos y sumar los importes


# cuadro de carga del archivo
def cargar_archivo():
    archivo = filedialog.askopenfilename(
        filetypes=[
            ("Archivos XLSX", "*.xlsx"),
            ("Archivos XLS", "*.xls"),
            ("Archivos TXT", "*.txt"),
        ]
    )

    # obtenemos la extension del archivo cargado
    extension = Path(archivo).suffix

    if extension == ".txt" or extension == ".TXT":
        df = pd.read_csv(archivo, sep=";", skipinitialspace=True, encoding="latin-1")
        # se elimina la ultima columna vacia
        last_column = df.columns[-1]
        df = df.drop(last_column, axis=1)

        # se agregan las cabeceras de las columnas
        df.columns = columnas
        
        # Divide los valores por 100
        df[columnas_a_sumar] = df[columnas_a_sumar] / 100
    else:
        df = pd.read_excel(archivo, sheet_name="Hoja1")
    return df


# Lista personalizada para los nombres de las columnas
columnas = [
    "CUIT",
    "ORGANISMO",
    "LEGAJO",
    "AGENTE",
    "CUIL",
    "REMUNERACIONES",
    "ASIGNACIONES FLIARES",
    "HS EXTRAS",
    "SAC",
    "%REMU",
    "APORTES JUBILATORIOS",
    "APORTES O.SOCIAL",
    "SINDICATO",
    "SEGURO DE VIDA",
]

# Definir las columnas que deben sumarse
columnas_a_sumar = columnas[5:]

# funcion que ordena el DF por CUIL y suma los valores
def consolidar_cuiles(df):

    # se agregan las cabeceras de las columnas
    df.columns = columnas

    # Identificar las filas con CUIL duplicados
    cuil_duplicados = df[df.duplicated("CUIL", keep=False)]

    # Crear una lista para almacenar las filas consolidadas
    filas_consolidadas = []

    # Recorrer los CUIL duplicados
    for cuil, grupo in cuil_duplicados.groupby("CUIL"):
        # Sumar las filas del grupo
        fila_sumada = grupo.iloc[0].copy()  # Tomar la primera fila como base

        for columna in columnas_a_sumar:
            fila_sumada[columna] = (grupo[columna]).sum()  # Sumar los valores

        # Agregar la fila consolidada a la lista
        filas_consolidadas.append(fila_sumada)

    # Convertir la lista de filas consolidadas en un DataFrame
    df_consolidado = pd.DataFrame(filas_consolidadas)

    # Eliminar las filas duplicadas del DataFrame original
    df = df.drop(cuil_duplicados.index)

    # Agregar las filas consolidadas al DataFrame original
    df = pd.concat([df, df_consolidado], ignore_index=True)
    
    return df

df = cargar_archivo()

# se ordena el DataFrame por CUIL, y luego por REMUNERACIONES
ordenado = df.sort_values(by=["CUIL", "REMUNERACIONES"], ascending=[True, False])

# se le aplica la funcion de suma de valores y eliminacion de cuiles repetidos al DataFrame ordenado
df_consolidado = consolidar_cuiles(ordenado)

# se convierte el DataFrame a Excel
nombre = datetime.datetime.now().microsecond
df_consolidado.to_excel(
    f"SALIDA/liq-{nombre}.xlsx",
    sheet_name="hoja1",
    header=True,
    index=False,
)
