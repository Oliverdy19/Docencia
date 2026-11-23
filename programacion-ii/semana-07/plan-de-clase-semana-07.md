---
title: "Semana 7: Automatización de procesos analíticos"
subtitle: "Programación II para Analistas de Datos · ITLA · Prof. Oliver Díaz Ynoa"
lang: es-DO
---

# Ficha de la sesión

| Elemento | Detalle |
|---|---|
| Módulo | 2: Datos con Python |
| Semana | 7 de 13 |
| Enfoque | Eficiencia operativa |
| Duración | 3 horas (180 minutos), incluye receso de 10 minutos |
| Prerrequisitos | Funciones, try/except y limpieza de datos con pandas (semana 6) |
| Metodología | Codificación en vivo + trabajo en parejas + taller guiado |
| Datos | `datos/ventas_2026_01.csv` a `ventas_2026_03.csv`: ventas de recargas y paquetes por sucursal, y `ventas_2026_04.csv`, un archivo dañado a propósito |
| Recursos | VS Code (o cualquier editor) y terminal, pandas, proyector, Moodle |
| Evaluación de la semana | Práctica Semana 7 (5 pts) + hoja de presentación (0.5 pts) + foro |

# Objetivo de la semana

Que el estudiante sea capaz de **convertir un proceso analítico repetitivo en un script de Python que se ejecuta con un solo comando**, procesa varios archivos por lotes, registra lo que pasó y entrega un resultado listo para usar.

**Objetivos específicos:**

1. Pasar de un notebook a un script `.py` con estructura `main()` e `if __name__ == "__main__":`.
2. Recorrer una carpeta de archivos con `pathlib` y procesarlos por lotes.
3. Manejar archivos dañados sin detener el proceso completo, usando `try/except` por archivo.
4. Registrar el proceso en un log con fecha y hora.
5. Organizar el flujo en funciones: extraer → limpiar → resumir → exportar.
6. Programar la ejecución con un archivo `.bat` y el Programador de tareas de Windows.

**Indicadores de logro:**

- Ejecuta un script desde la terminal y explica qué hace cada función.
- Procesa una carpeta con varios CSV y obtiene un solo DataFrame.
- Su script no se detiene ante un archivo dañado: lo anota en el log y continúa.

# Agenda de la clase (3 horas)

| Tiempo | Bloque | Actividad | Técnica |
|---|---|---|---|
| 0:00 – 0:10 | Apertura | El reporte de los lunes: a mano vs con un script | Pregunta detonante |
| 0:10 – 0:40 | Bloque 1 | De notebook a script | Codificación en vivo |
| 0:40 – 1:05 | Bloque 2 | Procesamiento por lotes | Codificación en vivo + parejas |
| 1:05 – 1:15 | Receso | | |
| 1:15 – 1:40 | Bloque 3 | Errores y registro (log) | Codificación en vivo |
| 1:40 – 2:05 | Bloque 4 | Flujo de automatización y programar la ejecución | Exposición + ejemplos |
| 2:05 – 2:45 | Taller guiado | Script que automatiza limpieza y resumen de ventas | Parejas |
| 2:45 – 3:00 | Cierre | Quiz, ticket de salida, práctica y foro | Evaluación formativa |

# Desarrollo de la clase

## Apertura (10 min): el reporte de los lunes

Plantea el caso: **"Cada lunes, el gerente comercial pide las ventas de recargas por sucursal y por mes. Llegan tres archivos de Excel, uno por mes."**

Pregunta a la clase cómo lo harían a mano y escribe los pasos en la pizarra: abrir los archivos, copiar y pegar en uno, corregir sucursales mal escritas, hacer la tabla dinámica, guardar, enviar. Luego pregunta:

1. ¿Cuánto tiempo toma? ¿Y si son 12 meses o 30 sucursales?
2. ¿Qué pasa si un lunes alguien pega una fila de menos?
3. Si el proceso es siempre igual, ¿por qué lo hace una persona?

> **Nota para el docente:** la idea central de la semana es que **automatizar no es solo ir más rápido: es hacer el proceso repetible y verificable**. El script hace lo mismo cada vez y deja un registro de lo que hizo.

## Bloque 1 (30 min): de notebook a script

Un notebook es ideal para explorar. Para algo que se repite cada semana, se necesita un **script**: un archivo `.py` que se ejecuta de principio a fin con un comando.

{{code:s7_script}}

Se ejecuta desde la terminal:

{{code:s7_terminal}}

Explica la estructura:

