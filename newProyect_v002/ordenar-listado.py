import re

archivo_entrada = "ordenarlista-.txt"
archivo_salida = "lista_ordenada.txt"

datos = []

with open(archivo_entrada, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()

        # eliminar líneas con DBR
        if "DBR" in linea:
            continue

        # buscar el primer número después del "-"
        match = re.search(r"-\s*(\d+)_", linea)
        if match:
            numero = int(match.group(1))
            datos.append((numero, linea))

# ordenar por el número extraído
datos.sort(key=lambda x: x[0])

# guardar resultado
with open(archivo_salida, "w", encoding="utf-8") as f:
    for _, linea in datos:
        f.write(linea + "\n")

print("Archivo ordenado guardado como:", archivo_salida)