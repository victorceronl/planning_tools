import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime

# =====================================================
# RUTAS
# =====================================================

ORIGEN_XLSX = r"C:\Users\Diseño 1\Documents\7.-Avance de producción\xls\TIEMPO-PRODUCCION.xlsx"

CARPETA_SCRIPT = Path(
    r"C:\Users\Diseño 1\Documents\REPORTE-PRODUCCION_v006"
)

DESTINO_XLSX = CARPETA_SCRIPT / "TIEMPO-PRODUCCION.xlsx"

SCRIPT_PYTHON = CARPETA_SCRIPT / "produccion_estatus.py"

HTML_GENERADO = CARPETA_SCRIPT / "produccion-estatus.html"

DESTINO_HTML_1 = (
    r"\\192.168.1.2\Arbeit2\TMIP2026\7.-Avance de producción\CheckList\produccion-estatus.html"
)

DESTINO_HTML_2 = (
    r"C:\Users\Diseño 1\Documents\7.-Avance de producción\CheckList\produccion-estatus.html"
)

# =====================================================
# CONFIGURACIÓN
# =====================================================

INTERVALO_SEGUNDOS = 1    # 1 minuto
DURACION_HORAS = 8

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def ejecutar_ciclo():

    print(f"\n[{datetime.now():%d/%m/%Y %H:%M:%S}] Iniciando ciclo")

    try:

        # -------------------------------------------------
        # COPIAR EXCEL
        # -------------------------------------------------

        print("Copiando corte.xlsx...")

        shutil.copy2(
            ORIGEN_XLSX,
            DESTINO_XLSX
        )

        print("Excel actualizado.")

        # -------------------------------------------------
        # EJECUTAR SCRIPT
        # -------------------------------------------------

        print("Ejecutando corte_estatus.py...")

        resultado = subprocess.run(
            ["python", str(SCRIPT_PYTHON)],
            cwd=str(CARPETA_SCRIPT),
            capture_output=True,
            text=True
        )

        print(resultado.stdout)

        if resultado.returncode != 0:
            print("ERROR EN EL SCRIPT:")
            print(resultado.stderr)
            return

        print("Script terminado correctamente.")

        # -------------------------------------------------
        # COPIAR HTML GENERADO
        # -------------------------------------------------

        if not HTML_GENERADO.exists():
            print("No se encontró corte-estatus.html")
            return

        print("Copiando HTML...")

        shutil.copy2(
            HTML_GENERADO,
            DESTINO_HTML_1
        )

        shutil.copy2(
            HTML_GENERADO,
            DESTINO_HTML_2
        )

        print("HTML actualizado correctamente.")

    except Exception as e:
        print(f"ERROR: {e}")

# =====================================================
# BUCLE DE 8 HORAS
# =====================================================

inicio = time.time()
fin = inicio + (DURACION_HORAS * 3600)

print("Proceso iniciado.")

while time.time() < fin:

    ejecutar_ciclo()

    if time.time() < fin:
        print(
            f"Esperando {INTERVALO_SEGUNDOS // 60} minutos..."
        )
        time.sleep(INTERVALO_SEGUNDOS)

print("Proceso finalizado después de 8 horas.")