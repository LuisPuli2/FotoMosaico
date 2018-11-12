import tkFileDialog
import types
from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
import os
from Imagen import *
from Agua import cifra
from Agua import decifra
from Agua import filtroMosaico
from Mosaico import getPromedioRGB


# La interfaz principal.
class Interfaz(Frame):

    global imagenes1
    
    # Constructor.
    def __init__(self, padre):
        Frame.__init__(self,padre)
        self.pack(fill=BOTH, expand=True)
        self.img = None
        self.cambia = None
        self.creaCanvas()
        self.creaMenu()

    def creaMenu(self):

        self.barra_Menu = Menu(self)
        
        self.abrir_Menu_Archivo = Menu(self.barra_Menu, tearoff=0)
        self.abrir_Menu_Archivo.add_command(label="Abrir", command=self.escogerImagen)
        self.abrir_Menu_Archivo.add_command(label="Guardar", command=self.preguntaGuardar)
        
        self.barra_Menu.add_cascade(label="Imagen", menu=self.abrir_Menu_Archivo)

        self.comboboxFiltro = Menu(self.barra_Menu, tearoff=0)
        self.comboboxFiltro.add_command(label="Cifrar imagen", command=  self.procesa)
        self.comboboxFiltro.add_command(label="Decifrar imagen", command= lambda: self.decifra())
        self.comboboxFiltro.add_command(label="Mosaico con Cubo Rubik", command= lambda: self.aplicaRubik())
        self.comboboxFiltro.add_command(label="Foto Mosaico", command= lambda: self.aplicaMosaico())

        self.barra_Menu.add_cascade(label="Filtros", menu=self.comboboxFiltro)
        self.barra_Menu.add_command(label="Salir", command = self.salir)
        
        root.config(menu=self.barra_Menu)


    def creaCanvas(self):

        self.nuevaVentana = Canvas(self, bg="white",width=500,height=400)
        self.nuevaVentana.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.FiltroImagen = Canvas(self,bg ="white",width=500,height=400 )
        self.FiltroImagen.pack(side=RIGHT, fill=BOTH, expand=True)


    def salir(self):
        os._exit(0)
        

    def preguntaGuardar(self):
        if self.FiltroImagen.find_all() != ():
            self.tope = Toplevel()

            self.escrito = Label (self.tope, text= "Puedes guardar la imagen en formato jpg o png")
            self.escrito.pack()

            self.buttontext = StringVar()
            self.buttontext.set("Guardar")
            self.button = Button(self.tope, textvariable=self.buttontext, command= self.guardarImagen).pack()
        else:
            tkMessageBox.showwarning("Error","No hay imagen")

    def guardarImagen(self):
        self.nuevaImagen.save(tkFileDialog.asksaveasfilename())
        self.tope.destroy()

    def escogerImagen(self):
        
        ruta = tkFileDialog.askopenfilename()
        imagenes1 = Imagen(ruta)
        self.img = imagenes1.getImagen()
        self.cambia = imagenes1.getAplica()
        
        imageFile = ImageTk.PhotoImage(self.img)
        imagenCambia = ImageTk.PhotoImage(self.cambia)

        self.nuevaVentana.imagenes1 = imageFile
        self.nuevaVentana.create_image(imageFile.width()/2, imageFile.height()/2, anchor=CENTER, image=imageFile, tags="bg_img")

        self.FiltroImagen.imagenes1 = imagenCambia
        self.FiltroImagen.create_image(imagenCambia.width()/2, imagenCambia.height()/2, anchor=CENTER, image=imagenCambia, tags="bg_img")

        self.nuevaVentana.create_text((250,380),text="Imagen original")

    #Procesa los calores para cifrar
    def procesa(self):
        if self.FiltroImagen.find_all() != ():
            self.tope = Toplevel()

            self.escrito = Label (self.tope, text= "Introduce el texto que quieres cifrar. Recuerda que tienes que guardar la imagen",width=80)
            self.escrito.pack()

            self.entrytext = StringVar()
            Entry(self.tope, textvariable=self.entrytext, width=60).pack()

            self.buttontext = StringVar()
            self.buttontext.set("Aplicar ")
            self.button = Button(self.tope, textvariable=self.buttontext, command= lambda: self.cifra(self.entrytext)).pack()
        else:
            tkMessageBox.showwarning("Error","Escoge una imagen antes de aplicar un filtro")

    # Para cubo Rubik
    def aplicaRubik (self):
        if self.FiltroImagen.find_all() != ():
            self.nuevaImagen = filtroMosaico(self.img,1,1)
            imagenCambia = ImageTk.PhotoImage(self.nuevaImagen)
            self.FiltroImagen.imagenes1 = imagenCambia
            self.FiltroImagen.create_image(imagenCambia.width()/2, imagenCambia.height()/2, anchor=CENTER, image=imagenCambia, tags="bg_img")   
        else:
            tkMessageBox.showwarning("Error","Elige una imagen antes de aplicar un filtro")

    # Para foto mosaico
    def aplicaMosaico(self):
        if self.FiltroImagen.find_all() != ():
            self.nuevaImagen = getPromedioRGB(self.img)
            imagenCambia = ImageTk.PhotoImage(self.nuevaImagen)
            self.FiltroImagen.imagenes1 = imagenCambia
            self.FiltroImagen.create_image(imagenCambia.width()/2, imagenCambia.height()/2, anchor=CENTER, image=imagenCambia, tags="bg_img")   
        else:
            tkMessageBox.showwarning("Error","Elige una imagen antes de aplicar un filtro")
            
    # Cifrar imagen.
    def cifra(self,valor):
        self.entrytext = valor.get()

        self.nuevaImagen = cifra(self.img,self.entrytext)
        imagenCambia = ImageTk.PhotoImage(self.nuevaImagen)
        self.FiltroImagen.imagenes1 = imagenCambia
        self.FiltroImagen.create_image(imagenCambia.width()/2, imagenCambia.height()/2, anchor=CENTER, image=imagenCambia, tags="bg_img")
        self.tope.destroy()

    # Decifrar imagen.
    def decifra(self):

        if self.FiltroImagen.find_all() != ():
            self.nuevaImagen,texto = decifra(self.img)
            imagenCambia = ImageTk.PhotoImage(self.nuevaImagen)
            self.FiltroImagen.imagenes1 = imagenCambia
            self.FiltroImagen.create_image(imagenCambia.width()/2, imagenCambia.height()/2, anchor=CENTER, image=imagenCambia, tags="bg_img")
            tkMessageBox.showinfo("Texto encontrado:",texto)        
        else:
            tkMessageBox.showwarning("Error","Elige una imagen antes de aplicar un filtro")


    def sacaValor(self,valor):
        
        self.entrytext = valor.get()
        self.nuevaImagen = filtroBrillo(self.img,self.cambia,self.entrytext)
        imageAplica = ImageTk.PhotoImage(self.nuevaImagen)
        self.FiltroImagen.imagenes1 = imageAplica
        self.FiltroImagen.create_image(imageAplica.width()/2, imageAplica.height()/2, anchor=CENTER, image=imageAplica, tags="bg_img")
        self.tope.destroy()

root = Tk()
root.title("Proceso Digital de Imagenes ")
root.wm_state("normal")
app = Interfaz(root)
root.mainloop()
