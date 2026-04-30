import pandas as pd

# cargar archivo
df = pd.read_excel("tabla.xlsx")

# crear lista nueva para columna C ordenada
columnaC_ordenada = []

for _, fila in df.iterrows():
    bnumero = fila["B"].replace(".", "").lower()   # ejemplo B70355336
    encontrado = None

    for texto in df["C"].dropna():
        if bnumero in texto.lower():
            encontrado = texto
            break

    columnaC_ordenada.append(encontrado)

# reemplazar columna C
df["C"] = columnaC_ordenada

# guardar resultado
df.to_excel("tabla_ordenada.xlsx", index=False)

print("Archivo generado: tabla_ordenada.xlsx")