import pandas as pd

# TOMA 2 EXCEL CON EL FORMATO DE "CONCEPTO_EMPLEADO" Y SUMA LOS CÓDIGOS POR CADA CUIL QUE SE ENCUENTRE EN LOS 2 EXCELS Y CREA UNA TERCERA PLANILLA CON CUIL, CÓDIGO E IMPORTE

# Cargar los archivos Excel
df1 = pd.read_excel("./SALIDA-COBOL/COBOL_BBDD_COMPLE.xlsx")  # COMPLE A SUMAR
df2 = pd.read_excel("./SALIDA-COBOL/COBOL_BBDD_GCIAS.xlsx")  # GANANCIAS SIN COMPLE

# Combinar los dos DataFrames por CUIL y CODIGO
df_combined = pd.concat([df1, df2])  # Combina ambos archivos en uno solo

# Agrupar por CUIL y CODIGO y sumar el importe
df_result = df_combined.groupby(["CUIL", "COD_CONCEPTO"], as_index=False)[
    "IMPORTE_GEN_HAB"
].sum()

# print(df_result)

# Guardar el resultado en un tercer archivo Excel
df_result.to_excel("./SALIDA-COBOL/SUMA_COBOL_Y_COMPLE.xlsx", index=False)


print("Archivo guardado como resultado.xlsx")
