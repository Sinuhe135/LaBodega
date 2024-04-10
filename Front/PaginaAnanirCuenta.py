import Back.variablesGlobales as vg
import customtkinter

class PaginaAnanirCuenta(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master
        self.ocultado = True
        customtkinter.CTkFrame.__init__(self,master)
        master.cambiar_geometria("500x500")

        lblTitulo = customtkinter.CTkLabel(self, text="Añadir cuenta",font=("Consolas",24))
        lblTitulo.pack(pady=(30,12),padx=10)

        self.lblMensaje = customtkinter.CTkLabel(self, text="Ingrese los datos",font=("Verdana",14))
        self.lblMensaje.pack(pady=12,padx=10)

        self.txtCuenta = customtkinter.CTkEntry(self, placeholder_text="Nombre",font=("Gadugi",14))
        self.txtCuenta.pack(pady=12,padx=10)
        self.txtCuenta.bind("<KeyRelease>",self.limitarCaracteresCuenta)

        self.txtCorreo = customtkinter.CTkEntry(self, placeholder_text="Correo/Usuario",font=("Gadugi",14))
        self.txtCorreo.pack(pady=12,padx=10)
        self.txtCorreo.bind("<KeyRelease>",self.limitarCaracteresCorreo)

        frmContra = customtkinter.CTkFrame(self,fg_color="transparent")
        frmContra.pack()
        frmContra.columnconfigure(0, weight=1)
        frmContra.columnconfigure(1, weight=2)
        frmContra.columnconfigure(2, weight=1)

        self.txtContra = customtkinter.CTkEntry(frmContra, placeholder_text="Contraseña", show="*",font=("Gadugi",14))
        self.txtContra.grid(pady=12,padx=10, column=1, row=0)
        self.txtContra.bind("<KeyRelease>",self.limitarCaracteresContra)

        self.btnOcultar = customtkinter.CTkButton(frmContra, text="Mostrar",font=("Verdana",14), width=70, command=self.ocultarContra)
        self.btnOcultar.grid(column=2, row=0)

        lblCentradora = customtkinter.CTkLabel(frmContra, text="", width=70)
        lblCentradora.grid(column=0, row=0)

        btnConfirmar = customtkinter.CTkButton(self, text="Confirmar",font=("Verdana",14),height=40,width=120,command= self.ananir)
        btnConfirmar.pack(pady=20,padx=10)

        btnCancelar = customtkinter.CTkButton(self, text="Cancelar",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",width=100,command=lambda: self.master.cambiarPaginaPrincipal())
        btnCancelar.pack(pady=30,padx=10)

    def limitarCaracteresCuenta(self,event):
        if(len(self.txtCuenta.get()) > 30):
            self.txtCuenta.delete(30,customtkinter.END)
            self.lblMensaje.configure(text="Limite de caracteres alcanzado en cuenta", text_color="red")

    def limitarCaracteresCorreo(self,event):
        if(len(self.txtCorreo.get()) > 40):
            self.txtCorreo.delete(40,customtkinter.END)
            self.lblMensaje.configure(text="Limite de caracteres alcanzado en correo/usuario", text_color="red")

    def limitarCaracteresContra(self,event):
        if(len(self.txtContra.get()) > 40):
            self.txtContra.delete(40,customtkinter.END)
            self.lblMensaje.configure(text="Limite de caracteres alcanzado en contraseña", text_color="red")

    def ocultarContra(self):
        if (self.ocultado):
            self.txtContra.configure(show="")
            self.btnOcultar.configure(text="Ocultar")
            self.ocultado=False
        else:
            self.txtContra.configure(show="*")
            self.btnOcultar.configure(text="Mostrar")
            self.ocultado=True

    def ananir(self):
        if(self.txtCuenta.get()=="" or self.txtCorreo.get()=="" or self.txtContra.get()==""):
            self.lblMensaje.configure(text="No se pueden dejar campos en blanco", text_color="red")
            return 0            
        
        if (self.txtCuenta.get().count("\\")>0 or self.txtCuenta.get().count("\"")>0 or self.txtCuenta.get().count(":")>0):
            self.lblMensaje.configure(text="No se puede utilizar \"  \\  :", text_color="red")
            return 0
        
        if (self.txtCorreo.get().count("\\")>0 or self.txtCorreo.get().count("\"")>0 or self.txtCorreo.get().count(":")>0):
            self.lblMensaje.configure(text="No se puede utilizar \"  \\  :", text_color="red")
            return 0
        
        if (self.txtContra.get().count("\\")>0 or self.txtContra.get().count("\"")>0 or self.txtContra.get().count(":")>0):
            self.lblMensaje.configure(text="No se puede utilizar \"  \\  :", text_color="red")
            return 0

        if(vg.pm.is_registered(self.txtCuenta.get())):
            self.lblMensaje.configure(text="Cuenta ya existente", text_color="red")
            return 0
        
        try:
            vg.pm.add_password(self.txtCuenta.get(),self.txtContra.get(),self.txtCorreo.get())
        except:
            self.lblMensaje.configure(text="Error", text_color="red")
            return 0
        
        if(not vg.cFTP.IsEnabled()):
            self.master.cambiarPaginaPrincipal()
            return 0

        if(vg.getSincronizado()):
            self.master.cambiarSubirNube()
        else:
            self.master.cambiarComprobarNube()