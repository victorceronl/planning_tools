import fitz
from PIL import Image
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen import canvas
import os

# =========================
# CONFIGURACIÓN
# =========================
CARPETA_ENTRADA = "pdf_entrada"
CARPETA_SALIDA = "piezas_carta"

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# =========================
# LAYOUTS DISPONIBLES
# =========================
LAYOUTS = {
    1: [  # PLANO COMPLETO (SIN RECORTE)
        (0.00, 0.00, 1.00, 1.00),
    ],
    2: [
        (0.00, 0.00, 0.50, 1.00),
        (0.50, 0.00, 1.00, 1.00),
    ],
    3: [
        (0.00, 0.00, 0.50, 0.50),
        (0.50, 0.00, 1.00, 0.50),
        (0.00, 0.50, 1.00, 1.00),
    ],
    4: [
        (0.00, 0.00, 0.50, 0.50),
        (0.50, 0.00, 1.00, 0.50),
        (0.00, 0.50, 0.50, 1.00),
        (0.50, 0.50, 1.00, 1.00),
    ],
    5: [
        (0.00, 0.00, 0.33, 0.50),
        (0.33, 0.00, 0.66, 0.50),
        (0.66, 0.00, 1.00, 0.50),
        (0.00, 0.50, 0.50, 1.00),
        (0.50, 0.50, 1.00, 1.00),
    ],
    6: [
        (0.00, 0.00, 0.33, 0.50),
        (0.33, 0.00, 0.66, 0.50),
        (0.66, 0.00, 1.00, 0.50),
        (0.00, 0.50, 0.33, 1.00),
        (0.33, 0.50, 0.66, 1.00),
        (0.66, 0.50, 1.00, 1.00),
    ],
}

# =========================
# PROCESAR CADA PDF
# =========================
pdfs = [f for f in os.listdir(CARPETA_ENTRADA) if f.lower().endswith(".pdf")]

for pdf_nombre in pdfs:
    ruta_pdf = os.path.join(CARPETA_ENTRADA, pdf_nombre)
    print(f"\nProcesando: {pdf_nombre}")

    doc = fitz.open(ruta_pdf)
    page = doc[0]

    pix = page.get_pixmap(dpi=150)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Mostrar PDF
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.title(f"{pdf_nombre} – Cierra esta ventana para continuar")
    plt.axis("off")
    plt.show()

    # =========================
    # SELECCIÓN DE LAYOUT
    # =========================
    print("\nLayouts disponibles:")
    for k in LAYOUTS:
        print(f"  {k} plano(s)")

    while True:
        try:
            seleccion = int(input("¿Cuántos planos tiene este PDF? (1–6): "))
            if seleccion in LAYOUTS:
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Ingresa solo un número.")

    zonas = LAYOUTS[seleccion]

    # Carpeta por PDF
    nombre_base = os.path.splitext(pdf_nombre)[0]
    carpeta_pdf = os.path.join(CARPETA_SALIDA, nombre_base)
    os.makedirs(carpeta_pdf, exist_ok=True)

    # =========================
    # EXPORTACIÓN
    # =========================
    pieza_id = 1

    for zx0, zy0, zx1, zy1 in zonas:
        x0 = int(zx0 * pix.width)
        y0 = int(zy0 * pix.height)
        x1 = int(zx1 * pix.width)
        y1 = int(zy1 * pix.height)

        # Para 1 plano: imagen completa
        if seleccion == 1:
            recorte = img.copy()
        else:
            recorte = img.crop((x0, y0, x1, y1))

        if recorte.getbbox() is None:
            continue

        # Rotación automática solo para 2 planos
        if seleccion == 2:
            ancho, alto = recorte.size
            if alto > ancho:
                recorte = recorte.rotate(90, expand=True)

        temp = f"temp_{pieza_id}.png"
        recorte.save(temp)

        salida_pdf = os.path.join(
            carpeta_pdf,
            f"{nombre_base}_Pieza_{pieza_id}.pdf"
        )

        c = canvas.Canvas(salida_pdf, pagesize=landscape(LETTER))
        w, h = landscape(LETTER)

        c.drawImage(
            temp,
            0,
            0,
            width=w,
            height=h,
            preserveAspectRatio=True,
            anchor="c"
        )

        c.showPage()
        c.save()

        os.remove(temp)
        pieza_id += 1

    doc.close()
    print(f"PDF terminado: {pdf_nombre}")

print("\nTodos los PDFs fueron procesados correctamente.")
