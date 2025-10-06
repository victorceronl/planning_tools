import re

def limpiar_txt(archivo_entrada, archivo_salida, debug=False):
    # Leer contenido del archivo original
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Eliminar tabs
    clean_text = content.replace("\t", " ")

    # 2. Reemplazar múltiples espacios consecutivos
    clean_text = re.sub(r" +", " ", clean_text)

    # 3. Reducir múltiples saltos de línea
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

    # 4. Dividir en líneas
    lines = clean_text.splitlines()
    merged_lines = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue  # ignorar líneas vacías

        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()

            # Detectar si unir o no
            if (line.endswith((".", "?", "!", ":"))
                or line.startswith("CHAPTER")
                or next_line.startswith("CHAPTER")
                or next_line.isupper()):
                merged_lines.append(line)
            else:
                merged_lines.append(line + " " + next_line)
                lines[i + 1] = ""  # evita repetir línea
        else:
            merged_lines.append(line)

        if debug:
            print(f"[Línea {i}] {line[:60]}...")

    # Reconstruir texto limpio
    final_text = "\n".join([l for l in merged_lines if l.strip() != ""])

    # Guardar resultado
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ Archivo procesado y guardado en: {archivo_salida}")


# Ejemplo de uso:
if __name__ == "__main__":
    limpiar_txt("salida.txt", "salida_legible.txt", debug=True)
