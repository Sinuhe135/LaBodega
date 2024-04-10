from cryptography.fernet import Fernet

class passwordManager:

    def __init__(self):
        self.key = None
        self.key_file = None
        self.password_file = None
        self.password_dict = {}
        self.email_dict={}

    def create_key(self,path):
        open(path,"x")
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

        self.key_file = path
        
    def load_key(self,path):
        with open(path,'rb') as f:
            self.key = f.read()

        self.key_file = path

    def create_password_file(self,path):
        open(path, "x")

        self.password_file = path
        self.password_dict = {}
        self.email_dict = {}

    def load_password_file(self,path):
        with open(path,'r') as f:
            self.unload_password()
            for line in f:
                site, encryptedPw, encryptedEm = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encryptedPw.encode()).decode()
                self.email_dict[site] = Fernet(self.key).decrypt(encryptedEm.encode()).decode()

        self.password_file = path
    
    def add_password(self,site,password,email):
        self.password_dict[site] = password
        self.email_dict[site] = email

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encryptedPw = Fernet(self.key).encrypt(password.encode())
                encryptedEm = Fernet(self.key).encrypt(email.encode())
                f.write(site + ":" + encryptedPw.decode() +":"+encryptedEm.decode() +"\n")

    def delete_site(self,site):
        self.password_dict.pop(site)

        passwordsLines = []

        with open(self.password_file, "r") as f:
            passwordsLines = f.readlines()

        with open(self.password_file,"w") as f:
            for line in passwordsLines:
                ogSite, pw, email = line.split(":")
                if(ogSite != site):
                    f.write(ogSite + ":" + pw + ":"+email.replace("\n","")+"\n")  

    def unload_password(self):
        self.password_file = None
        self.password_dict = {}
        self.email_dict={}

    def unload_key(self):
        self.key = None
        self.key_file = None

    def get_password_file(self):
        return self.password_file
    
    def get_key_file(self):
        return self.key_file

    def get_password(self,site):
        return self.password_dict[site]
    
    def get_email(self,site):
        return self.email_dict[site]
    
    def get_password_list(self):
        return self.password_dict
    
    def is_key_lodaded(self):
        if(self.key is not None):
            return True
        else:
            return False
        
    def are_files_loaded(self):
        if(self.password_file is not None):
            return True
        else:
            return False
    
    def is_registered(self, site):
        if(site in self.password_dict):
            return True
        else:
            return False
        
    #Cloud functions

    def recover_password_file(self):
        for site in self.password_dict.keys():
            with open(self.password_file, 'w') as f:
                encryptedPw = Fernet(self.key).encrypt(self.password_dict[site].encode())
                encryptedEm = Fernet(self.key).encrypt(self.email_dict[site].encode())
                f.write(site + ":" + encryptedPw.decode() +":"+encryptedEm.decode() +"\n")

    def decrypt_cloud(self,cloud_dict):
        for site in cloud_dict.keys():
            cloud_dict[site] = Fernet(self.key).decrypt(cloud_dict[site].encode()).decode()

        return cloud_dict
    
    def cloud_diff(self, cloud_dict):
        not_in_cloud = set(self.password_dict.keys())
        not_in_local = set(cloud_dict.keys())
        diff_in_cloud = set()

        for default_key in self.password_dict.keys():
            for cloud_key in cloud_dict.keys():

                if default_key == cloud_key:
                    
                    corrected_value = self.password_dict[default_key].replace("\n","")
                    if(corrected_value != cloud_dict[cloud_key]):
                        diff_in_cloud.add(default_key)
                    not_in_cloud.remove(default_key)
                    not_in_local.remove(cloud_key)
                    break
        
        return not_in_cloud, not_in_local, diff_in_cloud

                
