import pandas as pd
import random

def celda_aleatoria_excel(nombre_archivo, hoja=0):
    """
    Lee un Excel y devuelve una celda aleatoria.
    :param nombre_archivo: Ruta del archivo Excel (.xlsx)
    :param hoja: Índice o nombre de la hoja (por defecto la primera)
    :return: Texto con el nombre de la columna, número de fila y valor de la celda
    """
    # Cargar Excel
    df = pd.read_excel(nombre_archivo, sheet_name=hoja)

    # Elegir fila y columna aleatoria
    fila_idx = random.randint(0, len(df) - 1)
    col_idx = random.randint(0, len(df.columns) - 1)

    # Obtener valor
    columna = df.columns[col_idx]
    valor = df.iloc[fila_idx, col_idx]

    return f"Fila {fila_idx+1}, Columna '{columna}': {valor}"

if __name__ == "__main__":
    archivo = "ejemplo.xlsx"  # Cambia esto por tu archivo
    resultado = celda_aleatoria_excel(archivo)
    print("Celda aleatoria seleccionada:\n")
    print(resultado)
