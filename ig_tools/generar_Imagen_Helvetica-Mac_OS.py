from PIL import Image, ImageDraw, ImageFont

def crear_imagen(texto, fondo_rgb=(0, 0, 0), tamano_fuente=80, nombre_archivo="salida.jpg"):
    # Resolución 3024x4032 px
    ancho, alto = 3024, 4032
    img = Image.new("RGB", (ancho, alto), color=fondo_rgb)

    draw = ImageDraw.Draw(img)

    # Fuente Helvetica en macOS
    try:
        fuente = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", tamano_fuente)
    except:
        fuente = ImageFont.load_default()
        print("No se pudo cargar Helvetica. Se usará la fuente por defecto.")

    # Separar líneas
    lineas = texto.split("\n")

    # Calcular posición inicial para centrar verticalmente
    total_alto = sum([draw.textbbox((0,0), linea, font=fuente)[3] for linea in lineas]) + (len(lineas)-1)*10
    y = (alto - total_alto) // 2

    # Dibujar cada línea centrada
    for linea in lineas:
        bbox = draw.textbbox((0,0), linea, font=fuente)
        ancho_texto = bbox[2] - bbox[0]
        x = (ancho - ancho_texto) // 2
        draw.text((x, y), linea, font=fuente, fill=(255, 255, 255))  # Texto en blanco
        y += (bbox[3] - bbox[1]) + 10

    # Guardar imagen
    img.save(nombre_archivo, "JPEG")
    print(f"Imagen guardada como {nombre_archivo}")

# Ejemplo de uso
texto = "Lo que es para ti, ni aunque te quites.\nLo que no, ni aunque te pongas."
crear_imagen(texto, fondo_rgb=(0, 0, 0), tamano_fuente=150, nombre_archivo="frase.jpg")
