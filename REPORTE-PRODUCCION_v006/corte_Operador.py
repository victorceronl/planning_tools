import pandas as pd
import re
from datetime import datetime
from collections import defaultdict

# ==========================================
# CONFIGURACION
# ==========================================

ARCHIVO_CORTE = "corte.xlsx"
ARCHIVO_PROYECTOS = "proyectos.xlsx"
HTML_SALIDA = "corte-Operador.html"

# ==========================================
# FUNCIONES
# ==========================================

def extraer_proyecto_posiciones(tm):
    """
    Convierte:

    TM2604022-109- 153- 323- 367-
    ->
    proyecto = TM2604022
    posiciones = ['109','153','323','367']

    TM2605008_001
    ->
    proyecto = TM2605008
    posiciones = ['001']
    """

    tm = str(tm).strip()

    if "_" in tm:
        partes = tm.split("_", 1)
        return partes[0].strip(), [partes[1].strip()]

    proyecto_match = re.match(r"(TM\d+)", tm, re.IGNORECASE)

    if not proyecto_match:
        return tm, []

    proyecto = proyecto_match.group(1)

    resto = tm[len(proyecto):]

    posiciones = re.findall(r"\d+", resto)

    return proyecto, posiciones


def normalizar_tm_proyecto(tm):
    proyecto, posiciones = extraer_proyecto_posiciones(tm)

    return {
        "proyecto": proyecto,
        "posiciones": posiciones
    }






def segundos_a_hm(segundos):

    segundos = int(segundos)

    h = segundos // 3600
    m = round((segundos % 3600) / 60)

    if m == 60:
        h += 1
        m = 0

    return f"{h:02}:{m:02}"


# ==========================================
# CARGA EXCEL
# ==========================================

print("Leyendo archivos...")

df_corte = pd.read_excel(ARCHIVO_CORTE)
df_proy = pd.read_excel(ARCHIVO_PROYECTOS)

# ==========================================
# PREPARAR PROYECTOS
# ==========================================

proyectos = {}

for _, row in df_proy.iterrows():

    tm = str(row["TM"]).strip()

    info = normalizar_tm_proyecto(tm)

    cantidad = (
        pd.to_numeric(row["Most (Qty.)"], errors="coerce")
        + pd.to_numeric(row["Opust (Qty.)"], errors="coerce")
    )

    cantidad = 0 if pd.isna(cantidad) else int(cantidad)

    material = str(row["MATERIAL"]).strip()
    acabado = str(row["ACABADO"]).strip()

    for pos in info["posiciones"]:

        clave = f"{info['proyecto']}-{pos}"

        proyectos[clave] = {
            "cantidad": cantidad,
            "material": material,
            "acabado": acabado
        }

# ==========================================
# PREPARAR CORTE
# ==========================================


df_corte["HORA"] = (
    df_corte["HORA"]
    .astype(str)
    .str.replace("a. m.", "AM", regex=False)
    .str.replace("p. m.", "PM", regex=False)
    .str.replace("a.m.", "AM", regex=False)
    .str.replace("p.m.", "PM", regex=False)
    .str.replace(" a. m.", " AM", regex=False)
    .str.replace(" p. m.", " PM", regex=False)
    .str.strip()
)

df_corte["DATETIME"] = pd.to_datetime(
    df_corte["FECHA"].astype(str) + " " + df_corte["HORA"].astype(str),
    format="%d/%m/%Y %I:%M %p",
    errors="coerce"
)

# SOLO REGISTROS DE HOY
from datetime import date
hoy = date.today()

df_corte = df_corte[
    df_corte["DATETIME"].dt.date == hoy
]



df_corte = df_corte.sort_values("DATETIME")

# ==========================================
# EMPAREJAR INICIO / FIN
# ==========================================

abiertos = defaultdict(list)

operaciones = []
incidencias = []

for _, row in df_corte.iterrows():

    tm = str(row["TM"]).strip()

    tipo = str(row["TIPO"]).strip().upper()

    fecha = pd.to_datetime(
        row["FECHA"],
        format="%d/%m/%Y"
    ).date()

    operador = str(row["OPERADOR"]).strip()
    maquina = str(row["MAQUINA"]).strip()

    dt = row["DATETIME"]

    if tipo == "INICIO":

        abiertos[tm].append({
            "inicio": dt,
            "fecha": fecha,
            "operador": operador,
            "maquina": maquina
        })

    elif tipo == "FIN":

        if abiertos[tm]:

            inicio = abiertos[tm].pop(0)

            duracion = (dt - inicio["inicio"]).total_seconds()

            proyecto, posiciones = extraer_proyecto_posiciones(tm)

            cantidad_total = 0
            material = ""
            acabado = ""

            for pos in posiciones:

                clave = f"{proyecto}-{pos}"

                if clave in proyectos:

                    cantidad_total += proyectos[clave]["cantidad"]

                    if not material:
                        material = proyectos[clave]["material"]

                    if not acabado:
                        acabado = proyectos[clave]["acabado"]

            operaciones.append({
                "fecha": fecha,
                "tm": tm,
                "proyecto": proyecto,
                "posiciones": posiciones,
                "operador": inicio["operador"],
                "maquina": inicio["maquina"],
                "inicio": inicio["inicio"],
                "fin": dt,
                "duracion": duracion,
                "cantidad": cantidad_total,
                "material": material,
                "acabado": acabado
            })

        else:

            incidencias.append(
                f"FIN sin INICIO: {tm}"
            )

