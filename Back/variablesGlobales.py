from Back.passwordManager import *
from Back.ConexionFTP import *

pm = passwordManager()
cFTP = ConexionFTP()

rutaPw = "pw.pass" #default
sincronizado = False

def setSincronizado(estado):
    global sincronizado
    sincronizado = estado

def getSincronizado():
    return sincronizado

def setRutaPw(ruta):
    global rutaPw
    rutaPw = ruta

def getRutaPw():
    return rutaPw

