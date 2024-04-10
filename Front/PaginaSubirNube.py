import Back.variablesGlobales as vg
import customtkinter

import threading

class PaginaSubirNube(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master

        self.frmActual = None

        customtkinter.CTkFrame.__init__(self,master)
        
        self.mostrarSubiendo()

    def borrarFrameBase(self):
        if(self.frmActual is not None):
            self.frmActual.destroy()

        self.frmActual = customtkinter.CTkFrame(self)
        self.frmActual.pack(fill="both",expand=True)

    def mostrarSubiendo(self):
        self.borrarFrameBase()

        self.master.cambiar_geometria("1200x535")
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        if(not vg.cFTP.IsEnabled()):
            self.frmActual.rowconfigure(1,weight=1)

            lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Conexion con la nube deshabilitada",font=("Consolas",16))
            lblMensaje.grid(row=0,column=0,sticky="s",pady=20)

            btnRegresar = customtkinter.CTkButton(self.frmActual,text="Regresar",font=("Verdana",14),height=50,command=lambda: self.master.cambiarPaginaPrincipal())
            btnRegresar.grid(row=1,column=0,sticky="n",pady=20)

            return 0

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Subiendo a la nube...",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,pady=20)

        subir = threading.Thread(target=self.subirALaNube)
        subir.start()

    def subirALaNube(self):
        try:
            vg.cFTP.Upload(vg.pm.get_password_file())
            vg.setSincronizado(True)
            self.mostrarSubidaExito()
        except:
            vg.setSincronizado(False)
            self.mostrarErrorConexion()

    def mostrarErrorConexion(self):
        self.borrarFrameBase()
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.rowconfigure(2,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Error de conexion",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,sticky="s",pady=10)

        btnReintentar = customtkinter.CTkButton(self.frmActual,text="Reintentar",font=("Verdana",14),height=50,command=self.mostrarSubiendo)
        btnReintentar.grid(row=1,column=0,pady=(0,50))

        btnCancelar = customtkinter.CTkButton(self.frmActual,text="Cancelar",height=30,width=100,fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",command=lambda: self.master.cambiarPaginaPrincipal())
        btnCancelar.grid(row=2,column=0,sticky="n",pady=10)

    def mostrarSubidaExito(self):
        self.borrarFrameBase()
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.rowconfigure(1,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Subida realizada con exito",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,sticky="s",pady=20)

        btnContinuar = customtkinter.CTkButton(self.frmActual,text="Continuar",font=("Verdana",14),height=50,command=lambda: self.master.cambiarPaginaPrincipal())
        btnContinuar.grid(row=1,column=0,sticky="n",pady=20)
            