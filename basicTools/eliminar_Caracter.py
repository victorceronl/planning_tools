def eliminar_caracter():
    # Pedimos el caracter a eliminar
    caracter = input("Ingresa el caracter que quieres eliminar: ")
    
    # Validamos que solo sea un caracter
    if len(caracter) != 1:
        print("Debes ingresar exactamente un solo caracter.")
        return
    
    # Pedimos el texto completo
    texto = input("Ingresa el texto completo: ")
    
    # Eliminamos todas las apariciones del caracter
    texto_filtrado = texto.replace(caracter, "")
    
    # Mostramos el resultado
    print("\nTexto sin el caracter especificado:")
    print(texto_filtrado)


# Ejecutamos la función
if __name__ == "__main__":
    eliminar_caracter()
