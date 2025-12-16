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

# Umbrales ajustables según tus planos
AREA_MINIMA = 300_000      # descarta cuadros pequeños
RELACION_MIN = 0.5         # ancho / alto
RELACION_MAX = 2.5

for page in doc:
    dibujos = page.get_drawings()
    rectangulos = []

    for d in dibujos:
        for item in d["items"]:
            if item[0] == "re":  # rectangle
                rect = fitz.Rect(item[1])

                area = rect.width * rect.height
                relacion = rect.width / rect.height if rect.height else 0

                if (
                    area > AREA_MINIMA and
                    RELACION_MIN < relacion < RELACION_MAX
                ):
                    rectangulos.append(rect)

    # Eliminar duplicados (rectángulos casi iguales)
    rectangulos_limpios = []
    for r in rectangulos:
        if not any(r.intersects(o) and abs(r.area - o.area) < 0.1 * r.area for o in rectangulos_limpios):
            rectangulos_limpios.append(r)

    if not rectangulos_limpios:
        continue

    # Renderizar página completa
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    escala_x = pix.width / page.rect.width
    escala_y = pix.height / page.rect.height

    for rect in rectangulos_limpios:
        x0 = int(rect.x0 * escala_x)
        y0 = int(rect.y0 * escala_y)
        x1 = int(rect.x1 * escala_x)
        y1 = int(rect.y1 * escala_y)

        recorte = img.crop((x0, y0, x1, y1))

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

print("Separación por marcos finalizada correctamente.")
