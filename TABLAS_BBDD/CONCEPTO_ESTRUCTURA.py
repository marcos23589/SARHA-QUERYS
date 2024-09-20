import pandas as pd
from datetime import datetime
from tkinter import filedialog
import tkinter as tk

# PROGRAMA QUE CARGA EN UN EXCEL LOS DATOS NECESARIOS PARA PARAMETRIZAR UN CONCEPTO PARA UNA ESTRUCTURA
# SE DEBE DESCARGAR LA TABLA DESDE LA BBDD, SE COMPLETAN LOS DATOS NECESARIOS Y SE HACE UN INSERT.

# Constantes globales
COLUMNAS = [
    "COD_CONVENIO",
    "COD_ESTRUCTURA_REAL",
    "COD_CONCEPTO",
    "VIGENCIA_DESDE",
    "COD_SUBCONCEPTO",
    "FECHA_TRANSACCION",
    "COD_TIPO_UNIDAD",
    "COD_UNIDAD",
    "COD_USUARIO",
    "DEPENDE_ESCALAFON",
    "DEPENDE_FUNCION",
]

""" -------- COMPLETAR TODOS ESTOS DATOS DESDE ACA --------  """

COD_CONVENIO = [35, 36, 40, 42, 47, 48, 49, 71]
ESTRUCTURAS = [
    "AAACABBA000000000000",
    "AAACABBB000000000000",
    "AAACAB000AAA00000000",
    "AAACAB000AAB00000000",
    "AAACABBAA00000000000",
    "AAACABBAB00000000000",
    "AAACABBAC00000000000",
    "AAACABBBA00000000000",
    "AAACABBBB00000000000",
    "AAACABBBC00000000000",
    "AAACABBBD00000000000",
    "AAACABBAAAAA00000000",
    "AAACABBABAAA00000000",
    "AAACABBACAAA00000000",
    "AAACABBBBAAA00000000",
    "AAACADDD0AAB00000000",
    "AAAC000D000000000000",
    "AAACAE000AAA00000000",
    "AAACAE000AAB00000000",
    "AAACAE000AABAAA00000",
    "AAACAE0A000000000000",
    "AAACAE0AA00000000000",
    "AAACAE0AB00000000000",
    "AAACAE0ABAAA00000000",
    "AAACAEA0000000000000",
    "AAACAEAA000000000000",
    "AAACAEAA0AAA00000000",
    "AAACAEA0A00000000000",
    "AAACAEABA00000000000",
    "AAACAEABAAAA00000000",
    "AAACAEABB00000000000",
    "AAACAEABBAAA00000000",
    "AAACAEABC00000000000",
    "AAACAEABCAAA00000000",
    "AAACABBC000000000000",
    "AAACABBCA00000000000",
    "AAACABBD000000000000",
    "AAACABBDA00000000000",
    "AAACABBDB00000000000",
    "AAACABBDC00000000000",
    "AAACABBDD00000000000",
    "AAACABBDAAAA00000000",
    "AAACABBDAAAB00000000",
    "AAACABBDBAAA00000000",
    "AAACABBDCAAA00000000",
    "AAACABBDCAAB00000000",
    "AAACABBDCAAC00000000",
    "AAACABBD0AAA00000000",
    "AAAC00000AAB00000000",
    "AAAC000A000000000000",
    "AAAC00F0000000000000",
    "AAAC000B000000000000",
    "AAAC000CA00000000000",
    "AAAC00DB000000000000",
    "AAAC00D00AAA00000000",
    "AAAC00DAA00000000000",
    "AAAC00DA0AAA00000000",
    "AAAC00DA0AAAAAA00000",
    "AAAC00DA0AAAAAB00000",
    "AAAC00DA0AAAAAC00000",
    "AAAC00DBA00000000000",
    "AAAC00DBB00000000000",
    "AAAC00DBB000AAA00000",
    "AAAC00EA000000000000",
    "AAAC00EB000000000000",
    "AAAC00EC000000000000",
    "AAAC00E00AAA00000000",
    "AAAC00EA0AAA00000000",
    "AAAC00EA0AAB00000000",
    "AAAC00EB0AAA00000000",
    "AAAC00EB0AAB00000000",
    "AAAC00EC0AAA00000000",
    "AAAC00EC0AAB00000000",
    "AAACADA0000000000000",
    "AAACADAAA00000000000",
    "AAACADAAAAAA00000000",
    "AAACADAAAAAB00000000",
    "AAACADAAB00000000000",
    "AAACADAABAAA00000000",
    "AAACADAACAAA00000000",
    "AAACADAAD00000000000",
    "AAACADAADAAA00000000",
    "AAACADAAE00000000000",
    "AAACADAAEAAA00000000",
    "AAACADAAF00000000000",
    "AAACADAAFAAA00000000",
    "AAACADAAFAAB00000000",
    "AAACADAA0AAA00000000",
    "AAAC00E00AAAAAA00000",
    "AAAC00E00AAAAAB00000",
    "AAAC00EA0AAAAAA00000",
    "AAAC00EA0AAAAAB00000",
    "AAAC00EA0AABAAA00000",
    "AAAC00EA0AABAAB00000",
    "AAAC00EB0AAAAAA00000",
    "AAAC00EB0AABAAA00000",
    "AAAC00EB0AABAAB00000",
    "AAAC00EC0AAAAAA00000",
    "AAAC00EC0AABAAA00000",
    "AAACADA0A000AAA00000",
    "AAACADA00AAAAAA00000",
    "AAACADA00AAAAAB00000",
    "AAACAD000AAA00000000",
    "AAACAD000AAB00000000",
    "AAACADB0000000000000",
    "AAACADB0A00000000000",
    "AAACADB0B00000000000",
    "AAACADB0C00000000000",
    "AAACADC0000000000000",
    "AAACADCAA00000000000",
    "AAACADCAB00000000000",
    "AAACADCB000000000000",
    "AAACADCBA00000000000",
    "AAACADCBAAAA00000000",
    "AAACADCBB00000000000",
    "AAACADCBC00000000000",
    "AAACADD0000000000000",
    "AAACADDA000000000000",
    "AAACADDB000000000000",
    "AAACADDBA00000000000",
    "AAACADDBB00000000000",
    "AAACADDC000000000000",
    "AAACADDCA00000000000",
    "AAACADDCA000AAA00000",
    "AAACADDCB00000000000",
    "AAACADDD000000000000",
    "AAACADDD0AAA00000000",
]
COD_CONCEPTO = 125
VIGENCIA_DESDE = 202407
COD_SUBCONCEPTO = [1]
COD_TIPO_UNIDAD = 5
COD_UNIDAD = 1
COD_USUARIO = 3633
DEPENDE_ESCALAFON = 2
DEPENDE_FUNCION = 2

