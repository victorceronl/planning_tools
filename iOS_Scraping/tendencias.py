import requests
import textwrap

# --- CONFIGURACIÓN ---
API_KEY = "TU_API_KEY_DE_NEWSAPI0f7bdb268ff746ed97295670f5c23a98"  # Consigue una gratis en newsapi.org
URL = f"https://newsapi.org/v2/top-headlines?category=technology&language=es&apiKey={API_KEY}"

def obtener_tendencias():
    resp = requests.get(URL)
    data = resp.json()

    if "articles" not in data:
        return "No se pudieron obtener las tendencias."

    articulos = data["articles"][:5]  # Tomamos 5 noticias principales
    resumen = "📌 Tendencias tecnológicas:\n\n"
    
    for i, art in enumerate(articulos, start=1):
        titulo = art.get("title", "Sin título")
        fuente = art["source"]["name"] if art.get("source") else "Desconocido"
        resumen += f"{i}. {titulo} ({fuente})\n"

    return textwrap.fill(resumen, width=80)

if __name__ == "__main__":
    print(obtener_tendencias())
