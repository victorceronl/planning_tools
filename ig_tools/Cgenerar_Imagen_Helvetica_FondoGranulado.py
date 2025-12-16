from PIL import Image, ImageDraw, ImageFont
import os
import random

def crear_imagen(
    texto,
    fondo_rgb=(0, 0, 0),
    tamano_fuente=80,
    nombre_archivo="salida.jpg",
    granulado_intensidad=30,
    interlineado=20
):
    # Resolución
    ancho, alto = 3024, 4032
    img = Image.new("RGB", (ancho, alto), color=fondo_rgb)

    # Granulado
    for x in range(ancho):
        for y in range(alto):
            ruido = random.randint(-granulado_intensidad, granulado_intensidad)
            r = max(0, min(255, fondo_rgb[0] + ruido))
            g = max(0, min(255, fondo_rgb[1] + ruido))
            b = max(0, min(255, fondo_rgb[2] + ruido))
            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    # Fuentes
    fuentes_posibles = [
        "helvetica.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]

    fuente = None
    for f in fuentes_posibles:
        if os.path.exists(f):
            try:
                fuente = ImageFont.truetype(f, tamano_fuente)
                break
            except:
                pass

    if fuente is None:
        fuente = ImageFont.load_default()

    # Separar líneas
    lineas = texto.split("\n")

    # Altura base de línea (para líneas vacías)
    bbox_ref = draw.textbbox((0, 0), "Ag", font=fuente)
    altura_linea = bbox_ref[3] - bbox_ref[1]

    # Calcular ancho máximo del bloque
    ancho_max_texto = 0
    for linea in lineas:
        if linea.strip():
            bbox = draw.textbbox((0, 0), linea, font=fuente)
            ancho_max_texto = max(ancho_max_texto, bbox[2] - bbox[0])

    # Calcular altura total del bloque
    total_alto = 0
    for linea in lineas:
        if linea.strip() == "":
            total_alto += altura_linea
        else:
            bbox = draw.textbbox((0, 0), linea, font=fuente)
            total_alto += (bbox[3] - bbox[1])
        total_alto += interlineado

    total_alto -= interlineado

    # Posiciones iniciales (bloque centrado)
    x_inicial = (ancho - ancho_max_texto) // 2
    y = (alto - total_alto) // 2

    # Dibujar texto
    for linea in lineas:
        if linea.strip() == "":
            y += altura_linea + interlineado
        else:
            draw.text(
                (x_inicial, y),
                linea,
                font=fuente,
                fill=(255, 255, 255)
            )
            bbox = draw.textbbox((0, 0), linea, font=fuente)
            y += (bbox[3] - bbox[1]) + interlineado

    # Guardar imagen
    img.save(nombre_archivo, "JPEG")
    print(f"Imagen guardada como {nombre_archivo}")

# Ejemplo de uso
texto = "Las personas que trabajan en\nsi mismas no te necesitan.\n\n\nTe eligen."
crear_imagen(
    texto,
    fondo_rgb=(20, 20, 20),
    tamano_fuente=150,
    nombre_archivo="frase_granulado.jpg"
)
