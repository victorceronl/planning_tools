def eliminar_caracteres_archivo():
    # Pedimos los caracteres a eliminar
    caracteres = input("Ingresa los caracteres que quieres eliminar (ejemplo: 'aeiou'): ")
    
    # Pedimos la ruta del archivo
    ruta = input("Ingresa la ruta del archivo .txt: ")
    
    try:
        # Leer contenido del archivo
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()
        
        # Filtrar el texto
        texto_filtrado = "".join([c for c in texto if c not in caracteres])
        
        # Guardar el resultado en un nuevo archivo
        salida = "resultado.txt"
        with open(salida, "w", encoding="utf-8") as f:
            f.write(texto_filtrado)
        
        print(f"\n✅ Proceso terminado. El texto filtrado se guardó en '{salida}'.")
    
    except FileNotFoundError:
        print("❌ El archivo no existe. Verifica la ruta.")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")


# Ejecutamos la función
if __name__ == "__main__":
    eliminar_caracteres_archivo()
