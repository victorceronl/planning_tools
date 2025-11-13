import os
import pandas as pd

# === CONFIGURACIÓN AUTOMÁTICA ===
# Obtiene la ruta donde está guardado el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas automáticas basadas en la ubicación del script
EXCEL = os.path.join(BASE_DIR, "nombresNuevos.xlsx")
CARPETA = os.path.join(BASE_DIR, "carpeta_pdfs")

# === LEE EL EXCEL ===
try:
    df = pd.read_excel(EXCEL)
except Exception as e:
    raise SystemExit(f"❌ Error al leer el archivo Excel '{EXCEL}': {e}")

# Verifica columnas
if df.shape[1] < 2:
    raise SystemExit("❌ El Excel debe tener al menos 2 columnas: A (nombre original) y B (texto a agregar)")

# Verifica que exista la carpeta
if not os.path.exists(CARPETA):
    raise SystemExit(f"❌ No se encontró la carpeta: {CARPETA}")

# === RENOMBRAR ARCHIVOS ===
renombrados = 0
no_encontrados = []

for _, fila in df.iterrows():
    nombre_original = str(fila[0]).strip()
    texto_agregar = str(fila[1]).strip()

    encontrado = False
    for archivo in os.listdir(CARPETA):
        nombre_sin_ext, extension = os.path.splitext(archivo)

        # Coincidencia flexible (ignora mayúsculas y espacios)
        if nombre_sin_ext.strip().lower() == nombre_original.lower():
            nuevo_nombre = f"{nombre_sin_ext}{texto_agregar}{extension}"
            ruta_vieja = os.path.join(CARPETA, archivo)
            ruta_nueva = os.path.join(CARPETA, nuevo_nombre)

            # Evita sobrescribir si ya existe
            if os.path.exists(ruta_nueva):
                print(f"⚠️ Ya existe un archivo con el nombre destino: {nuevo_nombre}")
                continue

            os.rename(ruta_vieja, ruta_nueva)
            print(f"✅ {archivo} → {nuevo_nombre}")
            renombrados += 1
            encontrado = True
            break

    if not encontrado:
        no_encontrados.append(nombre_original)

# === RESUMEN ===
print("\n=== RESUMEN ===")
print(f"✔️ Archivos renombrados: {renombrados}")
if no_encontrados:
    print("⚠️ No se encontraron los siguientes nombres:")
    for n in no_encontrados:
        print("   -", n)
else:
    print("✅ Todos los nombres fueron encontrados y renombrados correctamente.")
