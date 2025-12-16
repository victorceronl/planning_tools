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

DISTANCIA_MIN_Y = 150  # evita detectar la misma pieza varias veces

for page in doc:
    text_dict = page.get_text("dict")

    candidatos = []

    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue

        for line in block["lines"]:
            texto = " ".join(span["text"] for span in line["spans"])

            if "TEIL / Part" in texto:
                x0, y0, x1, y1 = line["bbox"]
                candidatos.append((y0, y1))

    # Ordenar de arriba a abajo
    candidatos.sort()

    # Eliminar duplicados cercanos
    encabezados = []
    for y0, y1 in candidatos:
        if not encabezados or abs(y0 - encabezados[-1][0]) > DISTANCIA_MIN_Y:
            encabezados.append((y0, y1))

    if not encabezados:
        continue

    # Renderizar página completa una sola vez
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    for i, (y0, _) in enumerate(encabezados):
        if i < len(encabezados) - 1:
            y_fin = encabezados[i + 1][0]
        else:
            y_fin = pix.height

        # Margen de seguridad
        y_inicio = max(int(y0 - 40), 0)
        y_fin = min(int(y_fin + 20), pix.height)

        if y_fin - y_inicio < 300:
            continue  # evita recortes vacíos

        recorte = img.crop((0, y_inicio, pix.width, y_fin))

        temp_img = f"temp_{pieza_id}.png"
        recorte.save(temp_img)

        salida_pdf = os.path.join(SALIDA, f"Pieza_{pieza_id}.pdf")
        c = canvas.Canvas(salida_pdf, pagesize=LETTER)

        w, h = LETTER
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

print("Separación correcta de piezas finalizada.")
