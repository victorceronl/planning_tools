def eliminar_tabs(archivo_entrada, archivo_salida):
    try:
        with open(archivo_entrada, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Reemplazar tabs por nada (o puedes poner un espacio si prefieres)
        contenido_sin_tabs = contenido.replace("\t", "")

        with open(archivo_salida, "w", encoding="utf-8") as f:
            f.write(contenido_sin_tabs)

        print(f"Se eliminaron los tabs y se guardó el resultado en '{archivo_salida}'")

    except FileNotFoundError:
        print("❌ No se encontró el archivo de entrada.")

# Ejemplo de uso:
eliminar_tabs("entrada.txt", "salida.txt")
