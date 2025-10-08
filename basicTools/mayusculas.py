# Script: convertir_mayusculas_usuario.py
# Convierte a mayúsculas el texto ingresado por el usuario

def convertir_a_mayusculas():
    texto = input("Escribe el texto que deseas convertir a MAYÚSCULAS:\n> ")
    texto_mayus = texto.upper()
    print("\nTexto en mayúsculas:")
    print(texto_mayus)


if __name__ == "__main__":
    convertir_a_mayusculas()
