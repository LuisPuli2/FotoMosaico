# coding=utf-8
from PIL import Image


# Aplica un filtro rojo equis.
def filtroRojo(img,tono):
	# Accedemos a la matriz de pixeles de ambas imagenes.
	pixeles = img.load()
	# Iteramos sobre cada pixel y comparamos.
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			r,g,b = pixeles[i,j]
			newRojo = int(tono) + r
			if newRojo > 255:
				newRojo = 255
			elif newRojo < 0:
				newRojo = 0
			pixeles[i,j] = (newRojo,0,0)

def filtroGris(img):
	# Accedemos a la matriz de pixeles de ambas imagenes.
	pixeles = img.load()
	# Iteramos sobre cada pixel y comparamos.
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			r,g,b = pixeles[i,j]
			gris = int(r/3)
			gris = r
			if gris != 255:
				gris -= 45
			if gris < 0:
				gris = 0
			pixeles[i,j] = (gris,gris,gris)

def quitaMarcaAgua (img):
	try:
		# Trata de abrir las imagenes.
		tono = 40
		filtroRojo(img,tono)
		filtroGris(img)
		return img
	# Si se genera una excepcion, la cachamos.
	except:
		print("No pude abrir las imagenes, revisa los nombres.")

def cifra(img,texto):
	texto_binario = ""
	# Iteramos el texto
	for char in texto:
		# Valor ASCII
		asci = ord(char)
		# A binario
		binario = "{0:b}".format(asci);
		binario = completaCeros(binario);
		texto_binario += binario 
	# Lo pegamos en la imagen.
	aux = completaCeros("{0:b}".format(128))
	aux = completaCeros("{0:b}".format(178))
	texto_binario += aux
	# Accedemos a la matriz de pixeles de ambas imagenes.
	pixeles = img.load()
	cont = 0
	cont_aux = 0
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			r,g,b = pixeles[i,j]
			# Asignamos el rojo
			if cont < len(texto_binario):
				r = cambiaBit(r,texto_binario[cont])
			else:
				break
			cont += 1
			# Asignamos el verde
			if cont < len(texto_binario):
				g = cambiaBit(g,texto_binario[cont])
			else:
				break
			cont += 1
			# Asignamos el azul
			if cont < len(texto_binario):
				b = cambiaBit(b,texto_binario[cont])
			else:
				break
			cont += 1
			pixeles[i,j] = (r,g,b)
	print("Proceso Terminado")
	return img


def decifra(img):
	texto = ""
	cont = 0
	actual = ''
	pixeles = img.load()
	romper = False
	for i in range(0,img.size[0]):
		if romper:
			break
		for j in range(0,img.size[1]):
			r,g,b = pixeles[i,j]
			if cont%8 == 0 and cont != 0:
				actual = int(actual,2)
				if actual == 128 or actual == 178:
					romper = True
					break
				texto += unichr(actual)
				actual = ''
			actual += getBit(r)
			cont += 1
			if cont%8 == 0:
				actual = int(actual,2)
				if actual == 128 or actual == 178:
					romper = True
					break
				texto += unichr(actual)
				actual = ''
			actual += getBit(g)
			cont += 1
			if cont%8 == 0:
				actual = int(actual,2)
				if actual == 128 or actual == 178:
					romper = True
					break
				texto += unichr(actual)
				actual = ''
			actual += getBit(b)
			cont += 1

	return img,texto

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
            rprom = 0
            gprom = 0
            bprom = 0
            prom = 0
            # Desmadres del Duis
            new_r,new_g,new_b = getClosestColor(promRojo,promVerde,promAzul)
            # Fin de desmadres del Duis
            for k in range(i,recorreX):
                if (k >= ancho):
                    break
                for l in range(j,recorreY):
                    if (l >= alto):
                        break
                    pixels[k,l] = (new_r,new_g,new_b)
       
    return imagen

# Regresa el color más cercano a uno dado.
def getClosestColor (r,g,b):
	min_distance = -1;
	colors = getColors()
	for color in colors:
		# Distancia euclideana.
		distancia = (((color[0] - r)**2) + ((color[1] - g)**2) + ((color[2] - b)**2))**(.5)
		# distancia = int(distancia)
		if min_distance == -1:
			min_distance = distancia
			new_r = color[0]
			new_g = color[1]
			new_b = color[2] 
		elif distancia < min_distance:
			min_distance = distancia
			new_r = color[0]
			new_g = color[1]
			new_b = color[2] 
	return (new_r,new_g,new_b)

# Funciones auxiliares.
def getColors ():
	verde 	= (0,155,72)
	rojo 	= (185,0,0)
	azul 	= (0,69,173)
	naranja = (255,89,0)
	blanco 	= (255,255,255)
	amarillo= (255,213,0)

	return [verde,rojo,azul,naranja,blanco,amarillo]

def getBit(num):
	# Lo pasamos a binario.
	binario = "{0:b}".format(num)
	return binario[len(binario)-1]

def cambiaBit(num,bit):
	# Lo pasamos a binario.
	binario = "{0:b}".format(num)
	# Rellenamos con ceros
	binario = completaCeros(binario)
	# Quitamos el ultimo bit
	binario = binario[:-1]
	# Le poenmos el nuestro
	binario = binario+bit
	# Lo regresamos a decimal.
	num = int(binario, 2)
	return num

# Rellenamos con ceros
def completaCeros(binario):
	if len(binario) == 8:
		return binario
	extra = ''
	for i in range (8-len(binario)):
		extra += '0'
	return extra+binario


	