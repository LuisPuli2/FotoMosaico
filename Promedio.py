# coding=utf-8
from PIL import Image
import os

# Explicar por que no tube elecsion
# Variables globales.
# La base da datos donde se guardarán los promedios de cada imagen.
BD = "BD.txt"
f = None

# Obtiene el promedio general de (R,G,B) de toda la imagen.
def getPromedioRGB(img):
	# Los futuros promedios
	r_prom = 0
	g_prom = 0
	b_prom = 0
	total = 0
	# Accedemos a la matriz de pixeles de ambas imagenes.
	pixeles = None
	try:
		pixeles = img.load()
	except Exception as e:
		return None
	# Iteramos sobre cada pixel y comparamos.
	try:
		for i in range(0,img.size[0]):
			for j in range(0,img.size[1]):
				r,g,b = pixeles[i,j]
				r_prom += r
				g_prom += g
				b_prom += b
				total += 1
	except Exception as e:
		return None
	
	# Lo divimos para que sea el promedio
	r_prom = r_prom//total
	g_prom = g_prom//total
	b_prom = b_prom//total

	# Lo regresamos en forma de cadena
	return str(r_prom) + ","+ str(g_prom) + ","+ str(b_prom)

# Itera sobre la carpeta con imágenes para obtener su color promedio.
def getPromedios (directorio):
	global BD,f
	# Una ""Base de Datos"" para guardar el nombre de la imagen y su color promedio en RGB.
	for filename in os.listdir(directorio):
		if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".png") or filename.endswith(".jpeg"):
			im = None
			try:
				im = Image.open(directorio + "/" + filename)
			except Exception as e:
				continue
			
			prom = getPromedioRGB(im) 
			if prom:	
				f.write(directorio+"/"+filename + "," + prom  + "\n")
		elif os.path.isdir(directorio+"/"+filename):
			print("Directorio acutal: " + filename)
			getPromedios(directorio+"/"+filename)

# Dada una carpeta raíz, saca el promedio de todas las imágenes contenidas en él.
def main():
	print("Comienza...")
	global f
	# Abrimos el archivo.
	f = open(BD,"w+")
	directory = raw_input("Dame la ruta del directorio raiz \n")
	getPromedios(directory)
	f.close()

if __name__ == '__main__':
	main()
