import PyPDF2

def pdf_a_txt(pdf_path, txt_path):
    try:
        # Abrir el archivo PDF en modo lectura binaria
        with open(pdf_path, 'rb') as pdf_file:
            lector = PyPDF2.PdfReader(pdf_file)
            
            texto = ""
            # Recorrer todas las páginas
            for i, pagina in enumerate(lector.pages):
                texto += pagina.extract_text() or ""  # Extraer texto de cada página
                texto += "\n" + "="*40 + f" [Página {i+1}] " + "="*40 + "\n\n"
            
        # Guardar el texto en un archivo TXT
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(texto)
        
        print(f"✅ Texto extraído correctamente en: {txt_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Ejemplo de uso
pdf_a_txt("ejemplo.pdf", "salida.txt")
