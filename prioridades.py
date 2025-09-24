# Script: prioridades.py

def definir_prioridades():
    prioridades = []

    print("=== Definición de Prioridades ===")
    print("Ingresa tus prioridades y su nivel de importancia (1 = más alta, 5 = más baja).")
    print("Cuando termines, escribe 'fin' para dejar de ingresar prioridades.\n")

    while True:
        tarea = input("📌 Ingresa una prioridad (o escribe 'fin' para terminar): ")
        if tarea.lower() == "fin":
            break
        try:
            nivel = int(input(f"Nivel de importancia para '{tarea}' (1-5): "))
            if nivel < 1 or nivel > 5:
                print("⚠️ El nivel debe estar entre 1 y 5.")
                continue
            prioridades.append((nivel, tarea))
        except ValueError:
            print("⚠️ Debes ingresar un número entre 1 y 5.")

    # Ordenamos por nivel (más baja prioridad = número más alto)
    prioridades.sort(key=lambda x: x[0])

    # Guardamos en archivo TXT
    with open("prioridades.txt", "w", encoding="utf-8") as f:
        f.write("=== Lista de Prioridades ===\n\n")
        for i, (nivel, tarea) in enumerate(prioridades, start=1):
            f.write(f"{i}. {tarea} (Importancia: {nivel})\n")

    print("\n✅ Tus prioridades fueron guardadas en 'prioridades.txt'.")

if __name__ == "__main__":
    definir_prioridades()
