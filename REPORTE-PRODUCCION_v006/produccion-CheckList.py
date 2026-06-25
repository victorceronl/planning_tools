import pandas as pd
import re
from collections import defaultdict
from datetime import datetime

# =====================================================
# CONFIGURACION
# =====================================================

ARCHIVO_PROYECTOS = "proyectos.xlsx"
ARCHIVO_EMPAQUE = "produccion-checklist.xlsx"

HTML_SALIDA = "produccion-CheckList.html"

# =====================================================
# FUNCIONES
# =====================================================

def extraer_proyecto_posiciones(tm):
    """
    Ejemplos:

    TM2605007-001
    -> proyecto TM2605007
       posiciones ['001']

    TM2605007-001-002-003
    -> proyecto TM2605007
       posiciones ['001','002','003']
    """

    tm = str(tm).strip().upper()

    proyecto_match = re.match(r"(TM\d+)", tm)

    if not proyecto_match:
        return "", []

    proyecto = proyecto_match.group(1)

    resto = tm[len(proyecto):]

    posiciones = re.findall(r"\d+", resto)

    return proyecto, posiciones


def formato_fecha(valor):

    if pd.isna(valor):
        return ""

    try:
        return pd.to_datetime(valor).strftime("%d/%m/%Y")
    except:
        return str(valor)


def formato_hora(valor):

    if pd.isna(valor):
        return ""

    try:
        return pd.to_datetime(str(valor)).strftime("%H:%M")
    except:
        return str(valor)


# =====================================================
# LEER ARCHIVOS
# =====================================================

print("Leyendo archivos...")

df_proy = pd.read_excel(ARCHIVO_PROYECTOS)

df_material = pd.read_excel(
    ARCHIVO_EMPAQUE,
    sheet_name="Sheet1"
)


# =====================================================
# INDICE MATERIAL
# GUARDA EL REGISTRO MAS ANTIGUO
# =====================================================

material_index = {}

for _, row in df_material.iterrows():

    tm = str(row["TM"]).strip()

    fecha = row["FECHA"]
    hora = row["HORA"]

    proyecto, posiciones = extraer_proyecto_posiciones(tm)

    for pos in posiciones:

        clave = (proyecto, pos)

        # conservar primer registro encontrado
        if clave not in material_index:

            material_index[clave] = {
                "fecha": formato_fecha(fecha),
                "hora": formato_hora(hora)
            }


# =====================================================
# PROYECTOS
# =====================================================

proyectos = defaultdict(list)

for _, row in df_proy.iterrows():

    tm_original = str(row["TM"]).strip()

    proyecto, posiciones = extraer_proyecto_posiciones(
        tm_original
    )

    most = row["Most (Qty.)"]
    opust = row["Opust (Qty.)"]
    material = str(row["MATERIAL"]).strip()

    try:
        acabado = str(row["ACABADO"]).strip()
    except:
        acabado = ""


    try:
        acabado_1 = str(row["IMAGEN"]).strip()
    except:
        acabado_1 = ""


    for pos in posiciones:

        tm_pos = f"{proyecto}-{pos}"

        mat_check = (proyecto, pos) in material_index

        mat_fecha = ""
        mat_hora = ""

        if mat_check:

            mat_fecha = material_index[
                (proyecto, pos)
            ]["fecha"]

            mat_hora = material_index[
                (proyecto, pos)
            ]["hora"]



        proyectos[proyecto].append({

            "tm": tm_pos,

            "most": most,
            "opust": opust,

            "material": material,
            "acabado": acabado,
            "acabado_1": acabado_1,

            "mat_check": mat_check,
            "mat_fecha": mat_fecha,
            "mat_hora": mat_hora,

        })

# =====================================================
# HTML
# =====================================================

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<title>CheckList PRODUCCION</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background:#f4f6f9;
    margin:20px;
}}

h1 {{
    color:#222;
}}


.card {{
    background:white;
    border-radius:10px;
    padding:15px;
    margin-bottom:25px;
    box-shadow:0 0 8px rgba(0,0,0,0.15);
}}

table {{
    width:100%;
    border-collapse:collapse;
    margin-top:10px;
}}

th {{
    background:#222;
    color:white;
    padding:8px;
    font-size:14px;
}}

td {{
    border:1px solid #ddd;
    padding:6px;
    font-size:13px;
}}

tr:hover {{
    background:#f7f7f7;
}}

summary {{
    cursor:pointer;
    font-size:20px;
    font-weight:bold;
}}

.ok {{
    color:#28a745;
    font-size:18px;
    font-weight:bold;
    text-align:center;
}}



.kpi {{
    display:inline-block;
    background:#fafafa;
    border:1px solid #ddd;
    border-radius:8px;
    padding:10px;
    margin-right:10px;
    min-width:140px;
}}


.img-acabado_1 {{
    max-width: 80px;
    max-height: 40px;
    object-fit: contain;
}}

.referencia {{
  width:auto;
  margin:auto;
  padding:25px;
  font-size:30px;
  text-align:center;

}}

div:hover {{
  background-color: #f7f7f7;
  cursor: pointer;
}}


</style>
</head>

<body>

<img src="imagenes/foto.jpg" alt="Logo">
<h1>CheckList Produccion</h1>

<p>
Actualizado:
{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
</p>

"""

# =====================================================
# TABLAS POR PROYECTO
# =====================================================

for proyecto in sorted(proyectos.keys()):

    registros = proyectos[proyecto]

    total_pos = len(registros)

    total_material = sum(
        r["mat_check"] for r in registros
    )



    html += f"""
    <details closed>

    <summary>{proyecto}</summary>

    <div class="card">

        <div class="kpi">
        <b>Posiciones</b><br>
        {total_pos}
        </div>

        <div class="kpi">
        <b>Piezas Entregadas</b><br>
        {total_material}
        </div>



        <table>

        <tr>
            <th>TM-POS</th>
            <th>Most (Qty.)</th>
            <th>Opust (Qty.)</th>
            <th>MATERIAL</th>
            <th>ACABADO</th>
            <th>IMAGEN</th>

            <th>Produccion</th>
            <th>FECHA</th>
            <th>HORA</th>

        </tr>
    """

    for r in registros:

        mat = "✔" if r["mat_check"] else ""

        html += f"""
        <tr>

            <td>{r['tm']}</td>
            <td>{r['most']}</td>
            <td>{r['opust']}</td>

            <td>{r['material']}</td>
            <td>{r['acabado']}</td>
            
            <td>
                <img src="imagenes/{r['acabado_1']}.png" alt="{r['acabado_1']}" class="img-acabado_1">
            </td>

            <td class="ok">{mat}</td>
            <td>{r['mat_fecha']}</td>
            <td>{r['mat_hora']}</td>    

        </tr>
        """

    html += """
        </table>
    </div>
    </details>
    """

html += """
</body>
</html>
"""

with open(
    HTML_SALIDA,
    "w",
    encoding="utf-8"
) as f:

    f.write(html)

print("=" * 60)
print("Dashboard generado correctamente")
print(HTML_SALIDA)
print("=" * 60)