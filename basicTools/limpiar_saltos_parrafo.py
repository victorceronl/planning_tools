def limpiar_saltos_parrafo(entrada, salida):
    try:
        with open(entrada, "r", encoding="utf-8") as f:
            texto = f.read()
        
        # Reemplazar dobles saltos de línea por un espacio
        texto_limpio = texto.replace("\n\n", " ")
        # Opcional: eliminar también saltos de línea simples
        texto_limpio = texto_limpio.replace("\n", " ")

        # Guardar el texto procesado en otro archivo
        with open(salida, "w", encoding="utf-8") as f:
            f.write(texto_limpio)

        print(f"✅ Archivo limpio guardado en: {salida}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Ejemplo de uso
limpiar_saltos_parrafo("entrada.txt", "salida.txt")
