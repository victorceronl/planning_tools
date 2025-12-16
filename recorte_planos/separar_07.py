from pdf2image import convert_from_path
import cv2
import numpy as np
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from PIL import Image
import os

PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
SALIDA = "piezas_carta"

os.makedirs(SALIDA, exist_ok=True)

# Convertir PDF a imágenes
paginas = convert_from_path(PDF_ENTRADA, dpi=300)

pieza_id = 1

for pagina in paginas:
    img = np.array(pagina)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarización
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Detectar contornos
    contornos, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contornos:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filtros para marcos de planos
        area = w * h
        relacion = w / h if h else 0

        if area < 300_000:
            continue
        if not (0.5 < relacion < 2.5):
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

print("Separación de planos finalizada usando visión artificial.")
