def unir_archivos(archivo1, archivo2, archivo_salida):
    try:
        with open(archivo1, 'r', encoding='utf-8') as f1, open(archivo2, 'r', encoding='utf-8') as f2:
            contenido1 = f1.read()
            contenido2 = f2.read()

        with open(archivo_salida, 'w', encoding='utf-8') as salida:
            salida.write(contenido1 + "\n" + contenido2)

        print(f"✅ Archivos unidos correctamente en '{archivo_salida}'")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")

# Ejemplo de uso
unir_archivos("archivo1.txt", "archivo2.txt", "resultado.txt")
