import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# Registrar fuente
pdfmetrics.registerFont(TTFont("Arial-Black", "Arial-Black.ttf"))

# Rutas
carpeta_pdfs = "planos_originales"
archivo_excel = "etiquetas.xlsx"
archivo_txt = "lista_excluir.txt"   # <-- NUEVO
salida_pdfs = "pdf_etiquetados"

os.makedirs(salida_pdfs, exist_ok=True)

# Leer Excel
df = pd.read_excel(archivo_excel, usecols=[0, 1, 2, 3, 4, 5, 6], header=None)
df.columns = ['nombre_pdf', 'etiqueta', 'descripcion', 'categoria', 'material', 'acabado', 'etiqueta_izquierda']

info_dict = {
    str(row['nombre_pdf']): {
        'etiqueta': str(row['etiqueta']),
        'descripcion': str(int(row['descripcion'])) if pd.notna(row['descripcion']) else '',
        'categoria': str(int(row['categoria'])) if pd.notna(row['categoria']) else '',
        'material': str(row['material']),
        'acabado': str(row['acabado']),
        'etiqueta_izquierda': str(row['etiqueta_izquierda']),
    }
    for _, row in df.iterrows()
}

# === LEER TXT (lista de exclusión) ===
with open(archivo_txt, 'r', encoding='utf-8') as f:
    lista_excluir = set(line.strip() for line in f if line.strip())

# Función etiqueta (SIN CAMBIOS)
def crear_etiqueta_pdf(info, ancho, alto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(ancho, alto))

    textos_grandes = [
        f"{info['etiqueta']}",
        f"{info['descripcion']}x/{info['categoria']}x"
    ]
    texto_pequeno = f"{info['material']}  {info['acabado']}"
    texto_izquierda = info['etiqueta_izquierda']

    font_name = "Arial-Black"
    font_size_derecha_grande = 30
    font_size_derecha_pequeno = 15
    font_size_izquierda = 35
    padding_x = 10
    padding_y = 6
    margen_derecho = 10
    margen_izquierdo = 10

    # IZQUIERDA
    c.setFont(font_name, font_size_izquierda)
    text_width_izq = c.stringWidth(texto_izquierda, font_name, font_size_izquierda)
    box_width_izq = text_width_izq + 2 * padding_x
    box_height_izq = font_size_izquierda + padding_y * 2
    x_izq = margen_izquierdo
    y_izq = alto - box_height_izq - 10

    c.setFillColorRGB(1, 1, 1)
    c.rect(x_izq, y_izq, box_width_izq, box_height_izq, fill=1)
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(x_izq, y_izq, box_width_izq, box_height_izq, fill=0)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x_izq + padding_x, y_izq + padding_y, texto_izquierda)

    # DERECHA
    y = alto - font_size_derecha_grande - 25
    c.setFont(font_name, font_size_derecha_grande)

    for texto in textos_grandes:
        text_width = c.stringWidth(texto, font_name, font_size_derecha_grande)
        box_width = text_width + 2 * padding_x
        box_height = font_size_derecha_grande + padding_y * 2
        x = ancho - box_width - margen_derecho

        c.setFillColorRGB(1, 1, 1)
        c.rect(x, y, box_width, box_height, fill=1)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x, y, box_width, box_height, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x + padding_x, y + padding_y, texto)

        y -= box_height + 2

    # Texto pequeño
    c.setFont(font_name, font_size_derecha_pequeno)
    text_width = c.stringWidth(texto_pequeno, font_name, font_size_derecha_pequeno)
    box_width = text_width + 2 * padding_x
    box_height = font_size_derecha_pequeno + padding_y * 2
    x = ancho - box_width - margen_derecho
    y -= -10

    c.setFillColorRGB(1, 1, 1)
    c.rect(x, y, box_width, box_height, fill=1)
    c.setStrokeColorRGB(0, 0, 0)
    c.rect(x, y, box_width, box_height, fill=0)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x + padding_x, y + padding_y, texto_pequeno)

    c.save()
    buffer.seek(0)
    return PdfReader(buffer)

# === PROCESO PRINCIPAL MODIFICADO ===
for archivo in os.listdir(carpeta_pdfs):
    if archivo.lower().endswith('.pdf'):
        nombre_sin_extension = os.path.splitext(archivo)[0]

        # 🔴 NUEVA CONDICIÓN: SOLO LOS QUE NO ESTÁN EN EL TXT
        if nombre_sin_extension not in lista_excluir:

            if nombre_sin_extension in info_dict:
                datos = info_dict[nombre_sin_extension]
            else:
                print(f"⚠ Sin info en Excel (omitido): {archivo}")
                continue

            path_pdf = os.path.join(carpeta_pdfs, archivo)
            reader = PdfReader(path_pdf)
            writer = PdfWriter()

            for pagina in reader.pages:
                ancho = float(pagina.mediabox.width)
                alto = float(pagina.mediabox.height)

                etiqueta_pdf = crear_etiqueta_pdf(datos, ancho, alto)
                pagina.merge_page(etiqueta_pdf.pages[0])
                writer.add_page(pagina)

            output_path = os.path.join(salida_pdfs, archivo)
            with open(output_path, "wb") as salida_pdf:
                writer.write(salida_pdf)

            print(f"✔ Etiquetado (NO en TXT): {archivo}")

        else:
            print(f"⏭ Omitido (en TXT): {archivo}")