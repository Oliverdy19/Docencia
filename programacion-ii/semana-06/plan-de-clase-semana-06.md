---
title: "Semana 6: Limpieza y transformación de datos"
subtitle: "Programación II para Analistas de Datos · ITLA · Prof. Oliver Díaz Ynoa"
lang: es-DO
---

# Ficha de la sesión

| Elemento | Detalle |
|---|---|
| Módulo | 2: Datos con Python |
| Semana | 6 de 13 |
| Enfoque | Preparación de datos |
| Duración | 3 horas (180 minutos), incluye receso de 10 minutos |
| Prerrequisitos | Estructuras de control (try/except, if, for), funciones con parámetros y `return` |
| Metodología | Codificación en vivo + trabajo en parejas + taller guiado |
| Dataset | `datos/clientes_plan_movil.csv`: 41 filas de clientes de un plan móvil con problemas de calidad a propósito |
| Recursos | Jupyter Notebook o VS Code con pandas, proyector, Moodle (quiz y foro) |
| Evaluación de la semana | Práctica Semana 6 (5 pts) + hoja de presentación (0.5 pts) + foro |

**Nota de continuidad.** Según el cronograma oficial, la semana 5 era "Introducción al manejo de datos" (lectura de CSV y exploración), pero en clase se dio Funciones. Por eso el Bloque 1 de esta semana incluye la carga y el diagnóstico del dataset con pandas, para que nadie llegue a la limpieza sin haber leído un CSV.

# Objetivo de la semana

Que el estudiante sea capaz de **convertir un dataset con problemas de calidad en un dataset confiable y listo para el análisis**, aplicando criterios explícitos y documentados para cada decisión de limpieza.

**Objetivos específicos:**

1. Cargar un CSV con pandas y diagnosticar sus problemas: nulos, duplicados, tipos incorrectos, valores imposibles y categorías mal escritas.
2. Decidir con criterio cuándo eliminar y cuándo imputar valores nulos.
3. Estandarizar texto (espacios, mayúsculas, abreviaturas) y corregir tipos de datos (números guardados como texto, fechas).
4. Crear nuevas variables analíticas a partir de las existentes: antigüedad, excedentes y segmentos.
5. Encapsular la limpieza en funciones reutilizables, conectando con lo visto en la semana de funciones.

**Indicadores de logro (lo que el estudiante demuestra al salir de clase):**

- Explica qué problema de calidad tiene cada columna del dataset y cómo lo detectó.
- Justifica en una oración cada decisión de limpieza (por qué eliminó, por qué imputó con la mediana).
- Entrega un `clientes_limpio.csv` sin nulos en las columnas clave, sin duplicados y con tipos correctos.

# Agenda de la clase (3 horas)

| Tiempo | Bloque | Actividad | Técnica |
|---|---|---|---|
| 0:00 – 0:10 | Apertura | "¿Cuántos clientes hay en Santo Domingo?" con datos sucios | Pregunta detonante |
| 0:10 – 0:40 | Bloque 1 | Cargar y diagnosticar el dataset | Codificación en vivo |
| 0:40 – 1:05 | Bloque 2 | Valores nulos y duplicados | Codificación en vivo + parejas |
| 1:05 – 1:15 | Receso | | |
| 1:15 – 1:45 | Bloque 3 | Transformación de variables: texto y tipos | Codificación en vivo |
| 1:45 – 2:05 | Bloque 4 | Nuevas variables analíticas y funciones de limpieza | Exposición + ejemplos |
| 2:05 – 2:45 | Taller guiado | Limpieza estructurada del dataset de clientes | Parejas con criterios definidos |
| 2:45 – 3:00 | Cierre | Quiz, ticket de salida, práctica y foro | Evaluación formativa |

# Desarrollo de la clase

## Apertura (10 min): ¿cuántos clientes hay en Santo Domingo?

Proyecta la columna `provincia` del dataset sin explicar nada y pregunta: **"¿Cuántos clientes tenemos en Santo Domingo?"**