""" -------- HASTA ACA -------- """


# Función para obtener la fecha de transacción actual
def obtener_fecha_actual():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# Función para cargar el archivo Excel
def cargar_archivo_excel():
    try:
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        archivo = filedialog.askopenfilename(filetypes=[("Archivos XLSX", "*.xlsx")])
        if archivo:
            df = pd.read_excel(archivo, sheet_name="Sheet 1")
            return df, archivo
        else:
            raise FileNotFoundError("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None, None


# Función para crear nuevas filas a insertar en el Excel
def generar_nuevas_filas():
    filas = []
    fecha_transaccion = obtener_fecha_actual()
    for estructura in ESTRUCTURAS:
        for convenio in COD_CONVENIO:
            vigencia = VIGENCIA_DESDE
            for subconcepto in COD_SUBCONCEPTO:
                filas.append(
                    [
                        convenio,
                        estructura,
                        COD_CONCEPTO,
                        vigencia,
                        subconcepto,
                        fecha_transaccion,
                        COD_TIPO_UNIDAD,
                        COD_UNIDAD,
                        COD_USUARIO,
                        DEPENDE_ESCALAFON,
                        DEPENDE_FUNCION,
                    ]
                )
                if len(COD_SUBCONCEPTO) > 1:
                    vigencia -= 1
    return filas


# Función para guardar el DataFrame en el archivo Excel
def guardar_excel(df, archivo):
    try:
        with pd.ExcelWriter(
            archivo, engine="openpyxl", mode="a", if_sheet_exists="replace"
        ) as writer:
            df.to_excel(writer, sheet_name="Sheet 1", index=False)
        print("Archivo actualizado correctamente.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


# Función principal
def actualizar_excel():
    df, archivo = cargar_archivo_excel()
    if df is not None:
        nuevas_filas = generar_nuevas_filas()
        df_nuevas_filas = pd.DataFrame(nuevas_filas, columns=COLUMNAS)
        df_actualizado = pd.concat([df, df_nuevas_filas], ignore_index=True)
        guardar_excel(df_actualizado, archivo)


# Ejecutar el programa
if __name__ == "__main__":
    actualizar_excel()
