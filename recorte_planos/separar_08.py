import fitz
import cv2
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
SALIDA = "piezas_carta"

os.makedirs(SALIDA, exist_ok=True)

doc = fitz.open(PDF_ENTRADA)
pieza_id = 1

for page in doc:
    # Rasterizar página
    pix = page.get_pixmap(dpi=300)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape(pix.height, pix.width, 3)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarización adaptativa (mejor para planos)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        51, 5
    )

    # Detectar contornos
    contornos, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contornos:
        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h
        relacion = w / h if h else 0

        # Filtros ajustables
        if area < 500_000:
            continue
        if not (0.6 < relacion < 2.5):
            continue

        recorte = img[y:y+h, x:x+w]

        # Guardar temporal
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

print("Separación de planos completada SIN Poppler.")
