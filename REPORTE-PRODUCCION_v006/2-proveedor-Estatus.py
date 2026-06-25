import pandas as pd
import re
from collections import defaultdict
from datetime import datetime

ARCHIVO_PROYECTOS = "proyectos.xlsx"
ARCHIVO_EMPAQUE = "TIME-TM.xlsx"
ARCHIVO_TM_PO = "TM-a-PO.xlsx"
HTML_SALIDA = "empaque-CheckList.html"

def extraer_proyecto_posiciones(tm):
    tm = str(tm).strip().upper()
    m = re.match(r"(TM\d+)", tm)
    if not m:
        return "", []
    proyecto = m.group(1)
    resto = tm[len(proyecto):]
    posiciones = re.findall(r"\d+", resto)
    return proyecto, posiciones

def formato_fecha(valor):
    if pd.isna(valor):
        return ""

    try:
        return pd.to_datetime(valor, format="%d/%m/%Y").strftime("%d/%m/%Y")
    except:
        return str(valor)

def formato_hora(valor):
    if pd.isna(valor):
        return ""
    try:
        return pd.to_datetime(str(valor)).strftime("%H:%M")
    except:
        return str(valor)

print("Leyendo archivos...")

df_proy = pd.read_excel(ARCHIVO_PROYECTOS)
df_tm_po = pd.read_excel(ARCHIVO_TM_PO)

df_material = pd.read_excel(ARCHIVO_EMPAQUE, sheet_name="PROVEEDOR")

df_packing = pd.read_excel(ARCHIVO_EMPAQUE, sheet_name="PACKING-CHECK")

material_index = {}
for _, row in df_material.iterrows():
    proyecto, posiciones = extraer_proyecto_posiciones(row["TM"])
    for pos in posiciones:
        clave = (proyecto, pos)
        if clave not in material_index:
            material_index[clave] = {
                "fecha": formato_fecha(row["FECHA"]),
                "hora": formato_hora(row["HORA"])
            }

packing_index = {}
for _, row in df_packing.iterrows():
    proyecto, posiciones = extraer_proyecto_posiciones(row["TM"])
    for pos in posiciones:
        clave = (proyecto, pos)
        if clave not in packing_index:
            packing_index[clave] = {
                "fecha": formato_fecha(row["FECHA"]),
                "hora": formato_hora(row["HORA"])
            }

proyectos = defaultdict(list)

for _, row in df_proy.iterrows():
    proyecto, posiciones = extraer_proyecto_posiciones(row["TM"])
    acabado = str(row["ACABADO"]).strip() if "ACABADO" in df_proy.columns else ""
    acabado_1 = str(row["IMAGEN"]).strip() if "IMAGEN" in df_proy.columns else ""

    for pos in posiciones:
        mat_check = (proyecto, pos) in material_index
        pack_check = (proyecto, pos) in packing_index

        proyectos[proyecto].append({
            "tm": f"{proyecto}-{pos}",
            "most": row["Most (Qty.)"],
            "opust": row["Opust (Qty.)"],
            "material": row["MATERIAL"],
            "acabado": acabado,
            "acabado_1": acabado_1,
            "mat_check": mat_check,
            "mat_fecha": material_index.get((proyecto,pos),{}).get("fecha",""),
            "mat_hora": material_index.get((proyecto,pos),{}).get("hora",""),
            "pack_check": pack_check,
            "pack_fecha": packing_index.get((proyecto,pos),{}).get("fecha",""),
            "pack_hora": packing_index.get((proyecto,pos),{}).get("hora",""),
            "completo": mat_check and pack_check
        })

orden_compra = defaultdict(list)

