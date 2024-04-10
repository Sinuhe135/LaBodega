import Back.variablesGlobales as vg
import customtkinter
from customtkinter import filedialog
import os

class PaginaContrasenas(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master

        customtkinter.CTkFrame.__init__(self,master)
        master.cambiar_geometria("500x430")
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        lblTitle = customtkinter.CTkLabel(self, text="Seleccion de contraeñas",font=("Consolas",24))
        lblTitle.grid(row=0,column=0,columnspan=2,pady=(30,12),padx=10)

        self.lblMensaje = customtkinter.CTkLabel(self, text="Elige un archivo de contraseñas",font=("Verdana",14))
        self.lblMensaje.grid(row=1,column=0,columnspan=2,pady=12,padx=10)

        btnEscogerContra = customtkinter.CTkButton(self,text="Elegir",font=("Verdana",14),height=50,command=self.escogerContra)
        btnEscogerContra.grid(row=2,column=0,pady=(12,0),padx=(20,10))

        btnCrearContra = customtkinter.CTkButton(self,text="Crear",font=("Verdana",14),height=50,command=self.crearContra)
        btnCrearContra.grid(row=2,column=1,pady=(12,0),padx=(10,20))

        self.lblContra = customtkinter.CTkLabel(self, text="",font=("Verdana",12))
        self.lblContra.grid(row=3,column=0,columnspan=2,pady=(40,60),padx=10)

        btnVolver = customtkinter.CTkButton(self,text="Regresar",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",width=100,command=lambda: self.master.cambiarPaginaLlave())
        btnVolver.grid(row=4,column=0,columnspan=2,pady=12,padx=10)


        self.cargarNombreLlave()

    def cargarNombreLlave(self):
        if(vg.pm.is_key_lodaded()):
            nombreArchivo = os.path.basename(vg.pm.get_key_file())
            nombre, extencion = os.path.splitext(nombreArchivo)
            self.lblContra.configure(text="Llave seleccionada: "+nombre)

    def escogerContra(self):
        initial_directory=os.getenv("USERPROFILE")
        file_types = [("Contraseñas", "*.pass"), ("Todos los archivos", "*.*")]

        path = filedialog.askopenfilename(initialdir=initial_directory,title="Escoger archivo de contraseñas",filetypes=file_types)
        if(path!=""):
            try:
                vg.pm.load_password_file(path)
                vg.setRutaPw(path)
                self.cambiarNubeOPrincipal()
            except:
                self.lblMensaje.configure(text="Llave incorrecta", text_color="red")

    def crearContra(self):
        initial_directory=os.getenv("USERPROFILE")
        file_types = [("Contraseñas", "*.pass"), ("Todos los archivos", "*.*")]

        path = filedialog.asksaveasfilename(initialdir=initial_directory,title="Guardar archivo de contraseñas",filetypes=file_types)
        if (path != ""):
            try:
                finalPath = path+".pass"
                
                vg.pm.create_password_file(finalPath)
                vg.setRutaPw(finalPath)
                self.cambiarNubeOPrincipal()
            except:
                self.lblMensaje.configure(text="Error", text_color="red")

    def cambiarNubeOPrincipal(self):
        if(vg.cFTP.IsEnabled()):
            self.master.cambiarComprobarNube()
        else:
            self.master.cambiarPaginaPrincipal()