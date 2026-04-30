import os
import shutil

# === OBTENER LA CARPETA DONDE ESTÁ EL SCRIPT ===
ruta_script = os.path.dirname(os.path.abspath(__file__))

# === DEFINIR CARPETAS AUTOMÁTICAMENTE ===
carpeta_principal = os.path.join(ruta_script, "planos")
carpeta_salida = os.path.join(ruta_script, "todos")

# Verificar que exista la carpeta "planos"
if not os.path.exists(carpeta_principal):
    print(f"Error: No se encontró la carpeta 'planos' en:\n{carpeta_principal}")
    exit()

# Crear carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Recorrer cada carpeta dentro de la principal
for nombre_carpeta in os.listdir(carpeta_principal):
    ruta_carpeta = os.path.join(carpeta_principal, nombre_carpeta)

    if os.path.isdir(ruta_carpeta):

        # Recorrer archivos dentro de la subcarpeta
        for archivo in os.listdir(ruta_carpeta):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)

            if os.path.isfile(ruta_archivo):

                # Crear nuevo nombre
                nuevo_nombre = f"{nombre_carpeta}_{archivo}"

                ruta_destino = os.path.join(carpeta_salida, nuevo_nombre)

                # Copiar archivo con nuevo nombre
                shutil.copy2(ruta_archivo, ruta_destino)

print(f"Proceso terminado. Archivos consolidados en:\n{carpeta_salida}")