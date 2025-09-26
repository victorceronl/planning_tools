def eliminar_caracteres():
    # Pedimos los caracteres a eliminar
    caracteres = input("Ingresa los caracteres que quieres eliminar (ejemplo: 'aeiou'): ")
    
    # Pedimos el texto completo
    texto = input("Ingresa el texto completo: ")
    
    # Recorremos todos los caracteres a eliminar
    texto_filtrado = "".join([c for c in texto if c not in caracteres])
    
    # Mostramos el resultado
    print("\nTexto sin los caracteres especificados:")
    print(texto_filtrado)


# Ejecutamos la función
if __name__ == "__main__":
    eliminar_caracteres()