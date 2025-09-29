from PIL import Image
import pytesseract

def extraer_texto_imagen(ruta_imagen, ruta_salida):
    try:
        # Abrir la imagen
        img = Image.open(ruta_imagen)

        # Usar pytesseract para extraer texto
        texto = pytesseract.image_to_string(img, lang="spa")  # "eng" para inglés, "spa" para español

        # Guardar el texto en un archivo .txt
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(texto)

        print(f"✅ Texto extraído y guardado en {ruta_salida}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Ejemplo de uso
extraer_texto_imagen("ejemplo.jpg", "salida.txt")
