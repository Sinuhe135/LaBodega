import customtkinter
import sys

from Front.PaginaLlave import PaginaLlave
from Front.PaginaContrasenas import PaginaContrasenas
from Front.PaginaPrincipal import PaginaPrincipal
from Front.PaginaAnanirCuenta import PaginaAnanirCuenta
from Front.PaginaEliminarCuenta import PaginaEliminarCuenta
from Front.PaginaEditarCuenta import PaginaEditarCuenta
from Front.PaginaComprobarNube import PaginaComprobarNube
from Front.PaginaDescagarNube import PaginaDescargarNube
from Front.PaginaSubirNube import PaginaSubirNube

#py -m PyInstaller  --icon=Media/logo.ico --noconfirm --onedir --windowed --add-data="C:\Users\Rubix\AppData\Roaming\Python\Python311\site-packages;customtkinter/"  "LaBodega.py"

class Aplicacion(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.geometry("500x350")
        self.title("La Bodega")
        self.resizable(False,False) 

        #self.iconbitmap("Media/logo.ico")
        self.iconbitmap(sys.executable)

        self._frame = None
        self.cambiarPaginaLlave()

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self)

        px,py = self.calcularMargenes(nuevo_frame)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = nuevo_frame
        self._frame.pack(pady=py,padx=px,fill="both",expand=True)

    def cambiarPaginaLlave(self):
        self.switch_frame(PaginaLlave)

    def cambiarPaginaContrasena(self):
        self.switch_frame(PaginaContrasenas)

    def cambiarPaginaPrincipal(self):
        self.switch_frame(PaginaPrincipal)

    def cambiarAnanirCuenta(self):
        self.switch_frame(PaginaAnanirCuenta)

    def cambiarEliminarCuenta(self):
        self.switch_frame(PaginaEliminarCuenta)

    def cambiarEditarCuenta(self):
        self.switch_frame(PaginaEditarCuenta)

    def cambiarComprobarNube(self):
        self.switch_frame(PaginaComprobarNube)

    def cambiarDescargarNube(self):
        self.switch_frame(PaginaDescargarNube)

    def cambiarSubirNube(self):
        self.switch_frame(PaginaSubirNube)

    def cambiar_geometria(self, dimensiones):
        self.geometry(dimensiones)

    def calcularMargenes(self, nuevo_frame):
        if isinstance(nuevo_frame, PaginaPrincipal):
            px = 20
            py = 20
        else:
            px = 60
            py = 20

        return px,py
        
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()