# coding=utf-8
from PIL import Image
import os

# Variables globales.
directorio = "birds"
BD = "BD.txt"
images = {}


# Obtiene el promedio general de (R,G,B) de toda la imagen.
def getPromedioRGB(img):
	# Los futuros promedios
	r_prom = 0
	g_prom = 0
	b_prom = 0
	total = 0
	# Accedemos a la matriz de pixeles de ambas imagenes.
	pixeles = img.load()
	# Iteramos sobre cada pixel y comparamos.
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			r,g,b = pixeles[i,j]
			r_prom += r
			g_prom += g
			b_prom += b
			total += 1
	# Lo divimos para que sea el promedio
	r_prom = r_prom//total
	g_prom = g_prom//total
	b_prom = b_prom//total

	# Lo regresamos en forma de cadena
	return str(r_prom) + ","+ str(g_prom) + ","+ str(b_prom)

# Dada una BD llena un diccionario con el nombre de la imagen como llave, y su tupla RGB como valor
def llenaHash ():
	global BD
	global images
	file = open(BD,"r")
	for line in file.readlines():
		line = line.replace("\n", "")
		# Lo separamos por comas
		arr = line.split(",")
		nombre = arr[0]
		R = int(arr[1]) 
		G = int(arr[2]) 
		B = int(arr[3]) 
		RGB = (R,G,B)
		# Lo metemos al diccionario
		images[nombre] = RGB
	file.close()


# Itera sobre la carpeta con imágenes para obtener su color promedio.
def getPromedios ():
	global BD,directorio
	# Una ""Base de Datos"" para guardar el nombre de la imagen y su color promedio en RGB.
	f = open(BD,"w+")
	for filename in os.listdir(directorio):
	    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
	    	im = Image.open(directorio + "/" + filename)
	    	prom = getPromedioRGB(im) 	
	    	f.write(filename + "," + prom  + "\n")
	f.close()

# Regresa la imagen cuyo color promedio es el más cercano a uno dado.
def getClosestColor (r,g,b):
	min_distance = -1;
	min_key = ''
	for key in images:
		color = images[key]
		# Distancia euclideana.
		distancia = (((color[0] - r)**2) + ((color[1] - g)**2) + ((color[2] - b)**2))**(.5)
		if min_distance == -1:
			min_distance = distancia
			min_key = key
		elif distancia < min_distance:
			min_distance = distancia
			min_key = key

	return min_key

def filtroMosaico(imagen,mosaicoX,mosaicoY):
    recorreX = 0
    recorreY = 0
    rprom = 0
    gprom = 0
    bprom = 0
    prom = 0
    ancho = imagen.size[0]
    alto = imagen.size[1]
    rgb = imagen.convert('RGB')
    pixels = imagen.load()
    # Para ajustar el tamaño de la imagen.
    tam = 6
    new_im = Image.new('RGB', (ancho*tam, alto*tam))
    for i in range(0,ancho,mosaicoX):
        recorreX = i + mosaicoX
        for j in range(0,alto,mosaicoY):
            recorreY = j + mosaicoY
            for k in range(i,recorreX):
                if (k >= ancho):
                    break
                for l in range(j,recorreY):
                    if (l >= alto):
                        break
                    r,g,b = rgb.getpixel((k,l))
                    rprom += r
                    gprom += g
                    bprom += b
                    prom += 1
            promRojo = (rprom/prom)
            promVerde = (gprom/prom)
            promAzul = (bprom/prom)
            # Reseteamos.
            rprom = 0
            gprom = 0
            bprom = 0
            prom = 0
            # Desmadres del Duis
            key = getClosestColor(promRojo,promVerde,promAzul)
            img = Image.open(directorio+"/"+key)
            img = img.resize((mosaicoX*tam,mosaicoY*tam))
            new_im.paste(img, (i*tam,j*tam))
            # Fin de desmadres del Duis

    new_im.show()
    new_im.save("PerroMosaico.jpg")
       
    return new_im


if __name__ == '__main__':
	getPromedios()
	llenaHash()
	img = Image.open ("prro.jpeg")
	# creaMosaico(img)
	filtroMosaico(img,5,5)
	# new_im.save('test.jpg')
	# Termina mi desvergue
	# print(images)

			