{{code:s6_provincias}}

Deja que la clase cuente. Si se filtra solo `"Santo Domingo"` escrito exacto salen 3; si se cuentan todas las variantes salen 10, pero ahí hay clientes repetidos. Ninguno es el número correcto todavía: `"Santo Domingo"`, `"santo domingo"`, `" SANTO DOMINGO "` y `"Sto. Dgo."` son la misma provincia para una persona, pero **cuatro valores distintos para la computadora**.

**Preguntas para la clase:**

1. Si con estos datos le reportamos al gerente los clientes por provincia, ¿qué le estaríamos diciendo mal?
2. ¿De dónde salen estos errores? (Formularios sin validación, distintas personas capturando, sistemas que exportan distinto.)
3. ¿Quién ha tenido que "arreglar un Excel" antes de poder usarlo?

> **Nota para el docente:** se suele decir que un analista pasa la mayor parte de su tiempo preparando datos y no analizándolos. No hace falta dar una cifra exacta; basta con que reconozcan que limpiar es parte central del trabajo, no un paso menor.

## Bloque 1 (30 min): cargar y diagnosticar el dataset

Antes de limpiar hay que **saber qué está sucio**. Limpiar sin diagnosticar es como recetar sin examinar.

### Cargar el CSV

{{code:s6_cargar}}

Lee la salida con la clase: 41 filas y 8 columnas. `minutos` y `gb` son `float64` (números), pero `monto_factura` y `fecha_alta` aparecen como `object`, es decir, **texto**. Eso ya es una pista: no podremos sumar montos ni restar fechas todavía.

### Diagnóstico

{{code:s6_diagnostico}}

Construye en la pizarra la **tabla de diagnóstico**, que también será el formato del taller:

| Columna | Problema encontrado | Cómo lo detecté |
|---|---|---|
| provincia | 2 nulos, mayúsculas/espacios/abreviaturas distintas | `isna()`, `unique()` |
| minutos | 3 nulos, 1 valor negativo | `isna()`, `(df["minutos"] < 0).sum()` |
| gb | 2 nulos | `isna()` |
| monto_factura | 2 nulos, guardado como texto con "RD$" y comas | `isna()`, `dtypes` |
| fecha_alta | 1 nulo, guardada como texto | `isna()`, `dtypes` |
| (todas) | 3 filas duplicadas | `duplicated()` |

**Comprueba la comprensión:** ¿qué diferencia hay entre `df.isna().sum()` y `df.isna().sum().sum()`? (La primera da los nulos por columna; la segunda, el total de nulos de toda la tabla.)

> **Nota para el docente:** insiste en que el diagnóstico se **escribe**. En el trabajo real, esta tabla es la que se le muestra al dueño de los datos para acordar qué hacer con cada problema.

## Bloque 2 (25 min): valores nulos y duplicados

No hay una regla única para los nulos. La pregunta es siempre: **¿puedo usar esta fila sin ese dato?**

| Situación | Decisión | Ejemplo en el dataset |
|---|---|---|
| El dato es la razón de ser de la fila | Eliminar la fila | Sin `monto_factura` no podemos analizar facturación |
| Es numérico y faltan pocos | Imputar con la mediana | `minutos`, `gb` |
| Es categórico | Imputar con una categoría explícita | `provincia` → "Desconocida" |
| Faltan demasiados en una columna | Evaluar eliminar la columna | No aplica aquí |

{{code:s6_nulos}}

Explica tres detalles del código:

- `drop_duplicates()` va **primero**: si no, los duplicados pesan doble en la mediana.
- Se usa la **mediana** y no el promedio porque no se deja arrastrar por valores extremos (un cliente con 600 minutos mueve el promedio, no la mediana).
- Queda 1 nulo en `fecha_alta` **a propósito**: no inventamos fechas. Ese cliente se marcará como "Revisar" en el Bloque 4.

**Actividad en parejas (5 min):** ¿qué harían con un cliente que no tiene `plan`? ¿Y con uno que no tiene `id_cliente`? Justifiquen en una oración.