- **Docstring del módulo:** la primera línea dice qué hace el script.
- **Constantes arriba** (`RUTA`): lo que cambia de un mes a otro se cambia en un solo lugar.
- **`main()`:** la función principal; el resto del programa son funciones que ella llama.
- **`if __name__ == "__main__":`** hace que `main()` se ejecute solo cuando el archivo se corre directamente, y no cuando otro script lo importa para usar sus funciones.

**Comprueba la comprensión:** ¿qué pasa si quitamos las dos últimas líneas y ejecutamos el script? (Nada: se definen las funciones, pero nadie llama a `main()`.)

## Bloque 2 (25 min): procesamiento por lotes

El script anterior lee un solo mes. Para leer todos, se recorre la carpeta.

{{code:s7_glob}}

`Path("datos").glob("ventas_*.csv")` devuelve todos los archivos que coinciden con el patrón; el `*` significa "cualquier cosa". `sorted` los ordena por nombre, que aquí también es orden cronológico.

Ahora se leen y se unen:

{{code:s7_lote}}

- Se guarda cada DataFrame en una **lista** y al final se unen con `pd.concat`: es más rápido y claro que ir pegando dentro del bucle.
- La columna `archivo` deja rastro de dónde vino cada fila; es útil cuando algo sale mal.
- `ignore_index=True` renumera las filas de 0 a 335.

**Actividad en parejas (5 min):** ¿qué patrón usarían para leer solo los archivos de 2026? ¿Y solo el primer trimestre? (`ventas_2026_*.csv` y `ventas_2026_0[1-3].csv`.)

## Bloque 3 (25 min): errores y registro

En la carpeta hay un cuarto archivo, `ventas_2026_04.csv`, exportado mal. Si el script se detiene por un archivo dañado, nadie recibe el reporte. La regla es: **un archivo malo se anota y se salta; no tumba el proceso.**

{{code:s7_errores}}

- El `try/except` va **dentro** del `for`: protege cada archivo por separado.
- Se valida que estén las columnas esperadas; si faltan, se lanza un error con un mensaje claro.
- Al final se informa cuántos archivos se cargaron y cuántos fallaron.

### Registrar lo que pasó

Cuando el script corre solo (por ejemplo, a las 6:00 a. m.), nadie ve la pantalla. Por eso se escribe un **log**: un archivo de texto con lo que pasó y a qué hora.

{{code:s7_log}}

El modo `"a"` (append) agrega al final del archivo en vez de sobrescribirlo, así queda el historial de todas las ejecuciones.

> **Nota para el docente:** existe el módulo `logging` de Python, más completo. Se menciona como siguiente paso, pero para esta semana basta con la función `log` propia: se entiende completa y refuerza funciones y archivos.

## Bloque 4 (25 min): flujo de automatización y programar la ejecución

Todo proceso analítico automatizado sigue el mismo flujo: **extraer → limpiar → resumir → exportar**. Cada paso es una función.

{{code:s7_limpiar_resumir}}

`pivot_table` arma la misma tabla dinámica que se haría en Excel: sucursales en filas, meses en columnas y la suma de ventas en las celdas. Fíjense en que `limpiar` usa lo mismo de la semana 6: `str.title()`, `fillna` y conversión de tipos.

{{code:s7_exportar}}

El nombre del archivo lleva la fecha de ejecución, así cada reporte queda guardado sin sobrescribir el anterior.

Con todas las piezas, `main()` se lee como una receta:

{{code:s7_main}}

### Programar la ejecución

Para que el script corra solo cada lunes se crea un archivo `.bat` y se agenda en el **Programador de tareas de Windows** (en Linux o Mac se usa `cron`).

{{code:s7_bat}}

Pasos en el Programador de tareas: *Crear tarea básica* → nombre "Reporte de ventas" → *Semanalmente*, lunes 6:00 a. m. → *Iniciar un programa* → seleccionar `ejecutar_reporte.bat`.

# Taller guiado (40 min): script que automatiza limpieza y resumen

**Consigna (en parejas).** Construyan `reporte_ventas.py`, que al ejecutarse:

1. Lea todos los archivos `ventas_*.csv` de la carpeta `datos/`.
2. Valide las columnas y salte los archivos dañados, registrándolos en `proceso.log`.
3. Limpie: sucursales en formato título, cantidades vacías en 0, fechas como fecha.
4. Calcule la venta de cada fila (`cantidad * precio_unitario`).
5. Resuma las ventas por sucursal y mes.
6. Exporte el resumen a `salida/resumen_ventas_AAAAMMDD.csv`.
7. Escriba en el log el inicio, los errores y la ruta del reporte.

