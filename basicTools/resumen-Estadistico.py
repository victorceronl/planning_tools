import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict

nltk.download("punkt")
nltk.download("stopwords")

def resumen_basico(ruta_txt, num_frases=5):
    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    # Tokenizar oraciones y palabras
    oraciones = sent_tokenize(texto, language="spanish")
    palabras = word_tokenize(texto.lower(), language="spanish")

    # Filtrar stopwords
    stop_words = set(stopwords.words("spanish"))
    palabras_importantes = [p for p in palabras if p.isalnum() and p not in stop_words]

    # Frecuencia de palabras
    frec = defaultdict(int)
    for palabra in palabras_importantes:
        frec[palabra] += 1

    # Puntuar oraciones según las palabras que contienen
    puntuacion = defaultdict(int)
    for oracion in oraciones:
        for palabra in word_tokenize(oracion.lower(), language="spanish"):
            if palabra in frec:
                puntuacion[oracion] += frec[palabra]

    # Ordenar y elegir las mejores
    oraciones_clave = sorted(puntuacion, key=puntuacion.get, reverse=True)[:num_frases]

    return "\n".join(oraciones_clave)

# Ejemplo de uso
print(resumen_basico("entrada.txt"))
