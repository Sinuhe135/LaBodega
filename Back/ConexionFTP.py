import ftplib
import os

class ConexionFTP:
    def __init__(self):
        #FTP Configuration
        self.url = ''
        self.user = ''
        self.password = ''

        self.serverFolderPath = "" #ServerPathWithoutFileName

    def IsEnabled(self):
        if(self.url != '' and self.user != '' and self.password != ''):
            return True
        else:
            return False
        
    def CheckIfExists(self, session,file):
        try:
            session.cwd(self.serverFolderPath)
            session.size(file)
            return True
        except:
            return False


    def Upload(self, pathPw):
        session = ftplib.FTP(self.url,self.user,self.password)
        fileName = os.path.basename(pathPw)
        serverPath = self.serverFolderPath + fileName

        file = open(pathPw,'rb')
        session.storbinary("STOR "+serverPath,file)
        file.close()

        session.quit()       

    def Download(self, pathPw):
        session = ftplib.FTP(self.url,self.user,self.password)
        fileName = os.path.basename(pathPw)
        serverPath = self.serverFolderPath + fileName
        
        if(self.CheckIfExists(session,fileName)):
            file = open(pathPw,'wb')
            session.retrbinary("RETR "+serverPath,file.write)
            file.close()

        session.quit()
        
        
    def CheckPw(self, pathPw):
        session = ftplib.FTP(self.url,self.user,self.password)
        list = []
        dict={}
        fileName = os.path.basename(pathPw)
        serverPath = self.serverFolderPath + fileName
        if(self.CheckIfExists(session,fileName)):
            session.retrlines("RETR "+serverPath,list.append)

            session.quit()

            dict = self.ConvertToDict(list)

            return dict
        else:
            session.quit()
            return dict
    
    def ConvertToDict(self,list):
        newList = []
        dict = {}
        for element in list:
            if(element!=""):
                newList.append(element)
        
        for element in newList:
            site, encrypted,email = element.split(":")
            dict[site] = encrypted

        return dict
        
