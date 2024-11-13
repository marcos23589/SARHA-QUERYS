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
OUTPUT_DIRECTORY = "S:/LDDAT/SICORE"

# Organismos en COBOL
ORGANISMOS = {
    30711796602: "SALUD",
    30654106378: "VIALIDAD",
    30656997806: "POLICIA",
    30716401959: "SPP",
    30717554287: "AMA",
    30653141994: "IDUV",
}

# Ingresar número de interface
numero_interface = int(input("Ingrese número de interface SICORE: "))

# Conexión a la base de datos Oracle de SARHA
engine = create_engine(os.getenv("USUARIO_GANANCIAS"))


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
        AND I.IMPORTE_RETENCION > 0
        ORDER BY I.NRO_DOCUMENTO_RETENIDO
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(query), {"cuit": key, "nro_interfase": numero_interface}
            )
            file_name = f"{OUTPUT_DIRECTORY}/{value} {tipo}-{numero_interface}.txt"

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
