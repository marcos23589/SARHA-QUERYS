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

COD_CONVENIO = [40, 71]
ESTRUCTURAS = [
    "AAACACCDA000AAA00000",
    "AAACACCFCAAAAAA00000",
    "AAACACCEBAAAAAA00000",
    "AAACACCEAAAAAAA00000",
]
COD_CONCEPTO = 127
VIGENCIA_DESDE = 202407
COD_SUBCONCEPTO = [1, 2, 3]
COD_TIPO_UNIDAD = 5
COD_UNIDAD = 1
COD_USUARIO = 3633
DEPENDE_ESCALAFON = 1
DEPENDE_FUNCION = 1

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
