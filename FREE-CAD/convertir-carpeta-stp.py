import os
import FreeCAD
import Part

# === CONFIGURACIÓN ===
# Ruta donde están tus archivos .CATPart
carpeta_entrada = r"C:\Ruta\A\Tu\Carpeta"  # ← CAMBIA ESTA RUTA

# Crear carpeta de salida (si no existe)
carpeta_salida = os.path.join(carpeta_entrada, "STP_convertidos")
os.makedirs(carpeta_salida, exist_ok=True)

# === CONVERSIÓN ===
for archivo in os.listdir(carpeta_entrada):
    if archivo.lower().endswith(".catpart"):
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        nombre_salida = os.path.splitext(archivo)[0] + ".stp"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        print(f"Convirtiendo: {archivo} → {nombre_salida}")

        try:
            # Cargar documento CATPart
            doc = FreeCAD.open(ruta_entrada)
            objetos = [obj for obj in doc.Objects if hasattr(obj, "Shape")]

            # Exportar a STEP
            if objetos:
                Part.export(objetos, ruta_salida)
                print(f"✅ Guardado en: {ruta_salida}")
            else:
                print(f"⚠️ No se encontraron sólidos en {archivo}")

            FreeCAD.closeDocument(doc.Name)
        except Exception as e:
            print(f"❌ Error al convertir {archivo}: {e}")

print("\n🚀 Conversión finalizada.")
