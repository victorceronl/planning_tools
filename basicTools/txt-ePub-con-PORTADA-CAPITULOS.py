import re
from ebooklib import epub

def txt_a_epub(ruta_txt, ruta_epub, titulo="Mi Libro", autor="Desconocido", portada=None, marcador="#CAP#"):
    # Leer el contenido del archivo .txt
    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    # Expresión regular para detectar capítulos del tipo: #CAP# Título #CAP#
    patron = rf"{re.escape(marcador)}(.*?){re.escape(marcador)}"
    coincidencias = list(re.finditer(patron, texto, flags=re.DOTALL))

    # Crear libro EPUB
    libro = epub.EpubBook()
    libro.set_identifier("id123456")
    libro.set_title(titulo)
    libro.set_language("es")
    libro.add_author(autor)

    # Agregar portada si existe
    if portada:
        with open(portada, "rb") as img:
            libro.set_cover("cover.jpg", img.read())

    capitulos = []
    # Procesar capítulos
    for i, match in enumerate(coincidencias):
        # Título del capítulo
        titulo_cap = match.group(1).strip()

        # Posición del final del marcador
        fin = match.end()

        # Contenido: desde el final del marcador actual hasta el siguiente marcador o fin de texto
        inicio_contenido = fin
        fin_contenido = coincidencias[i + 1].start() if i + 1 < len(coincidencias) else len(texto)
        contenido = texto[inicio_contenido:fin_contenido].strip()

        # Crear capítulo EPUB
        capitulo = epub.EpubHtml(
            title=titulo_cap,
            file_name=f"chap{i + 1}.xhtml",
            lang="es"
        )
        capitulo.content = f"<h2>{titulo_cap}</h2><p>{contenido.replace('\n', '<br/>')}</p>"

        libro.add_item(capitulo)
        capitulos.append(capitulo)

    # Crear TOC (tabla de contenidos)
    libro.toc = tuple(epub.Link(c.file_name, c.title, f"chap_{i+1}") for i, c in enumerate(capitulos))

    # Agregar navegación y estilo
    libro.add_item(epub.EpubNcx())
    libro.add_item(epub.EpubNav())

    estilo = """
    body { font-family: Arial; line-height: 1.6; margin: 5%; }
    h1, h2 { text-align: center; }
    p { text-align: justify; }
    """
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=estilo)
    libro.add_item(nav_css)

    # Definir el orden de lectura
    libro.spine = ["nav"] + capitulos

    # Guardar archivo
    epub.write_epub(ruta_epub, libro, {})
    print(f"✅ Conversión completada. Archivo guardado en: {ruta_epub}")
    print(f"📚 Capítulos detectados: {len(capitulos)}")


# Ejemplo de uso:
if __name__ == "__main__":
    txt_a_epub(
        "mi_texto.txt",         # archivo de entrada
        "mi_libro.epub",        # archivo de salida
        titulo="Mi Libro de Prueba",
        autor="Autor Desconocido",
        portada="portada.jpg",  # opcional
        marcador="#CAP#"        # marcador de capítulo
    )
