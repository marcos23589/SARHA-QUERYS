import pandas as pd
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Constantes
CABECERAS = [
    "LEGAJO",
    "NOMBRE",
    "DNI",
    "CUIL",
    "ESTADO",
    "MOTIVO-BAJA",
    "FECHA-NAC",
    "FECHA-BAJA",
]
MOTIVOS_BAJA = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "P",
    "X",
]
COLUMNAS_DESEADAS = [1, 11, 25, 26, 29, 30, 31, 198, 199, 200, 201, 202]
CABECERAS_ORIGINALES = [
    "LEGAJO",
    "NOMBRE",
    "DNI",
    "CUIL",
    "DIA-NAC",
    "MES-NAC",
    "ANIO-NAC",
    "ESTADO",
    "DIA-BAJA",
    "MES-BAJA",
    "ANIO-BAJA",
    "MOTIVO-BAJA",
]


# Función para limpiar caracteres ilegales
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)
    return text


# Función para procesar un archivo y devolver un DataFrame procesado
def process_file(file_path):
    chunks = pd.read_csv(
        file_path,
        sep=";",
        encoding="latin-1",
        chunksize=1000,
        on_bad_lines="skip",
        header=None,
    )

    cleaned_chunks = []
    for chunk in chunks:
        cleaned_chunk = chunk.apply(
            lambda col: col.map(clean_text) if col.dtype == "object" else col
        )
        cleaned_chunks.append(cleaned_chunk)

    df_concat = pd.concat(cleaned_chunks)
    df_concat.columns = range(1, len(df_concat.columns) + 1)

    df = df_concat[COLUMNAS_DESEADAS]
    df.columns = CABECERAS_ORIGINALES

    df["FECHA-NAC"] = (
        df["DIA-NAC"].astype(str)
        + "/"
        + df["MES-NAC"].astype(str)
        + "/"
        + df["ANIO-NAC"].astype(str)
    )
    df["FECHA-BAJA"] = (
        df["DIA-BAJA"].astype(str)
        + "/"
        + df["MES-BAJA"].astype(str)
        + "/"
        + df["ANIO-BAJA"].astype(str)
    )

    df = df.drop(
        columns=["DIA-NAC", "MES-NAC", "ANIO-NAC", "DIA-BAJA", "MES-BAJA", "ANIO-BAJA"]
    )
    df.columns = CABECERAS
    return df


# Función para identificar movimientos entre dos DataFrames
def identify_movements(maestro1_df, maestro2_df):
    movimientos = pd.merge(
        maestro1_df, maestro2_df, on="LEGAJO", how="outer", suffixes=("_m1", "_m2")
    )

    movimientos["SITUACION"] = ""

    # Condiciones
    movimientos.loc[
        (movimientos["ESTADO_m1"].isna()) & (movimientos["ESTADO_m2"] == 0),
        "SITUACION",
    ] = "ALTA"

    movimientos.loc[
        (movimientos["ESTADO_m1"] == 0)
        & (
            (movimientos["MOTIVO-BAJA_m2"].isin(MOTIVOS_BAJA))
            | (movimientos["ESTADO_m2"] > 0)
            | movimientos["FECHA-BAJA_m2"].notna()
        ),
        "SITUACION",
    ] = "BAJA"

    movimientos.loc[
        (movimientos["ESTADO_m1"] >= 1)
        & (movimientos["ESTADO_m2"] == 0)
        & (movimientos["MOTIVO-BAJA_m2"] == "0"),
        "SITUACION",
    ] = "REINCORPORACION"

    # Filtrar registros
    movimientos = movimientos[
        ~((movimientos["ESTADO_m1"] != 0) & (movimientos["ESTADO_m2"] != 0))
    ]
    movimientos = movimientos[
        ~((movimientos["ESTADO_m1"] == 0) & (movimientos["ESTADO_m2"] == 0))
    ]
    movimientos = movimientos[
        ~(
            (movimientos["ESTADO_m1"] == 1)
            & (movimientos["MOTIVO-BAJA_m2"].isin(MOTIVOS_BAJA))
        )
    ]

    # Eliminar columnas no deseadas
    columnas_a_eliminar = ["NOMBRE_m1", "DNI_m1", "CUIL_m1", "FECHA-NAC_m1"]
    movimientos = movimientos.drop(
        columns=[col for col in columnas_a_eliminar if col in movimientos.columns]
    )

    # Reordenar columnas
    columnas_ordenadas = [
        "LEGAJO",
        "NOMBRE_m2",
        "DNI_m2",
        "CUIL_m2",
        "FECHA-NAC_m2",
        "ESTADO_m1",
        "MOTIVO-BAJA_m1",
        "FECHA-BAJA_m1",
        "ESTADO_m2",
        "MOTIVO-BAJA_m2",
        "FECHA-BAJA_m2",
        "SITUACION",
    ]
    movimientos = movimientos[columnas_ordenadas]

    return movimientos


# Función principal para ejecutar el script
def main():
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter

    # Solicitar archivos al usuario
    maestro1 = askopenfilename(
        title="Seleccione el archivo MAESTRO 1",
        filetypes=[["Archivos TXT", "*.txt"]],
    )
    maestro2 = askopenfilename(
        title="Seleccione el archivo MAESTRO 2",
        filetypes=[["Archivos TXT", "*.txt"]],
    )

    if not maestro1 or not maestro2:
        print("Debe seleccionar ambos archivos. No sea pelotudo.")
        return

    # Procesar archivos
    maestro1_df = process_file(maestro1)
    maestro2_df = process_file(maestro2)

    # Identificar movimientos
    movimientos_df = identify_movements(maestro1_df, maestro2_df)

    # Solicitar ubicación para guardar el archivo
    output_file = asksaveasfilename(
        title="Donde quiere guardar el resultado?",
        defaultextension=".xlsx",
        filetypes=[["Archivos Excel", "*.xlsx"]],
    )

    if not output_file:
        print("No se seleccionó un archivo para guardar.")
        return

    # Exportar a Excel
    movimientos_df.to_excel(output_file, index=False)
    print(f"Archivo guardado en: {output_file}")


if __name__ == "__main__":
    main()
