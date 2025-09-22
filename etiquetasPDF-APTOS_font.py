import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# Registrar la fuente Aptos Black (asegúrate de tener el archivo .ttf en la ruta indicada)
pdfmetrics.registerFont(TTFont("Arial-Black", "Arial-Black.ttf"))

# Configura tus rutas
carpeta_pdfs = "carpeta_pdfs"
archivo_excel = "etiquetas.xlsx"
salida_pdfs = "pdf_etiquetados"

# Crear carpeta de salida si no existe
os.makedirs(salida_pdfs, exist_ok=True)

# Leer el Excel con columnas A-G (índices 0 a 6)
df = pd.read_excel(archivo_excel, usecols=[0, 1, 2, 3, 4, 5, 6], header=None)
df.columns = ['nombre_pdf', 'etiqueta', 'descripcion', 'categoria', 'material', 'acabado', 'etiqueta_izquierda']

# Crear diccionario con datos convertidos
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

# Función que genera los recuadros individuales por texto
def crear_etiqueta_pdf(info, ancho, alto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(ancho, alto))

    # Textos del lado derecho
    textos_grandes = [
        f"{info['etiqueta']}",
        f"{info['descripcion']}x/{info['categoria']}x"
    ]
    texto_pequeno = f"{info['material']}  {info['acabado']}"
    texto_izquierda = info['etiqueta_izquierda']

    # Configuración estilos
    font_name = "Arial-Black"
    font_size_derecha_grande = 35
    font_size_derecha_pequeno = 20
    font_size_izquierda = 40
    padding_x = 10
    padding_y = 6
    margen_derecho = 10
    margen_izquierdo = 10

    # === ETIQUETA IZQUIERDA ===
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

    # === ETIQUETAS DERECHA ===
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

    # Recuadro para texto pequeño
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

# Procesar cada PDF
for archivo in os.listdir(carpeta_pdfs):
    if archivo.lower().endswith('.pdf'):
        nombre_sin_extension = os.path.splitext(archivo)[0]
        if nombre_sin_extension in info_dict:
            datos = info_dict[nombre_sin_extension]
            path_pdf = os.path.join(carpeta_pdfs, archivo)
            reader = PdfReader(path_pdf)
            writer = PdfWriter()

            for pagina in reader.pages:
                ancho = float(pagina.mediabox.width)
                alto = float(pagina.mediabox.height)

                etiqueta_pdf = crear_etiqueta_pdf(datos, ancho, alto)
                etiqueta_pagina = etiqueta_pdf.pages[0]
                pagina.merge_page(etiqueta_pagina)
                writer.add_page(pagina)

            output_path = os.path.join(salida_pdfs, archivo)
            with open(output_path, "wb") as salida_pdf:
                writer.write(salida_pdf)

            print(f"✔ Etiqueta agregada: {archivo}")
        else:
            print(f"⚠ Sin información en Excel: {archivo}")
