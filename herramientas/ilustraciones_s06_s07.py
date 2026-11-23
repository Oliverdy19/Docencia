"""Ilustraciones de concepto para las semanas 6 y 7 (colores de la plantilla ITLA)."""
import pathlib, sys
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(sys.argv[1]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:transparent;font-family:Inter,sans-serif;color:#1f2937}
.c{display:inline-block;padding:28px}
.card{background:#fff;border-radius:18px;box-shadow:0 8px 24px rgba(2,38,100,.12);border:1px solid #dbe4f0}
.t{font-weight:800;color:#023877}
.mono{font-family:'DejaVu Sans Mono',monospace}
</style></head><body><div class="c" id="c">%s</div></body></html>"""

def table(rows, bad=None, good=None, head_bg="#023877"):
    h = "".join(f"<th style='padding:12px 16px;text-align:left'>{c}</th>" for c in rows[0])
    body = ""
    for r in rows[1:]:
        tds = ""
        for c in r:
            style = "padding:11px 16px;border-top:1px solid #e5e7eb"
            if bad and c in bad: style += ";background:#fde2e2;color:#b91c1c;font-weight:700"
            if good and c in good: style += ";background:#dcfce7;color:#15803d;font-weight:700"
            tds += f"<td class='mono' style='{style}'>{c if c else '&nbsp;'}</td>"
        body += f"<tr>{tds}</tr>"
    return f"<table style='border-collapse:collapse;font-size:22px'><thead style='background:{head_bg};color:#fff;font-size:20px'><tr>{h}</tr></thead><tbody>{body}</tbody></table>"

ARROW = "<svg width='90' height='60' viewBox='0 0 90 60'><path d='M5 30h65' stroke='#023877' stroke-width='8' stroke-linecap='round'/><path d='M55 10l25 20-25 20' fill='none' stroke='#023877' stroke-width='8' stroke-linecap='round' stroke-linejoin='round'/></svg>"

ICON = {
 "file": "<svg width='70' height='70' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.6'><path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><path d='M14 2v6h6M8 13h8M8 17h6'/></svg>",
 "broom": "<svg width='70' height='70' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.6'><path d='M19 3l-7 7M9 11l4 4-3 6-7-7 6-3z'/><path d='M6 17l-2 2'/></svg>",
 "sigma": "<svg width='70' height='70' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.8'><path d='M18 4H6l7 8-7 8h12'/></svg>",
 "export": "<svg width='70' height='70' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.6'><path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3'/></svg>",
 "search": "<svg width='60' height='60' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.8'><circle cx='11' cy='11' r='7'/><path d='M21 21l-5-5'/></svg>",
 "hole": "<svg width='60' height='60' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.8'><rect x='3' y='3' width='18' height='18' rx='3'/><path d='M8 12h8' stroke-dasharray='2 2'/></svg>",
 "text": "<svg width='60' height='60' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.8'><path d='M4 7V4h16v3M9 20h6M12 4v16'/></svg>",
 "plus": "<svg width='60' height='60' viewBox='0 0 24 24' fill='none' stroke='#023877' stroke-width='1.8'><rect x='3' y='3' width='18' height='18' rx='3'/><path d='M12 8v8M8 12h8'/></svg>",
 "check": "<svg width='60' height='60' viewBox='0 0 24 24' fill='none' stroke='#15803d' stroke-width='2'><circle cx='12' cy='12' r='9'/><path d='M8 12l3 3 5-6'/></svg>",
}

def step(icon, title, sub, w=230):
    return (f"<div class='card' style='width:{w}px;height:210px;box-sizing:border-box;padding:22px 16px;text-align:center'>{icon}"
            f"<div class='t' style='font-size:26px;margin-top:10px'>{title}</div>"
            f"<div style='font-size:18px;color:#4b5563;margin-top:6px;line-height:1.35'>{sub}</div></div>")

ILL = {}

# 1. Antes / después de la limpieza (datos reales del dataset de la semana 6)
antes = [["id", "provincia", "minutos", "monto_factura"], ["1003", " SANTO DOMINGO ", "", "RD$1,823.10"],
         ["1027", "Sto. Dgo.", "392", "RD$1,795.96"], ["1020", "San Cristóbal", "-50", "RD$2,916.37"],
         ["1031", "", "192", "RD$2,531.10"], ["1026", "San Cristobal", "244", ""]]
despues = [["id", "provincia", "minutos", "monto_factura"], ["1003", "Santo Domingo", "392.0", "1823.10"],
           ["1027", "Santo Domingo", "392.0", "1795.96"], ["1020", "San Cristóbal", "0.0", "2916.37"],
           ["1031", "Desconocida", "192.0", "2531.10"], ["1026", "Fila eliminada", "—", "(sin monto)"]]
ILL["ill6_antes_despues"] = (
 "<div style='display:flex;align-items:center;gap:26px'>"
 f"<div class='card' style='padding:20px'><div class='t' style='font-size:28px;margin-bottom:12px;color:#b91c1c'>Antes: datos sucios</div>"
 + table(antes, bad={" SANTO DOMINGO ", "Sto. Dgo.", "San Cristobal", "-50", "RD$1,823.10", "RD$1,795.96", "RD$2,916.37", "RD$2,531.10", ""}) + "</div>"
 + ARROW +
 f"<div class='card' style='padding:20px'><div class='t' style='font-size:28px;margin-bottom:12px;color:#15803d'>Después: datos listos</div>"
 + table(despues, good={"Santo Domingo", "Desconocida", "392.0", "0.0", "1823.10", "1795.96", "2916.37", "2531.10"}, head_bg="#15803d") + "</div></div>")

# 2. Flujo de limpieza
ILL["ill6_flujo"] = ("<div style='display:flex;align-items:center;gap:10px'>" + ARROW.join([
 step(ICON["search"], "Diagnosticar", "info(), isna(), duplicated()"),
 step(ICON["hole"], "Nulos", "eliminar o imputar con criterio"),
 step(ICON["text"], "Texto y tipos", "strip, title, replace, astype"),
 step(ICON["plus"], "Nuevas variables", "antigüedad, segmento, excedente"),
 step(ICON["check"], "Validar", "volver a revisar y guardar")]) + "</div>")

# 3. Manual vs automatizado
def lista(items, color):
    return "".join(f"<div style='display:flex;gap:12px;align-items:flex-start;margin:10px 0;font-size:24px'><span style='color:{color};font-weight:800'>{i+1}.</span><span>{t}</span></div>" for i, t in enumerate(items))
ILL["ill7_manual_vs_script"] = (
 "<div style='display:flex;gap:34px'>"
 "<div class='card' style='width:560px;padding:28px;border-top:10px solid #b91c1c'>"
 "<div class='t' style='font-size:32px;color:#b91c1c'>A mano, cada lunes</div>"
 + lista(["Abrir 3 archivos de Excel", "Copiar y pegar en uno solo", "Corregir sucursales mal escritas", "Hacer la tabla dinámica", "Guardar y enviar el reporte"], "#b91c1c") +
 "<div style='margin-top:18px;font-size:30px;font-weight:800;color:#b91c1c'>≈ 2 horas · errores al copiar</div></div>"
 "<div class='card' style='width:560px;padding:28px;border-top:10px solid #15803d'>"
 "<div class='t' style='font-size:32px;color:#15803d'>Con un script</div>"
 + lista(["Poner los archivos en la carpeta datos/", "Ejecutar: python reporte_ventas.py", "Revisar el log y el reporte en salida/"], "#15803d") +
 "<div style='margin-top:96px;font-size:30px;font-weight:800;color:#15803d'>≈ 1 minuto · siempre igual</div></div></div>")

# 4. Pipeline ETL
ILL["ill7_pipeline"] = ("<div style='display:flex;align-items:center;gap:10px'>" + ARROW.join([
 step(ICON["file"], "Extraer", "leer todos los CSV de la carpeta", 260),
 step(ICON["broom"], "Limpiar", "texto, nulos y tipos de datos", 260),
 step(ICON["sigma"], "Resumir", "ventas por sucursal y mes", 260),
 step(ICON["export"], "Exportar", "CSV con la fecha en el nombre", 260)]) + "</div>")

# 5. Procesamiento por lotes
def fichero(nombre, ok=True):
    col = "#023877" if ok else "#b91c1c"
    mark = "" if ok else "<div style='position:absolute;right:-8px;top:-8px;background:#b91c1c;color:#fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:22px'>✕</div>"
    return (f"<div style='position:relative;display:flex;align-items:center;gap:12px;margin:10px 0' class='card'>"
            f"<div style='padding:10px 14px;display:flex;align-items:center;gap:12px'>{ICON['file'].replace('#023877', col).replace('70', '44')}"
            f"<span class='mono' style='font-size:22px;color:{col}'>{nombre}</span></div>{mark}</div>")
ILL["ill7_lotes"] = (
 "<div style='display:flex;align-items:center;gap:26px'>"
 "<div><div class='t' style='font-size:26px;margin-bottom:6px'>datos/</div>"
 + fichero("ventas_2026_01.csv") + fichero("ventas_2026_02.csv") + fichero("ventas_2026_03.csv") + fichero("ventas_2026_04.csv", False) +
 "</div>" + ARROW +
 "<div class='card' style='padding:26px;text-align:center;width:300px'><div class='mono t' style='font-size:26px'>for archivo in<br>carpeta.glob(...)</div>"
 "<div style='font-size:20px;color:#4b5563;margin-top:10px'>leer · validar · guardar en una lista<br>si falla: anotar y seguir</div></div>"
 + ARROW +
 "<div class='card' style='padding:26px;text-align:center;width:300px'><div class='t' style='font-size:28px'>pd.concat(...)</div>"
 "<div style='font-size:22px;color:#4b5563;margin-top:10px'>1 DataFrame<br><b style='color:#15803d'>336 filas · 3 archivos</b><br><b style='color:#b91c1c'>1 archivo con error en el log</b></div></div></div>")

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(device_scale_factor=2, viewport={"width": 2200, "height": 1200})
    for k, v in ILL.items():
        f = OUT / f"_{k}.html"; f.write_text(BASE % v, encoding="utf-8")
        pg.goto("file://" + str(f)); pg.wait_for_timeout(150)
        pg.locator("#c").screenshot(path=str(OUT / f"{k}.png"), omit_background=True); f.unlink(); print("ok", k)
    b.close()
