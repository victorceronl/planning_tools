import os
import shutil

# ===== OBTENER LA CARPETA DONDE ESTÁ EL SCRIPT =====
ruta_script = os.path.dirname(os.path.abspath(__file__))

# ===== CONFIGURACION AUTOMATICA =====
carpeta_origen = os.path.join(ruta_script, "piezas_carta")
carpeta_destino = os.path.join(ruta_script, "pdf-recorte")

# Verificar que exista la carpeta origen
if not os.path.exists(carpeta_origen):
    print(f"Error: No se encontró la carpeta 'piezas_carta' en:\n{carpeta_origen}")
    exit()

# Crear carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

copiados = 0

for root, dirs, files in os.walk(carpeta_origen):
    for file in files:
        # Solo copiar PDFs
        if not file.lower().endswith(".pdf"):
            continue

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
        copiados += 1

print(f"Proceso terminado. Se copiaron {copiados} archivos PDF en:\n{carpeta_destino}")