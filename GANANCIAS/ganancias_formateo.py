import datetime
import pandas as pd
from tkinter import filedialog


# cuadro de carga del archivo
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
    df = pd.read_csv(archivo, sep=";", skipinitialspace=True, encoding="latin-1")
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

# se elimina la ultima columna vacia
df = cargar_archivo()
last_column = df.columns[-1]
df = df.drop(last_column, axis=1)

# se agregan las cabeceras de las columnas
df.columns = columnas

# se ordena el DataFrame por CUIL, y luego por REMUNERACIONES
ordenado = df.sort_values(by=["CUIL", "REMUNERACIONES"], ascending=[True, False])


def consolidar_cuiles(df):
    # Definir las columnas que deben sumarse
    columnas_a_sumar = [
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

    # Dividir los valores por 100
    df[columnas_a_sumar] = df[columnas_a_sumar] / 100

    return df


# se le aplica la funcion al DataFrame ordenado
df_consolidado = consolidar_cuiles(ordenado)

# se convierte el DataFrame a Excel
df_consolidado.to_excel(
    f"salida-{datetime.datetime.now().microsecond}.xlsx",
    sheet_name="hoja1",
    header=True,
    index=False,
)