> **Nota para el docente:** el error más común es usar `df.dropna()` sin `subset`, que borra cualquier fila con al menos un nulo. Muéstralo: `df.dropna()` deja 31 filas, mientras que quitar duplicados y luego `dropna(subset=["monto_factura"])` deja 36. Pregunta: ¿valía la pena perder 5 clientes por un dato de GB o de minutos?

## Bloque 3 (30 min): transformación de variables

### Estandarizar texto

{{code:s6_texto}}

`str.strip()` quita espacios al inicio y al final; `str.title()` pone la primera letra de cada palabra en mayúscula. Con eso, tres de las cuatro variantes de Santo Domingo ya coinciden. Las abreviaturas (`"Sto. Dgo."`) necesitan un diccionario de correcciones con `replace`.

**Comprueba la comprensión:** ¿por qué `"Sto. Dgo."` no se arregla solo con `strip()` y `title()`? (Porque no es un problema de formato, sino otra forma de escribir el nombre: hay que decirle a Python a qué equivale.)

### Corregir tipos de datos

{{code:s6_tipos}}

- `monto_factura` venía como texto `"RD$1,823.10"`. Hay que quitar el símbolo y la coma **antes** de convertir con `astype(float)`.
- `regex=False` le dice a pandas que `"$"` es un carácter normal y no un símbolo especial.
- `pd.to_datetime` convierte las fechas; el nulo queda como `NaT` (la versión de `NaN` para fechas).
- Los minutos negativos son un **error de captura**: se llevan a 0 y se anota la decisión. En un caso real se consultaría con el área que generó el dato.

> **Nota para el docente:** pide que intenten `df["monto_factura"].astype(float)` sin limpiar primero. El `ValueError` que sale es la mejor explicación de por qué el orden importa.

## Bloque 4 (20 min): nuevas variables analíticas y funciones de limpieza

Las columnas que vienen en el archivo rara vez son las que responden la pregunta de negocio. Se crean a partir de ellas.

{{code:s6_nuevas}}

- **meses_cliente:** antigüedad, clave para retención (los clientes nuevos se van más).
- **excedente_gb:** cuánto se pasó del plan; `clip(lower=0)` evita excedentes negativos.
- **segmento:** `pd.cut` convierte un número en categorías por rangos.

### Funciones de limpieza: lo que aprendimos en funciones, aplicado a datos

{{code:s6_funcion}}

`apply(..., axis=1)` llama a la función **una vez por fila**. Fíjense en que la función devuelve con `return`: si usara `print`, la columna `tipo` quedaría llena de `None`. Es la misma lección de print vs return, ahora con un DataFrame.

# Taller guiado (40 min): limpieza estructurada del dataset

**Consigna (en parejas).** Partiendo del archivo original, produzcan `clientes_limpio.csv` siguiendo estos criterios:

1. Eliminar filas duplicadas.
2. Eliminar clientes sin `monto_factura`.
3. Imputar `minutos` y `gb` con la mediana; los minutos negativos pasan a 0.
4. Estandarizar `provincia`, `plan` y `nombre`; los nulos de provincia pasan a "Desconocida".
5. Convertir `monto_factura` a número y `fecha_alta` a fecha.
6. Crear `meses_cliente`, `excedente_gb` y `segmento`.
7. Todo dentro de una función `limpiar_clientes(ruta)` que devuelva el DataFrame limpio.
8. Escribir la tabla de decisiones: columna, problema, decisión y por qué.

**Pasos y tiempos:** diagnóstico y tabla (10 min) → función con los pasos 1 a 5 (15 min) → nuevas variables (5 min) → validación y exportación (10 min).

**Resultado esperado de la validación:** 36 clientes, 0 duplicados, `monto_factura` de tipo `float64`.

**Solución de referencia** (se proyecta al final, después de que las parejas presenten):

{{code:s6_taller}}

