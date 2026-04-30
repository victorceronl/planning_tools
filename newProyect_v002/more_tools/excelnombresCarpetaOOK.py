import os

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
# CREAR TXT DE SALIDA
# =========================================
txt_salida = os.path.join(ruta_script, "lista_excluir.txt")

with open(txt_salida, 'w', encoding='utf-8') as archivo_txt:
    for archivo in archivos_ordenados:
        nombre_sin_extension = os.path.splitext(archivo)[0]
        archivo_txt.write(nombre_sin_extension + '\n')

print(f"Se han exportado {len(archivos_ordenados)} archivos a '{txt_salida}'.")