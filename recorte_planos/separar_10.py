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

# ZONAS RELATIVAS (ajustables)
ZONAS = [
    (0.00, 0.00, 0.50, 0.50),
    (0.50, 0.00, 1.00, 0.50),
    (0.00, 0.50, 0.50, 1.00),
    (0.50, 0.50, 1.00, 1.00),
]

for page in doc:
    pix = page.get_pixmap(dpi=200)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    for zx0, zy0, zx1, zy1 in ZONAS:
        x0 = int(zx0 * pix.width)
        y0 = int(zy0 * pix.height)
        x1 = int(zx1 * pix.width)
        y1 = int(zy1 * pix.height)

        recorte = img.crop((x0, y0, x1, y1))

        # Descartar zonas vacías
        if recorte.getbbox() is None:
            continue

        temp = f"temp_{pieza_id}.png"
        recorte.save(temp)

        salida = os.path.join(SALIDA, f"Pieza_{pieza_id}.pdf")
        c = canvas.Canvas(salida, pagesize=LETTER)

        w, h = LETTER
        c.drawImage(temp, 0, 0, width=w, height=h, preserveAspectRatio=True)
        c.showPage()
        c.save()

        os.remove(temp)
        pieza_id += 1

print("Separación por layout fijo completada.")