> **Cierre del taller:** vuelve a la pregunta de la apertura. Ahora la respuesta es una sola: Santo Domingo tiene 9 clientes. Lo que cambió no fue el análisis, fueron los datos.

# Cierre (15 min)

- **Quiz en Moodle (5 preguntas):** detectar nulos, elegir entre eliminar e imputar, `strip`/`title`, conversión de tipos, `pd.cut`.
- **Ticket de salida:** "Menciona un problema de calidad de datos que hayas visto en tu trabajo o en tus estudios y cómo lo limpiarías."
- **Presentación de la práctica y del foro.**

# Práctica Semana 6 (5 puntos)

Archivo: `practica-semana-06.ipynb`. Se entrega el notebook ejecutado y el PDF con hoja de presentación (0.5 pts).

| # | Ejercicio | Puntos |
|---|---|---|
| 1 | Diagnóstico completo del dataset en una tabla | 0.75 |
| 2 | Nulos: eliminar o imputar, con justificación | 0.75 |
| 3 | Estandarizar provincia, plan y nombre | 0.75 |
| 4 | Corregir tipos (monto y fecha) y valores imposibles | 0.75 |
| 5 | Tres variables nuevas, una de ellas con `pd.cut` | 1.0 |
| 6 | Función `limpiar_clientes(ruta)` y exportación a CSV | 1.0 |

## Rúbrica

| Criterio | Peso | Excelente | Necesita mejorar |
|---|---|---|---|
| El código funciona | 40 % | Ejecuta de principio a fin sin errores | Celdas que fallan o dependen del orden |
| Criterio de limpieza | 35 % | Cada decisión tiene una justificación clara | Decisiones sin explicar o arbitrarias |
| Orden y documentación | 25 % | Funciones con docstring, celdas de texto que explican | Código suelto sin explicación |

# Foro Semana 6: "Datos sucios de la vida real"

**Aporte (antes del miércoles):** describe un caso real (trabajo, universidad, negocio familiar) en el que los datos venían sucios. ¿Qué problema tenían? ¿Qué decisión de limpieza tomarías y por qué?

**Réplica (dos, antes del domingo):** a un compañero, propón una forma de **prevenir** ese problema desde la captura (validación en el formulario, listas desplegables, etc.).

# Errores comunes y cómo corregirlos

| Error | Por qué pasa | Cómo corregirlo |
|---|---|---|
| `df.dropna()` borra casi todo | Elimina filas con cualquier nulo | Usar `subset=[...]` con las columnas clave |
| `ValueError` al convertir montos | El texto tiene "RD$" o comas | Limpiar con `str.replace` antes de `astype(float)` |
| La limpieza "no se guarda" | Se calcula pero no se asigna | `df["col"] = df["col"].str.strip()` |
| `SettingWithCopyWarning` | Se modifica un filtro del DataFrame | Usar `df.loc[condición, "col"] = valor` o `.copy()` |
| Categorías siguen duplicadas | Falta una variante en el diccionario | Revisar `value_counts()` después de cada paso |
| Mediana distinta a la esperada | No se quitaron duplicados antes | Ordenar los pasos: duplicados → nulos |

# Glosario

- **Valor nulo (`NaN`, `NaT`):** dato faltante en una celda.
- **Imputar:** rellenar un valor faltante con uno estimado (mediana, moda, categoría fija).
- **Duplicado:** fila idéntica a otra en todas sus columnas.
- **Estandarizar:** llevar valores que significan lo mismo a una sola forma escrita.
- **Variable derivada:** columna nueva calculada a partir de otras.
- **Mediana:** valor del medio cuando los datos se ordenan; resiste mejor los valores extremos que el promedio.

# Recursos recomendados

- Documentación de pandas: "Working with missing data" y "Working with text data" (pandas.pydata.org).
- McKinney, W. *Python for Data Analysis*, capítulo 7: Data Cleaning and Preparation.
- Dataset de la clase: `semana-06/datos/clientes_plan_movil.csv` en el repositorio del curso.
