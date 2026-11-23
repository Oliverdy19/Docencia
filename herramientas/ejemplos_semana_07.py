import json, shutil, pathlib
SRC = pathlib.Path(__file__).resolve().parents[1] / "programacion-ii" / "semana-07" / "datos"
RUN = pathlib.Path(__file__).resolve().parent / "run7"
if RUN.exists():
    shutil.rmtree(RUN)
shutil.copytree(SRC, RUN / "datos")
CWD = str(RUN)
PD = 'import pandas as pd\nfrom pathlib import Path\npd.set_option("display.width", 70)\n'
VENTAS = PD + '''partes = [pd.read_csv(a) for a in sorted(Path("datos").glob("ventas_2026_0[1-3].csv"))]
ventas = pd.concat(partes, ignore_index=True)
'''
FUNCS = VENTAS + '''from datetime import datetime, date
def log(m):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {m}")
COLUMNAS = {"fecha", "sucursal", "producto", "cantidad", "precio_unitario"}
def extraer(carpeta):
    partes = []
    for a in sorted(Path(carpeta).glob("ventas_*.csv")):
        try:
            df = pd.read_csv(a)
            if COLUMNAS - set(df.columns):
                raise ValueError("columnas incorrectas")
            partes.append(df)
        except Exception as e:
            log(f"[ERROR] {a.name}: {e}")
    log(f"{len(partes)} archivos cargados")
    return pd.concat(partes, ignore_index=True)
def limpiar(df):
    df["sucursal"] = df["sucursal"].str.title()
    df["cantidad"] = df["cantidad"].fillna(0).astype(int)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["venta"] = df["cantidad"] * df["precio_unitario"]
    return df
def resumir(df):
    df["mes"] = df["fecha"].dt.strftime("%Y-%m")
    return df.pivot_table(index="sucursal", columns="mes", values="venta", aggfunc="sum")
def exportar(resumen, carpeta="salida"):
    Path(carpeta).mkdir(exist_ok=True)
    ruta = Path(carpeta) / f"resumen_ventas_{date.today():%Y%m%d}.csv"
    resumen.to_csv(ruta)
    return ruta
'''

specs = [
 {"id": "s7_script", "filename": "reporte_ventas.py", "cwd": CWD, "setup": PD,
  "code": '''"""reporte_ventas.py - Resumen de ventas de recargas de enero."""
import pandas as pd

RUTA = "datos/ventas_2026_01.csv"

def main():
    df = pd.read_csv(RUTA)
    total = (df["cantidad"] * df["precio_unitario"]).sum()
    print(f"Ventas de enero: RD${total:,.2f}")

if __name__ == "__main__":
    main()
'''},
 {"id": "s7_terminal", "filename": "Terminal — PowerShell", "lang": "powershell", "run": False,
  "code": '''PS C:\\analitica\\reporte_ventas> python reporte_ventas.py
Ventas de enero: RD$__TOTAL__
'''},
 {"id": "s7_glob", "filename": "reporte_ventas.py", "cwd": CWD, "setup": PD,
  "code": '''from pathlib import Path

carpeta = Path("datos")
for archivo in sorted(carpeta.glob("ventas_*.csv")):
    print(archivo.name, "-", archivo.stat().st_size, "bytes")
'''},
 {"id": "s7_lote", "filename": "reporte_ventas.py", "cwd": CWD, "setup": PD,
  "code": '''partes = []
for archivo in sorted(Path("datos").glob("ventas_2026_0[1-3].csv")):
    df = pd.read_csv(archivo)
    df["archivo"] = archivo.name      # de dónde vino cada fila
    partes.append(df)

ventas = pd.concat(partes, ignore_index=True)
print(ventas.shape)
print(ventas["archivo"].value_counts())
'''},
 {"id": "s7_errores", "filename": "reporte_ventas.py", "cwd": CWD, "setup": PD, "font": 18,
  "code": '''COLUMNAS = {"fecha", "sucursal", "producto", "cantidad", "precio_unitario"}
partes, fallidos = [], []

for archivo in sorted(Path("datos").glob("ventas_*.csv")):
    try:
        df = pd.read_csv(archivo)
        faltan = COLUMNAS - set(df.columns)
        if faltan:
            raise ValueError("faltan columnas: " + ", ".join(sorted(faltan)))
        partes.append(df)
    except Exception as e:
        fallidos.append(archivo.name)
        print(f"[ERROR] {archivo.name}: {e}")

print(len(partes), "archivos cargados,", len(fallidos), "con error")
''', "width": 1100},
 {"id": "s7_log", "filename": "reporte_ventas.py", "cwd": CWD, "setup": PD,
  "code": '''from datetime import datetime

def log(mensaje):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{hora}] {mensaje}"
    print(linea)
    with open("proceso.log", "a", encoding="utf-8") as f:
        f.write(linea + "\\n")

log("Inicio del proceso")
log("3 archivos cargados, 1 con error")
'''},
 {"id": "s7_limpiar_resumir", "filename": "reporte_ventas.py", "cwd": CWD, "setup": VENTAS,
  "code": '''def limpiar(df):
    df["sucursal"] = df["sucursal"].str.title()
    df["cantidad"] = df["cantidad"].fillna(0).astype(int)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["venta"] = df["cantidad"] * df["precio_unitario"]
    return df

def resumir(df):
    df["mes"] = df["fecha"].dt.strftime("%Y-%m")
    return df.pivot_table(index="sucursal", columns="mes",
                          values="venta", aggfunc="sum")

print(resumir(limpiar(ventas)))
'''},
 {"id": "s7_exportar", "filename": "reporte_ventas.py", "cwd": CWD, "setup": FUNCS,
  "code": '''from datetime import date

def exportar(resumen, carpeta="salida"):
    Path(carpeta).mkdir(exist_ok=True)
    nombre = f"resumen_ventas_{date.today():%Y%m%d}.csv"
    ruta = Path(carpeta) / nombre
    resumen.to_csv(ruta)
    return ruta

resumen = resumir(limpiar(ventas))
print("Guardado en:", exportar(resumen))
'''},
 {"id": "s7_main", "filename": "reporte_ventas.py", "cwd": CWD, "setup": FUNCS,
  "code": '''def main():
    log("Inicio del reporte de ventas")
    ventas = extraer("datos")          # lote + validación
    ventas = limpiar(ventas)           # texto, nulos, tipos
    resumen = resumir(ventas)          # sucursal x mes
    ruta = exportar(resumen)           # CSV con fecha en el nombre
    log(f"Reporte listo: {ruta}")

if __name__ == "__main__":
    main()
''', "width": 1050},
 {"id": "s7_bat", "filename": "ejecutar_reporte.bat", "lang": "batch", "run": False,
  "code": '''@echo off
REM Ejecuta el reporte y guarda todo lo que imprime en el log
cd /d C:\\analitica\\reporte_ventas
python reporte_ventas.py >> proceso.log 2>&1
'''},
]
# total real de enero para la captura de la terminal
import pandas as pd
_df = pd.read_csv(SRC / "ventas_2026_01.csv")
_total = (_df["cantidad"] * _df["precio_unitario"]).sum()
for s in specs:
    s["code"] = s["code"].replace("__TOTAL__", f"{_total:,.2f}")
json.dump(specs, open("specs_s7.json", "w"), ensure_ascii=False, indent=1)
