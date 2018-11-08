from PIL import ImageTk, Image

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