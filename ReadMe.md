# **Foto Mosaico: Proyecto Final para Proceso Digital de Imágenes.**

## Primero que nada, ¿Qué es un foto mosaico? 

Un foto mosaico es una imagen generada a partir de imágenes más pequeñas colocadas en forma de mosaico. 

![](https://github.com/LuisPuli2/FotoMosaico/tree/master/sample/noche.jpg-m-mosaicoo.jpg)

## ¿Cómo hacer un foto mosaico?

La elaboración de un foto mosaico requiere tener una colección de imágenes (mientras más grandes y variadas mejor) para formar la imagen de nuestro interes. La creación de la imagen se divide en dos pasos esenciales: 

* Obtener el mosaico de la foto, con regiones cuadradas de su color promedio.
* Para cada región cuadrada del mosaico, buscar la imagen cuyo color promedio sea el más cercano al color del mosaico. 

## Complejidad

La idea para generar los fotomosaicos es bastante intuitiva, sin embargo cuando se tiene factores como:

* Imagen de gran tamaño.
* Gran número de imágenes para buscar al momento de colocar un mosaico.
* Mosaicos muy pequeños. (Hay que colocar más)
* Una combinación de las tres anteriores.

El procesamiento del foto mosaico se puede tornar muy lento. Y, debido a que buscar la imagen cuyo color promedio se "acerque" más al color que estamos buscando es la operación principal, si logramos que la búsqueda sea mucho más eficiente, mejoraŕa mucho el procesamiento de la imagen.

Centrandonos en el problema de buscar las imágenes, ¿Qué quiere decir que un color de "acerque" a otro?. Básicamente se trata de que sus componentes R,G y B sean muy parecidos, en otras palabras, si vemos sus componente R,G y B como *tuplas* *(R,G,B)*, dos colores son *"cercanos"* si los valores de cada entrada no son tan diferentes. Por ejemplo si tenemos un color **c1 = (129,45,67)** y un color **c2 = (135,44,70)** a pesar de que no son el mismo, podemos decir que son colores cercanos. 

 Ahora bien, las tuplas las podemos ver como puntos en el espacio y ya que estamos trabajando con tuplas de tamaño tres, veremos su componente (R,G,B) como puntos en 3 dimensiones.

Así, ya más formalmente, diremos que un color es cercano a otro si la distancia (euclideana) entre los dos puntos correspondientes a su *RGB* es *pequeña*. Entonces, dado el color de un mosaico, encontrar la imagen cuyo color promedio sea el más parecido a él, se resume a encontrar la imagen o imágenes cuya distancia entre su color promedio y el color dado sea mínima entre todas las demás distancias.

Si para cada mosaico buscamos la imagen o imágenes más cercanas a ese color una por una, es decir, linelamente la complejidad de buscar la imagen para cada mosaico será: ***(nxm)xs***

Dónde ***n*** y ***m*** son las dimensiones de la imagen e ***i*** es el número de imágenes de nuestra colección.  Lo cuál es bastante costoso.

Ahora bien, como ya sabemos, cuando de encontrar un elemento de manera eficiente se trata, lo primero que se nos viene a la mente es ordenar los elementos respecto a algún valor que posean y depués, aplicar una búsqueda binaria. También sabemos que esto es equivalente a buscar el elemento en un árbol binario ordenado bien balanceado. Pero en  nuestro caso, ¿cómo buscamos de manera eficiente una tupla de la forma (R,G,B)?, ¿Cómo podemos darle un orden a las tuplas?.  Afortunadamente existe una estructura de datos que nos puede ayudarnos con este problema: ***El árbol de rangos de búsqueda*** (Range Search Tree)

## Árbol de Rangos de Búsqueda

**El árbol de búsqueda de rangos** es una estructura de datos que se construye a partir de puntos en el espacio y es utilizada para hacer queries de la forma **[x:x'] *x* [y,y'] *x* [z,z'] *x* ...**  y el árbol regresaŕa todos los puntos que están dentro de esos límites con un tiempo de respuesta de ***O(log²(n) + k)*** donde n es el número total de puntos y k el número de puntos reportados dentro de ese rango.

### ¿Cómo funciona?

pass




## Ejecución del Programa. 

Para ejecutar el programa, primero hay que especificarle la carpeta raíz que contiene las imágenes para calcular el promedio de cada una de ellas y llenar la "base de datos". Para ello, hay que ejecutar el script Promedio.py. Ya que son alrededor de 60,000 imágenes tomará algo de tiempo.

Ya con la base de datos generada, hay que ejecutar el script Main.py, tardará un poco en abrir la interfaz por qué primero construirá el árbol de rangos. Ya abierta la interfaz, lo demás es historia.


**Love of mi life... 
Bring it back, bring it back, don't take it away from me because you don't know what it means to me. (Lis <3)**