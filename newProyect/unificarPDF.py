import os
from PyPDF2 import PdfMerger  # Usa PdfMerger en lugar de PdfFileMerger (más actualizado)

carpeta_pdfs = 'pdf_etiquetados'  # Cambia esta ruta a tu carpeta
archivo_salida = 'PDF_unido.pdf'

# Obtener lista de PDFs ordenada alfabéticamente
pdfs = sorted([f for f in os.listdir(carpeta_pdfs) if f.lower().endswith('.pdf')])

merger = PdfMerger()

for pdf in pdfs:
    ruta_pdf = os.path.join(carpeta_pdfs, pdf)
    merger.append(ruta_pdf)
    print(f"📥 Añadido: {pdf}")

# Guardar el PDF final
merger.write(archivo_salida)
merger.close()

print(f"✅ PDF fusionado guardado como: {archivo_salida}")