import fitz
from PIL import Image
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen import canvas
import os

PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
SALIDA = "piezas_carta"

os.makedirs(SALIDA, exist_ok=True)

doc = fitz.open(PDF_ENTRADA)
pieza_id = 1

# =========================
# DEFINICIÓN DE LAYOUTS
# =========================
LAYOUTS = {
    "1_plano": [
        (0.00, 0.00, 1.00, 1.00),
    ],
    "2_planos": [
        (0.00, 0.00, 0.50, 1.00),
        (0.50, 0.00, 1.00, 1.00),
    ],
    "3_planos": [
        (0.00, 0.00, 0.50, 0.50),
        (0.50, 0.00, 1.00, 0.50),
        (0.00, 0.50, 1.00, 1.00),
    ],
    "4_planos": [
        (0.00, 0.00, 0.50, 0.50),
        (0.50, 0.00, 1.00, 0.50),
        (0.00, 0.50, 0.50, 1.00),
        (0.50, 0.50, 1.00, 1.00),
    ],
}

def tiene_contenido(img: Image.Image) -> bool:
    """
    Determina si un recorte está vacío (solo blanco)
    """
    bbox = img.getbbox()
    return bbox is not None

# =========================
# PROCESAMIENTO
# =========================
for page in doc:
    pix = page.get_pixmap(dpi=200)
    imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    for nombre_layout, zonas in LAYOUTS.items():
        recortes_validos = []

        for zx0, zy0, zx1, zy1 in zonas:
            x0 = int(zx0 * pix.width)
            y0 = int(zy0 * pix.height)
            x1 = int(zx1 * pix.width)
            y1 = int(zy1 * pix.height)

            recorte = imagen.crop((x0, y0, x1, y1))

            if tiene_contenido(recorte):
                recortes_validos.append(recorte)

        # Si este layout no tiene contenido real, se ignora
        if not recortes_validos:
            continue

        # Exportar cada recorte válido
        for recorte in recortes_validos:
            temp_img = f"temp_{pieza_id}.png"
            recorte.save(temp_img)

            salida_pdf = os.path.join(SALIDA, f"Pieza_{pieza_id}.pdf")
            c = canvas.Canvas(
                salida_pdf,
                pagesize=landscape(LETTER)
            )

            w, h = landscape(LETTER)
            c.drawImage(
                temp_img,
                0,
                0,
                width=w,
                height=h,
                preserveAspectRatio=True,
                anchor="c"
            )

            c.showPage()
            c.save()

            os.remove(temp_img)
            pieza_id += 1

print("Exportación finalizada en formato Carta Horizontal.")
