import fitz
import cv2
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os
import warnings

# Evitar warning de imágenes grandes
Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
SALIDA = "piezas_carta"

os.makedirs(SALIDA, exist_ok=True)

doc = fitz.open(PDF_ENTRADA)
pieza_id = 1

for page in doc:
    # Rasterizar a DPI razonable
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape(pix.height, pix.width, 3)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detección de bordes (mejor para planos)
    edges = cv2.Canny(gray, 50, 150)

    # Engrosar líneas para cerrar marcos
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    edges = cv2.dilate(edges, kernel, iterations=2)

    # Detectar contornos
    contornos, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contornos:
        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h
        relacion = w / h if h else 0

        # Filtros AJUSTADOS a planos grandes
        if area < 200_000:
            continue
        if not (0.6 < relacion < 3.0):
            continue

        recorte = img[y:y+h, x:x+w]

        temp_img = f"temp_{pieza_id}.png"
        Image.fromarray(recorte).save(temp_img)

        salida_pdf = os.path.join(SALIDA, f"Pieza_{pieza_id}.pdf")
        c = canvas.Canvas(salida_pdf, pagesize=LETTER)

        w_c, h_c = LETTER
        c.drawImage(
            temp_img,
            0,
            0,
            width=w_c,
            height=h_c,
            preserveAspectRatio=True,
            anchor="c"
        )

        c.showPage()
        c.save()

        os.remove(temp_img)
        pieza_id += 1

print("Separación de planos completada correctamente.")
