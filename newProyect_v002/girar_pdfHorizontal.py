import fitz  # PyMuPDF
import os

# =========================
# CONFIGURACIÓN
# =========================
PDF_ENTRADA = "US-30D_406919_A00_GRIPPER_6380R01G01.pdf"
PDF_SALIDA = "US-30D_406919_A00_GRIPPER_6380R01G01-h.pdf"

# =========================
# PROCESO
# =========================
def rotar_pdf_a_horizontal(pdf_entrada, pdf_salida):
    doc = fitz.open(pdf_entrada)

    for i, pagina in enumerate(doc):
        # Obtener rotación actual
        rotacion_actual = pagina.rotation

        # Rotar 90 grados si está en vertical
        # (normalmente vertical = 0 o 180)
        if rotacion_actual in (0, 180):
            pagina.set_rotation((rotacion_actual + 90) % 360)

        print(f"Página {i + 1} rotada a horizontal")

    doc.save(pdf_salida)
    doc.close()

    print("\nProceso finalizado")
    print(f"PDF generado: {pdf_salida}")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    if not os.path.exists(PDF_ENTRADA):
        print("❌ No se encontró el archivo de entrada")
    else:
        rotar_pdf_a_horizontal(PDF_ENTRADA, PDF_SALIDA)
