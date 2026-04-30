import pandas as pd
import re

# === CONFIG ===
archivo = "datos-.xlsx"

# Leer archivo
df = pd.read_excel(archivo)

# === FUNCIONES ===

def limpiar_nombre(texto):
    texto = str(texto).upper().strip()
    texto = re.sub(r'(\d+\-\s*)+', '', texto)
    return texto.strip()

# 🔥 CAMBIO AQUÍ: separador " - "
def extraer_codigos(texto):
    texto = str(texto)
    codigos = re.findall(r'(\d+)-', texto)
    return " - ".join(codigos)

# === NORMALIZACION ===
df["BASE_NOMBRE"] = (
    df["NOMBRE"]
    .astype(str)
    .str.replace(".stp", "", regex=False)
    .str.strip()
    .str.upper()
)

df["CORRECTO_LIMPIO"] = df["CORRECTO"].apply(limpiar_nombre)

# Nueva columna con formato solicitado
df["CODIGOS"] = df["CORRECTO"].apply(extraer_codigos)

# === DICCIONARIO ===
dim_dict = {}

for _, row in df.iterrows():
    base = row["BASE_NOMBRE"]
    if pd.notna(row["LARGO"]):
        dim_dict[base] = (
            row["NOMBRE"],
            row["LARGO"],
            row["ANCHO"],
            row["ESPESOR"]
        )

# Columnas nuevas
df["ARCHIVO_MATCH"] = ""
df["STATUS"] = ""

# === PROCESO PRINCIPAL ===
for i, row in df.iterrows():
    clave = row["CORRECTO_LIMPIO"]

    if clave in dim_dict:
        archivo_match, largo, ancho, espesor = dim_dict[clave]

        df.at[i, "NOMBRE"] = archivo_match
        df.at[i, "LARGO"] = largo
        df.at[i, "ANCHO"] = ancho
        df.at[i, "ESPESOR"] = espesor

        df.at[i, "ARCHIVO_MATCH"] = archivo_match
        df.at[i, "STATUS"] = "OK"
    else:
        df.at[i, "STATUS"] = "NO MATCH"

# Limpiar auxiliares
df.drop(columns=["BASE_NOMBRE", "CORRECTO_LIMPIO"], inplace=True)

# Guardar
output = "resultado_con_codigos2.xlsx"
df.to_excel(output, index=False)

print(f"Archivo generado: {output}")