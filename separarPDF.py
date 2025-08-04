import os
from PyPDF2 import PdfReader, PdfWriter

archivo_original = 'documento.pdf'  # Cambia por tu archivo PDF
carpeta_salida = 'paginas_separadas'
os.makedirs(carpeta_salida, exist_ok=True)

# Leer el PDF original
pdf = PdfReader(archivo_original)

for i in range(len(pdf.pages)):
    writer = PdfWriter()
    writer.add_page(pdf.pages[i])

    nombre_salida = f'{i+1}- .pdf'
    ruta_salida = os.path.join(carpeta_salida, nombre_salida)

    with open(ruta_salida, 'wb') as f:
        writer.write(f)

    print(f"📄 Página {i+1} guardada como: {nombre_salida}")