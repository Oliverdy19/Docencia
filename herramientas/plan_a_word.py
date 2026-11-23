"""Convierte un plan de clase en Markdown a Word con estilos nativos y tabla de contenido.

Uso: python3 build_docx.py plan.md specs.json salidas.json salida.docx
Los marcadores {{code:ID}} se reemplazan por el código y la salida real de ese ejemplo.
"""
import json, re, subprocess, sys, pathlib, copy
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

md, specs_p, outs_p, out = sys.argv[1:5]
HERE = pathlib.Path(__file__).parent
specs = {s["id"]: s for s in json.load(open(specs_p))}
outs = json.load(open(outs_p))
AZUL = RGBColor(0x02, 0x38, 0x77)


def code_block(m):
    s = specs[m.group(1)]
    lang = {"powershell": "powershell", "batch": "bat"}.get(s.get("lang", ""), "python")
    txt = f"```{lang}\n{s['code'].rstrip()}\n```\n"
    o = outs.get(m.group(1))
    if o:
        txt += f"\n*Salida:*\n\n```text\n{o}\n```\n"
    return txt


src = re.sub(r"\{\{code:([\w]+)\}\}", code_block, open(md, encoding="utf-8").read())
tmp_md = HERE / "_tmp_plan.md"
tmp_md.write_text(src, encoding="utf-8")

# --- documento de referencia con los estilos de la casa ---
ref = HERE / "reference.docx"
if not (HERE / "reference.ok").exists():
    subprocess.run(["pandoc", "-o", str(ref), "--print-default-data-file", "reference.docx"], check=True)
    (HERE / "reference.ok").write_text("1")
    d = Document(ref)
    st = d.styles
    byname = {x.name: x for x in st}
    byname["Normal"].font.name = "Calibri"; byname["Normal"].font.size = Pt(11)
    for name in ["Body Text", "First Paragraph", "Compact"]:
        if name in [s.name for s in st]:
            byname[name].font.name = "Calibri"; byname[name].font.size = Pt(11)
    for name, size in [("Title", 26), ("Subtitle", 13), ("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12)]:
        s = byname[name]; s.font.name = "Calibri"; s.font.size = Pt(size); s.font.color.rgb = AZUL; s.font.bold = name != "Subtitle"
        rpr = s.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
        if rf is None: rf = OxmlElement("w:rFonts"); rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(a), "Calibri")
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    byname["Heading 1"].paragraph_format.space_before = Pt(18)
    d.save(ref)

subprocess.run(["pandoc", str(tmp_md), "-o", out, "--toc", "--toc-depth=2", "--reference-doc", str(ref),
                "--highlight-style", "tango", "-M", "toc-title=Contenido"], check=True)
tmp_md.unlink()

# --- retoques: bordes en tablas, cabecera azul, fondo en código, notas del docente ---
d = Document(out)


def shade(el, color):
    pr = el.get_or_add_pPr() if hasattr(el, "get_or_add_pPr") else el
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), color)
    pr.append(shd)


for t in d.tables:
    tblPr = t._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}"); b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4"); b.set(qn("w:color"), "B7C6DB"); borders.append(b)
    tblPr.append(borders)
    for c in t.rows[0].cells:
        tcPr = c._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "023877"); tcPr.append(shd)
        for p in c.paragraphs:
            for r in p.runs: r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.bold = True
    for row in t.rows:
        for c in row.cells:
            mar = OxmlElement("w:tcMar")
            for side in ("top", "bottom", "start", "end"):
                m = OxmlElement(f"w:{side}"); m.set(qn("w:w"), "60" if side in ("top", "bottom") else "100"); m.set(qn("w:type"), "dxa"); mar.append(m)
            c._tc.get_or_add_tcPr().append(mar)

for p in d.paragraphs:
    sname = p.style.name if p.style is not None else ""
    if sname == "Source Code":
        pPr = p._p.get_or_add_pPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "F3F5F9"); pPr.append(shd)
        bdr = OxmlElement("w:pBdr"); l = OxmlElement("w:left"); l.set(qn("w:val"), "single"); l.set(qn("w:sz"), "18"); l.set(qn("w:color"), "023877"); l.set(qn("w:space"), "6"); bdr.append(l); pPr.append(bdr)
        for r in p.runs: r.font.size = Pt(9.5)
    elif sname == "Block Text":
        pPr = p._p.get_or_add_pPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "E8EEF6"); pPr.append(shd)
        bdr = OxmlElement("w:pBdr"); l = OxmlElement("w:left"); l.set(qn("w:val"), "single"); l.set(qn("w:sz"), "24"); l.set(qn("w:color"), "F2A900"); l.set(qn("w:space"), "8"); bdr.append(l); pPr.append(bdr)

# Word actualiza la tabla de contenido al abrir
settings = d.settings.element
uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true"); settings.append(uf)

# pie de página con número de página
sec = d.sections[0]
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run("Programación II · ITLA · Prof. Oliver Díaz Ynoa  —  Página "); run.font.size = Pt(9); run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
r2 = fp.add_run(); r2.font.size = Pt(9)
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tag:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag); r2._r.append(e)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; r2._r.append(e)
d.save(out)
print("ok", out)
