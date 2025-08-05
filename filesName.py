import os
import csv

# Ruta de la carpeta que deseas explorar
ruta_carpeta = 'C:\\Users\\Diseño 1\\Documents\\test-02\\carpeta_pdfs'  # Reemplaza con la ruta real

# Obtener lista de archivos (excluye subcarpetas)
archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]

# Ordenar de menor a mayor (alfabéticamente)
archivos_ordenados = sorted(archivos)

# Nombre del archivo CSV de salida
csv_salida = 'archivos_ordenados.csv'

# Guardar en CSV sin la extensión de archivo
with open(csv_salida, 'w', newline='', encoding='utf-8') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Nombre de Archivo'])  # Encabezado
    for archivo in archivos_ordenados:
        nombre_sin_extension = os.path.splitext(archivo)[0]
        writer.writerow([nombre_sin_extension])

print(f"Se han exportado {len(archivos_ordenados)} archivos a '{csv_salida}'.")