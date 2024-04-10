import Back.variablesGlobales as vg
import customtkinter
from tkinter import messagebox
from PIL import Image
import pyperclip
import time
import threading

class PaginaPrincipal(customtkinter.CTkFrame):
    def __init__(self, master):
        self.master = master
        self.dictLblContra={}
        self.dictBtnOcultar={}
        self.dictBtnCopiar={}
        self.ocultado={}

        self.frmBaseBaseCuentas = None

        customtkinter.CTkFrame.__init__(self,master, fg_color="transparent")
        master.cambiar_geometria("800x600")

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1,weight=1)

        #Seccion izquierda

        frmBaseOpciones = customtkinter.CTkFrame(self,width=200,fg_color="transparent")
        frmBaseOpciones.grid(row=0,column=0, rowspan = 2,padx=(0,20),sticky="ns")
        frmBaseOpciones.rowconfigure(2,weight=1)

        logo = customtkinter.CTkImage(light_image=Image.open("Media/logo.png"),size=(100,100))
        lblLogo = customtkinter.CTkLabel(frmBaseOpciones,image=logo,text="")
        lblLogo.grid(row=0,column=0)

        lblNombre = customtkinter.CTkLabel(frmBaseOpciones,text="La Bodega\nv1.0",justify="center",font=("Consolas",18))
        lblNombre.grid(row=1,column=0,pady=(10,20))

        btnCerrar = customtkinter.CTkButton(self, text="Cerrar archivos",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white", command=self.cerrarArchivos)
        btnCerrar.grid(row=2,column=0,padx=(0,20))

        #Seccion opciones

        frmOpciones = customtkinter.CTkFrame(frmBaseOpciones)
        frmOpciones.grid(row=2,column=0,sticky="nsew",pady=(0,20))
        frmOpciones.rowconfigure(4, weight=1)

        lblTituloOpciones = customtkinter.CTkLabel(frmOpciones,text="Opciones",font=("Consolas",16))
        lblTituloOpciones.grid(row=0,column=0,pady=(20,0),padx=20)

        btnAnanir = customtkinter.CTkButton(frmOpciones, text ="Añadir",font=("Verdana",14), command=lambda: self.master.cambiarAnanirCuenta())
        btnAnanir.grid(row=1,column = 0, pady=(20,0),padx=20)

        btnAnanir = customtkinter.CTkButton(frmOpciones, text ="Editar",font=("Verdana",14), command=lambda: self.master.cambiarEditarCuenta())
        btnAnanir.grid(row=2,column = 0, pady=(20,0),padx=20)

        btnEliminar = customtkinter.CTkButton(frmOpciones, text ="Eliminar",font=("Verdana",14), command= lambda: self.master.cambiarEliminarCuenta())
        btnEliminar.grid(row=3,column = 0, pady=(20,0),padx=20)

        btnNube = customtkinter.CTkButton(frmOpciones, text ="Nube",font=("Verdana",14),width=100, fg_color="dark sea green", hover_color="pale green",
                                            text_color="black",command= lambda: self.master.cambiarComprobarNube())
        btnNube.grid(row=5,column = 0, pady=20,padx=20)

        #Elementos buscador

        self.txtBuscar = customtkinter.CTkEntry(self,placeholder_text="Buscar",font=("Gadugi",14))
        self.txtBuscar.bind("<Return>",self.buscarMostrarCuenta)
        self.txtBuscar.grid(row=0,column=1, sticky="ew",padx = 20)

        btnBuscar = customtkinter.CTkButton(self, text ="Buscar",font=("Verdana",14))
        btnBuscar.bind("<Button-1>",self.buscarMostrarCuenta)
        btnBuscar.grid(row=0,column = 2)

        self.btnMostrarTodas = customtkinter.CTkButton(self,text="Mostrar todas",font=("Verdana",14),width=200,state="disabled" ,command=self.mostrarTodasCuentas)
        self.btnMostrarTodas.grid(row=2,column=1,columnspan=2)

        #Seccion cuentas
        
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

        self.frmBaseBaseCuentas = customtkinter.CTkFrame(self,fg_color="transparent")
        self.frmBaseBaseCuentas.grid(row=1,columnspan=2, column=1, sticky="nsew",pady=20)

        self.frmBaseCuentas = customtkinter.CTkScrollableFrame(self.frmBaseBaseCuentas)
        self.frmBaseCuentas.pack(fill="both",expand=True)

    def cargarSinCuentas(self):
        frmCuenta = customtkinter.CTkFrame(self.frmBaseCuentas,fg_color="gray20")
        frmCuenta.pack(pady=10,padx=10, fill="x")

        lblCuenta = customtkinter.CTkLabel(frmCuenta,text="Sin cuentas registradas",font=("Verdana",16))
        lblCuenta.pack(padx=10,pady=15)

    def cargarSinResultados(self):
        frmCuenta = customtkinter.CTkFrame(self.frmBaseCuentas,fg_color="gray20")
        frmCuenta.pack(pady=10,padx=10, fill="x")

        lblCuenta = customtkinter.CTkLabel(frmCuenta,text="Sin resultados",font=("Verdana",16))
        lblCuenta.pack(padx=10,pady=15)
        
    def cargarElementosCuentas(self,site):
        #Base

        frmCuenta = customtkinter.CTkFrame(self.frmBaseCuentas,fg_color="gray20")
        frmCuenta.pack(pady=10,padx=10, fill="x")
        frmCuenta.columnconfigure(0,weight=1)

        #datos

        lblCuenta = customtkinter.CTkLabel(frmCuenta,text=site,font=("Gadugi",18))
        lblCuenta.grid(row=0,column=0,padx=10,pady=(10,0),sticky="w")

        lblCorreo = customtkinter.CTkLabel(frmCuenta,text=vg.pm.get_email(site),font=("Gadugi",14))
        lblCorreo.grid(row=1,column=0,padx=(20,10),pady=0,sticky="w")

        lblContra = customtkinter.CTkLabel(frmCuenta,text=self.censurar(site),font=("Gadugi",14))
        lblContra.grid(row=2,column=0,padx=(20,10),pady=(0,10),sticky="w")
        self.dictLblContra[site] = lblContra

        # Botones
        
        frmBotonesCuenta = customtkinter.CTkFrame(frmCuenta,fg_color="transparent")
        frmBotonesCuenta.grid(row=0,column=1, rowspan = 3,sticky="nsew")
        frmBotonesCuenta.rowconfigure(0,weight=1)
        frmBotonesCuenta.rowconfigure(1,weight=1)

        btnOcultar = customtkinter.CTkButton(frmBotonesCuenta, text ="Mostrar",font=("Verdana",14), width=80, command=lambda sitio=site: self.ocultarMostrarContra(sitio))
        btnOcultar.grid(row=0,column = 0,padx=(0,10))
        self.dictBtnOcultar[site] = btnOcultar
        self.ocultado[site] = True

        btnCopiar = customtkinter.CTkButton(frmBotonesCuenta, text ="Copiar",font=("Verdana",14), width=80, command=lambda sitio=site:self.copiarPortapapeles(sitio))
        btnCopiar.grid(row=1,column = 0,padx=(0,10))
        self.dictBtnCopiar[site] = btnCopiar

    def ocultarMostrarContra(self,sitio):
        if(self.ocultado[sitio]):
            self.mostrarContra(sitio)
        else:
            self.ocultarContra(sitio)

    def mostrarContra(self,sitio):
        texto = vg.pm.get_password(sitio)
        self.dictLblContra[sitio].configure(text=texto)
        self.dictBtnOcultar[sitio].configure(text="Ocultar")
        self.ocultado[sitio] = False

    def ocultarContra(self, sitio):
        texto = self.censurar(sitio)
        self.dictLblContra[sitio].configure(text=texto)
        self.dictBtnOcultar[sitio].configure(text="Mostrar")
        self.ocultado[sitio] = True

    def censurar(self, sitio):
        texto = vg.pm.get_password(sitio)
        censura = "*"*len(texto)
        return censura
    
    def copiarPortapapeles(self, sitio):
        pyperclip.copy(vg.pm.get_password(sitio))
        mensaje = threading.Thread(target=self.mostrarCopiado,args=(sitio,))
        mensaje.start()

    def mostrarCopiado(self,sitio):
        self.dictBtnCopiar[sitio].configure(text="Copiado")
        time.sleep(2)
        self.dictBtnCopiar[sitio].configure(text="Copiar")

    def cerrarArchivos(self):
        if(messagebox.askyesno(message="¿Seguro que quiere salir?",title="Cerrar archivos")):
            vg.pm.unload_key()
            vg.pm.unload_password()
            vg.setRutaPw("")
            vg.setSincronizado(False)
            
            self.master.cambiarPaginaLlave()
        