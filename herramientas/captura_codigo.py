"""Renderiza fragmentos de código como captura de editor (tema oscuro) con su salida real.

Uso: python3 render.py specs.json carpeta_salida
Cada spec: {"id", "filename", "code", "setup"(opcional, código oculto que se ejecuta antes),
            "run"(bool, por defecto True), "cwd"(carpeta donde se ejecuta), "max_out"(líneas)}
El código se EJECUTA de verdad y la salida que se muestra es la que produjo.
"""
import json, sys, os, io, contextlib, html, pathlib, traceback
from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
FONT = HERE / "node_modules/@fontsource/jetbrains-mono/files"  # npm i @fontsource/jetbrains-mono@5.0.20 en esta carpeta


def run_code(spec):
    if not spec.get("run", True):
        return None
    cwd = spec.get("cwd") or os.getcwd()
    old = os.getcwd()
    os.chdir(cwd)
    buf = io.StringIO()
    g = {"__name__": "__main__"}
    try:
        with contextlib.redirect_stdout(buf):
            if spec.get("setup"):
                exec(spec["setup"], g)
            exec(spec["code"], g)
    except Exception:
        if not spec.get("expect_error"):
            os.chdir(old)
            raise RuntimeError(f"[{spec['id']}] el código falló:\n" + traceback.format_exc())
        tb = traceback.format_exc().strip().splitlines()
        buf.write(tb[-1] + "\n")
    finally:
        os.chdir(old)
    out = buf.getvalue().rstrip("\n")
    mx = spec.get("max_out", 14)
    lines = out.splitlines()
    if len(lines) > mx:
        lines = lines[:mx] + ["..."]
    return "\n".join(lines)


def page(spec, out):
    fmt = HtmlFormatter(style="one-dark", nowrap=True)
    lexer = get_lexer_by_name(spec["lang"]) if spec.get("lang") else PythonLexer()
    code_html = highlight(spec["code"].rstrip("\n"), lexer, fmt)
    n = len(spec["code"].rstrip("\n").splitlines())
    nums = "\n".join(str(i) for i in range(1, n + 1))
    css = fmt.get_style_defs(".code")
    out_block = ""
    if out is not None:
        out_block = f"""
        <div class="out"><div class="outlbl">▶ Salida</div><pre>{html.escape(out) if out else '(sin salida)'}</pre></div>"""
    width = spec.get("width", 1000)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: JB; src: url('file://{FONT}/jetbrains-mono-latin-400-normal.woff2'); font-weight: 400; }}
@font-face {{ font-family: JB; src: url('file://{FONT}/jetbrains-mono-latin-700-normal.woff2'); font-weight: 700; }}
html,body {{ margin:0; background: transparent; }}
#w {{ display:inline-block; padding: 0; }}
.win {{ width:{width}px; background:#282c34; border-radius:8px; overflow:hidden; border:1px solid #3a3f4b;
        box-shadow: 0 10px 30px rgba(0,0,0,.25); font-family: JB, 'DejaVu Sans Mono', monospace; }}
.bar {{ height:40px; background:#21252b; display:flex; align-items:stretch; padding:0 0 0 14px; }}
.ico {{ align-self:center; width:18px; height:18px; border-radius:3px; background:linear-gradient(135deg,#3776ab 50%,#ffd43b 50%); }}
.fname {{ align-self:center; margin-left:12px; color:#abb2bf; font-size:15px; font-family: Inter, sans-serif; }}
.sp {{ flex:1; }}
.ctl {{ width:52px; display:flex; align-items:center; justify-content:center; color:#c8ccd4; font-family: Inter, sans-serif; font-size:16px; }}
.ctl.x {{ font-size:18px; }}
.ctl svg {{ width:12px; height:12px; stroke:#c8ccd4; stroke-width:1.2; fill:none; }}
.body {{ display:flex; padding:18px 22px 20px 0; }}
.nums {{ color:#4b5263; text-align:right; padding:0 16px 0 18px; user-select:none; }}
pre {{ margin:0; font-size:{spec.get('font', 19)}px; line-height:1.55; white-space:pre; }}
.code pre {{ color:#abb2bf; }}
{css}
.code {{ background: transparent !important; }}
.out {{ background:#1b1f25; border-top:1px solid #3a3f4b; padding:12px 22px 18px 22px; }}
.outlbl {{ color:#98c379; font-size:14px; font-family: Inter, sans-serif; font-weight:600; margin-bottom:6px; letter-spacing:.5px; }}
.out pre {{ color:#e5e5e5; font-size:{spec.get('font', 19) - 1}px; }}
</style></head><body><div id="w"><div class="win">
<div class="bar"><span class="ico"></span><span class="fname">{html.escape(spec['filename'])} — Visual Studio Code</span><span class="sp"></span><span class="ctl"><svg viewBox="0 0 12 12"><path d="M1 6.5h10"/></svg></span><span class="ctl"><svg viewBox="0 0 12 12"><rect x="1.5" y="1.5" width="9" height="9"/></svg></span><span class="ctl"><svg viewBox="0 0 12 12"><path d="M1.5 1.5l9 9M10.5 1.5l-9 9"/></svg></span></div>
<div class="body"><pre class="nums">{nums}</pre><div class="code"><pre>{code_html}</pre></div></div>{out_block}
</div></div></body></html>"""


def main():
    specs = json.load(open(sys.argv[1]))
    dest = pathlib.Path(sys.argv[2]).resolve(); dest.mkdir(parents=True, exist_ok=True)
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(device_scale_factor=2, viewport={"width": 1400, "height": 900})
        for s in specs:
            out = run_code(s)
            results[s["id"]] = out
            tmp = dest / f"_{s['id']}.html"
            tmp.write_text(page(s, out), encoding="utf-8")
            pg.goto("file://" + str(tmp))
            pg.wait_for_timeout(150)
            pg.locator(".win").screenshot(path=str(dest / f"{s['id']}.png"), omit_background=True)
            tmp.unlink()
            print("ok", s["id"])
        b.close()
    json.dump(results, open(dest / "salidas.json", "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
