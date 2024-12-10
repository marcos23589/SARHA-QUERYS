import pandas as pd
from datetime import datetime
from tkinter import filedialog
import tkinter as tk

# PROGRAMA QUE CARGA EN UN EXCEL LOS DATOS NECESARIOS PARA PARAMETRIZAR UN CONCEPTO PARA UNA ESTRUCTURA
# SE DEBE DESCARGAR LA TABLA DESDE LA BBDD, SE COMPLETAN LOS DATOS NECESARIOS Y SE HACE UN INSERT.



# Leer el archivo Excel y se extraen las columnas necesarias
#archivo = filedialog.askopenfilename()
archivo = 'D:\workspace\sarha-querys\GANANCIAS\SALIDA-COBOL\liq-8824-76.xlsx'
df = pd.read_excel(archivo, sheet_name="Sheet1")
columns=['CUIL', 'CODIGO', 'IMPORTE']

df = df[columns]

#print(df)

cod_sac = (214, 314, 414, 514, 614, 714, 814)
cod_gremio = (951, 955, 960, 980, 983, 990, 996, 997)
cod_no_aporta = (
    240, 241, 242, 243, 245, 292, 293, 294, 291, 299, 458, 248, 340, 341, 342, 345, 346, 391, 399, 832, 833, 430, 435, 440, 442, 443, 445, 446, 491, 499, 543, 635, 640, 641, 642, 643, 645, 646, 649, 691, 699, 735, 740, 741, 742, 743, 745, 746, 791, 799, 344, 444, 644, 744, 292, 392, 492, 692, 792, 474, 548, 285, 276, 277, 278, 648, 540, 541, 281, 681, 298, 221, 432, 433, 832, 833, 830, 840, 842, 858, 254, 844, 259, 293, 294, 759, 834, 434
)

cod_concepto = [
    8021,  # BRUTO GRAVADO
    8023,  # ASIGNACIONES
    8770,  # HS EXTRAS
    8121,  # SAC
    8221,  # 12% REMUNERATIVO
    8024,  # JUBILACION (CPS)
    8025,  # OB.SOCIAL (CSS)
    8790,  # SINDICATOS/GREMIOS
    8793,  # ISPRO
]

for cuil in df['CUIL']:
    if df['CODIGO'] in cod_sac:
        8121 += df['IMPORTE']
    elif df['CODIGO'] in cod_gremio:
        8790 += df['IMPORTE']
    elif df['CODIGO'] < 200:
        8023 += df['IMPORTE']
    elif df['CODIGO'] == 248:
        8770 += df['IMPORTE']
    elif df['CODIGO'] == 901:
        8024 += df['IMPORTE']
    elif df['CODIGO'] == 911:
        8025 += df['IMPORTE']
    elif df['CODIGO'] == 921:
        8793 += df['IMPORTE']
    elif df['CODIGO'] > 200 and df['CODIGO'] < 900:
        8021 += df['IMPORTE']