**Pasos y tiempos:** estructura con `main()` y constantes (5 min) → `extraer` con lote y validación (12 min) → `limpiar` y `resumir` (12 min) → `exportar` y `log` (6 min) → prueba con el archivo dañado (5 min).

**Resultado esperado:** 3 archivos cargados, 1 con error en el log, y una tabla de 4 sucursales por 3 meses. La solución de referencia está en `taller/reporte_ventas.py`.

> **Cierre del taller:** pide a una pareja que saque `ventas_2026_03.csv` de la carpeta `datos/` y vuelva a ejecutar: el reporte sale con dos meses. Al devolverlo, vuelve a tres. El código no se tocó: el script se adapta a lo que haya en la carpeta. Esa es la diferencia con el proceso manual.

# Cierre (15 min)

- **Quiz en Moodle (5 preguntas):** `if __name__ == "__main__"`, patrones de `glob`, `try/except` dentro del bucle, modo `"a"`, orden del flujo.
- **Ticket de salida:** "¿Qué tarea repetitiva de tu trabajo o tus estudios automatizarías con lo de hoy?"
- **Presentación de la práctica y del foro.**

# Práctica Semana 7 (5 puntos)

Archivo: `practica-semana-07.ipynb` (el entregable final es un script `.py`). Se entrega el script, la carpeta `salida/` con el resultado, el `proceso.log` y el PDF con hoja de presentación (0.5 pts).

| # | Ejercicio | Puntos |
|---|---|---|
| 1 | Convertir un análisis de notebook a script con `main()` | 0.75 |
| 2 | Leer por lotes todos los CSV de una carpeta | 0.75 |
| 3 | Validar columnas y saltar archivos dañados | 1.0 |
| 4 | Función `log` y archivo de registro | 0.75 |
| 5 | Resumen por sucursal y producto, exportado con fecha | 1.0 |
| 6 | Archivo `.bat` y captura de la tarea programada | 0.75 |

## Rúbrica

| Criterio | Peso | Excelente | Necesita mejorar |
|---|---|---|---|
| El script funciona | 40 % | Corre con un comando y produce el reporte | Necesita pasos manuales o falla |
| Robustez | 30 % | Un archivo dañado no detiene el proceso y queda en el log | Se cae ante el primer error |
| Estructura | 30 % | Funciones con una tarea cada una, constantes arriba, docstrings | Todo en un solo bloque |

# Foro Semana 7: "Lo que automatizaría"

**Aporte (antes del miércoles):** describe una tarea repetitiva real. ¿Cada cuánto se hace? ¿Cuánto tarda? ¿Qué partes seguirían el flujo extraer → limpiar → resumir → exportar?

**Réplica (dos, antes del domingo):** a un compañero, identifica qué podría salir mal en su automatización (un archivo que no llega, un formato que cambia) y cómo lo manejaría el script.

# Errores comunes y cómo corregirlos

| Error | Por qué pasa | Cómo corregirlo |
|---|---|---|
| `FileNotFoundError` al ejecutar | La terminal está en otra carpeta | Ejecutar desde la carpeta del script o usar `cd /d` en el `.bat` |
| `glob` no encuentra nada | Patrón mal escrito o carpeta equivocada | Imprimir `list(Path("datos").glob("*"))` para ver qué hay |
| Un archivo dañado detiene todo | El `try` está fuera del `for` | Poner el `try/except` dentro del bucle |
| El log se borra cada vez | Se abre con `"w"` | Abrir con `"a"` |
| `main()` no hace nada | Falta llamarla al final | `if __name__ == "__main__": main()` |
| El reporte se sobrescribe | Nombre fijo | Agregar la fecha al nombre del archivo |

# Glosario

- **Script:** archivo `.py` que se ejecuta de principio a fin con un comando.
- **Procesamiento por lotes:** aplicar el mismo proceso a muchos archivos o registros de una vez.
- **Log:** archivo de texto donde el programa anota lo que hizo y cuándo.
- **Pipeline (flujo):** secuencia de pasos donde la salida de uno es la entrada del siguiente.
- **Tarea programada:** ejecución automática de un programa en un horario definido.

# Recursos recomendados

- Documentación de Python: `pathlib` y `logging` (docs.python.org).
- Sweigart, A. *Automate the Boring Stuff with Python*, capítulos sobre archivos y tareas programadas (automatetheboringstuff.com).
- Datos de la clase: `semana-07/datos/` en el repositorio del curso.
