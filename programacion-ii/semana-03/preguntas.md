# Semana 3 — Preguntas para los estudiantes

Programación II · Estructuras de control

## Repaso

1. ¿Cuál es la diferencia entre `=` y `==`? Da un ejemplo de cada uno.
2. ¿Cuándo conviene usar `while` y cuándo `for`? Da un ejemplo de cada caso.
3. ¿Qué diferencia hay entre `break` y `continue`?
4. ¿Por qué es mejor escribir `except ValueError:` que un `except:` solo?

## Predice la salida (sin ejecutar)

5. ```python
   for i in range(10, 0, -3):
       print(i, end=" ")
   ```
6. ```python
   total = 0
   n = 0
   while total < 15:
       n += 1
       total += n
   print(n, total)
   ```
7. ```python
   for c in "datos":
       if c in "aeiou":
           continue
       print(c, end="")
   ```
8. ```python
   try:
       r = 10 / int("0")
   except ValueError:
       print("V")
   except ZeroDivisionError:
       print("Z")
   ```

## Discusión (foro)

9. En el notebook de clase, el programa que valida el número falla si el usuario se equivoca **dos veces**. ¿Por qué pasa eso y cómo lo arreglarías con un `while`?

## Reto

10. Escribe un programa que pida notas una por una hasta que el usuario escriba `fin`. Si escribe algo que no es número, avísale y vuelve a pedir. Al final muestra cuántas notas se registraron, el promedio y la nota más alta.
