import os

# Ruta a la carpeta con los archivos
carpeta = 'C:\Users\Diseño 1\Downloads\vBooks'  # <-- CAMBIA esto a la ruta real de tu carpeta

# Texto a eliminar del nombre de archivo
texto_a_eliminar = '_OceanofPDF.com_'

# Recorre todos los archivos en la carpeta
for nombre_archivo in os.listdir(carpeta):
    if texto_a_eliminar in nombre_archivo:
        nuevo_nombre = nombre_archivo.replace(texto_a_eliminar, '')
        ruta_vieja = os.path.join(carpeta, nombre_archivo)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)

        try:
            os.rename(ruta_vieja, ruta_nueva)
            print(f"Renombrado: {nombre_archivo} -> {nuevo_nombre}")
        except Exception as e:
            print(f"Error al renombrar {nombre_archivo}: {e}")