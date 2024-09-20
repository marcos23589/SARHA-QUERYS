import pandas as pd
from datetime import datetime

#SE TOMA LA LIQUIDACION DE COBOL Y SE GENERA UN EXCEL

# Variables globales
cod_concepto = [
    8021, 8023, 8024, 8025, 8121, 8221, 8770, 8790, 8793
]
sub_concepto = '1'
fecha_desde = '01092024'
periodo_desde = '202409'
reintegro = '8'
fecha_hasta = '31092024'
cantidad = '1'

    # Leer el archivo Excel y limpiar las columnas innecesarias
df = pd.read_excel('./liq-sept.xlsx', sheet_name='Hoja1')
df = df.drop(columns=['CUIT', 'ORGANISMO', 'LEGAJO', 'AGENTE'])

# Tupla de 13,555 CUITs (ejemplo, cambiar por la lista real)
cuiles = tuple(df.pop('CUIL'))  

# Función transpuesta optimizada
def transpuesta():


    # Definir las columnas
    columnas = [
        'CUIL', 'COD_CONCEPTO', 'COD_SUBCONCEPTO', 'FECHA_DESDE', 
        'PERIODO_DESDE', 'REINTEGRO', 'FECHA_HASTA', 'CANTIDAD', 'IMPORTE_GENERADO'
    ]
    
    # Precompilamos todas las listas con valores repetitivos
    total_filas = len(cuiles) * len(cod_concepto)  # Total de filas a generar
    cuil_list = [cuil for cuil in cuiles for _ in cod_concepto]  # Repetir cada CUIL
    cod_concepto_list = cod_concepto * len(cuiles)  # Repetir lista de conceptos
    sub_concepto_list = [sub_concepto] * total_filas
    fecha_desde_list = [fecha_desde] * total_filas
    periodo_desde_list = [periodo_desde] * total_filas
    reintegro_list = [reintegro] * total_filas
    fecha_hasta_list = [fecha_hasta] * total_filas
    cantidad_list = [cantidad] * total_filas
    importe_generado_list = ['importe'] * total_filas

    # Crear el DataFrame final con las listas generadas
    preconcepto = pd.DataFrame({
        'CUIL': cuil_list,
        'COD_CONCEPTO': cod_concepto_list,
        'COD_SUBCONCEPTO': sub_concepto_list,
        'FECHA_DESDE': fecha_desde_list,
        'PERIODO_DESDE': periodo_desde_list,
        'REINTEGRO': reintegro_list,
        'FECHA_HASTA': fecha_hasta_list,
        'CANTIDAD': cantidad_list,
        'IMPORTE_GENERADO': importe_generado_list
    })
    
    return preconcepto

df = df.T

# SE GUARDA EL EXCEL
def crear_excel(df):
    df.to_excel(
        f'./COBOL_GCIAS_{datetime.now().strftime("%H-%M-%S")}.xlsx', index=False
    )

#crear_excel(transpuesta())
crear_excel(df)

