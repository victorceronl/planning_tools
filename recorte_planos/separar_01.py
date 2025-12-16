import fitz  # PyMuPDF
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

# ========= CONFIGURACIÓN =========
PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
CARPETA_SALIDA = "planos_separados"
PALABRAS_CLAVE = ["TEIL / Part", "GRIPPER", "US-30D"]

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# ========= ABRIR PDF =========
doc = fitz.open(PDF_ENTRADA)

planos = []
plano_actual = []

def contiene_palabra_clave(texto):
    texto = texto.upper()
    return any(palabra.upper() in texto for palabra in PALABRAS_CLAVE)

# ========= DETECTAR PLANOS =========
for i, page in enumerate(doc):
    texto = page.get_text()

    if contiene_palabra_clave(texto) and plano_actual:
        planos.append(plano_actual)
        plano_actual = []

    plano_actual.append(i)

if plano_actual:
    planos.append(plano_actual)

# ========= CREAR PDF CARTA =========
for idx, paginas in enumerate(planos, start=1):
    salida_pdf = os.path.join(CARPETA_SALIDA, f"Plano_{idx}.pdf")
    c = canvas.Canvas(salida_pdf, pagesize=LETTER)

    for num_pagina in paginas:
        pagina = doc.load_page(num_pagina)
        pix = pagina.get_pixmap(dpi=200)

        img_path = f"temp_{idx}.png"
        pix.save(img_path)

        ancho, alto = LETTER
        c.drawImage(img_path, 0, 0, width=ancho, height=alto)
        c.showPage()

        os.remove(img_path)

    c.save()

print(f"Proceso terminado. {len(planos)} planos separados.")
