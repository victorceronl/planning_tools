import pandas as pd
import re
from collections import defaultdict
from datetime import datetime

# =====================================================
# CONFIGURACION
# =====================================================

ARCHIVO_PROYECTOS = "proyectos.xlsx"
ARCHIVO_EMPAQUE = "proveedor.xlsx"

HTML_SALIDA = "proveedor-estatus.html"

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

df_proveedor = pd.read_excel(
    ARCHIVO_EMPAQUE,
    sheet_name="Sheet1"
)



# =====================================================
# PROVEEDOR
# =====================================================

material_index = {}
packing_index = {}
proveedor_index = {}

for _, row in df_proveedor.iterrows():

    tm = str(row["TM"]).strip()
    nombre = str(row["NOMBRE"]).strip().upper()

    fecha = row["FECHA"]
    hora = row["HORA"]

    tipo = str(row["TIPO"]).strip().upper()

    proyecto, posiciones = extraer_proyecto_posiciones(tm)

    if tipo == "SALIDA MATERIAL":
        for pos in posiciones:

            clave = (proyecto, pos)

        # conservar primer registro encontrado
        if clave not in material_index:

            material_index[clave] = {
                "fecha": formato_fecha(fecha),
                "hora": formato_hora(hora)
            }
    




    if tipo == "ENTRADA MATERIAL":
        for pos in posiciones:

            clave = (proyecto, pos)

        if clave not in packing_index:

            packing_index[clave] = {
                "fecha": formato_fecha(fecha),
                "hora": formato_hora(hora),
                "nombre": nombre
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
        pack_nombre = ""

        mat_check = (proyecto, pos) in material_index
        pack_check = (proyecto, pos) in packing_index

        mat_fecha = ""
        mat_hora = ""

        pack_fecha = ""
        pack_hora = ""
        
        if pack_check:

            pack_nombre = packing_index[
                (proyecto, pos)
            ]["nombre"]

        if mat_check:

            mat_fecha = material_index[
                (proyecto, pos)
            ]["fecha"]

            mat_hora = material_index[
                (proyecto, pos)
            ]["hora"]

        if pack_check:

            pack_fecha = packing_index[
                (proyecto, pos)
            ]["fecha"]

            pack_hora = packing_index[
                (proyecto, pos)
            ]["hora"]



        completo = mat_check and pack_check

        proyectos[proyecto].append({

            "tm": tm_pos,

            "most": most,
            "opust": opust,

            "material": material,
            "acabado": acabado,
            "acabado_1": acabado_1,
            
            "pack_nombre": pack_nombre,

            "mat_check": mat_check,
            "mat_fecha": mat_fecha,
            "mat_hora": mat_hora,

            "pack_check": pack_check,
            "pack_fecha": pack_fecha,
            "pack_hora": pack_hora,
            

            "completo": completo
        })

# =====================================================
# HTML
# =====================================================

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<title>Piezas Proveedor</title>

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

.completo {{
    background:#28a745;
    color:white;
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

</style>
</head>

<body>

<h1>Proveedor</h1>

<p>
Actualizado:
{datetime.now().strftime("%d/%m/%Y %H:%M")}
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

    total_packing = sum(
        r["pack_check"] for r in registros
    )

    total_completo = sum(
        r["completo"] for r in registros
    )

    html += f"""
    <details open>

    <summary>{proyecto}</summary>

    <div class="card">

        <div class="kpi">
        <b>Posiciones</b><br>
        {total_pos}
        </div>

        <div class="kpi">
        <b>Piezas con Proveedor</b><br>
        {total_material}
        </div>

        <div class="kpi">
        <b>Piezas Entregadas</b><br>
        {total_packing}
        </div>

        <div class="kpi">
        <b>Check SALIDA ENTRADA</b><br>
        {total_completo}
        </div>

        <table>

        <tr>
            <th>TM-POS</th>
            <th>Most (Qty.)</th>
            <th>Opust (Qty.)</th>
            <th>MATERIAL</th>
            <th>ACABADO</th>
            <th>NOMBRE</th>

            <th>SALIDA MATERIAL</th>
            <th>FECHA</th>
            <th>HORA</th>

            <th>ENTRADA MATERIAL</th>
            <th>FECHA</th>
            <th>HORA</th>

            <th>COMPLETO</th>
        </tr>
    """

    for r in registros:

        mat = "✔" if r["mat_check"] else ""
        pack = "✔" if r["pack_check"] else ""

        completo = (
            "<span class='completo'>COMPLETO</span>"
            if r["completo"]
            else ""
        )

        html += f"""
        <tr>

            <td>{r['tm']}</td>
            <td>{r['most']}</td>
            <td>{r['opust']}</td>

            <td>{r['material']}</td>
            <td>{r['acabado']}</td>
            <td>{r['pack_nombre']}</td>

            
            <td class="ok">{mat}</td>
            <td>{r['mat_fecha']}</td>
            <td>{r['mat_hora']}</td>

            <td class="ok">{pack}</td>
            <td>{r['pack_fecha']}</td>
            <td>{r['pack_hora']}</td>
            

            <td>{completo}</td>

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