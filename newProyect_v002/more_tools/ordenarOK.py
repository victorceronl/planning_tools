import pandas as pd

# === CONFIG ===
archivo = "datos-.xlsx"

# Leer archivo
df = pd.read_excel(archivo)

# Normalizar nombres (sin .stp y en mayúsculas para evitar errores)
df["BASE_NOMBRE"] = (
    df["NOMBRE"]
    .astype(str)
    .str.replace(".stp", "", regex=False)
    .str.strip()
    .str.upper()
)

df["CORRECTO"] = df["CORRECTO"].astype(str).str.strip().str.upper()

# Crear diccionario: nombre base -> (archivo original, dimensiones)
dim_dict = {}

for _, row in df.iterrows():
    base = row["BASE_NOMBRE"]
    if pd.notna(row["LARGO"]):
        dim_dict[base] = (
            row["NOMBRE"],  # nombre completo
            row["LARGO"],
            row["ANCHO"],
            row["ESPESOR"]
        )

# Columnas nuevas
df["ARCHIVO_MATCH"] = ""
df["STATUS"] = ""

# === PROCESO PRINCIPAL (CORREGIDO) ===
for i, row in df.iterrows():
    clave = row["CORRECTO"]

    if clave in dim_dict:
        archivo_match, largo, ancho, espesor = dim_dict[clave]

        # 🔥 FORZAR actualización completa
        df.at[i, "NOMBRE"] = archivo_match
        df.at[i, "LARGO"] = largo
        df.at[i, "ANCHO"] = ancho
        df.at[i, "ESPESOR"] = espesor

        df.at[i, "ARCHIVO_MATCH"] = archivo_match
        df.at[i, "STATUS"] = "OK"
    else:
        df.at[i, "STATUS"] = "NO MATCH"

# Eliminar columna auxiliar
df.drop(columns=["BASE_NOMBRE"], inplace=True)

# Guardar resultado
output = "resultado_acabadoOKvalidado.xlsx"
df.to_excel(output, index=False)

print(f"Archivo generado: {output}")