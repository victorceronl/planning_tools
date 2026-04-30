import os
import csv

# =========================================
# OBTENER RUTA DEL SCRIPT
# =========================================
ruta_script = os.path.dirname(os.path.abspath(__file__))

# Carpeta "carpeta_pdfs" dentro del directorio del script
ruta_carpeta = os.path.join(ruta_script, "carpeta_pdfs")

# Validar que la carpeta exista
if not os.path.isdir(ruta_carpeta):
    raise FileNotFoundError(f"No se encontró la carpeta: {ruta_carpeta}")

# =========================================
# OBTENER ARCHIVOS (SIN SUBCARPETAS)
# =========================================
archivos = [
    f for f in os.listdir(ruta_carpeta)
    if os.path.isfile(os.path.join(ruta_carpeta, f))
]

# Ordenar alfabéticamente
archivos_ordenados = sorted(archivos)

# =========================================
# CREAR CSV DE SALIDA
# =========================================
csv_salida = os.path.join(ruta_script, "archivos_ordenados.csv")

with open(csv_salida, 'w', newline='', encoding='utf-8') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Nombre de Archivo'])
    for archivo in archivos_ordenados:
        nombre_sin_extension = os.path.splitext(archivo)[0]
        writer.writerow([nombre_sin_extension])

print(f"Se han exportado {len(archivos_ordenados)} archivos a '{csv_salida}'.")
