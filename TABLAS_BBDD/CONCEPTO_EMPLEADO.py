import pandas as pd
from datetime import datetime
from tkinter import filedialog
import tkinter as tk

# Leer el archivo Excel y se extraen las columnas necesarias
archivo = 'D:\workspace\sarha-querys\GANANCIAS\SALIDA-COBOL\liq-8824-71.xlsx'
df = pd.read_excel(archivo, sheet_name="Sheet1")
columns=['CUIL', 'CODIGO', 'IMPORTE']
df = df[columns]

# Definición de códigos
cod_sac = (214, 314, 414, 514, 614, 714, 814)
cod_gremio = (951, 955, 960, 980, 983, 990, 996, 997)
cod_no_aporta = (
    240, 241, 242, 243, 245, 292, 293, 294, 291, 299, 458, 248, 340, 341, 342, 345, 346, 391, 399, 832, 833, 430, 435, 440, 442, 443, 445, 446, 491, 499, 543, 635, 640, 641, 642, 643, 645, 646, 649, 691, 699, 735, 740, 741, 742, 743, 745, 746, 791, 799, 344, 444, 644, 744, 292, 392, 492, 692, 792, 474, 548, 285, 276, 277, 278, 648, 540, 541, 281, 681, 298, 221, 432, 433, 832, 833, 830, 840, 842, 858, 254, 844, 259, 293, 294, 759, 834, 434
)

# Crear un DataFrame vacío para almacenar los resultados
resultados = []

# Agrupar por CUIL
for cuil, group in df.groupby('CUIL'):
    # Inicializar variables
    total_8021 = 0
    total_8023 = 0
    total_8770 = 0
    total_8121 = 0
    total_8024 = 0
    total_8025 = 0
    total_8790 = 0
    total_8793 = 0
    aportes = 0
    descuentos = 0

    # Procesar cada fila del grupo
    for index, row in group.iterrows():
        codigo = row['CODIGO']
        importe = row['IMPORTE']

        
        if codigo < 200:
            total_8023 += importe
        elif codigo == 248:
            total_8770 += importe
        elif codigo in cod_sac:
            total_8121 += importe
        elif codigo == 901:
            total_8024 += importe
        elif codigo == 911:
            total_8025 += importe
        elif codigo in cod_gremio:
            total_8790 += importe
        elif codigo == 921:
            total_8793 += importe
        elif 200 < codigo < 900:
            total_8021 += importe
        if codigo not in cod_no_aporta:
            aportes += importe
        if codigo > 900:
            descuentos += importe

    # Calcular el importe para el código 8221
    total_8221 = (aportes - descuentos - total_8023) * 0.06833333

    # Agregar los resultados al DataFrame
    resultados.append([cuil, 8021, total_8021])
    resultados.append([cuil, 8023, total_8023])
    resultados.append([cuil, 8770, total_8770])
    resultados.append([cuil, 8121, total_8121])
    resultados.append([cuil, 8221, total_8221])
    resultados.append([cuil, 8024, total_8024])
    resultados.append([cuil, 8025, total_8025])
    resultados.append([cuil, 8790, total_8790])
    resultados.append([cuil, 8793, total_8793])



# Crear un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados, columns=['CUIL', 'COD_CONCEPTO', 'IMPORTE'])

df_resultados = df_resultados[df_resultados['IMPORTE'] != 0]


# Renombrar la columna 'IMPORTE' a 'IMPORTE_GEN_HAB'
df_resultados.rename(columns={'IMPORTE': 'IMPORTE_GEN_HAB'}, inplace=True)
# Agregar las columnas faltantes con valores iniciales
df_resultados = df_resultados.assign(
    COD_SUBCONCEPTO="1",
    FECHA_DESDE="11/2/2024",
    PERIODO_DESDE="202411",
    REINTEGRO="8",
    FECHA_HASTA="30/10/2024",
    CANTIDAD="1",
    ID_TRANSACCION="210957",
    FECHA_TRANSACCION="09/12/2024",
    COD_TIPO_UNIDAD="5",
    COD_UNIDAD="1",
    COD_USUARIO="3633",
    COD_CONVENIO="1",
    OBSERVACION="GCIAS SALUD CA NOVIEMBRE",
    GENERADO_HABERES="1",
    FECHA_HASTA_TRANSITORIA=None,
    NO_AUTOMATICO=None,
    NRO_LIQ_PROCESADO=None,
    POSPUESTO=None,
    FECHA_POSPUESTO=None,
    FECHA_ACTIVACION=None,
    SECUENCIA_RETRO=None,
    AUDICHK=None,
    COD_EGRESO=None,
    FECHA_HASTA_ANTERIOR=None
)

# Formatear la columna 'IMPORTE_GEN_HAB' para mostrar 2 decimales
df_resultados['IMPORTE_GEN_HAB'] = pd.to_numeric(df_resultados['IMPORTE_GEN_HAB'], errors='coerce').round(2)

# Reordenar las columnas del DataFrame
columnas_ordenadas = [
    "CUIL", "COD_CONCEPTO", "COD_SUBCONCEPTO", "FECHA_DESDE", "PERIODO_DESDE", "REINTEGRO",
    "FECHA_HASTA", "CANTIDAD", "ID_TRANSACCION", "FECHA_TRANSACCION", "COD_TIPO_UNIDAD",
    "COD_UNIDAD", "COD_USUARIO", "COD_CONVENIO", "OBSERVACION", "FECHA_HASTA_TRANSITORIA",
    "GENERADO_HABERES", "IMPORTE_GEN_HAB", "NO_AUTOMATICO", "NRO_LIQ_PROCESADO", "POSPUESTO",
    "FECHA_POSPUESTO", "FECHA_ACTIVACION", "SECUENCIA_RETRO", "AUDICHK", "COD_EGRESO",
    "FECHA_HASTA_ANTERIOR"
]

df_resultados = df_resultados[columnas_ordenadas]

# Ver el resultado
print(df_resultados.head())



# Guardar el DataFrame en un archivo Excel
output_file = 'resultados.xlsx'
df_resultados.to_excel(output_file, index=False)