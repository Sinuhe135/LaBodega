import Back.variablesGlobales as vg
import customtkinter
import threading

class PaginaComprobarNube(customtkinter.CTkFrame):
    def __init__(self,master):
        self.master = master

        self.frmActual = None

        customtkinter.CTkFrame.__init__(self,master)
        
        self.mostrarSincronizando()

    def borrarFrameBase(self):
        if(self.frmActual is not None):
            self.frmActual.destroy()

        self.frmActual = customtkinter.CTkFrame(self)
        self.frmActual.pack(fill="both",expand=True)

    def mostrarSincronizando(self):
        self.borrarFrameBase()

        self.master.cambiar_geometria("1200x535")
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        if(not vg.cFTP.IsEnabled()):
            self.frmActual.rowconfigure(1,weight=1)

            lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Conexión con la nube deshabilitada",font=("Consolas",16))
            lblMensaje.grid(row=0,column=0,sticky="s",pady=20)

            btnRegresar = customtkinter.CTkButton(self.frmActual,text="Regresar",font=("Verdana",14),fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",width=100,command=lambda: self.master.cambiarPaginaPrincipal())
            btnRegresar.grid(row=1,column=0,sticky="n",pady=20)

            return 0


        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Comprobando sincronizacion con la nube...",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,pady=20)

        comprobar = threading.Thread(target=self.comprobarSincronizacion)
        comprobar.start()

    def comprobarSincronizacion(self):
        contraseñasNube = {}
        dictNube = {}

        try:
            contraseñasNube = vg.cFTP.CheckPw(vg.pm.get_password_file())
        except:
            self.mostrarErrorConexion()
            return 0
        
        try:
            dictNube = vg.pm.decrypt_cloud(contraseñasNube)
        except:
            self.mostrarErrorLLave()
            return 0

        faltaEnNube, faltaEnLocal, difEnNube = vg.pm.cloud_diff(dictNube)

        if(len(faltaEnNube) == 0 and len(faltaEnLocal) == 0 and len(difEnNube) == 0):
            vg.setSincronizado(True)
            self.mostrarSincronizadoExito()
            return 0
        
        vg.setSincronizado(False)
        self.mostrarDesincronizado(faltaEnNube, faltaEnLocal, difEnNube)
    
    def mostrarErrorConexion(self):
        self.borrarFrameBase()
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.rowconfigure(2,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Error de conexion",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,sticky="s",pady=10)

        btnReintentar = customtkinter.CTkButton(self.frmActual,text="Reintentar",font=("Verdana",14),height=50,command=self.mostrarSincronizando)
        btnReintentar.grid(row=1,column=0,pady=(0,50))

        btnCancelar = customtkinter.CTkButton(self.frmActual,text="Cancelar",font=("Verdana",14),height=30,width=100,fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",command=lambda: self.master.cambiarPaginaPrincipal())
        btnCancelar.grid(row=2,column=0,sticky="n",pady=10)

    def mostrarErrorLLave(self):
        self.borrarFrameBase()
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.rowconfigure(1,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Llave no concide con contraseñas de la nube",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,sticky="s",pady=20)

        btnCancelar = customtkinter.CTkButton(self.frmActual,text="Cancelar",font=("Verdana",14),height=30,fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",command=lambda: self.master.cambiarPaginaPrincipal())
        btnCancelar.grid(row=1,column=0,sticky="n",pady=20)

    def mostrarSincronizadoExito(self):
        self.borrarFrameBase()
        self.frmActual.rowconfigure(0,weight=1)
        self.frmActual.rowconfigure(1,weight=1)
        self.frmActual.columnconfigure(0,weight=1)

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Cuentas sincronizadas con la nube",font=("Consolas",16))
        lblMensaje.grid(row=0,column=0,sticky="s",pady=20)

        btnContinuar = customtkinter.CTkButton(self.frmActual,text="Continuar",font=("Verdana",14),height=50,command=lambda: self.master.cambiarPaginaPrincipal())
        btnContinuar.grid(row=1,column=0,sticky="n",pady=20)

    def mostrarDesincronizado(self,faltaEnNube,faltaEnLocal, difEnNube):
        numeroColumnas = 0
        indiceColumna = 0

        self.borrarFrameBase()

        if(len(faltaEnNube)!= 0):
            numeroColumnas+=1

        if(len(faltaEnLocal)!= 0):
            numeroColumnas+=1

        if(len(difEnNube)!= 0):
            numeroColumnas+=1

        numeroColumnas*=3

        for columna in range(numeroColumnas):
            self.frmActual.columnconfigure(columna,weight=1)

        self.frmActual.rowconfigure(2, weight=1)

        lblMensaje = customtkinter.CTkLabel(self.frmActual,text="Desincronizacion detectada",font=("Consolas",20))
        lblMensaje.grid(row=0,column=0,pady=20,columnspan=numeroColumnas)


        if(len(faltaEnNube)!= 0):
            lblFaltaNube = customtkinter.CTkLabel(self.frmActual,text="Cuentas faltantes en la nube",font=("Consolas",14))
            
            frmFaltaNube = customtkinter.CTkScrollableFrame(self.frmActual)

            margenX = (0,0)

            if(len(faltaEnLocal)!= 0 and len(difEnNube)!= 0):
                margenX = (20,10)
            elif(len(faltaEnLocal)!=0):
                margenX = (20,10)
            elif(len(difEnNube)!=0):
                margenX = (20,0)
            else:
                margenX = (20,20)

            lblFaltaNube.grid(row=1,column=indiceColumna,columnspan=3,padx=margenX)

            frmFaltaNube.grid(row=2,column=indiceColumna,columnspan=3, sticky="nswe",padx=margenX)

            for cuenta in faltaEnNube:
                frmCuenta = customtkinter.CTkFrame(frmFaltaNube,fg_color="gray20")
                frmCuenta.pack(pady=10,padx=10, fill="x")

                lblCuenta = customtkinter.CTkLabel(frmCuenta,text=cuenta,font=("Verdana",14))
                lblCuenta.pack(padx=10,pady=15)

            indiceColumna+=3


        if(len(faltaEnLocal)!= 0):
            lblFaltaLocal = customtkinter.CTkLabel(self.frmActual,text="Cuentas faltantes en local",font=("Consolas",14))

            frmFaltaLocal = customtkinter.CTkScrollableFrame(self.frmActual)

            margenX = (0,0)

            if(len(faltaEnNube)!= 0 and len(difEnNube)!= 0):
                margenX = (0,0)
            elif(len(faltaEnNube)!=0):
                margenX = (0,10)
            elif(len(difEnNube)!=0):
                margenX = (10,0)
            else:
                margenX = (20,20)

            lblFaltaLocal.grid(row=1,column=indiceColumna,columnspan=3,padx=margenX)
            frmFaltaLocal.grid(row=2,column=indiceColumna,columnspan=3, sticky="nswe",padx=margenX)

            for cuenta in faltaEnLocal:
                frmCuenta = customtkinter.CTkFrame(frmFaltaLocal,fg_color="gray20")
                frmCuenta.pack(pady=10,padx=10, fill="x")

                lblCuenta = customtkinter.CTkLabel(frmCuenta,text=cuenta,font=("Verdana",14))
                lblCuenta.pack(padx=10,pady=15)

            indiceColumna+=3


        if(len(difEnNube)!= 0):
            lbldiffNube = customtkinter.CTkLabel(self.frmActual,text="Cuentas diferentes en la nube",font=("Consolas",14))

            frmDifEnNube = customtkinter.CTkScrollableFrame(self.frmActual)

            margenX = (0,0)

            if(len(faltaEnNube)!= 0 and len(faltaEnLocal)!= 0):
                margenX = (10,20)
            elif(len(faltaEnNube)!=0):
                margenX = (10,20)
            elif(len(faltaEnLocal)!=0):
                margenX = (10,20)
            else:
                margenX = (20,20)

            lbldiffNube.grid(row=1,column=indiceColumna,columnspan=3,padx=margenX)
            frmDifEnNube.grid(row=2,column=indiceColumna,columnspan=3, sticky="nswe",padx=margenX)

            for cuenta in difEnNube:
                frmCuenta = customtkinter.CTkFrame(frmDifEnNube,fg_color="gray20")
                frmCuenta.pack(pady=10,padx=10, fill="x")

                lblCuenta = customtkinter.CTkLabel(frmCuenta,text=cuenta,font=("Verdana",14))
                lblCuenta.pack(padx=10,pady=15)

        btnSubirNube= customtkinter.CTkButton(self.frmActual,text="Subir a la nube",font=("Verdana",14),height=50, command=lambda:self.master.cambiarSubirNube())
        btnSubirNube.grid(column=0,row=3,columnspan=int(numeroColumnas/3),pady=30,padx=(20,0))

        btnDescargarNube= customtkinter.CTkButton(self.frmActual,text="Descargar de la nube",font=("Verdana",14),height=50, command=lambda:self.master.cambiarDescargarNube())
        btnDescargarNube.grid(column=int(numeroColumnas/3*2),row=3,columnspan=int(numeroColumnas/3),pady=30,padx=(0,20))
        
        btnCancelar = customtkinter.CTkButton(self.frmActual, text="Cancelar",height=30,width=100,fg_color="dark slate gray", hover_color="gray10",
                                            text_color="white",command=lambda:self.master.cambiarPaginaPrincipal())
        btnCancelar.grid(column=int(numeroColumnas/3),row=3,columnspan=int(numeroColumnas/3), pady=30)

            










        

