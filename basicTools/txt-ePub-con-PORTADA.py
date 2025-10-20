from ebooklib import epub

def txt_a_epub(ruta_txt, ruta_epub, titulo="Mi Libro", autor="Desconocido", portada=None):
    # Leer el contenido del archivo .txt
    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    # Crear el libro EPUB
    libro = epub.EpubBook()

    # Metadata
    libro.set_identifier("id123456")
    libro.set_title(titulo)
    libro.set_language("es")
    libro.add_author(autor)

    # Agregar portada si existe
    if portada:
        with open(portada, "rb") as img:
            libro.set_cover("cover.jpg", img.read())

    # Crear un capítulo con el contenido del TXT
    capitulo = epub.EpubHtml(title="Contenido", file_name="chap1.xhtml", lang="es")
    capitulo.content = f"<h1>{titulo}</h1><p>{texto.replace('\n', '<br/>')}</p>"

    # Añadir capítulo al libro
    libro.add_item(capitulo)

    # Definir la estructura
    libro.toc = (epub.Link("chap1.xhtml", "Contenido", "intro"),)
    libro.add_item(epub.EpubNcx())
    libro.add_item(epub.EpubNav())

    # Definir CSS básico
    estilo = "BODY { font-family: Arial; } h1 { text-align: center; }"
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=estilo)
    libro.add_item(nav_css)

    # Spine (orden de lectura)
    libro.spine = ["nav", capitulo]

    # Guardar como archivo EPUB
    epub.write_epub(ruta_epub, libro, {})

    print(f"✅ Conversión completada. Archivo guardado en: {ruta_epub}")


# Ejemplo de uso:
if __name__ == "__main__":
    txt_a_epub(
        "mi_texto.txt",        # archivo de entrada
        "The Miracle Morning.epub",       # archivo de salida
        titulo="The Miracle Morning",
        autor="Hal Elrod",
        portada="portada.jpg"  # imagen de portada opcional
    )