import Back.variablesGlobales as vg
import customtkinter
from tkinter import messagebox

class PaginaEditarCuenta(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master
        self.dictBtnEditar = {}
        self.dictFrmCuenta = {}

        self.frmActual = None
        self.frmBaseBaseCuentas = None

        customtkinter.CTkFrame.__init__(self,master,fg_color="transparent")

        self.mostrarPantallaSeleccion()

    def borrarFrameBase(self):
        if(self.frmActual is not None):
            self.frmActual.destroy()

        self.frmActual = customtkinter.CTkFrame(self)
        self.frmActual.pack(fill="both",expand=True)

    def mostrarPantallaSeleccion(self):
        self.borrarFrameBase()

        self.master.cambiar_geometria("600x650")

        self.frmActual.rowconfigure(2, weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        lblTitulo = customtkinter.CTkLabel(self.frmActual,text="Editar cuenta",font=("Consolas",24))
        lblTitulo.grid(row=0,column=0,pady=(30,0),columnspan=2)

        self.txtBuscar = customtkinter.CTkEntry(self.frmActual,placeholder_text="Buscar",font=("Gadugi",14))
        self.txtBuscar.bind("<Return>",self.buscarMostrarCuenta)
        self.txtBuscar.grid(row=1,column=0,pady=20,padx=20, sticky="ew")

        btnBuscar = customtkinter.CTkButton(self.frmActual,text="Buscar",width=70,font=("Verdana",14))
        btnBuscar.bind("<Button-1>",self.buscarMostrarCuenta)
        btnBuscar.grid(row=1,column=1,padx=(0,20))

        self.btnMostrarTodas = customtkinter.CTkButton(self.frmActual,text="Mostrar todas",font=("Verdana",14),width=200,state="disabled" ,command=self.mostrarTodasCuentas)
        self.btnMostrarTodas.grid(row=3,column=0,columnspan=2)

        btnRegresar = customtkinter.CTkButton(self.frmActual,text="Regresar",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",width=100,command=lambda:self.master.cambiarPaginaPrincipal())
        btnRegresar.grid(row=4,column=0,columnspan=2,pady=20)

        self.mostrarTodasCuentas()

    def mostrarTodasCuentas(self):
        self.reiniciarBaseCuentas()
        self.btnMostrarTodas.configure(state="disabled")

        if(len(vg.pm.get_password_list())==0):
            self.cargarSinCuentas()
            return 0

        for site in vg.pm.get_password_list().keys():
            self.cargarElementosCuentas(site)
        
    def buscarMostrarCuenta(self,event):
        self.reiniciarBaseCuentas()
        self.btnMostrarTodas.configure(state="normal")

        site = self.txtBuscar.get()
        if(not vg.pm.is_registered(site)):
            self.cargarSinResultados()
            return 0

        self.cargarElementosCuentas(site)
    
    def reiniciarBaseCuentas(self):
        if(self.frmBaseBaseCuentas is not None):
            self.frmBaseBaseCuentas.destroy()

        self.frmBaseBaseCuentas = customtkinter.CTkFrame(self.frmActual,fg_color="transparent")
        self.frmBaseBaseCuentas.grid(row=2,columnspan=2, column=0, sticky="nsew",pady=(0,20),padx=20)

        self.frmBaseCuentas = customtkinter.CTkScrollableFrame(self.frmBaseBaseCuentas,fg_color="gray20")
        self.frmBaseCuentas.pack(fill="both",expand=True)

    def cargarSinCuentas(self):
        frmCuenta = customtkinter.CTkFrame(self.frmBaseCuentas,fg_color="gray25")
        frmCuenta.pack(pady=10,padx=10, fill="x")

        lblCuenta = customtkinter.CTkLabel(frmCuenta,text="Sin cuentas registradas",font=("Verdana",16))
        lblCuenta.pack(padx=10,pady=15)

    def cargarSinResultados(self):
        frmCuenta = customtkinter.CTkFrame(self.frmBaseCuentas,fg_color="gray25")
        frmCuenta.pack(pady=10,padx=10, fill="x")

        lblCuenta = customtkinter.CTkLabel(frmCuenta,text="Sin resultados",font=("Verdana",16))
        lblCuenta.pack(padx=10,pady=15)

    def cargarElementosCuentas(self,site):
        #Base

        frmCuenta = customtkinter.CTkFrame(self.frmBaseCuentas,fg_color="gray25")
        frmCuenta.pack(pady=10,padx=10, fill="x")
        frmCuenta.columnconfigure(0,weight=1)
        self.dictFrmCuenta[site] = frmCuenta

        #datos

        lblCuenta = customtkinter.CTkLabel(frmCuenta,text=site,font=("Gadugi",14))
        lblCuenta.grid(row=0,column=0,padx=10,pady=15,sticky="w")

        # Botones

        btnEditar = customtkinter.CTkButton(frmCuenta, text ="Editar",font=("Verdana",14), width=70,command=lambda sitio=site:self.mostrarPantallaIngreso(sitio))
        btnEditar.grid(row=0,column = 1,padx=(0,10))
        self.dictBtnEditar[site] = btnEditar

    def mostrarPantallaIngreso(self, site):
        self.borrarFrameBase()
        self.ocultado = True

        self.master.cambiar_geometria("500x500")

        contra = vg.pm.get_password(site)
        correo = vg.pm.get_email(site)

        lblTitulo = customtkinter.CTkLabel(self.frmActual, text="Editar cuenta",font=("Consolas",24))
        lblTitulo.pack(pady=(30,12),padx=10)

        self.lblMensaje = customtkinter.CTkLabel(self.frmActual, text="Ingrese los datos",font=("Verdana",14))
        self.lblMensaje.pack(pady=12,padx=10)

        self.txtCuenta = customtkinter.CTkEntry(self.frmActual, placeholder_text="Nombre",font=("Gadugi",14))
        self.txtCuenta.pack(pady=12,padx=10)
        self.txtCuenta.insert(0, site)
        self.txtCuenta.bind("<KeyRelease>",self.limitarCaracteresCuenta)

        self.txtCorreo = customtkinter.CTkEntry(self.frmActual, placeholder_text="Correo/Usuario",font=("Gadugi",14))
        self.txtCorreo.pack(pady=12,padx=10)
        self.txtCorreo.insert(0,correo)
        self.txtCorreo.bind("<KeyRelease>",self.limitarCaracteresCorreo)

        frmContra = customtkinter.CTkFrame(self.frmActual,fg_color="transparent")
        frmContra.pack()
        frmContra.columnconfigure(0, weight=1)
        frmContra.columnconfigure(1, weight=2)
        frmContra.columnconfigure(2, weight=1)

        self.txtContra = customtkinter.CTkEntry(frmContra, placeholder_text="Contraseña",font=("Gadugi",14), show="*")
        self.txtContra.grid(pady=12,padx=10, column=1, row=0)
        self.txtContra.insert(0,contra)
        self.txtContra.bind("<KeyRelease>",self.limitarCaracteresContra)

        self.btnOcultar = customtkinter.CTkButton(frmContra, text="Mostrar",font=("Verdana",14), width=70, command=self.ocultarContra)
        self.btnOcultar.grid(column=2, row=0)

        lblCentradora = customtkinter.CTkLabel(frmContra, text="", width=70)
        lblCentradora.grid(column=0, row=0)

        btnConfirmar = customtkinter.CTkButton(self.frmActual,text="Confirmar",font=("Verdana",14),height=40,width=120,command= lambda:self.editar(site))
        btnConfirmar.pack(pady=20,padx=10)

        btnCancelar = customtkinter.CTkButton(self.frmActual, text="Regresar",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",width=100,command=self.mostrarPantallaSeleccion)
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

    def editar(self,ogSite):
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

        if(vg.pm.is_registered(self.txtCuenta.get()) and self.txtCuenta.get() != ogSite):
            self.lblMensaje.configure(text="Cuenta ya existente", text_color="red")
            return 0
        
        try:
            vg.pm.delete_site(ogSite)
            vg.pm.add_password(self.txtCuenta.get(),self.txtContra.get(),self.txtCorreo.get())
        except:
            self.lblMensaje.configure(text="Error", text_color="red")
            return 0
        
        if(not vg.cFTP.IsEnabled()):
            self.master.cambiarEditarCuenta()
            return 0
        
        if (vg.getSincronizado()):
            self.master.cambiarSubirNube()
        else:
            self.master.cambiarComprobarNube()
        
