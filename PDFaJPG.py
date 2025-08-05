import os
import fitz  # PyMuPDF

carpeta_pdfs = 'carpeta_pdfs'  # Ajusta a tu ruta
carpeta_salida = 'imagenes_jpg'
os.makedirs(carpeta_salida, exist_ok=True)

for archivo in os.listdir(carpeta_pdfs):
    if archivo.lower().endswith('.pdf'):
        ruta_pdf = os.path.join(carpeta_pdfs, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        doc = fitz.open(ruta_pdf)

        for i, pagina in enumerate(doc):
            # 👑 Aquí subimos el dpi para mejor calidad
            pix = pagina.get_pixmap(dpi=400)  # Puedes subir hasta 600 si tu equipo lo soporta
            nombre_imagen = f"{nombre_base}_pagina_{i+1}.jpg"
            ruta_imagen = os.path.join(carpeta_salida, nombre_imagen)
            pix.save(ruta_imagen)

        print(f"🖼️ Convertido: {archivo} ({len(doc)} página/s)")
        doc.close()