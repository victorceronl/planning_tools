from PyPDF2 import PdfReader
import re
import unicodedata

# Rutas
entrada_pdf = "/mnt/data/ejemplo.pdf"
salida_txt = "/mnt/data/ejemplo_legible_corregido.txt"

# Leer PDF
reader = PdfReader(entrada_pdf)
texto = ""
for page in reader.pages:
    texto += page.extract_text() + "\n"

# --- LIMPIEZA INICIAL ---
# Quitar espacios múltiples, tabs y marcas de página
texto = re.sub(r"\t+", " ", texto)
texto = re.sub(r" {2,}", " ", texto)
texto = re.sub(r"Page\s*\d+", "", texto, flags=re.I)
texto = re.sub(r"\n{3,}", "\n\n", texto)

# Corregir palabras partidas con guiones
texto = re.sub(r"(\w)-\s+(\w)", r"\1\2", texto)

# --- CORRECCIÓN DE CARACTERES MAL FORMADOS ---
# Reemplazos comunes de PDF
reemplazos = {
    "a ́": "á", "e ́": "é", "i ́": "í", "o ́": "ó", "u ́": "ú",
    "A ́": "Á", "E ́": "É", "I ́": "Í", "O ́": "Ó", "U ́": "Ú",
    "n ̃": "ñ", "N ̃": "Ñ",
    "’": "'", "“": '"', "”": '"', "‘": "'",
    "´": "'", "–": "-", "—": "-",
}

for k, v in reemplazos.items():
    texto = texto.replace(k, v)

# Normalizar combinaciones Unicode (NFD → NFC)
texto = unicodedata.normalize("NFC", texto)

# --- LIMPIEZA FINAL ---
texto = texto.strip()

# Guardar archivo corregido
with open(salida_txt, "w", encoding="utf-8") as f:
    f.write(texto)

print("✅ Texto corregido y limpio guardado en:", salida_txt)
