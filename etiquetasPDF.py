import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Configura tus rutas
carpeta_pdfs = "carpeta_pdfs"
archivo_excel = "etiquetas.xlsx"
salida_pdfs = "pdf_etiquetados"

# Crear carpeta de salida si no existe
os.makedirs(salida_pdfs, exist_ok=True)

# Leer el Excel con columnas A, B, C, D, E, F
df = pd.read_excel(archivo_excel, usecols=[0, 1, 2, 3, 4, 5], header=None)
df.columns = ['nombre_pdf', 'etiqueta', 'descripcion', 'categoria', 'material', 'acabado']

# Crear diccionario con datos convertidos
info_dict = {
    str(row['nombre_pdf']): {
        'etiqueta': str(row['etiqueta']),
        'descripcion': str(int(row['descripcion'])) if pd.notna(row['descripcion']) else '',
        'categoria': str(int(row['categoria'])) if pd.notna(row['categoria']) else '',
        'material': str(row['material']),
        'acabado': str(row['acabado']),
    }
    for _, row in df.iterrows()
}

# Función que genera los recuadros individuales por texto
def crear_etiqueta_pdf(info, ancho, alto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(ancho, alto))

    # Textos y configuración
    textos_grandes = [
        f"{info['etiqueta']}",
        f"{info['descripcion']}x/{info['categoria']}x"
    ]
    texto_pequeno = f"{info['material']}  {info['acabado']}"

    # Configuración estilos
    font_size_grande = 20
    font_size_pequeno = 8
    padding_x = 10
    padding_y = 6
    margen_derecho = 10

    # Posición inicial desde arriba
    y = alto - font_size_grande - 25

    # Dibujar recuadros para textos grandes
    c.setFont("Helvetica-Bold", font_size_grande)
    for texto in textos_grandes:
        text_width = c.stringWidth(texto, "Helvetica-Bold", font_size_grande)
        box_width = text_width + 2 * padding_x
        box_height = font_size_grande + padding_y * 2
        x = ancho - box_width - margen_derecho

        c.setFillColorRGB(1, 1, 1)
        c.rect(x, y, box_width, box_height, fill=1)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x, y, box_width, box_height, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x + padding_x, y + padding_y, texto)

        y -= box_height + 2

    # Dibujar recuadro para texto pequeño
    c.setFont("Helvetica-Bold", font_size_pequeno)
    text_width = c.stringWidth(texto_pequeno, "Helvetica-Bold", font_size_pequeno)
    box_width = text_width + 2 * padding_x
    box_height = font_size_pequeno + padding_y * 2
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