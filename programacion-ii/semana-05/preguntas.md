# Semana 5 — Preguntas para los estudiantes

Programación II · Funciones

## Repaso

1. ¿Qué diferencia hay entre un **parámetro** y un **argumento**?
2. ¿Por qué en análisis de datos casi siempre conviene que una función **devuelva** (`return`) en vez de **imprimir** (`print`)?
3. ¿Qué devuelve una función que no tiene ninguna línea `return`?
4. Explica con tus palabras por qué una variable creada dentro de una función no existe fuera de ella.

## Predice la salida (sin ejecutar)

5. ```python
   def f(a, b=2):
       return a ** b

   print(f(3), f(2, 3), f(b=1, a=5))
   ```
6. ```python
   def g(x):
       print(x * 2)

   r = g(4)
   print(r)
   ```
7. ```python
   def promedio(notas):
       if not notas:
           return 0
       return sum(notas) / len(notas)

   print(promedio([80, 90, 100]), promedio([]))
   ```
8. ¿Qué error lanza este código y por qué?
   ```python
   contador = 0

   def sumar():
       contador += 1

   sumar()
   ```

## Discusión (foro "No te repitas")

9. Busca en una práctica tuya de semanas anteriores un bloque de código que se repite. Muéstralo, conviértelo en una función y explica qué ganaste (líneas, claridad, facilidad para cambiar una tarifa o un porcentaje).

## Reto

10. Escribe una función `clasificar_cliente(meses, gasto_mensual)` que devuelva `"Nuevo"` si tiene menos de 6 meses, `"VIP"` si tiene 6 meses o más y gasta más de RD$3,000, y `"Regular"` en cualquier otro caso. Pruébala con `assert` usando al menos tres clientes distintos.
