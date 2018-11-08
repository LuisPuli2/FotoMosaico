# coding=utf-8
from PIL import Image

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
	
	return (r_prom,g_prom,b_prom)
			