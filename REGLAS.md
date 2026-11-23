# Reglas de trabajo — Docencia

Este documento define **cómo se prepara cada semana de clase**: qué se entrega, con qué estructura y con qué nivel de calidad. Aplica a Programación II (ITLA) y sirve de base para las demás asignaturas.

Prof. Oliver Díaz Ynoa

---

## 1. Principio general

Cada semana es un **paquete completo** que vive en su propia carpeta y contiene siempre lo mismo:

| Pieza | Archivo en la carpeta | Dónde se edita |
|---|---|---|
| Ficha de la semana | `README.md` | GitHub |
| Plan de clase (documento) | `plan-de-clase-semana-XX.docx` (y/o `.md`) | Word / GitHub |
| Presentación | enlace en el `README.md` (+ PDF exportado cuando se pueda) | Canva |
| Práctica | `practica-semana-XX.ipynb` | Jupyter |
| Preguntas para los estudiantes | `preguntas.md` | GitHub |

Una semana **no está terminada** hasta que tiene las cinco piezas y pasa la lista de calidad de la sección 8.

---

## 2. Estructura del repositorio

```
Docencia/
├── README.md                 ← portada del repositorio
├── REGLAS.md                 ← este documento
├── CLAUDE.md                 ← instrucciones para la IA (las lee sola al conectarse)
└── programacion-ii/
    ├── README.md             ← cronograma de las 13 semanas y estado de cada una
    ├── plantillas/           ← plantillas para la ficha y las preguntas
    ├── semana-01/
    ├── semana-03/
    └── semana-05/
```

Nombres: carpetas `semana-XX` con dos dígitos (`semana-01`, `semana-12`), archivos en minúscula y con guiones, sin tildes ni espacios.

---

## 3. Flujo semanal (paso a paso)

1. **Tema desde el cronograma.** El tema sale de `programacion-ii/README.md`. Si la semana dice "Por definir", primero se define ahí; nunca se inventa el tema al momento.
2. **Plan de clase.** Se escribe el documento de la semana con la estructura de la sección 5. Cubre las **3 horas** completas.
3. **Presentación.** Se duplica la plantilla de Canva y se llena siguiendo la sección 4. La plantilla maestra nunca se edita directamente.
4. **Práctica.** Notebook con 5–7 ejercicios graduados (🟢 🟡 🟠), rúbrica y valor en puntos.
5. **Preguntas.** Banco de 8–12 preguntas para los estudiantes (sección 6).
6. **Subir a GitHub.** Se crea la carpeta `semana-XX`, se actualiza el cronograma y se hace commit con el mensaje `Semana XX: <tema>`.
7. **Evaluaciones aparte.** Parciales, quizzes con respuestas y notas **no se suben** a este repositorio mientras sea público (sección 9).

---

## 4. Estructura de la presentación (Canva)

**Plantilla:** diseño "Programación II" en Canva (ITLA, azul `#002664` en separadores, azul `#023877` en encabezados, pie "© Oliver Diaz Ynoa").
**Cada semana es un diseño aparte**, llamado `Programación II – Semana X`, creado como copia de la plantilla.

Orden fijo de diapositivas (modelo: Semana 5, 24 diapositivas):

| # | Tipo | Contenido |
|---|---|---|
| 1 | Portada | Instituto, asignatura, facilitador |
| 2 | Separador | `Semana X - <Tema>` |
| 3 | Índice | Tabla de contenido con los bloques de la clase (máximo 8) |
| 4–5 | Separador + contenido | `01 - Objetivo de la semana` (objetivo general y específicos) |
| … | Separador + 1 a 3 de contenido | Un bloque por tema (`02`, `03`, …), en el mismo orden que la agenda del plan |
| — | Separador + 1–2 de contenido | Taller guiado: enunciado, pasos, casos de prueba y solución de referencia |
| — | Separador + contenido | Cierre: quiz, ticket de salida, práctica, foro, Q & A |
| última | Cierre | GRACIAS |

Reglas de las diapositivas:

- Una idea por diapositiva. Si el texto no cabe con letra legible, se divide.
- El código va en bloque con barra de acento azul a la izquierda, nunca como imagen borrosa.
- Todo código que aparece en una diapositiva **se ejecutó antes** y la salida mostrada es la real.
- Los bloques de la presentación coinciden 1 a 1 con los bloques de la agenda del plan de clase.

