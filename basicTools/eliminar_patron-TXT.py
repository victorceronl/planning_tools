import re

def limpiar_texto(archivo_entrada, archivo_salida):
    # Leer contenido
    with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
        texto = f.read()

    # Expresión regular para eliminar las repeticiones del patrón
    # Detecta frases como:
    # "Duhi_9781400069286_2p_all_r1.j.indd   i 10/17/11   12:01 PM"
    patron = r"(Duhi_9781400069286_2p_all_r1\.j\.indd\s+i\s+\d{1,2}/\d{1,2}/\d{2}\s+\d{1,2}:\d{2}\s+[AP]M\s*)+"

    texto_limpio = re.sub(patron, '', texto)

    # Guardar resultado
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(texto_limpio)

    print(f"✅ Limpieza completada. Archivo guardado como: {archivo_salida}")


# Ejemplo de uso
if __name__ == "__main__":
    limpiar_texto("entrada.txt", "salida_limpia.txt")
