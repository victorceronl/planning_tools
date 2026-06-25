from flask import Flask, request, jsonify
from openpyxl import load_workbook
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = r"C:\Users\Diseño 1\Documents\7.-Avance de producción"
EXCEL_PATH = os.path.join(BASE_DIR, "xls", "TIEMPO-PRODUCCION.xlsx")

@app.route("/registro", methods=["POST"])
def registro():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    tm = data.get("tm", "")
    tipo = data.get("tipo", "")
    maquina = data.get("maquina", "")
    operador = data.get("operador", "")

    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y")
    hora = now.strftime("%I:%M %p")

    wb = load_workbook(EXCEL_PATH)
    ws = wb.active  # o ws = wb["NOMBRE_HOJA"] si quieres fijarlo

    ws.append([
        tm,
        fecha,
        hora,
        tipo,
        maquina,
        operador
    ])

    wb.save(EXCEL_PATH)

    return jsonify({
        "ok": True,
        "tm": tm
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)