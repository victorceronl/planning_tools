from ebooklib import epub

def txt_a_epub(ruta_txt, ruta_epub, titulo="Mi Libro", autor="Desconocido", portada=None, imagenes=[]):
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

    # Crear capítulo principal con el texto
    capitulo = epub.EpubHtml(title="Contenido", file_name="chap1.xhtml", lang="es")
    capitulo.content = f"<h1>{titulo}</h1><p>{texto.replace('\n', '<br/>')}</p>"

    # Si hay imágenes, agregarlas al libro y al capítulo
    for i, ruta_img in enumerate(imagenes, start=1):
        with open(ruta_img, "rb") as img_file:
            # Crear recurso de imagen
            imagen = epub.EpubItem(
                uid=f"image_{i}",
                file_name=f"images/img{i}.jpg",
                media_type="image/jpeg",
                content=img_file.read()
            )
            libro.add_item(imagen)

        # Insertar imagen en el contenido del capítulo
        capitulo.content += f'<div style="text-align:center;"><img src="images/img{i}.jpg" alt="Imagen {i}" /></div>'

    # Añadir capítulo al libro
    libro.add_item(capitulo)

    # Definir la estructura
    libro.toc = (epub.Link("chap1.xhtml", "Contenido", "intro"),)
    libro.add_item(epub.EpubNcx())
    libro.add_item(epub.EpubNav())

    # Definir CSS básico
    estilo = """
    body { font-family: Arial; line-height: 1.4; }
    h1 { text-align: center; }
    img { max-width: 100%; margin: 20px 0; }
    """
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
        "mi_texto.txt",         # archivo de entrada
        "mi_libro.epub",        # archivo de salida
        titulo="Mi Ebook con Imágenes",
        autor="Victor Ceron",
        portada="portada.jpg",  # opcional
        imagenes=["img1.jpg", "img2.jpg"]  # lista de imágenes a insertar en el capítulo
    )