---

## 5. Estructura del documento de la semana (plan de clase)

1. **Ficha de la sesión** — módulo, semana, duración, prerrequisitos, metodología, recursos, evaluación.
2. **Objetivo de la semana** — objetivo general, 4–6 objetivos específicos e indicadores de logro.
3. **Agenda de 3 horas** — tabla con tiempo, bloque, actividad y técnica (incluye receso de 10 min).
4. **Desarrollo de la clase** — por cada bloque: explicación, ejemplo en vivo, preguntas de comprobación y nota para el docente.
5. **Taller guiado** (≈40 min) — un mismo caso que atraviesa la clase.
6. **Cierre** — quiz, ticket de salida, presentación de la práctica y del foro.
7. **Práctica** con rúbrica.
8. **Foro** de la semana (aporte + réplica).
9. **Errores comunes, glosario y recursos.**

Formato Word: estilos de título nativos y tabla de contenido automática.

---

## 6. Preguntas para los estudiantes (`preguntas.md`)

Entre 8 y 12 preguntas por semana, en cuatro grupos:

| Grupo | Para qué | Cantidad |
|---|---|---|
| Repaso | Comprobar conceptos clave | 3–4 |
| Predice la salida | Leer código sin ejecutarlo | 3–4 |
| Discusión / foro | Conectar con el trabajo de un analista de datos | 1–2 |
| Reto | Un ejercicio corto para resolver en casa | 1 |

- El archivo del repositorio lleva **solo las preguntas**. Las respuestas se guardan fuera mientras el repositorio sea público.
- Las preguntas de esta carpeta alimentan los parciales: un parcial se arma tomando preguntas de las semanas que cubre.

---

## 7. Evaluaciones

- Formato de parcial usado hasta ahora: 15 preguntas, 10 puntos exactos (10 × 0.6 + 5 × 0.8), selección múltiple con una o varias respuestas correctas.
- Plataforma: Moodle (formato GIFT) o Microsoft Teams (Forms, armado con Copilot a partir de un prompt).
- Las entregas de los estudiantes son en PDF con hoja de presentación (vale 0.5 pts).

---

## 8. Lista de calidad (antes de dar una semana por terminada)

- [ ] El tema coincide con el cronograma.
- [ ] La agenda suma 180 minutos y cada bloque tiene actividad para el estudiante, no solo exposición.
- [ ] Todo el código del plan, la presentación, la práctica y las preguntas se ejecutó y las salidas son reales.
- [ ] Los bloques de la presentación coinciden con los de la agenda.
- [ ] Los ejemplos usan casos reales del país o del trabajo de analista (facturas, ITBIS, telecom, colmado, etc.).
- [ ] La práctica tiene valor en puntos y rúbrica.
- [ ] Hay preguntas de repaso, de predicción, de discusión y un reto.
- [ ] La carpeta está en GitHub y el cronograma está actualizado.

---

## 9. Qué no va en este repositorio

Mientras el repositorio sea **público**, no se suben:

- Parciales, quizzes ni sus claves de respuesta.
- Respuestas de las preguntas semanales.
- Calificaciones o datos de estudiantes.

Si el repositorio se vuelve privado, las evaluaciones irán en `programacion-ii/evaluaciones/`.

---

## 10. Cómo trabajar con la IA (Claude)

La IA rinde más cuando recibe el tema ya definido y el formato ya decidido. Para cada semana:

1. Conectar este repositorio en la sesión: la IA lee `CLAUDE.md` y estas reglas sola.
2. Pedir la semana con el prompt de abajo.
3. Revisar el borrador del plan **antes** de pedir la presentación (corregir temprano es más barato).
4. Pedir la presentación en Canva, luego la práctica y las preguntas.
5. Pedir que suba la carpeta a GitHub y actualice el cronograma.

Prompt base para una semana nueva:

```
Prepara la Semana X de Programación II siguiendo REGLAS.md del repositorio Docencia.
Tema (del cronograma): <tema>
Temas que ya vieron: <semanas anteriores>
Caso práctico para el taller: <opcional, ej. factura de un plan móvil>
Entregables: plan de clase (Word), presentación en Canva copiada de la plantilla,
práctica en notebook, preguntas.md, y subir todo a programacion-ii/semana-XX.
Empieza por el plan de clase y muéstramelo antes de seguir.
```
