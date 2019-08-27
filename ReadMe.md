# **Foto Mosaico: Proyecto Final para Proceso Digital de Imágenes.**

## Primero que nada, ¿qué es un foto mosaico? 

Un foto mosaico es una imagen generada a partir de imágenes más pequeñas colocadas en forma de mosaico. 

![alt text](https://github.com/LuisPuli2/FotoMosaico/blob/master/sample/noche.jpg-m-mosaicoo.jpg "GG")

## ¿Cómo hacer un foto mosaico?

La elaboración de un foto mosaico requiere tener una colección de imágenes (mientras más grandes y variadas mejor) para formar la imagen de nuestro interés. La creación de la imagen se divide en dos pasos esenciales: 

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

**El árbol de búsqueda de rangos** es una estructura de datos que se construye a partir de puntos en el espacio y es utilizada para hacer queries de la forma **[x:x'] *x* [y,y'] *x* [z,z'] *x* ...**  y el árbol regresaŕa todos los puntos que están dentro de esos límites con un tiempo de respuesta de ***O(log²(n) + k)*** donde ***n*** es el número total de puntos y ***k*** el número de puntos reportados dentro de ese rango.

### ¿Cómo funciona?

Una busqueda de rangos en **2** dimensiones es esencialmente **2** sub búsquedas en una dimensión, uno sobre la coordenada ***x*** y otro sobre la coordenada ***y***. Esto da la idea de dividir el conjunto de puntos ***x*** alternativamente sobre el eje ***x*** y el eje ***y***. 

Sea ***P*** el conjunto de ***n*** puntos en el plano que queremos preprocesar para nuestra búsqueda rectangular. Sea **[x:x'] x [y:y']** el query de búsqueda. Lo que haremos es, primero enfocarnos en los puntos cuya coordenada ***x*** esté en **[x:x']**. Si solo nos fijamos en la coordenada ***x***, eso es una búsqueda en una dimensión y eso lo sabemos resolver: Árbol binario de búsqueda de los ***n*** puntos ordenado respecto a su coordenada ***x***. Con esto en mente, el algoritmo para resolver nuestros queries es de la siguiente forma. Buscamos con ***x*** y ***x'*** en el árbol hasta que obtengamos el nodo ***V split*** donde la ruta de búsqueda se divide. Desde el hijo izquierdo de ***V split*** buscamos con ***x***, ***y*** para cada nodo ***v*** donde la ruta de la búsqueda de ***x*** va a la izquierda, reportamos todos los puntos en el subárbol derecho. De manera similar, desde el hijo izquerdo de ***V split*** buscamos con ***x'***, y para cada nodo ***v*** donde la ruta de la búsqueda de ***x'*** va a la derecha, reportamos todos los puntos que viven en el subárbol izquierdo de ***v***. Cuando llegamos a las hojas ***M*** y ***M'*** donde las dos rutas terminan para ver si ellas un punto en el rango. En efecto, seleccionamos una colección de ***O(log n)*** subárboles, qué, juntos contienen exactamente todos los puntos cuya coordenada ***x*** está en ***[x:x']***.

![alt text](https://github.com/LuisPuli2/FotoMosaico/blob/master/sample/RangeTree-2.png "GGGG")

Vamos a llamar a ese subconjunto de puntos almacenados en las hojas de el subárbol con ***v*** como raíz el Subconjunto canónico de ***v***. Por ejemplo, el  subconjunto canónico de la raíz del árbol es todo el conjunto ***P***. El subconjunto canónico de una hoja es simplemente el punto almacenado en la hoja. Denotaremos el subconjunto canónico de ***v*** como ***P(v)***. Hasta ahora, hemos visto que el subconjunto de puntos que viven dentro del rango ***[x:x']*** puede ser expresado como la unión disjunta de ***O(log n)*** subconjuntos canónicos; Esos son el conjunto ***P(v)*** de los nodos ***v*** que son la raíz de los subárboles seleccionados. Sin embargo, no estamos interesados en todos los puntos de ese subconjunto, nos interesan los puntos que viven en ***P(v)*** y que además su coordenada ***y*** vive en ***[y:y']***. Esto involucra otra búsqueda en una dimensión, pero solo sobre el subconjunto canónico ***P(v)***. Esto nos deja la siguiente estructura para queries de rangos rectangulares en un conjunto ***P*** de ***n*** puntos en el plano:
* El árbol principal es un árbol binario de búsqueda balanceado ***T*** ordenado respecto a la coordenada de ***x*** de los puntos de ***P***.
* Para cada nodo ***v*** del árbol ***T***, el subconjunto canónico ***P(v)*** es almacenado en un árbol binario de búsqueda balanceado ***Tassoc(v)*** ordenado sobre la coordenada ***y*** de los puntos de ***P(v)***. El nodo ***v*** almacena un apuntador a la raíz de ***Tassoc(v)***, y lo llamaremos estructura asociada de ***v***.

La estructura queda de la siguiente forma:

![alt text](https://github.com/LuisPuli2/FotoMosaico/blob/master/sample/RangeTree.png "GGG")

El query para buscar todos los puntos que viven dentro ***[x:x']x[y:y']*** se realiza primero buscando en el árbol principal y obtener el subconjunto canónico ***P(v)*** donde todos los puntos que están en ***P(v)*** viven en ***[x:x']***. Después en el árbol asociado a ***v***, buscamos todos los puntos que viven en ***[y:y']*** y esos puntos serán los que viven en ***[x:x']x[y:y']***.

El árbol de rangos puede ser adaptado para ***n*** dimensiones. En nuestro caso, fue para 3.

## Ejecución del Programa. 

Para ejecutar el programa, primero hay que especificarle la carpeta raíz que contiene las imágenes para calcular el promedio de cada una de ellas y llenar la "base de datos". Para ello, hay que ejecutar el script Promedio.py. Ya que son alrededor de 60,000 imágenes tomará algo de tiempo.

Ya con la base de datos generada, hay que ejecutar el script Main.py, tardará un poco en abrir la interfaz por qué primero construirá el árbol de rangos. Ya abierta la interfaz, lo demás, es historia.
