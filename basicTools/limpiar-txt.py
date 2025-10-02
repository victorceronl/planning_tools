import re

def limpiar_txt(archivo_entrada, archivo_salida):
    # Leer contenido del archivo original
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Eliminar tabs (\t)
    clean_text = content.replace("\t", " ")

    # 2. Reemplazar múltiples espacios consecutivos por uno
    clean_text = re.sub(r" +", " ", clean_text)

    # 3. Reducir múltiples saltos de línea (más de 2) a solo 2
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

    # 4. Dividir en líneas
    lines = clean_text.splitlines()
    merged_lines = []

    for i, line in enumerate(lines):
        if not line.strip():
            continue  # ignorar líneas vacías

        if i < len(lines) - 1:
            next_line = lines[i+1].strip()

            # Detectar si la línea es un título o capítulo
            if (line.strip().startswith("CHAPTER") or 
                next_line.startswith("CHAPTER") or 
                next_line.isupper() or 
                line.strip().endswith((".", "?", "!", ":"))):
                merged_lines.append(line.strip())
            else:
                # Unir con la siguiente línea
                merged_lines.append(line.strip() + " " + next_line)
                lines[i+1] = ""  # evitar duplicado
        else:
            merged_lines.append(line.strip())

    # Reconstruir el texto limpio
    final_text = "\n".join([l for l in merged_lines if l.strip() != ""])

    # Guardar en archivo nuevo
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ Archivo procesado y guardado en: {archivo_salida}")


# Ejemplo de uso:
# limpiar_txt("salida.txt", "salida_legible.txt")
