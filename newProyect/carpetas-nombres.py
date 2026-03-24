import os
import shutil

# === CONFIGURACIÓN ===
carpeta_principal = r"C:\Users\Diseño 1\Documents\TM2603003\planos"
carpeta_salida = r"C:\Users\Diseño 1\Documents\TM2603003\todos"

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

print("Proceso terminado. Archivos consolidados en la carpeta de salida.")