import pandas as pd
import random

def fila_aleatoria_excel(nombre_archivo, hoja=0):
    """
    Lee un Excel y devuelve una fila aleatoria en formato texto.
    :param nombre_archivo: Ruta del archivo Excel (.xlsx)
    :param hoja: Índice o nombre de la hoja (por defecto la primera)
    :return: Texto con los datos de la fila
    """
    # Cargar Excel
    df = pd.read_excel(nombre_archivo, sheet_name=hoja)

    # Elegir una fila aleatoria
    indice = random.randint(0, len(df) - 1)
    fila = df.iloc[indice]

    # Convertir a texto
    texto = " | ".join([f"{col}: {fila[col]}" for col in df.columns])
    return texto

if __name__ == "__main__":
    archivo = "ejemplo.xlsx"  # Cambia esto por tu archivo
    resultado = fila_aleatoria_excel(archivo)
    print("Fila aleatoria seleccionada:\n")
    print(resultado)
