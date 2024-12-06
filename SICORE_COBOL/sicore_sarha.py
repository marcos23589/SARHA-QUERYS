import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Cargar módulos personalizados y configurar ruta
sys.path.append(os.path.abspath(".."))

# Cargar variables de entorno
load_dotenv()

# Directorio de salida
OUTPUT_DIRECTORY = "S:\LDDAT\SARHA\SICORE"

# Organismos en COBOL
ORGANISMOS = {
    30656949836: "CAP",
    30673639603: "MEFI",
    30673656524: "HTD",
    30673656699: "MGO",
    30673657687: "MSGG",
    30707677879: "CSC",
    30710660839: "MPCI",
    30711853738: "MDS",
    30715443577: "GOB",
    30716110326: "MTES",
    30716837250: "JGM",
    33716718439: "MSEG",
    30637174262: "LOAS",
    30717532879: "ICT",
    30636881607: "ISPRO",
    30715322745: "FISC",
    30652487080: "POSC",
    30673674433: "HTC",
    #    30670270730: 'CPS',
    #    30638247395: 'CSS',
    #    30711796602: "SALUD",
    #    30654106378: "VIALIDAD",
    #    30656997806: "POLICIA",
    #    30716401959: "SPP",
    #    30717554287: "AMA",
    #    30653141994: "IDUV",
    #    30718410130: 'MEM',
    #    30711218358: 'IESC',
    #    30715200437: 'ASIP',
}

# Ingresar número de interface
numero_interface = int(input("Ingrese número de interface SICORE: "))

# Conexión a la base de datos Oracle de SARHA
engine = create_engine(os.getenv("USUARIO_ORACLE"))


def generar_archivo(tipo, key, value, numero_interface):
    # Genera un archivo de retenciones o sujetos basado en el tipo y el organismo.
    query = f"""
        SELECT {'I.REGISTRO_INTERFASE' if tipo == 'RETENCIONES' else 'S.REGISTRO_INTERFASE'}
        FROM 
            SARHA.INTERFASE_SICORE I
            INNER JOIN SARHA.INTERFASE_SICORE_SUJETOS_RET S 
            ON I.NRO_DOCUMENTO_RETENIDO = S.CUIL 
            AND I.NRO_INTERFASE = S.NRO_INTERFASE
        WHERE S.CUIT = :cuit
        AND S.NRO_INTERFASE = :nro_interfase
        --AND I.IMPORTE_RETENCION > 0
        ORDER BY I.NRO_DOCUMENTO_RETENIDO
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query), {"cuit": key, "nro_interfase": numero_interface}
            )
            file_name = f"{OUTPUT_DIRECTORY}/{key}_SICORE_{value}_{tipo}.txt"

            # Guardar resultados en archivo de texto
            with open(file_name, "w") as file:
                for row in result:
                    file.write(f"{row[0]}\n")
            print(f"Archivo {file_name} generado correctamente.")
    except SQLAlchemyError as e:
        print(f"Error al generar {tipo} para {value}: {e}")


# Generar archivos para cada organismo en ambos tipos
for key, value in ORGANISMOS.items():
    generar_archivo("RETENCIONES", key, value, numero_interface)
    generar_archivo("SUJETOS", key, value, numero_interface)
