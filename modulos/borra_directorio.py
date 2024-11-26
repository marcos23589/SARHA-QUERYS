import os


def delete_directory(directorio):
    # Obtener la lista de archivos en el directorio
    archivos = os.listdir(directorio)
  # Iterar sobre la lista de archivos y eliminarlos uno por uno
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        # Verificar si es un archivo (no un directorio)
        if os.path.isfile(ruta_completa):
            os.remove(ruta_completa)
    return (f"Directorio {directorio} borrado exitosamente")
