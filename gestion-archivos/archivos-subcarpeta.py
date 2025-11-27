import os
import shutil

def mover_archivos(carpeta_origen, carpeta_destino):
    # Crear carpeta destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Recorrer todas las subcarpetas
    for ruta_actual, carpetas, archivos in os.walk(carpeta_origen):
        for archivo in archivos:
            ruta_archivo = os.path.join(ruta_actual, archivo)
            nueva_ruta = os.path.join(carpeta_destino, archivo)

            # Si el archivo ya existe en destino, renombrarlo
            if os.path.exists(nueva_ruta):
                nombre, ext = os.path.splitext(archivo)
                contador = 1
                while True:
                    nuevo_nombre = f"{nombre}_{contador}{ext}"
                    nueva_ruta = os.path.join(carpeta_destino, nuevo_nombre)
                    if not os.path.exists(nueva_ruta):
                        break
                    contador += 1

            shutil.move(ruta_archivo, nueva_ruta)
            print(f"Movido: {ruta_archivo} -> {nueva_ruta}")

    print("\n✔ Archivos movidos correctamente.")

# === CONFIGURA AQUÍ ===
carpeta_origen = r"C:\Users\Diseño 1\Downloads\UZ_KITS"
carpeta_destino = r"C:\Users\Diseño 1\Downloads\UZ_KITS_UNIDOS"

mover_archivos(carpeta_origen, carpeta_destino)
