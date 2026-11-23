"""reporte_ventas.py - Resumen automático de ventas de recargas por sucursal y mes.

Solución de referencia del taller de la Semana 7 (Programación II, ITLA).
Uso, desde la carpeta semana-07:  python taller/reporte_ventas.py
"""
from datetime import datetime, date
from pathlib import Path

import pandas as pd

CARPETA_DATOS = Path("datos")
CARPETA_SALIDA = Path("salida")
ARCHIVO_LOG = Path("proceso.log")
COLUMNAS = {"fecha", "sucursal", "producto", "cantidad", "precio_unitario"}


def log(mensaje):
    """Muestra el mensaje con fecha y hora y lo agrega al archivo de log."""
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {mensaje}"
    print(linea)
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def extraer(carpeta):
    """Lee todos los ventas_*.csv de la carpeta; salta y registra los dañados."""
    partes = []
    for archivo in sorted(Path(carpeta).glob("ventas_*.csv")):
        try:
            df = pd.read_csv(archivo)
            faltan = COLUMNAS - set(df.columns)
            if faltan:
                raise ValueError("faltan columnas: " + ", ".join(sorted(faltan)))
            df["archivo"] = archivo.name
            partes.append(df)
        except Exception as e:
            log(f"[ERROR] {archivo.name}: {e}")
    if not partes:
        raise SystemExit("No se pudo cargar ningún archivo de ventas.")
    log(f"{len(partes)} archivos cargados")
    return pd.concat(partes, ignore_index=True)


def limpiar(df):
    """Estandariza sucursales, rellena cantidades vacías y calcula la venta."""
    df = df.copy()
    df["sucursal"] = df["sucursal"].str.strip().str.title()
    df["cantidad"] = df["cantidad"].fillna(0).astype(int)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["venta"] = df["cantidad"] * df["precio_unitario"]
    return df


def resumir(df):
    """Tabla de ventas por sucursal (filas) y mes (columnas)."""
    df = df.copy()
    df["mes"] = df["fecha"].dt.strftime("%Y-%m")
    return df.pivot_table(index="sucursal", columns="mes", values="venta", aggfunc="sum")


def exportar(resumen, carpeta=CARPETA_SALIDA):
    """Guarda el resumen en un CSV con la fecha de hoy en el nombre."""
    Path(carpeta).mkdir(exist_ok=True)
    ruta = Path(carpeta) / f"resumen_ventas_{date.today():%Y%m%d}.csv"
    resumen.to_csv(ruta)
    return ruta


def main():
    log("Inicio del reporte de ventas")
    ventas = extraer(CARPETA_DATOS)
    ventas = limpiar(ventas)
    resumen = resumir(ventas)
    ruta = exportar(resumen)
    print(resumen)
    log(f"Reporte listo: {ruta}")


if __name__ == "__main__":
    main()
