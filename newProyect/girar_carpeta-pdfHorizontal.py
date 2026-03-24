import fitz  # PyMuPDF
import os

# =========================
# CONFIGURACIÓN
# =========================
CARPETA_ENTRADA = "pdf_entrada"
CARPETA_SALIDA = "pdf_horizontal"

# =========================
# FUNCIÓN PRINCIPAL
# =========================
def rotar_pdfs_carpeta(carpeta_entrada, carpeta_salida):

    os.makedirs(carpeta_salida, exist_ok=True)

    for archivo in os.listdir(carpeta_entrada):

        if not archivo.lower().endswith(".pdf"):
            continue

        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_salida = os.path.join(
            carpeta_salida,
            f"{nombre_base}-h.pdf"
        )

        print(f"\nProcesando: {archivo}")

        doc = fitz.open(ruta_entrada)

        for i, pagina in enumerate(doc):
            rotacion_actual = pagina.rotation

            # Rotar solo si está en vertical
            if rotacion_actual in (0, 180):
                pagina.set_rotation((rotacion_actual + 90) % 360)

        doc.save(ruta_salida)
        doc.close()

        print(f"Guardado como: {nombre_base}-h.pdf")

    print("\nProceso completado para todos los PDFs")

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":

    if not os.path.exists(CARPETA_ENTRADA):
        print("❌ La carpeta de entrada no existe")
    else:
        rotar_pdfs_carpeta(CARPETA_ENTRADA, CARPETA_SALIDA)
