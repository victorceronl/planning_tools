import os
from PyPDF2 import PdfMerger

def unir_pdfs(carpeta, archivo_salida):
    merger = PdfMerger()

    # Obtener todos los PDFs de la carpeta
    pdfs = [f for f in os.listdir(carpeta) if f.lower().endswith(".pdf")]
    pdfs.sort()  # Orden alfabético

    if not pdfs:
        print("⚠️ No se encontraron archivos PDF en la carpeta.")
        return

    # Agregar cada PDF
    for pdf in pdfs:
        ruta_pdf = os.path.join(carpeta, pdf)
        print(f"📄 Agregando: {pdf}")
        merger.append(ruta_pdf)

    # Guardar archivo combinado
    salida = os.path.join(carpeta, archivo_salida)
    merger.write(salida)
    merger.close()
    print(f"\n✅ Archivos combinados correctamente en: {salida}")

# Ejemplo de uso
if __name__ == "__main__":
    carpeta = input("Ruta de la carpeta con los PDF: ").strip()
    archivo_salida = input("Nombre del PDF final (por ejemplo, combinado.pdf): ").strip()
    unir_pdfs(carpeta, archivo_salida)