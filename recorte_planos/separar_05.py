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

AREA_MINIMA = 400_000     # ajustar si es necesario
RELACION_MIN = 0.6
RELACION_MAX = 2.8

for page in doc:
    dibujos = page.get_drawings()
    candidatos = []

    for d in dibujos:
        if not d["items"]:
            continue

        # Bounding box del drawing completo
        rect = fitz.Rect(d["bbox"])

        area = rect.width * rect.height
        if rect.height == 0:
            continue

        relacion = rect.width / rect.height

        if (
            area > AREA_MINIMA and
            RELACION_MIN < relacion < RELACION_MAX
        ):
            candidatos.append(rect)

    # Eliminar duplicados (solapados)
    rects_limpios = []
    for r in candidatos:
        if not any(r.intersects(o) and abs(r.area - o.area) < 0.15 * r.area for o in rects_limpios):
            rects_limpios.append(r)

    if not rects_limpios:
        continue

    # Renderizar página
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    escala_x = pix.width / page.rect.width
    escala_y = pix.height / page.rect.height

    for rect in rects_limpios:
        x0 = int(rect.x0 * escala_x)
        y0 = int(rect.y0 * escala_y)
        x1 = int(rect.x1 * escala_x)
        y1 = int(rect.y1 * escala_y)

        # Protección contra recortes inválidos
        if x1 - x0 < 300 or y1 - y0 < 300:
            continue

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

print("Separación por marcos (paths) finalizada correctamente.")
