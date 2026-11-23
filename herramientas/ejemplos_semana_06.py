import json
import pathlib
CWD = str(pathlib.Path(__file__).resolve().parents[1] / "programacion-ii" / "semana-06")
PD = 'import pandas as pd\npd.set_option("display.width", 70)\npd.set_option("display.max_columns", 8)\n'

LOAD = PD + 'df = pd.read_csv("datos/clientes_plan_movil.csv")\n'
NULOS = '''df = df.drop_duplicates()
df = df.dropna(subset=["monto_factura"])
df["minutos"] = df["minutos"].fillna(df["minutos"].median())
df["gb"] = df["gb"].fillna(df["gb"].median())
df["provincia"] = df["provincia"].fillna("Desconocida")
'''
TEXTO = '''df["provincia"] = df["provincia"].str.strip().str.title()
df["provincia"] = df["provincia"].replace({
    "Sto. Dgo.": "Santo Domingo",
    "Pto. Plata": "Puerto Plata",
    "San Cristobal": "San Cristóbal",
})
df["plan"] = df["plan"].str.title()
df["nombre"] = df["nombre"].str.strip().str.title()
'''
TIPOS = '''df["monto_factura"] = (df["monto_factura"]
    .str.replace("RD$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float))
df["fecha_alta"] = pd.to_datetime(df["fecha_alta"])
df.loc[df["minutos"] < 0, "minutos"] = 0
'''
NUEVAS = '''hoy = pd.Timestamp("2026-11-23")
df["meses_cliente"] = (hoy - df["fecha_alta"]).dt.days // 30
df["excedente_gb"] = (df["gb"] - 10).clip(lower=0)
df["segmento"] = pd.cut(df["monto_factura"],
                        bins=[0, 1500, 2500, 10000],
                        labels=["Bajo", "Medio", "Alto"])
'''

specs = [
 {"id": "s6_cargar", "filename": "limpieza.ipynb", "cwd": CWD, "setup": PD,
  "code": 'import pandas as pd\n\ndf = pd.read_csv("datos/clientes_plan_movil.csv")\nprint(df.shape)\nprint(df.dtypes)\n', "max_out": 12},
 {"id": "s6_diagnostico", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD,
  "code": 'print(df.isna().sum())\nprint("Filas duplicadas:", df.duplicated().sum())\nprint("Minutos negativos:", (df["minutos"] < 0).sum())\n', "max_out": 12},
 {"id": "s6_provincias", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD,
  "code": 'print(df["provincia"].unique())\n', "max_out": 6, "width": 1150},
 {"id": "s6_nulos", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD,
  "code": 'df = df.drop_duplicates()\ndf = df.dropna(subset=["monto_factura"])  # sin monto no sirve\n\nmediana = df["minutos"].median()\ndf["minutos"] = df["minutos"].fillna(mediana)\ndf["gb"] = df["gb"].fillna(df["gb"].median())\ndf["provincia"] = df["provincia"].fillna("Desconocida")\n\nprint(df.shape)\nprint(df.isna().sum()[df.isna().sum() > 0])\n', "max_out": 6},
 {"id": "s6_texto", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD + NULOS,
  "code": TEXTO + 'print(df["provincia"].value_counts())\n', "max_out": 9},
 {"id": "s6_tipos", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD + NULOS + TEXTO,
  "code": TIPOS + 'print(df[["fecha_alta", "minutos", "monto_factura"]].dtypes)\n', "max_out": 6},
 {"id": "s6_nuevas", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD + NULOS + TEXTO + TIPOS,
  "code": NUEVAS + 'print(df[["nombre", "meses_cliente", "segmento"]].head(4))\n', "max_out": 6},
 {"id": "s6_funcion", "filename": "limpieza.ipynb", "cwd": CWD, "setup": LOAD + NULOS + TEXTO + TIPOS + NUEVAS,
  "code": '''def clasificar_cliente(meses, monto):
    if pd.isna(meses):
        return "Revisar"
    if meses < 6:
        return "Nuevo"
    if monto > 2500:
        return "VIP"
    return "Regular"

df["tipo"] = df.apply(
    lambda f: clasificar_cliente(f["meses_cliente"], f["monto_factura"]),
    axis=1)
print(df["tipo"].value_counts())
''', "max_out": 6},
 {"id": "s6_taller", "filename": "taller_limpieza.py", "cwd": CWD, "setup": PD, "font": 17, "width": 1050,
  "code": '''import pandas as pd

CORRECCIONES = {"Sto. Dgo.": "Santo Domingo", "Pto. Plata": "Puerto Plata",
                "San Cristobal": "San Cristóbal"}

def limpiar_clientes(ruta):
    df = pd.read_csv(ruta).drop_duplicates()
    df = df.dropna(subset=["monto_factura"])
    for col in ["minutos", "gb"]:
        df[col] = df[col].fillna(df[col].median()).clip(lower=0)
    df["provincia"] = (df["provincia"].fillna("Desconocida").str.strip()
                       .str.title().replace(CORRECCIONES))
    df["monto_factura"] = (df["monto_factura"].str.replace("RD$", "", regex=False)
                           .str.replace(",", "", regex=False).astype(float))
    return df

limpio = limpiar_clientes("datos/clientes_plan_movil.csv")
print(limpio.groupby("provincia")["monto_factura"].agg(["count", "mean"]).round(2))
''', "max_out": 9},
]
json.dump(specs, open("specs_s6.json", "w"), ensure_ascii=False, indent=1)
