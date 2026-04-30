import pandas as pd
import re

# =============================
# DICCIONARIOS BASE
# =============================

component_map = {
    "FI": "FINGER",
    "NB": "REST",
    "PL": "PLATE",
    "RL": "ROUGH LOCATOR",
    "LB": "L BLOCK",
    "SA": "STL ANGLE",
    "BC": "BLOCK",
    "WC": "WELDMENT",
    "IT": "INSULATING",
    "SS": "SENSOR SUPPORT"
}

material_map = {
    "41": "SAE 4140",
    "60": "SAE 1060",
    "86": "SAE 8620",
    "HR": "HRS",
    "CS": "CRS",
    "S4": "STAINLESS STEEL AISI 304",
    "75": "ALUMINUM 7075-T6",
    "BZ": "BRONZE SAE 660",
    "BR": "BRASS",
    "NY": "NYLAMID",
    "N9": "NYLAMID 901"
}

finish_map = {
    "P": "BLACK OXIDE",
    "M": "PAINT MOVIL",
    "F": "PAINT FIXED",
    "S": "SIN ACABADO",
    "Y": "POKA YOKE (ROJO)",
    "B": "SENSOR SUPPORT (AZUL)",
    "C": "CARBURIZADO",
    "H": "FLAME HARDEN",
    "R": "HARDNESS + BLACK OXIDE"
}

# Casos especiales (muy importantes en tu dataset)
special_cases = {
    "PLHR": ("PLATE", "HRS"),
    "SAA": ("STL ANGLE", "A36"),
    "SSA": ("STL ANGLE", "A36"),
    "LBA": ("L BLOCK", "A36"),
    "LBH": ("L BLOCK", "HRS"),
    "BCH": ("BLOCK", "HRS"),
    "WCW": ("WELDMENT", "HRS"),
    "ITM": ("INSULATING", "MICARTA")
}

# =============================
# FUNCIÓN PRINCIPAL
# =============================

def parse_code(code):
    componente = "DESCONOCIDO"
    material = "DESCONOCIDO"
    acabado = "DESCONOCIDO"

    # detectar acabado (última letra útil antes de X)
    match_finish = re.search(r'([A-Z])X$', code)
    if match_finish:
        acabado = finish_map.get(match_finish.group(1), "DESCONOCIDO")

    # detectar especiales primero
    for key in special_cases:
        if code.startswith(key):
            componente, material = special_cases[key]
            return componente, material, acabado

    # patrón general: letras + números
    match = re.match(r'([A-Z]+)(\d+)', code)
    if match:
        comp_code = match.group(1)[:2]
        mat_code = match.group(2)

        componente = component_map.get(comp_code, comp_code)
        material = material_map.get(mat_code, mat_code)

    return componente, material, acabado


# =============================
# PROCESAMIENTO EXCEL
# =============================

archivo = "input.xlsx"  # <-- tu archivo
df = pd.read_excel(archivo)

# asumir que la columna A tiene el nombre
df["CODIGO"] = df.iloc[:, 0].apply(lambda x: str(x).split("_")[-1])

resultados = df["CODIGO"].apply(parse_code)

df["COMPONENTE"] = resultados.apply(lambda x: x[0])
df["MATERIAL"] = resultados.apply(lambda x: x[1])
df["ACABADO"] = resultados.apply(lambda x: x[2])

# guardar resultado
df.to_excel("output_clasificado.xlsx", index=False)

print("Proceso terminado.")