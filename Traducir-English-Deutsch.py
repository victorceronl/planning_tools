from googletrans import Translator

#importar libreria
#pip install googletrans==4.0.0-rc1

def traducir_archivo(ruta_entrada, ruta_salida, destino="en"):
    traductor = Translator()

    # Leer el archivo de entrada
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    # Traducir el contenido
    resultado = traductor.translate(texto, dest=destino)

    # Guardar en archivo de salida
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(resultado.text)

    print(f"Traducción completada ✅ Archivo guardado en: {ruta_salida}")


# Ejemplo de uso:
# archivo.txt contiene texto en alemán
traducir_archivo("alemán.txt", "ingles.txt", "en")
