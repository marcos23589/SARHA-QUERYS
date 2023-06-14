from pathlib import Path
from tkinter import filedialog
import pandas as pd
import os


# Mostrar el diálogo para abrir un archivo.
filename = filedialog.askopenfilename()
# Imprimir la ruta del archivo seleccionado por el usuario.
print(f'El archivo de embargos elegido es {filename}')

df_embargos = pd.ExcelFile(filename).parse(sheet_name='EMBARGOS', header=0, names=None, index_col=None, encoding='latin-1')

df_embargos.head(5)

# Read the large csv file into a pandas dataframe
df_embargos = pd.read_excel(filename)

print(df_embargos['DESCRIPCION'].unique())
###### CREO TODOS LOS DATAFRAMES SEPARADOS POR ORGANISMO
cap_df = df_embargos[df_embargos['DESCRIPCION'] == '(CAP) CONSEJO AGRARIO PROVINCIAL']
mds_df = df_embargos[df_embargos['DESCRIPCION'] == '(MDS) MINISTERIO DE DESARROLLO SOCIAL']
mpci_df = df_embargos[df_embargos['DESCRIPCION'] == '(MPCI) MINISTERIO DE PRODUCCIÓN COMERCIO E INDUSTRIA']
mtes_df = df_embargos[df_embargos['DESCRIPCION'] == '(MTES) MINISTERIO TRABAJO, EMPLEO Y SEG. SOCIAL']
mgo_df = df_embargos[df_embargos['DESCRIPCION'] == '(MGO) MINISTERIO DE GOBIERNO']
mefi_df = df_embargos[df_embargos['DESCRIPCION'] == '(MEFI) MINISTERIO DE ECONOMIA, FINANZAS E INFRAESTRUCTURA']
msgg_df = df_embargos[df_embargos['DESCRIPCION'] == '(MSGG) MINISTERIO SECRETARIA GENERAL DE LA GOBERNACION']
mseg_df = df_embargos[df_embargos['DESCRIPCION'] == '(MSEG) MINISTERIO DE SEGURIDAD']
csc_df = df_embargos[df_embargos['DESCRIPCION'] == '(CSC) CASA DE SANTA CRUZ']
gob_df = df_embargos[df_embargos['DESCRIPCION'] == '(GOB) GOBERNACIÓN']
jgm_df = df_embargos[df_embargos['DESCRIPCION'] == '(JGM) MINISTERIO JEFATURA DE GABINETE DE MINISTROS']
htd_df = df_embargos[df_embargos['DESCRIPCION'] == '(HTD) HONORABLE TRIBUNAL DISCIPLINARIO']
#cyt_df = intermedio[intermedio['organismo'] == '(ICT) INSTITUTO CIENTÍFICO Y TECNOLÓGICO']
#igualdad_df = intermedio[intermedio['organismo'] == '(MII) MINISTERIO DE LA IGUALDAD E INTEGRACIÓN']
#loas_df = intermedio[intermedio['organismo'] == '(LOAS) LOTERIA DE ACCION SOCIAL DE STA CRUZ']
#ispro_df = intermedio[intermedio['organismo'] == '(ISPRO) ISPRO']

###### EMBARGOS FULL
#embargosfull.to_excel('./SALIDA/EMBARGOS-FULL-ABRIL-2023.xlsx')

###### CONSEJO AGRARIO
cap = cap_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
cap.to_excel('./SALIDA/EMBARGOS-CAPR.xlsx')

##### MINISTERIO DE DESARROLLO
mds = mds_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
mds.to_excel('./SALIDA/EMBARGOS-DESA.xlsx')

##### MINISTERIO DE PRODUCCION
mpci = mpci_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
mpci.to_excel('./SALIDA/EMBARGOS-PROD.xlsx')

##### MINISTERIO DE TRABAJO
mtes = mtes_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
mtes.to_excel('./SALIDA/EMBARGOS-TRAB.xlsx')

##### MINISTERIO DE GOBIERNO
mgo = mgo_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
mgo.to_excel('./SALIDA/EMBARGOS-MGOB.xlsx')

##### MINISTERIO DE ECONOMIA
mefi = mefi_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
mefi.to_excel('./SALIDA/EMBARGOS-MEFI.xlsx')

##### MINISTERIO DE SECRETARIA GENERAL
msgg = msgg_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
msgg.to_excel('./SALIDA/EMBARGOS-MSGG.xlsx')

##### MINISTERIO DE SEGURIDAD
mseg = mseg_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
mseg.to_excel('./SALIDA/EMBARGOS-SEGU.xlsx')

##### CASA DE SANTA CRUZ
csc = csc_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
csc.to_excel('./SALIDA/EMBARGOS-CASA.xlsx')

##### MINISTERIO DE GOBERNACION
gob = gob_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
gob.to_excel('./SALIDA/EMBARGOS-GOBE.xlsx')

##### MINISTERIO DE JEFATURA DE GABINETE
jgm = jgm_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
jgm.to_excel('./SALIDA/EMBARGOS-JGAB.xlsx')

##### HONORABLE TRIBUNAL DISCIPLINARIO
htd = htd_df.loc[:,['NRO_LIQUIDACION','CUIT','DESCRIPCION','CUIL','APELLIDO','NOMBRE','COD_CONCEPTO','COD_SUBCONCEPTO','DESCRIPCION_1','CAUSA_JUDICIAL','VALOR']]
htd.to_excel('./SALIDA/EMBARGOS-HTDI.xlsx')

##### CIENCIA Y TECNOLOGIA
#cyt = cyt_df.loc[:,['concepto_liquidacion_cuil_1','apellido_nombre_empleado','cuit','organismo','embargo_importe_oficio_1','oficio_causa','concepto','concepto_liquidacion_descripcion_concepto','concepto_liquidacion_importe']]
#cyt.to_excel('./SALIDA/EMBARGOS-CYTEC.xlsx')

##### MINISTERIO DE IGUALDAD
#igualdad = igualdad_df.loc[:,['concepto_liquidacion_cuil_1','apellido_nombre_empleado','cuit','organismo','embargo_importe_oficio_1','oficio_causa','concepto','concepto_liquidacion_descripcion_concepto','concepto_liquidacion_importe']]
#igualdad.to_excel('./SALIDA/EMBARGOS-IGUALDAD.xlsx')

##### LOAS
#loas = loas_df.loc[:,['concepto_liquidacion_cuil_1','apellido_nombre_empleado','cuit','organismo','embargo_importe_oficio_1','oficio_causa','concepto','concepto_liquidacion_descripcion_concepto','concepto_liquidacion_importe']]
#loas.to_excel('./SALIDA/EMBARGOS-LOAS.xlsx')

##### ISPRO
#ispro = ispro_df.loc[:,['concepto_liquidacion_cuil_1','apellido_nombre_empleado','cuit','organismo','embargo_importe_oficio_1','oficio_causa','concepto','concepto_liquidacion_descripcion_concepto','concepto_liquidacion_importe']]
#ispro.to_excel('./SALIDA/EMBARGOS-ISPRO.xlsx')