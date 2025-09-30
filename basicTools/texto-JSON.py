import json

def texto_a_json(ruta_txt, ruta_json):
    datos = {}
    with open(ruta_txt, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if ":" in linea:  # si hay clave:valor
                clave, valor = linea.split(":", 1)
                datos[clave.strip()] = valor.strip()

    # Guardar en archivo JSON
    with open(ruta_json, "w", encoding="utf-8") as json_file:
        json.dump(datos, json_file, indent=4, ensure_ascii=False)

    print(f"Archivo JSON creado en: {ruta_json}")

# Ejemplo de uso:
# texto.txt contiene:
# nombre: Victor
# edad: 30
# ciudad: México

texto_a_json("texto.txt", "resultado.json")