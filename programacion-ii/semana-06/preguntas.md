# Semana 6 — Preguntas para los estudiantes

Programación II · Limpieza y transformación de datos

## Repaso

1. ¿Por qué hay que diagnosticar un dataset antes de limpiarlo? Menciona tres funciones de pandas que usarías para hacerlo.
2. ¿Cuándo conviene **eliminar** una fila con nulos y cuándo **imputar** el valor? Da un ejemplo de cada caso con el dataset de clientes.
3. ¿Por qué se suele imputar con la **mediana** y no con el promedio?
4. ¿Por qué hay que quitar los duplicados **antes** de calcular la mediana para imputar?

## Predice la salida (sin ejecutar)

5. ```python
   s = pd.Series([" La Vega", "la vega", "LA VEGA "])
   print(s.str.strip().str.title().nunique())
   ```
6. ```python
   df = pd.DataFrame({"gb": [4.0, None, 12.0, 30.0]})
   print(df["gb"].fillna(df["gb"].median()).tolist())
   ```
7. ```python
   m = pd.Series(["RD$1,200.50", "RD$950.00"])
   print(m.str.replace("RD$", "", regex=False)
          .str.replace(",", "", regex=False)
          .astype(float).sum())
   ```
8. ```python
   x = pd.Series([500, 1800, 3200])
   print(pd.cut(x, bins=[0, 1500, 2500, 10000],
                labels=["Bajo", "Medio", "Alto"]).tolist())
   ```

## Discusión (foro)

9. Describe un caso real en el que los datos venían sucios (en tu trabajo, la universidad o un negocio). ¿Qué problema tenían, qué decisión de limpieza tomarías y cómo se podría **prevenir** desde la captura?

## Reto

10. Con el dataset de clientes, crea la variable `riesgo_fuga` con el valor `"Alto"` cuando el cliente tiene menos de 6 meses **y** su factura es mayor que la mediana, y `"Bajo"` en cualquier otro caso. ¿Cuántos clientes quedan en riesgo alto? Explica en una oración por qué esa combinación podría indicar riesgo.
