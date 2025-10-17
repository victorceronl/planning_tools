from ebooklib import epub
import html
import re

def limpiar_texto(texto):
    # Reemplazar caracteres problemáticos
    texto = texto.replace("&", "&amp;")  # escapar ampersand
    texto = texto.replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"[^\x09\x0A\x0D\x20-\x7EáéíóúÁÉÍÓÚñÑüÜ’“”‘–—…]", "", texto)
    texto = texto.replace("\r", "")
    # Unir saltos de línea múltiples en uno solo
    texto = re.sub(r"\n{2,}", "\n", texto)
    return texto

def txt_a_epub(ruta_txt, ruta_epub, titulo="Mi Libro", autor="Desconocido", portada=None):
    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    texto = limpiar_texto(texto)
    contenido_seguro = html.escape(texto).replace('\n', '<br/>')

    libro = epub.EpubBook()
    libro.set_identifier("id123456")
    libro.set_title(titulo)
    libro.set_language("es")
    libro.add_author(autor)

    if portada:
        with open(portada, "rb") as img:
            libro.set_cover("cover.jpg", img.read())

    capitulo = epub.EpubHtml(title="Contenido", file_name="chap1.xhtml", lang="es")
    capitulo.content = f"<h1>{titulo}</h1><p>{contenido_seguro}</p>"
    libro.add_item(capitulo)

    libro.toc = (epub.Link("chap1.xhtml", "Contenido", "intro"),)
    libro.add_item(epub.EpubNcx())
    libro.add_item(epub.EpubNav())

    estilo = "body { font-family: Arial; line-height: 1.5; } h1 { text-align:center; }"
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css",
                            media_type="text/css", content=estilo)
    libro.add_item(nav_css)

    libro.spine = ["nav", capitulo]
    epub.write_epub(ruta_epub, libro, {})
    print(f"✅ Conversión completada. Archivo guardado en: {ruta_epub}")

if __name__ == "__main__":
    txt_a_epub(
        "Start with Why.txt",
        "Start with Why.epub",
        titulo="Start with Why",
        autor="Simon Sinek",
        portada="portada.jpg"
    )
