import os
from ebooklib import epub
from bs4 import BeautifulSoup

def epub_a_txt(ruta_epub, salida_txt):
    # Verificar que el archivo exista
    if not os.path.exists(ruta_epub):
        print(f"❌ El archivo {ruta_epub} no existe.")
        return

    try:
        # Cargar el libro
        libro = epub.read_epub(ruta_epub)
        texto_final = ""

        # Recorrer los ítems del epub
        for item in libro.get_items():
            if item.get_type() == 9:  # DOCUMENT
                contenido = item.get_body_content().decode("utf-8", errors="ignore")
                soup = BeautifulSoup(contenido, "html.parser")
                texto = soup.get_text(separator="\n", strip=True)
                texto_final += texto + "\n\n"

        # Guardar como archivo de texto
        with open(salida_txt, "w", encoding="utf-8") as archivo:
            archivo.write(texto_final)

        print(f"✅ Conversión completada: {salida_txt}")

    except Exception as e:
        print(f"❌ Error al convertir: {e}")

# Ejemplo de uso:
# Reemplaza 'libro.epub' por el nombre de tu archivo
epub_a_txt("libro.epub", "salida.txt")