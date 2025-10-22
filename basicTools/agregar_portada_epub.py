from ebooklib import epub
from PIL import Image
import os

def agregar_portada_epub(ruta_epub, ruta_imagen, salida_epub):
    # Validar rutas
    if not os.path.exists(ruta_epub):
        print(f"❌ El archivo EPUB no existe: {ruta_epub}")
        return
    if not os.path.exists(ruta_imagen):
        print(f"❌ La imagen no existe: {ruta_imagen}")
        return

    try:
        # Cargar el libro EPUB
        libro = epub.read_epub(ruta_epub)

        # Convertir la imagen a formato JPEG (si no lo está)
        imagen_temp = "temp_cover.jpg"
        with Image.open(ruta_imagen) as img:
            img.convert("RGB").save(imagen_temp, "JPEG")

        # Crear ítem de portada
        with open(imagen_temp, "rb") as f:
            portada_data = f.read()

        # Agregar la portada al libro
        libro.set_cover("cover.jpg", portada_data)

        # Guardar nuevo archivo EPUB con portada
        epub.write_epub(salida_epub, libro)
        print(f"✅ Portada agregada correctamente: {salida_epub}")

        # Eliminar archivo temporal
        os.remove(imagen_temp)

    except Exception as e:
        print(f"❌ Error al agregar la portada: {e}")

# Ejemplo de uso:
# Reemplaza los nombres por los tuyos
agregar_portada_epub("libro_original.epub", "portada.jpg", "libro_con_portada.epub")