for tm, registros in abiertos.items():

    for r in registros:

        incidencias.append(
            f"INICIO sin FIN: {tm}"
        )

# ==========================================
# AGRUPAR POR DIA
# ==========================================

dias = defaultdict(list)

for op in operaciones:
    dias[op["fecha"]].append(op)

# ==========================================
# HTML
# ==========================================

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Registro Corte</title>

<style>

body {{
    font-family: Arial;
    background:#f5f5f5;
    margin:20px;
}}

h1 {{
    color:#222;
}}

.card {{
    background:white;
    padding:15px;
    margin-bottom:20px;
    border-radius:8px;
    box-shadow:0 0 5px rgba(0,0,0,0.15);
}}

table {{
    border-collapse: collapse;
    width:100%;
    margin-top:10px;
}}

th {{
    background:#222;
    color:white;
    padding:8px;
}}

td {{
    border:1px solid #ddd;
    padding:6px;
}}

summary {{
    font-size:20px;
    font-weight:bold;
    cursor:pointer;
}}

.kpi {{
    display:inline-block;
    background:white;
    padding:15px;
    margin:5px;
    min-width:180px;
    border-radius:8px;
    box-shadow:0 0 4px rgba(0,0,0,.2);
}}

</style>
</head>
<body>

<img src="imagenes/foto.jpg" alt="Logo">

<h1>Registro Corte del Día</h1>
<h1>TUNKERS de Mexico</h1>

<p>Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
"""

for fecha in sorted(dias.keys(), reverse=True):

    registros = dias[fecha]

    operaciones_dia = len(registros)

    posiciones_dia = sum(
        len(r["posiciones"])
        for r in registros
    )

    piezas_dia = sum(
        r["cantidad"]
        for r in registros
    )

    tiempo_total = sum(
        r["duracion"]
        for r in registros
    )

    html += f"""
    <details open>
    <summary>{fecha.strftime('%d/%m/%Y')}</summary>

    <div class='card'>
    """

    html += f"""
    <div class='kpi'><b>Operaciones</b><br>{operaciones_dia}</div>
    <div class='kpi'><b>Posiciones</b><br>{posiciones_dia}</div>
    <div class='kpi'><b>Piezas</b><br>{piezas_dia}</div>
    <div class='kpi'><b>Tiempo Total</b><br>{segundos_a_hm(tiempo_total)}</div>
    """

    # ----------------------------------
    # Operadores
    # ----------------------------------

    resumen_operadores = defaultdict(
        lambda: {
            "operaciones":0,
            "piezas":0,
            "tiempo":0
        }
    )

    for r in registros:

        op = r["operador"]

        resumen_operadores[op]["operaciones"] += 1
        resumen_operadores[op]["piezas"] += r["cantidad"]
        resumen_operadores[op]["tiempo"] += r["duracion"]

    html += """
    <h3>Producción por Operador</h3>

    <table>
    <tr>
        <th>Operador</th>
        <th>Operaciones</th>
        <th>Piezas</th>
        <th>Tiempo</th>
    </tr>
    """

    for operador, d in sorted(resumen_operadores.items()):

        html += f"""
        <tr>
            <td>{operador}</td>
            <td>{d['operaciones']}</td>
            <td>{d['piezas']}</td>
            <td>{segundos_a_hm(d['tiempo'])}</td>
        </tr>
        """

    html += "</table>"

    # ----------------------------------
    # Detalle
    # ----------------------------------

    html += """
    <h3>Detalle de Operaciones</h3>

    <table>
    <tr>
        <th>Proyecto</th>
        <th>Posiciones</th>
        <th>Material</th>
        <th>Acabado</th>
        <th>Máquina</th>
        <th>Operador</th>
        <th>Piezas</th>
        <th>Inicio</th>
        <th>Fin</th>
    </tr>
    """

    for r in registros:

        html += f"""
        <tr>
            <td>{r['proyecto']}</td>
            <td>{', '.join(r['posiciones'])}</td>
            <td>{r['material']}</td>
            <td>{r['acabado']}</td>
            <td>{r['maquina']}</td>
            <td>{r['operador']}</td>
            <td>{r['cantidad']}</td>
            <td>{r['inicio'].strftime('%H:%M:%S')}</td>
            <td>{r['fin'].strftime('%H:%M:%S')}</td>
        </tr>
        """

    html += """
    </table>
    </div>
    </details>
    """

if incidencias:

    html += """
    <div class='card'>
    <h2>Incidencias</h2>
    <ul>
    """

    for i in incidencias:
        html += f"<li>{i}</li>"

    html += "</ul></div>"

html += """
</body>
</html>
"""

with open(HTML_SALIDA, "w", encoding="utf-8") as f:
    f.write(html)

print("=" * 60)
print("Dashboard generado correctamente")
print(HTML_SALIDA)
print("=" * 60)