for _, row in df_tm_po.iterrows():
    tm = str(row["TM"]).strip()
    proyecto, posiciones_tm = extraer_proyecto_posiciones(tm)
    if not posiciones_tm:
        continue

    pos_tm = posiciones_tm[0]

    lista_po = [p.strip() for p in str(row["PO-NUM"]).split(",") if p.strip()]
    qty_total = int(row["QTY"])
    qty_individual = int(qty_total / len(lista_po) if lista_po else qty_total)

    mat_check = (proyecto, pos_tm) in material_index
    pack_check = (proyecto, pos_tm) in packing_index

    mat_fecha = material_index.get((proyecto,pos_tm),{}).get("fecha","")
    mat_hora = material_index.get((proyecto,pos_tm),{}).get("hora","")
    pack_fecha = packing_index.get((proyecto,pos_tm),{}).get("fecha","")
    pack_hora = packing_index.get((proyecto,pos_tm),{}).get("hora","")

    for po in lista_po:
        orden_compra[proyecto].append({
            "pos": po,
            "nombre": row["NOMBRE"],
            "qty": qty_individual,
            "mat_check": mat_check,
            "mat_fecha": mat_fecha,
            "mat_hora": mat_hora,
            "pack_check": pack_check,
            "pack_fecha": pack_fecha,
            "pack_hora": pack_hora,
            "completo": mat_check and pack_check
        })

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Empaque CheckList</title>
<style>
body{{font-family:Arial;background:#f4f6f9;margin:20px}}
.card{{background:white;padding:15px;border-radius:10px;margin:10px 0;box-shadow:0 0 8px rgba(0,0,0,.15)}}
table{{width:100%;border-collapse:collapse;margin-top:10px}}
th,td{{border:1px solid #ddd;padding:6px;font-size:13px}}
th{{background:#222;color:white}}
tr:hover {{background:#f7f7f7;}}
.ok{{color:green;font-weight:bold;text-align:center}}
.completo{{background:#28a745;color:white;font-weight:bold;padding:3px 6px}}
summary{{cursor:pointer;font-weight:bold;font-size:18px}}
.kpi{{display:inline-block;border:1px solid #ddd;padding:10px;margin:4px;border-radius:8px}}

.img-acabado_1 {{
    max-width: 80px;
    max-height: 40px;
    object-fit: contain;
}}

</style></head><body>
<img src="imagenes/foto.jpg" alt="Logo">
<h1>Empaque CheckList</h1>
<p>Actualizado: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
"""

for proyecto in sorted(proyectos.keys()):
    registros = proyectos[proyecto]
    total_pos = len(registros)
    total_completo = sum(r["completo"] for r in registros)

    html += f'<details open><summary>{proyecto}</summary><div class="card">'
    html += f'<div class="kpi"><b>Posiciones</b><br>{total_pos}</div>'
    html += f'<div class="kpi"><b>Completas</b><br>{total_completo}</div>'

    html += """<table><tr>
    <th>TM-POS</th><th>Most</th><th>Opust</th><th>MATERIAL</th><th>ACABADO</th> <th>IMAGEN</th>
    <th>MATERIAL-CHECK</th><th>FECHA</th><th>HORA</th>
    <th>PACKING-CHECK</th><th>FECHA</th><th>HORA</th><th>COMPLETO</th></tr>"""

    for r in registros:
        html += f"""
        <tr>
            <td>{r['tm']}</td>
            <td>{r['most']}</td>
            <td>{r['opust']}</td>
            <td>{r['material']}</td>
            <td>{r['acabado']}</td>
            <td> <img src="imagenes/{r['acabado_1']}.png" alt="{r['acabado_1']}" class="img-acabado_1"> </td> 
            <td class='ok'>{'✔' if r['mat_check'] else ''}</td>
            <td>{r['mat_fecha']}</td>
            <td>{r['mat_hora']}</td>
            <td class='ok'>{'✔' if r['pack_check'] else ''}</td>
            <td>{r['pack_fecha']}</td>
            <td>{r['pack_hora']}</td>
            <td>{'COMPLETO' if r['completo'] else ''}</td>
        
        </tr>"""

    html += "</table>"

    if proyecto in orden_compra:
        total_oc = len(orden_compra[proyecto])
        completas_oc = sum(r["completo"] for r in orden_compra[proyecto])
        avance = round((completas_oc/total_oc)*100,2) if total_oc else 0

        html += f'<details><summary>{proyecto} A ORDEN DE COMPRA ({completas_oc}/{total_oc} COMPLETAS - {avance}%)</summary>'
        html += """<table><tr>
        <th>POS</th><th>NOMBRE</th><th>Qty</th>
        <th>MATERIAL-CHECK</th><th>FECHA</th><th>HORA</th>
        <th>PACKING-CHECK</th><th>FECHA</th><th>HORA</th><th>COMPLETO</th></tr>"""

        for r in orden_compra[proyecto]:
            html += f"<tr><td>{r['pos']}</td><td>{r['nombre']}</td><td>{r['qty']}</td><td class='ok'>{'✔' if r['mat_check'] else ''}</td><td>{r['mat_fecha']}</td><td>{r['mat_hora']}</td><td class='ok'>{'✔' if r['pack_check'] else ''}</td><td>{r['pack_fecha']}</td><td>{r['pack_hora']}</td><td>{'COMPLETO' if r['completo'] else ''}</td></tr>"

        html += "</table></details>"

    html += "</div></details>"

html += "</body></html>"

with open(HTML_SALIDA,"w",encoding="utf-8") as f:
    f.write(html)

print("Dashboard generado:", HTML_SALIDA)
