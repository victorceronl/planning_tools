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
# LAYOUTS GENERALES
# =========================
LAYOUTS = {
    1: [(0.00, 0.00, 1.00, 1.00)],
    2: [(0.00, 0.00, 0.50, 1.00), (0.50, 0.00, 1.00, 1.00)],
    4: [(0.00, 0.00, 0.50, 0.50), (0.50, 0.00, 1.00, 0.50),
        (0.00, 0.50, 0.50, 1.00), (0.50, 0.50, 1.00, 1.00)],
    5: [(0.00, 0.00, 0.33, 0.50), (0.33, 0.00, 0.66, 0.50),
        (0.66, 0.00, 1.00, 0.50), (0.00, 0.50, 0.50, 1.00),
        (0.50, 0.50, 1.00, 1.00)],
    6: [(0.00, 0.00, 0.33, 0.50), (0.33, 0.00, 0.66, 0.50),
        (0.66, 0.00, 1.00, 0.50), (0.00, 0.50, 0.33, 1.00),
        (0.33, 0.50, 0.66, 1.00), (0.66, 0.50, 1.00, 1.00)],
}

# =========================
# LAYOUTS PARA 3 PLANOS
# =========================
LAYOUTS_3 = {
    1: [(0.00, 0.50, 1.00, 1.00), (0.00, 0.00, 0.50, 0.50), (0.50, 0.00, 1.00, 0.50)],
    2: [(0.00, 0.00, 0.50, 1.00), (0.50, 0.00, 1.00, 0.50), (0.50, 0.50, 1.00, 1.00)],
    3: [(0.00, 0.00, 0.50, 0.50), (0.00, 0.50, 0.50, 1.00), (0.50, 0.00, 1.00, 1.00)],
    4: [(0.00, 0.50, 0.50, 1.00), (0.50, 0.50, 1.00, 1.00), (0.00, 0.00, 1.00, 0.50)],
}

# =========================
# PROCESAR PDFs
# =========================
pdfs = [f for f in os.listdir(CARPETA_ENTRADA) if f.lower().endswith(".pdf")]

for pdf_nombre in pdfs:
    ruta_pdf = os.path.join(CARPETA_ENTRADA, pdf_nombre)
    print(f"\nProcesando PDF: {pdf_nombre}")

    doc = fitz.open(ruta_pdf)
    nombre_base = os.path.splitext(pdf_nombre)[0]
    carpeta_pdf = os.path.join(CARPETA_SALIDA, nombre_base)
    os.makedirs(carpeta_pdf, exist_ok=True)

    for num_pagina in range(doc.page_count):
        page = doc[num_pagina]
        print(f"  Página {num_pagina + 1} de {doc.page_count}")

        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.title(f"{pdf_nombre} – Página {num_pagina + 1}")
        plt.axis("off")
        plt.show()

        # =========================
        # SELECCIÓN DE PLANOS
        # =========================
        while True:
            try:
                seleccion = int(input(
                    "¿Cuántos planos tiene esta hoja? (1–6 | 0 = Omitir página): "
                ))
                if 0 <= seleccion <= 6:
                    break
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Ingresa solo un número.")

        # =========================
        # OMITIR PÁGINA
        # =========================
        if seleccion == 0:
            print("  Página omitida por el usuario.")
            plt.close()
            continue

        # =========================
        # SELECCIÓN DE LAYOUT
        # =========================
        dist = None

        if seleccion == 3:
            print("\nDistribuciones para 3 planos:")
            print("  1 → 1 arriba / 2 abajo")
            print("  2 → 1 izquierda / 2 derecha")
            print("  3 → 2 izquierda / 1 derecha")
            print("  4 → 2 arriba / 1 abajo")

            while True:
                try:
                    dist = int(input("Selecciona la distribución (1–4): "))
                    if dist in LAYOUTS_3:
                        zonas = LAYOUTS_3[dist]
                        break
                    else:
                        print("Opción no válida.")
                except ValueError:
                    print("Ingresa solo un número.")
        else:
            zonas = LAYOUTS[seleccion]

        # =========================
        # EXPORTACIÓN
        # =========================
        pieza_id = 1

        for zx0, zy0, zx1, zy1 in zonas:
            x0 = int(zx0 * pix.width)
            y0 = int(zy0 * pix.height)
            x1 = int(zx1 * pix.width)
            y1 = int(zy1 * pix.height)

            recorte = img.copy() if seleccion == 1 else img.crop((x0, y0, x1, y1))

            if recorte.getbbox() is None:
                continue

            # =========================
            # ROTACIÓN AUTOMÁTICA
            # =========================
            rotar = False

            # Caso normal: 2 planos
            if seleccion == 2 and recorte.height > recorte.width:
                rotar = True

            # Caso especial: 3 planos, distribución 2 (1 izquierda / 2 derecha)
            # La primera pieza es la de la izquierda
            if seleccion == 3 and dist == 2 and pieza_id == 1 and recorte.height > recorte.width:
                rotar = True

            if rotar:
                recorte = recorte.rotate(-90, expand=True)

            temp = f"temp_{os.getpid()}_{pieza_id}.png"
            recorte.save(temp)

            salida_pdf = os.path.join(
                carpeta_pdf,
                f"{nombre_base}_Pag{num_pagina + 1}_Pieza_{pieza_id}.pdf"
            )

            c = canvas.Canvas(salida_pdf, pagesize=landscape(LETTER))
            w, h = landscape(LETTER)

            c.drawImage(
                temp,
                0, 0,
                width=w,
                height=h,
                preserveAspectRatio=True,
                anchor="c"
            )

            c.showPage()
            c.save()
            os.remove(temp)

            pieza_id += 1

        plt.close()

    doc.close()
    print(f"PDF terminado: {pdf_nombre}")

print("\nTodos los PDFs fueron procesados correctamente.")