# Script para convertir texto a mayúsculas

def convertir_a_mayusculas(texto: str) -> str:
    """
    Convierte el texto ingresado a mayúsculas.
    :param texto: Texto en minúsculas o mixto
    :return: Texto en mayúsculas
    """
    return texto.upper()


if __name__ == "__main__":
    # Solicita texto al usuario
    texto = input("Escribe el texto que deseas convertir a mayúsculas: ")
    resultado = convertir_a_mayusculas(texto)
    print("Texto en mayúsculas:", resultado)
