import os
import shutil

# ===== CONFIGURACION =====
carpeta_origen = r"C:\Users\Diseño 1\Documents\TM2603003\piezas_carta"
carpeta_destino = r"C:\Users\Diseño 1\Documents\TM2603003\pdf-recprte"

# Crear carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

for root, dirs, files in os.walk(carpeta_origen):
    for file in files:
        ruta_origen = os.path.join(root, file)
        ruta_destino = os.path.join(carpeta_destino, file)

        # Evitar sobrescribir archivos con el mismo nombre
        contador = 1
        nombre, extension = os.path.splitext(file)

        while os.path.exists(ruta_destino):
            nuevo_nombre = f"{nombre}_{contador}{extension}"
            ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
            contador += 1

        shutil.copy2(ruta_origen, ruta_destino)

print("Proceso terminado. Todos los archivos fueron copiados.")