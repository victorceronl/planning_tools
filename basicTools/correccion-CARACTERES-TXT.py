import re
import unicodedata

def corregir_texto(archivo_entrada="salida.txt", archivo_salida="salida_corregido.txt"):
    # Leer contenido del archivo de entrada
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    # --- LIMPIEZA INICIAL ---
    texto = re.sub(r"\t+", " ", texto)           # Eliminar tabs
    texto = re.sub(r" {2,}", " ", texto)         # Espacios múltiples
    texto = re.sub(r"\n{3,}", "\n\n", texto)     # Saltos de línea excesivos
    texto = re.sub(r"(\w)-\s+(\w)", r"\1\2", texto)  # Corregir palabras partidas
    texto = re.sub(r"Page\s*\d+", "", texto, flags=re.I)  # Quitar numeración de páginas

    # --- CORRECCIÓN DE CARACTERES MAL FORMADOS ---
    reemplazos = {
        "a ́": "á", "e ́": "é", "i ́": "í", "o ́": "ó", "u ́": "ú",
        "A ́": "Á", "E ́": "É", "I ́": "Í", "O ́": "Ó", "U ́": "Ú",
        "n ̃": "ñ", "N ̃": "Ñ",
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "´": "'", "–": "-", "—": "-",
        "o ̈": "ö", "u ̈": "ü",  # para textos con diéresis
    }

    for k, v in reemplazos.items():
        texto = texto.replace(k, v)

    # Normalizar combinaciones Unicode (acentos separados)
    texto = unicodedata.normalize("NFC", texto)

    # --- LIMPIEZA FINAL ---
    texto = texto.strip()

    # Guardar archivo corregido
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"✅ Archivo corregido guardado en: {archivo_salida}")


# Ejemplo de uso
if __name__ == "__main__":
    corregir_texto("salida.txt", "salida_corregido.txt")
