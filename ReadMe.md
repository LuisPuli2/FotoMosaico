# Foto Mosaico: Proyecto Final para Proceso Digital de Imágenes.

## Para generar un foto mosaico de una imagen, la idea es la siguiente:
###*Obtener el mosaico de la foto
###*Para cada región cuadrada del mosaico, buscar la imagen cuyo color promedio sea cercano al color del mosaico.   

## Optimizaciones:

La idea para generar los fotomosaicos es bastante intuitiva, sin embargo cuando se tiene factores como:

* Imagen de gran tamaño.
* Gran número de imágenes para buscar al momento de colocar un mosaico.
* Mosaicos muy pequeños.
* Una combinación de las tres anteriores.

El procesamiento del foto mosaico se puede tornar muy lento. Y, debido a que buscar la imagen que más se acerque al color que estamos buscando es la operación principal, si logramos que la búsqueda sea mucho más rápida, mejoraŕa mucho el procesamiento de la imagen.

Sabemos que dado un color, 

Cómo ya sabemos, cuando de buscar un elemento se trata, lo primero que se nos viene a la mente es ordenar los elementos y aplicar una búsqueda binaria, qué es equivalente a buscar en un árbol binario ordenado bien balanceado. Pero, ¿Cómo buscamos una 



### Una estructura de datos para realizar queries de búsqueda de la forma:
###	[x:x']**x**[y:y']**x**[z:z']**x**... 
### Con un tiempo de respuesta de O(log²(n) + k), donde k es el número de puntos que está dentro de ese rango. Para este caso utilizaremos tres dimensiones.


#### Para ejecutar el programa, primero hay que especificarle la carpeta raíz que contiene las imágenes para calcular el promedio de cada una de ellas y llenar la "base de datos". Para ello, hay que ejecutar el script Promedio.py. Ya que son alrededor de 60,000 imágenes tomará algo de tiempo.

### Ya con la base de datos generada, hay que ejecutar el script Main.py, tardará un poco en abrir la interfaz por qué primero construirá el árbol de rangos. Ya abierta la interfaz, lo demás es historia.


**Love of mi life... 
Bring it back, bring it back, don't take it away from me because you don't know what it means to me. (L)**