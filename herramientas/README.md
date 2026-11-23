# Herramientas

Scripts para producir el material siguiendo `REGLAS.md`.

| Script | Qué hace |
|---|---|
| `captura_codigo.py` | Ejecuta cada ejemplo de código y genera una captura tipo VS Code (tema oscuro, ventana de Windows) con su **salida real**. |
| `ejemplos_semana_XX.py` | Define los ejemplos de código de cada semana (archivo, código, código oculto de preparación). Genera `specs_sXX.json`. |
| `ilustraciones_s06_s07.py` | Genera las ilustraciones de concepto (antes/después, flujos, comparaciones) con los colores de la plantilla. |
| `plan_a_word.py` | Convierte `plan-de-clase-semana-XX.md` en Word con estilos nativos, tabla de contenido y el código y la salida reales en lugar de cada `{{code:ID}}`. |

## Uso

```bash
# una sola vez, en esta carpeta
npm i @fontsource/jetbrains-mono@5.0.20
pip install pandas==2.2.3 pygments playwright python-docx

# capturas de la semana 6
python ejemplos_semana_06.py                 # crea specs_s6.json
python captura_codigo.py specs_s6.json salida_s6/

# plan en Word
python plan_a_word.py ../programacion-ii/semana-06/plan-de-clase-semana-06.md specs_s6.json salida_s6/salidas.json ../programacion-ii/semana-06/plan-de-clase-semana-06.docx
```

Se usa pandas 2.2 porque es la versión que tienen los estudiantes (Anaconda/Colab); con pandas 3 cambian algunas salidas (`object` aparece como `str`).
