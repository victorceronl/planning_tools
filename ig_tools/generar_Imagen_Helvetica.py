from PIL import Image, ImageDraw, ImageFont
import os

def crear_imagen(texto, fondo_rgb=(0, 0, 0), tamano_fuente=80, nombre_archivo="salida.jpg"):
    # Resolución 3024x4032 px
    ancho, alto = 3024, 4032
    img = Image.new("RGB", (ancho, alto), color=fondo_rgb)

    draw = ImageDraw.Draw(img)

    # Intentar cargar Helvetica
    fuentes_posibles = [
        "helvetica.ttf",  # Ruta actual
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "C:\\Windows\\Fonts\\arial.ttf"  # Windows como fallback
    ]

    fuente = None
    for f in fuentes_posibles:
        if os.path.exists(f):
            try:
                fuente = ImageFont.truetype(f, tamano_fuente)
                break
            except:
                continue

    if fuente is None:
        fuente = ImageFont.load_default()
        print("No se encontró Helvetica. Se usará la fuente por defecto.")

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
        draw.text((x, y), linea, font=fuente, fill=(255, 255, 255))
        y += (bbox[3] - bbox[1]) + 10

    img.save(nombre_archivo, "JPEG")
    print(f"Imagen guardada como {nombre_archivo}")

# Ejemplo de uso
texto = "Lo que es para ti, ni aunque te quites.\nLo que no, ni aunque te pongas."
crear_imagen(texto, fondo_rgb=(0, 0, 0), tamano_fuente=150, nombre_archivo="frase.jpg")
