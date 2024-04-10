import Back.variablesGlobales as vg
import customtkinter
from tkinter import messagebox

class PaginaEliminarCuenta(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master
        self.dictBtnBorrar = {}
        self.dictFrmCuenta = {}
        self.frmBaseBaseCuentas = None

        customtkinter.CTkFrame.__init__(self,master)
        master.cambiar_geometria("600x650")

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0,weight=1)

        lblTitulo = customtkinter.CTkLabel(self,text="Eliminar cuenta",font=("Consolas",24))
        lblTitulo.grid(row=0,column=0,pady=(30,0),columnspan=2)

        self.txtBuscar = customtkinter.CTkEntry(self,placeholder_text="Buscar",font=("Gadugi",14))
        self.txtBuscar.bind("<Return>",self.buscarMostrarCuenta)
        self.txtBuscar.grid(row=1,column=0,pady=20,padx=20, sticky="ew")

        btnBuscar = customtkinter.CTkButton(self,text="Buscar",width=70,font=("Verdana",14))
        btnBuscar.bind("<Button-1>",self.buscarMostrarCuenta)
        btnBuscar.grid(row=1,column=1,padx=(0,20))

        self.btnMostrarTodas = customtkinter.CTkButton(self,text="Mostrar todas",font=("Verdana",14),width=200,state="disabled",command=self.mostrarTodasCuentas)
        self.btnMostrarTodas.grid(row=3,column=0,columnspan=2)

        btnRegresar = customtkinter.CTkButton(self,text="Regresar",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
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

        self.frmBaseBaseCuentas = customtkinter.CTkFrame(self,fg_color="transparent")
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

        btnBorrar = customtkinter.CTkButton(frmCuenta, text ="Borrar",font=("Verdana",14), width=70,command=lambda sitio=site:self.borrarCuenta(sitio))
        btnBorrar.grid(row=0,column = 1,padx=(0,10))
        self.dictBtnBorrar[site] = btnBorrar

    def borrarCuenta(self,site):
        if(messagebox.askyesno(message="¿Desea borrar "+site+"?",title="Aviso")):
            vg.pm.delete_site(site)
            self.dictFrmCuenta[site].pack_forget()
        else:
            return 0
        
        if(not vg.cFTP.IsEnabled()):
            return 0

        if(vg.getSincronizado()):
            self.master.cambiarSubirNube()
        else:
            self.master.cambiarComprobarNube()