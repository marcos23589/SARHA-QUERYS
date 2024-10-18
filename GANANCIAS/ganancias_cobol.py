import pandas as pd
from datetime import datetime

# este excel vacio lo rellena
df_concepto_empleado = pd.read_excel("./CONCEPTO_EMPLEADO.xlsx", sheet_name="Sheet 1")


# SE TOMA LA LIQUIDACION DE COBOL Y SE GENERA UN EXCEL

# Variables globales
cod_concepto = [8021, 8023, 8024, 8025, 8121, 8221, 8770, 8790, 8793]
sub_concepto = "1"
fecha_desde = "10/1/2024"
periodo_desde = "202410"
reintegro = "8"
fecha_hasta = "31/10/2024"
cantidad = "1"
transaccion = "210953"
fecha_transaccion = "10/18/2024"  # REVISAR FORMATO DE FECHA EN SQL DEVELOPER
cod_tipo_unidad = "5"
cod_unidad = "1"
cod_usuario = "3633"
cod_convenio = "1"
observacion = "GCIAS_OCT_TEST "
generado_haberes = "1"

# Leer el archivo Excel y limpiar las columnas innecesarias
df = pd.read_excel("./liq-400753.xlsx", sheet_name="hoja1")
df = df.drop(columns=["CUIT", "ORGANISMO", "LEGAJO", "AGENTE"])

# Tupla de 13,555 CUILS
cuiles = tuple(df.pop("CUIL"))


# Función transpuesta optimizada
def transpuesta():

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
    id_transaccion_list = [transaccion] * total_filas
    fecha_transaccion_list = [fecha_transaccion] * total_filas
    cod_tipo_unidad_list = [cod_tipo_unidad] * total_filas
    cod_unidad_list = [cod_unidad] * total_filas
    cod_usuario_list = [cod_usuario] * total_filas
    cod_convenio_list = [cod_convenio] * total_filas
    observacion_list = [observacion] * total_filas
    generado_haberes_list = [generado_haberes] * total_filas

    # Crear el DataFrame final con las listas generadas
    preconcepto = pd.DataFrame(
        {
            "CUIL": cuil_list,
            "COD_CONCEPTO": cod_concepto_list,
            "COD_SUBCONCEPTO": sub_concepto_list,
            "FECHA_DESDE": fecha_desde_list,
            "PERIODO_DESDE": periodo_desde_list,
            "REINTEGRO": reintegro_list,
            "FECHA_HASTA": fecha_hasta_list,
            "CANTIDAD": cantidad_list,
            "ID_TRANSACCION": id_transaccion_list,
            "FECHA_TRANSACCION": fecha_transaccion_list,
            "COD_TIPO_UNIDAD": cod_tipo_unidad_list,
            "COD_UNIDAD": cod_unidad_list,
            "COD_USUARIO": cod_usuario_list,
            "COD_CONVENIO": cod_convenio_list,
            "OBSERVACION": observacion_list,
            "FECHA_HASTA_TRANSITORIA": "",
            "GENERADO_HABERES": generado_haberes_list,
            "IMPORTE_GEN_HAB": "",
            "NO_AUTOMATICO": "1",
            "NRO_LIQ_PROCESADO": "",
            "POSPUESTO": "",
            "FECHA_POSPUESTO": "",
            "FECHA_ACTIVACION": "",
            "SECUENCIA_RETRO": "",
            "AUDICHK": "",
            "COD_EGRESO": "",
            "FECHA_HASTA_ANTERIOR": "",
        }
    )

    return preconcepto


# EL DF QUEDA CON LAS COLUMNAS DE LOS MONTOS, POR LO QUE SE TRANSPONE
df = df.T

# LUEGO SE CREA UNA COLUMNA UNICA
columna_unica = pd.concat([df[col] for col in df.columns], ignore_index=True)

# SE TRAE EL DF GENERADO POR LA LIQUIDACION TRAIDA DE COBOL
df_2 = transpuesta()

# SE AGREGA LOS DATOS DE LA COLUMNA UNICA AL DF
df_2["IMPORTE_GEN_HAB"] = columna_unica

# Eliminar las filas donde 'IMPORTE_GEN_HAB' es igual a 0
df = df_2[df_2["IMPORTE_GEN_HAB"] != 0]


# SE GUARDA EL EXCEL
def crear_excel(df):
    df.to_excel(
        f'./SALIDA-COBOL/COBOL_GCIAS_{datetime.now().strftime("%H-%M-%S")}.xlsx',
        index=False,
    )


crear_excel(df)
