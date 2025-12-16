import fitz
from PIL import Image
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
SALIDA = "piezas_carta"

os.makedirs(SALIDA, exist_ok=True)

doc = fitz.open(PDF_ENTRADA)

pieza_id = 1

for page_num, page in enumerate(doc):
    blocks = page.get_text("blocks")

    # Filtrar bloques que contienen "TEIL / Part"
    anchors = [b for b in blocks if "TEIL / Part" in b[4]]

    if not anchors:
        continue

    # Ordenar de arriba hacia abajo
    anchors.sort(key=lambda b: b[1])

    # Renderizar página completa
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    for i, anchor in enumerate(anchors):
        x0, y0, x1, y1 = anchor[:4]

        # Definir límite inferior
        if i < len(anchors) - 1:
            y_bottom = anchors[i + 1][1]
        else:
            y_bottom = pix.height

        # Margen de seguridad
        crop = img.crop((
            0,
            int(y0 - 20),
            pix.width,
            int(y_bottom)
        ))

        # Guardar temporal
        temp_img = f"temp_{pieza_id}.png"
        crop.save(temp_img)

        # Crear PDF Carta
        pdf_out = os.path.join(SALIDA, f"Pieza_{pieza_id}.pdf")
        c = canvas.Canvas(pdf_out, pagesize=LETTER)

        w, h = LETTER
        c.drawImage(temp_img, 0, 0, width=w, height=h, preserveAspectRatio=True, anchor='c')
        c.showPage()
        c.save()

        os.remove(temp_img)
        pieza_id += 1

print("Separación de piezas finalizada.")
