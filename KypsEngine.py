from cryptography.fernet import Fernet, InvalidToken
import json
import re
import hashlib
import os
import base64
import random

class Engine():
    def __init__(self):
        self.Reset()

    def Accesso(self,username, password):
        if not re.findall("[ -/-:-@-[-^-{-⁓]",username):
            contr = self.JSONFinder(username)
            if contr[0]:
                self.cred[0] = username
                self.cred[1] = password
                tabjson = json.loads(open("Accounts/" + contr[1], "r").read())
                if self.Decryption(tabjson["password"]):
                    self.file = contr[1]
                    self.LetturaJSON()
                    return True, 0, ""
                else:
                    return False, 0, "*Password errata"
            else:
                return False, 1, "*Username inesistente"
        else:
            return False, 1, "*Caratteri inseriti non validi"

    def Iscrizione(self, username, password1, password2):
        if not re.findall("[ -/-:-@-[-^-{-⁓]",username):
            if password1 == password2:
                if not self.JSONFinder(username)[0]:
                    with open("Accounts/" + str(random.randrange(1000000,10000000000)) + ".json", "w") as fo:
                        self.cred[0] = username
                        self.cred[1] = password1
                        dictz = {"username": username, "password": self.Encryption(password1), "salvataggi":{}}
                        json.dump(dictz,fo,indent=3)
                    return True, 0, ""
                else:
                    return False, 1, "*Username già esistente"
            else:
                return False, -1, "*Riscrivi la password correttamente"
        else:
            return False, 1, "*Caratteri inseriti non validi"

    def LetturaJSON(self):
        self.database = json.loads(open("Accounts/" + self.file, "r").read())

    def ScritturaJSON(self, dictz):
        with open("Accounts/" + self.file, "w") as fi:
            json.dump(dictz, fi, indent=3)

    def AddNewSave(self, servizio, username, password):
        self.database["salvataggi"][str(self.NumberSaves())] = {}
        self.database["salvataggi"][str(self.NumberSaves() - 1)]["servizio"] = self.Encryption(servizio)
        self.database["salvataggi"][str(self.NumberSaves() - 1)]["username"] = self.Encryption(username)
        self.database["salvataggi"][str(self.NumberSaves() - 1)]["password"] = self.Encryption(password)
        self.ScritturaJSON(self.database)

    def ModSave(self, servizio, username, password, ind):
        self.database["salvataggi"][str(ind)]["servizio"] = self.Encryption(servizio)
        self.database["salvataggi"][str(ind)]["username"] = self.Encryption(username)
        self.database["salvataggi"][str(ind)]["password"] = self.Encryption(password)
        self.ScritturaJSON(self.database)

    def DeleteCard(self, cont):
        num = 0
        prov = {"username": self.database["username"], "password": self.database["password"], "salvataggi":{}}
        for ogg in self.database["salvataggi"]:
            if cont != int(ogg):
                prov["salvataggi"][str(num)] = self.database["salvataggi"][ogg]
                num += 1
        self.database = prov
        self.ScritturaJSON(self.database)

    def SearchEngine(self, word):
        lista = []
        for sal in self.database["salvataggi"]:
            se = self.Decryption(self.database["salvataggi"][sal]["servizio"])
            us = self.Decryption(self.database["salvataggi"][sal]["username"])
            ps = self.Decryption(self.database["salvataggi"][sal]["password"])
            if word in se.lower() or word in us.lower() or word in ps.lower():
                lista.append([se, us, ps, int(sal)])
        return lista

    def JSONFinder(self, username):
        contr = [False,""]
        if os.path.isdir("Accounts"):
            file_list = os.listdir("Accounts")
            for f_n in file_list:
                if os.path.splitext(f_n)[1] == ".json":
                    tabjson = json.loads(open("Accounts/" + f_n,"r").read())
                    if tabjson["username"] == username:
                        contr = [True, f_n]
        else:
            os.mkdir("Accounts")
        return contr
            
    def Encryption(self, data):      
        return self.LoadKey().encrypt(data.encode()).decode()
    
    def Decryption(self, data):
        try:      
            return self.LoadKey().decrypt(data.encode()).decode()
        except InvalidToken:
            return False
       
    def LoadKey(self):
        sha = hashlib.sha256((self.cred[0] + "@" +  self.cred[1]).encode()).digest()
        return Fernet(base64.urlsafe_b64encode(sha))

    def NumberSaves(self):
        return len(self.database["salvataggi"])

    def Reset(self):
        self.database = {}
        self.file = ""
        self.cred = ["",""]
