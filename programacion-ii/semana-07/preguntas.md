# Semana 7 — Preguntas para los estudiantes

Programación II · Automatización de procesos analíticos

## Repaso

1. ¿Qué ventajas tiene un script `.py` sobre un notebook para una tarea que se repite cada semana?
2. ¿Para qué sirve `if __name__ == "__main__":`?
3. ¿Por qué el `try/except` va **dentro** del `for` cuando se procesan varios archivos?
4. ¿Qué diferencia hay entre abrir un archivo con el modo `"w"` y con el modo `"a"`? ¿Cuál conviene para un log y por qué?

## Predice la salida (sin ejecutar)

5. La carpeta `datos/` tiene `ventas_2026_01.csv`, `ventas_2026_02.csv`, `clientes.csv` y `ventas_2025_12.xlsx`. ¿Qué imprime?
   ```python
   from pathlib import Path
   print([a.name for a in sorted(Path("datos").glob("ventas_2026_*.csv"))])
   ```
6. ```python
   partes = []
   for nombre in ["a", "b", "c"]:
       try:
           if nombre == "b":
               raise ValueError("dañado")
           partes.append(nombre)
       except ValueError:
           print("Error en", nombre)
   print(len(partes))
   ```
7. ¿Qué imprime este script al ejecutarlo con `python script.py`? ¿Por qué?
   ```python
   def main():
       print("Hola desde main")

   print("Inicio")
   ```

## Discusión (foro)

8. Describe una tarea repetitiva real (trabajo, universidad, negocio familiar). ¿Cada cuánto se hace y cuánto tarda? ¿Qué partes seguirían el flujo extraer → limpiar → resumir → exportar? ¿Qué podría salir mal si se automatiza?

## Reto

9. Agrega al script del taller una función `resumen_texto(resumen)` que devuelva un texto como `"La sucursal con más ventas en 2026-03 fue X con RD$Y"` para el último mes disponible, y escríbelo en el log al final de cada ejecución.
