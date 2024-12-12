import pandas as pd
import re


# Función para limpiar caracteres ilegales
def clean_text(text):
    if isinstance(text, str):
        # Eliminar caracteres ilegales
        return re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)
    return text


archivo1 = "./MAESTRO-11.TXT"
archivo2 = "./MAESTRO-12.TXT"

cabeceras2 = [
        'LEGAJO',
        'NOMBRE',
        'DNI',
        'CUIL',
        'ESTADO',
        'MOTIVO-BAJA',
        'FECHA-NAC',
        'FECHA-BAJA',
    ]

def converse(df):    
    # Leer el archivo TXT, ignorando líneas problemáticas
    chunks = pd.read_csv(
        df, sep=";", encoding="latin-1", chunksize=1000, on_bad_lines="skip", header=None
    )

    # Limpiar cada fragmento
    cleaned_chunks = []
    for chunk in chunks:
        # Aplicar la limpieza a cada columna del DataFrame
        cleaned_chunk = chunk.apply(
            lambda col: col.map(clean_text) if col.dtype == "object" else col
        )
        cleaned_chunks.append(cleaned_chunk)

    # Concatenar todos los fragmentos en un solo DataFrame
    df_concat = pd.concat(cleaned_chunks)

    # Cambiar los nombres de todas las columnas a números
    df_concat.columns = range(1, len(df_concat.columns) + 1)  # Asigna números comenzando desde 1

    cabeceras = [
        'LEGAJO',
        'NOMBRE',
        'DNI',
        'CUIL',
        'DIA-NAC',
        'MES-NAC',
        'ANIO-NAC',
        'ESTADO',
        'DIA-BAJA',
        'MES-BAJA',
        'ANIO-BAJA',
        'MOTIVO-BAJA',
    ]

    # Seleccionar las columnas específicas
    columnas_deseadas = [1, 11, 25, 26, 29, 30, 31, 198, 199, 200, 201, 202]
    df = df_concat[columnas_deseadas]
    df.columns = cabeceras

    # Crear las columnas 'FECHA-NAC' y 'FECHA-BAJA' usando .loc
    df.loc[:, 'FECHA-NAC'] = df['DIA-NAC'].astype(str) + '/' + df['MES-NAC'].astype(str) + '/' + df['ANIO-NAC'].astype(str)
    df.loc[:, 'FECHA-BAJA'] = df['DIA-BAJA'].astype(str) + '/' + df['MES-BAJA'].astype(str) + '/' + df['ANIO-BAJA'].astype(str)

    # Eliminar las columnas de día, mes y año
    df = df.drop(columns=['DIA-NAC', 'MES-NAC', 'ANIO-NAC', 'DIA-BAJA', 'MES-BAJA', 'ANIO-BAJA'])

    
    df.columns = cabeceras2
    return df

noviembre = converse(archivo1)
diciembre = converse(archivo2)

motivos_baja = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","P","X"]

# Merge los DataFrames en base a 'LEGAJO'
movimientos = pd.merge(noviembre[cabeceras2], diciembre[cabeceras2], on='LEGAJO', how='outer', suffixes=('_nov', '_dic'))

# Inicializar la columna 'SITUACIÓN'
movimientos['SITUACION'] = ''


# Aplicar las condiciones
# 1) Si el legajo no se encuentra en 'noviembre', pero sí en 'diciembre' y el 'estado' es 0
movimientos.loc[(movimientos['ESTADO_nov'].isna()) & (movimientos['ESTADO_dic'] == 0), 'SITUACION'] = 'ALTA'

# 2) Si el legajo tiene 'estado' en 0 y en diciembre 'estado' es 1 o motivo de baja no es 0
movimientos.loc[
    (movimientos['ESTADO_nov'] == 0) & ((movimientos['MOTIVO-BAJA_dic'].isin(motivos_baja)) | (movimientos['ESTADO_dic'] > 0) | movimientos['FECHA-BAJA_dic'].str.contains(r'\D', na=False)), 'SITUACION'] = 'BAJA'

# 3) Si el legajo tiene 'estado' en 1 y en diciembre 'estado' en 0
movimientos.loc[(movimientos['ESTADO_nov'] >= 1) & ((movimientos['ESTADO_dic'] == 0) & (movimientos['MOTIVO-BAJA_dic'] == "0")), 'SITUACION'] = 'REINCORPORACION'

# 4) Filtrar los registros que no deben incluirse (estado en 1 en noviembre y diciembre)
movimientos = movimientos[~((movimientos['ESTADO_nov'] != 0) & (movimientos['ESTADO_dic'] != 0))]

# Filtrar registros donde ambos estados son 0
movimientos = movimientos[~((movimientos['ESTADO_nov'] == 0) & (movimientos['ESTADO_dic'] == 0))]

movimientos = movimientos[~((movimientos['ESTADO_nov'] == 1) & (movimientos['MOTIVO-BAJA_dic'].isin(motivos_baja)))]

movimientos.to_excel("movimientos.xlsx", index=False)
