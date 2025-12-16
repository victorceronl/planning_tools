import fitz
from PIL import Image
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen import canvas
import os

PDF_ENTRADA = "US-30D_406905______________________A00_GRIPPER_6200R01G01_BL18.pdf"
SALIDA = "piezas_carta"

os.makedirs(SALIDA, exist_ok=True)

# =========================
# LAYOUTS DISPONIBLES
# =========================
LAYOUTS = {
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
# ABRIR PDF Y MOSTRAR PÁGINA
# =========================
doc = fitz.open(PDF_ENTRADA)
page = doc[0]

pix = page.get_pixmap(dpi=150)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.title("PDF ORIGINAL – Cierra esta ventana para continuar")
plt.axis("off")
plt.show()

# =========================
# SELECCIÓN DE LAYOUT
# =========================
print("\nLayouts disponibles:")
for k in LAYOUTS:
    print(f"  {k} planos")

while True:
    try:
        seleccion = int(input("\n¿Cuántos planos tiene el PDF? (2–6): "))
        if seleccion in LAYOUTS:
            break
        else:
            print("Opción no válida.")
    except ValueError:
        print("Ingresa un número válido.")

zonas = LA
