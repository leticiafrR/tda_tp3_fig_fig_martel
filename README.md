# tp3
Primera entrega TP3
## Integrantes
  - Josue Martel: 110696
  - Andrea Figueroa: 110450
  - Leticia Figueroa: 110510
## Instrucciones de ejecución
### Programa
Para ejecutar el programa con un archivo de entrada (por ejemplo) datos.txt, ejecutar el siguiente comando en la terminal según el algoritmo preferido:

```python3 lp.py datos.txt```
```python3 greedy.py datos.txt```
```python3 bt.py datos.txt```
```python3 greedy_bt.py datos.txt```

Para un funcionamiento válido, el archivo datos.txt deberá tener el formato:<br>

\# Contexto (No obligatorio)<br>
3<br>
Sangok, 178<br>
Wei, 121<br>
Siku, 135<br>
Eska, 168<br>
Amon, 65<br>
La, 37<br>
Yue, 94<br>
Pakku, 91<br>
Sura, 159<br>
Tonraq, 27<br>

Omitiendo el contexto, La primera linea indica la cantidad de grupos a formar, las siguientes n lineas son de la forma 'nombre maestro, habilidad':

### Generador de datos
Para generar un set de datos con archivo de salida, cantidad de maestros y grupos específica, ejecutar el siguiente comando en la terminal:

```python3 data_generator.py archivo_salida.txt cant_maestros cant_grupos (opcional)b=cte```

Si el campo b tiene valor asignado, entonces ese valor será constante para todo el set de datos, caso contrario se generará un valor pseudoaleatorio para cada elemento.

Entonces, por ejemplo, si se desea generar un set de datos con un archivo de salida datos_10_4.txt, 10 maestros y 4, entonces ejecutar el siguiente comando:

```python3 data_generator.py datos_10_4.txt 10 4```

Contenido final en datos_10_4.txt:<br>

\# La primera linea indica la cantidad de grupos a formar, las siguientes son de la forma 'nombre maestro, habilidad'<br>
4<br>
Amon, 352<br>
Rafa, 520<br>
Yakone, 290<br>
Sura, 347<br>
Katara, 833<br>
Sangok, 547<br>
Rafa', 142<br>
Desna, 711<br>
Katara', 325<br>
Wei, 916<br>
