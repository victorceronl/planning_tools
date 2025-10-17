from ebooklib import epub
import html
import re
import os




def limpiar_texto(texto):
# Eliminar caracteres invisibles y problemáticos
texto = texto.replace("&", "&")
texto = texto.replace("<", "<").replace(">", ">")
texto = re.sub(r"[^\x09\x0A\x0D\x20-\x7EáéíóúÁÉÍÓÚñÑüÜ’“”‘–—…]", "", texto)
texto = texto.replace("\r", "")
texto = re.sub(r"\n{2,}", "\n", texto)
return texto.strip()




def dividir_en_capitulos(texto):
# Dividir por encabezados tipo PART o capítulo numerado
patron = re.compile(r"(?=(?\s+\d+|[0-9]{1,2}\s+[A-Z][A-Z\s]+))")
partes = patron.split(texto)
capitulos = [p.strip() for p in partes if len(p.strip()) > 100] # descartar basura
return capitulos




def txt_a_epub(ruta_txt, ruta_epub, titulo="Mi Libro", autor="Desconocido", portada=None):
# Leer y limpiar texto
with open(ruta_txt, "r", encoding="utf-8") as f:
texto = f.read()

texto = limpiar_texto(texto)
capitulos = dividir_en_capitulos(texto)

# Crear el libro EPUB
libro = epub.EpubBook()
libro.set_identifier("id123456")
libro.set_title(titulo)
libro.set_language("es")
libro.add_author(autor)

# Agregar portada
if portada and os.path.exists(portada):
    with open(portada, "rb") as img:
        libro.set_cover("cover.jpg", img.read())

# Crear capítulos
capitulos_items = []
for i, cap in enumerate(capitulos, start=1):
    titulo_cap = cap.split("\n", 1)[0][:60]
    contenido_seguro = html.escape(cap).replace("\n", "<br/>")
    capitulo = epub.EpubHtml(title=titulo_cap, file_name=f"chap{i}.xhtml", lang="es")
    capitulo.content = f"<h2>{titulo_cap}</h2><p>{contenido_seguro}</p>"
    libro.add_item(capitulo)
    capitulos_items.append(capitulo)

# Tabla de contenidos
libro.toc = tuple(epub.Link(f"chap{i+1}.xhtml", c.title, f"chap{i+1}") for i, c in enumerate(capitulos_items))

# Navegación
libro.add_item(epub.EpubNcx())
libro.add_item(epub.EpubNav())

# Estilo
estilo = "body { font-family: Arial; line-height: 1.5; } h1,h2 { text-align: center; }"
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=estilo)
libro.add_item(nav_css)

# Orden de lectura
libro.spine = ["nav"] + capitulos_items

epub.write_epub(ruta_epub, libro, {})
print(f"✅ EPUB generado con {len(capitulos_items)} capítulos: {ruta_epub}")




if name == "main":
txt_a_epub(
"Start with Why.txt",
"Start with Why.epub",
titulo="Start with Why",
autor="Simon Sinek",
portada="portada.jpg"
)