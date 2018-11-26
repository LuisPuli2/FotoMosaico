# coding=utf-8
from PIL import ImageTk, Image
import os

def filtroMosaico(imagen,aplica,mosaicoX,mosaicoY):
    recorreX = 0
    recorreY = 0
    rprom = 0
    gprom = 0
    bprom = 0
    prom = 0
    ancho = imagen.size[0]
    alto = imagen.size[1]
    rgb = imagen.convert('RGB')
    pixels = aplica.load()
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
            for k in range(i,recorreX):
                if (k >= ancho):
                    break
                for l in range(j,recorreY):
                    if (l >= alto):
                        break
                    pixels[k,l] = (promRojo,promVerde,promAzul)
       
    return aplica

# Filtro Gris.
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

# Pasa las imágenes que encuntra a tonos de grises.
def getPromedios(directorio='img'):
    # Una ""Base de Datos"" para guardar el nombre de la imagen y su color promedio en RGB.
    for filename in os.listdir(directorio):
        if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".png") or filename.endswith(".jpeg"):
            im = None
            try:
                im = Image.open(directorio + "/" + filename)
                # Las pasamos a tonos de grises.
                filtroGris(im)
                # La guardamos.
                im.save("img-gray/"+filename)
            except Exception as e:
                continue
            
            prom = getPromedioRGB(im) 
            if prom:    
                f.write("img-gray/"+filename + "," + prom  + "\n")
        elif os.path.isdir(directorio+"/"+filename):
            print("Directorio actual: " + filename)
            getPromedios(directorio+"/"+filename)

if __name__ == '__main__':
    print("Empieza: ")
    f = open("BD.txt","a")
    getPromedios()
    f.close()