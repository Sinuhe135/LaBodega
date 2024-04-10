import Back.variablesGlobales as vg
from customtkinter import filedialog
from tkinter import messagebox
import customtkinter
import os

class PaginaLlave(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master

        customtkinter.CTkFrame.__init__(self,master)
        master.cambiar_geometria("500x350")

        lblTitle = customtkinter.CTkLabel(self, text="Seleccion de llave",font=("Consolas",24))
        lblTitle.pack(pady=(30,12),padx=10)

        self.lblMensaje = customtkinter.CTkLabel(self, text="Elige una llave",font=("Verdana",14))
        self.lblMensaje.pack(pady=12,padx=10)

        btnEscogerLlave = customtkinter.CTkButton(self,text="Elegir",font=("Verdana",14),height=50,command=self.escogerLlave)
        btnEscogerLlave.pack(pady=12,padx=10)

        btnCrearLlave = customtkinter.CTkButton(self,text="Crear",font=("Verdana",14),height=50,command=self.crearLlave)
        btnCrearLlave.pack(pady=12,padx=10)

    def escogerLlave(self):
        initial_directory=os.getenv("USERPROFILE")
        file_types = [("Llave", "*.key"), ("Todos los archivos", "*.*")]

        path = filedialog.askopenfilename(initialdir=initial_directory,title="Elegir llave",filetypes=file_types)
        if(path!=""):
            vg.pm.load_key(path)
            self.cargarContraPorDefecto()

    def crearLlave(self):
        initial_directory=os.getenv("USERPROFILE")
        file_types = [("Llave", "*.key"), ("Todos los archivos", "*.*")]

        path = filedialog.asksaveasfilename(initialdir=initial_directory,title="Guardar llave",filetypes=file_types)
        if (path != ""):
            vg.pm.create_key(path+".key")
            self.cargarContraPorDefecto()

    def cargarContraPorDefecto(self):
        try:
            vg.pm.load_password_file(vg.getRutaPw())
        except:
            self.master.cambiarPaginaContrasena()
            return 0

        if(messagebox.askyesno(message="¿Desea continuar con las contraseñas por defecto?",title="Aviso")):
            self.cambiarNubeOPrincipal()
        else:
            self.master.cambiarPaginaContrasena()

    def cambiarNubeOPrincipal(self):
        if(vg.cFTP.IsEnabled()):
            self.master.cambiarComprobarNube()
        else:
            self.master.cambiarPaginaPrincipal()

