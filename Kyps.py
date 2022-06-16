from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QDialog ,QGraphicsDropShadowEffect, QGraphicsEffect, QGraphicsOpacityEffect ,QMessageBox ,QCheckBox, QGroupBox, QLabel, QLineEdit, QSizePolicy, QSpacerItem, QWidget, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QScrollArea,QGridLayout, QTableWidget,QListWidget,QGroupBox, QPushButton)
import sys
import importlib
from PyQt5.QtCore import QSize, Qt,QEvent
from qtwidgets import PasswordEdit

from cryptography.fernet import Fernet, InvalidToken
import json
import re
import hashlib
import os
import hashlib
import base64
import random

stylesheet = """
    QScrollBar::handle {
        background-color: #7582DF;
    }

    QScrollBar::add-line {
        border: none;
        background: none;
    }

    QScrollBar::sub-line {
        border: none;
        background: none;
    }
    """

class Accesso(QWidget):
    def __init__(self, k_eng,parent = None):
        super().__init__(parent)
        
        self.parent = parent
        self.k_eng = k_eng

        #FRAME COLORATO 
        frame = QFrame(self)
        frame.setStyleSheet('background-image: url("./Media/colb.jpg"); background-repeat: no-repeat;')
        frame.setGeometry(0 ,0, 315, 450)

        #FRAME2 BIANCO
        frame2 = QFrame(self)
        frame2.setStyleSheet("background-color: white; border-radius: 8px;")
        frame2.setGeometry(15, 15, 285, 420)

        self.vbox = QVBoxLayout(self)
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setSpacing(7)
        frame2.setLayout(self.vbox)

        #LABELS
        lab1 = QLabel("Inserisci l'username", self)
        lab2 = QLabel("Inserisci la password", self)
        lab3 = QLabel("oppure", self)
        titl = QLabel("Kyps", self)
        titl.setFont(QFont("Harlow Solid Italic", 30))
        titl.setAlignment(Qt.AlignCenter)
        lab3.setAlignment(Qt.AlignCenter)
        
        #TEXTFIELDS
        self.t1 = QLineEdit(self)
        self.t2 = PasswordEdit()
        self.t1.returnPressed.connect(self.Accesso)
        self.t2.returnPressed.connect(self.Accesso)
        
        #BUTTONS
        self.b1 = QPushButton("Accedi",self)
        self.b1.installEventFilter(parent)
        self.b2 = QPushButton("Iscriviti",self)
        self.b2.installEventFilter(parent)
        
        #CSS LABELS & STYLES
        titl.setStyleSheet("padding-bottom:15px; background-color:transparent;")
        lab3.setStyleSheet("color:#898889;")
        lab1.setFont(QFont("Roboto",10))
        lab2.setFont(QFont("Roboto",10))
        lab3.setFont(QFont("Roboto",10))

        #CSS BUTTON & STYLES
        self.b1.setStyleSheet("background-color:#E17BD6; color: white; border: none; border-radius: 5px; padding: 5px 5px;")
        self.b2.setStyleSheet("background-color:#E17BD6; color: white; border: none; border-radius: 5px; padding: 5px 5px;")
        self.b1.setFont(QFont("Roboto",10))
        self.b2.setFont(QFont("Roboto",10))
        self.b1.setFixedSize(150, 25)
        self.b2.setFixedSize(150, 25)
        
        #CSS ENTRYFIELDS
        self.t1.setStyleSheet("border-radius: 5px; border: 1px solid #BAB6BA; padding: 5px 5px;")
        self.t2.setStyleSheet("border-radius: 5px; border: 1px solid #BAB6BA; padding: 5px 5px;")
        self.t1.setObjectName("t1")
        self.t2.setObjectName("t2")
        self.t1.installEventFilter(self)
        self.t2.installEventFilter(self)
        
        #HBOX 1 & 2
        f1 = QFrame(self)
        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(self.b1)
        hbox1.setAlignment(Qt.AlignCenter)
        f1.setLayout(hbox1)
        f2 = QFrame(self)
        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(self.b2)
        hbox2.setAlignment(Qt.AlignCenter)
        f2.setLayout(hbox2)
        
        #ERROR LABELS
        self.lab4 = QLabel("", self)
        self.lab4.setFont(QFont("Roboto", 8))
        self.lab4.setStyleSheet("color: red; background-color:white;")
        self.lab5 = QLabel("", self)
        self.lab5.setFont(QFont("Roboto", 8))
        self.lab5.setStyleSheet("color: red; background-color:white;")
              
        #POSIZIONAMENTO WIDGETS
        self.vbox.addWidget(titl)
        self.vbox.addWidget(lab1)
        self.vbox.addWidget(self.t1)
        self.vbox.addWidget(self.lab4)
        self.vbox.addWidget(lab2) 
        self.vbox.addWidget(self.t2)
        self.vbox.addWidget(self.lab5)
        self.vbox.insertSpacing(10,20)
        self.vbox.addWidget(f1)  
        self.vbox.addWidget(lab3)
        self.vbox.addWidget(f2)

    def Accesso(self):
        username = self.t1.text()
        password = self.t2.text()
        if username != "" and password != "":
            contr, num, mess = self.k_eng.Accesso(username, password)
            if not contr:
                if num == 1:
                    self.lab4.setText(mess)
                    self.lab5.setText("")
                else:
                    self.lab5.setText(mess)
                    self.lab4.setText("")
            else:
                self.parent.LoadSchermataPrincipale()

    def eventFilter(self, obj, event):
         
        if obj.objectName() == "t1":
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.lab4.setText("")
        elif obj.objectName() == "t2":
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.lab5.setText("")
        return False
        
class Iscrizione(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.parent = parent

        #FRAME COLORATO 
        frame = QFrame(self)
        frame.setStyleSheet('background-image: url("./Media/colb.jpg"); background-repeat: no-repeat;')
        frame.setGeometry(0 ,0, 315, 450)

        #FRAME2 BIANCO
        frame2 = QFrame(self)
        frame2.setStyleSheet("background-color: white; border-radius: 8px;")
        frame2.setGeometry(15, 15, 285, 420)
        
        #LABELS
        lab1 = QLabel("Inserisci l'username", self)
        lab2 = QLabel("Inserisci la password", self)
        lab3 = QLabel("Riscrivi la password", self)
        titl = QLabel("Kyps", self)
        titl.setAlignment(Qt.AlignCenter)

        #BUTTONS
        self.b1 = QPushButton("Iscriviti",self)
        self.b1.installEventFilter(parent)
        self.b2 = QPushButton(self)
        self.b2.setIcon(QIcon("./Media/right-arrow.png"))
        self.b2.setIconSize(QtCore.QSize(32,32))

        #CSS BUTTON & STYLES
        self.b1.setStyleSheet("background-color:#E17BD6; color: white; border: none; border-radius: 5px; padding: 5px 5px;")
        self.b1.setFont(QFont("Roboto",10))      
        self.b2.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid #BAB6BA") 
        self.b2.setFixedSize(60, 40) 
        self.b2.installEventFilter(self)

        #TEXTFIELDS
        self.t1 = QLineEdit(self)
        self.t2 = PasswordEdit()
        self.t3 = PasswordEdit()
        self.t1.setObjectName("t1")
        self.t3.setObjectName("t3")
        self.t1.installEventFilter(self)
        self.t3.installEventFilter(self)
        self.t1.returnPressed.connect(self.Iscrizione)
        self.t2.returnPressed.connect(self.Iscrizione)
        self.t3.returnPressed.connect(self.Iscrizione)

        #CSS ENTRYFIELDS
        self.t1.setStyleSheet("border-radius: 5px; border: 1px solid #BAB6BA; padding: 5px 5px;")
        self.t2.setStyleSheet("border-radius: 5px; border: 1px solid #BAB6BA; padding: 5px 5px;")
        self.t3.setStyleSheet("border-radius: 5px; border: 1px solid #BAB6BA; padding: 5px 5px;")

        #ERROR LABELS
        self.lab4 = QLabel("", self)
        self.lab4.setFont(QFont("Roboto", 8))
        self.lab4.setStyleSheet("color: red; background-color:white;")
        self.lab5 = QLabel("", self)
        self.lab5.setFont(QFont("Roboto", 8))
        self.lab5.setStyleSheet("color: red; background-color:white;")
        
        #self.VBOX
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(titl)
        self.vbox.addWidget(lab1)
        self.vbox.addWidget(self.t1)
        self.vbox.addWidget(self.lab4)
        self.vbox.addWidget(lab2)
        self.vbox.addWidget(self.t2)
        self.vbox.addWidget(QLabel("",self))
        self.vbox.addWidget(lab3)
        self.vbox.addWidget(self.t3)
        self.vbox.addWidget(self.lab5)
        self.vbox.addWidget(self.b1,3, Qt.AlignBottom)
        self.vbox.addWidget(self.b2,5, Qt.AlignBottom)
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setSpacing(7)

        #CSS LABELS & STYLES
        titl.setStyleSheet("padding-bottom:15px; background-color:transparent;")
        titl.setFont(QFont("Harlow Solid Italic", 30))
        lab1.setFont(QFont("Roboto",10))
        lab2.setFont(QFont("Roboto",10))
        lab3.setFont(QFont("Roboto",10))

        frame2.setLayout(self.vbox)

        self.b1.clicked.connect(self.Iscrizione)

    def eventFilter(self, obj, event):
        if obj.objectName() != "t1" and obj.objectName() != "t3":
            if event.type() == QEvent.Enter:
                obj.setStyleSheet("background-color: #E8E8E8; border-radius: 5px; border: 1px solid #BAB6BA") 
            elif event.type() == QEvent.Leave:
                obj.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid #BAB6BA") 
        
        if obj.objectName() == "t1":
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.lab4.setText("")
        elif obj.objectName() == "t3":
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.lab5.setText("")
        return False

    def Iscrizione(self):
        username = self.t1.text()
        passwd1 = self.t2.text()
        passwd2 = self.t3.text()
        if username != "" and passwd1 != "" and passwd2 != "":
            contr, num, mess = self.parent.k_eng.Iscrizione(username, passwd1, passwd2)
            if not contr:
                if num == 1:
                    self.lab4.setText(mess)
                    self.lab5.setText("")
                else:
                    self.lab5.setText(mess)
                    self.lab4.setText("")
            else:
                self.lol = Pop(0)
                self.lol.exec_()
                self.lab5.setText("")
                self.lab4.setText("")
                self.t1.setText("")
                self.t2.setText("")
                self.t3.setText("")

    
        
        
                
class SchermataPrincipale(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.parent = parent

        self.Reset()

        #FRAME COLORATO 
        frame = QFrame(self)
        frame.setStyleSheet('background-image: url("./Media/colb.jpg"); background-repeat: no-repeat;')
        frame.setGeometry(0, 0, 800, 580)

        #FRAME BIANCO
        frame2 = QFrame(self)
        frame2.setStyleSheet("background-color:  #F3F3FD; border-radius: 5px;")
        frame2.setGeometry(10,10,780,540)

        #FRAME3 
        frame3 = QFrame(self)

        #VBOX
        self.vbox = QVBoxLayout(self)
        frame3.setLayout(self.vbox)
        
        #SCOLLAREA
        self.scroll = QScrollArea(self)
        self.scroll.setStyleSheet("border: none; background-color: #F3F3FD;")
        self.scroll.setWidget(frame3)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(110, 65, 680, 475)
        
        self.SearchBar()
        self.AddNos()
        self.AddPix()
        self.LettAddCards()
        self.AddButtons()
        
    def Reset(self):
        self.lista_cr = []
        self.plus = False
        self.botfr = [False, "", "", ""]
        self.ProvCardo()
        self.mod = [False, "", "", ""]
        self.cont = 0
        self.kk = False


    def LoadCard(self, serv, usern, passwd, plus, tag):
        frame = QFrame(self)
        frame.setObjectName(tag)
        st = "QFrame#" + tag + "{background-image: url('./Media/card1.jpg'); background-repeat: no-repeat;}"
        frame.setStyleSheet(st)    
        frame.setFixedSize(230,290)
        frame.installEventFilter(self)
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(15)
        vbox.setContentsMargins(20,20,0,0)
        
        service = QLineEdit(self)
        username = QLineEdit(self)
        password = PasswordEdit()

        service.installEventFilter(self)
        username.installEventFilter(self)
        password.installEventFilter(self)

        service.setFont(QFont("Roboto", 11))
        username.setFont(QFont("Roboto", 11))
        password.setFont(QFont("Roboto", 11))

        service.setStyleSheet("background-color: none; border-bottom: 2px solid #AC3AA5; padding-bottom: 5px;")
        username.setStyleSheet("background-color: none; border-bottom: 2px solid #AC3AA5; padding-bottom: 5px;")
        password.setStyleSheet("background-color: none; border-bottom: 2px solid #AC3AA5; padding-bottom: 5px;")

        lab1 = QLabel("Servizio", self)
        lab1.setFont(QFont("Courgette", 18,weight=QtGui.QFont.Bold))
        lab2 = QLabel("Username", self)
        lab2.setFont(QFont("Courgette", 18,weight=QtGui.QFont.Bold))
        lab3 = QLabel("Password", self)
        lab3.setFont(QFont("Courgette", 18,weight=QtGui.QFont.Bold))

        service.setFixedWidth(190)
        username.setFixedWidth(190)
        password.setFixedWidth(190)

        lab1.setAlignment(Qt.AlignCenter)
        lab2.setAlignment(Qt.AlignCenter)
        lab3.setAlignment(Qt.AlignCenter)

        lab1.setStyleSheet("background-color: none;")
        lab2.setStyleSheet("background-color: none;")
        lab3.setStyleSheet("background-color: none;")
        
        vbox.addWidget(lab1)
        vbox.addWidget(service)
        vbox.addWidget(lab2)
        vbox.addWidget(username)
        vbox.addWidget(lab3)
        vbox.addWidget(password)

        service.setObjectName(tag)
        username.setObjectName(tag)
        password.setObjectName(tag)

        if not plus:
            service.setText(serv)       
            username.setText(usern)       
            password.setText(passwd) 

            service.setReadOnly(True)
            username.setReadOnly(True)
            password.setReadOnly(True)
        else:
            self.LoadCardButtons(vbox, service, username, password, [False])

        frame.setLayout(vbox)
        return [frame, [service, username, password]]


    def LoadCardButtons(self, vbox, service, username, password, mod):
        but1 = QPushButton("Salva", self)
        but1.setStyleSheet("background-color: #763AAC; color: white; border-radius: 5px; font-size: 13px; padding: 3px;")
        but2 = QPushButton("Annulla", self)
        but2.setStyleSheet("background-color: #763AAC; color: white; border-radius: 5px; font-size: 13px; padding: 3px;")

        but1.setObjectName("salva")
        but2.setObjectName("annulla")

        if not mod[0]:
            self.plus = True
            but1.clicked.connect(lambda: self.Salva(service.text(),username.text(),password.text()))
            but2.clicked.connect(lambda: self.Annulla())
        else:
            but1.clicked.connect(lambda: self.SalvaMod(vbox, service, username, password, mod[1]))
            but2.clicked.connect(lambda: self.AnnullaMod(vbox, service, username, password))
            

        but1.installEventFilter(self)
        but2.installEventFilter(self)

        hbox = QHBoxLayout()
        hbox.addWidget(but2)
        hbox.addWidget(but1)

        frame_b = QFrame(self)
        frame_b.setLayout(hbox)

        frame_b.setStyleSheet("background-color: none;")
        frame_b.setFixedHeight(40)
        
        vbox.addWidget(frame_b)
        vbox.setSpacing(9)


    def AddCards(self, service, username, password, plus, keyb):
        
        hbox = QHBoxLayout()
        frame_hbox = QFrame(self)
        hbox.setSpacing(0)

        if plus:
            self.but.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid #8F6AAF; padding: 10px;") 
            self.but.setObjectName("None")
            self.labp.setParent(None)
           
        if len(self.lista_cr) > 0:
            for num, ogg in enumerate(self.lista_cr):
                if len(ogg) == 3:
                    self.prov_card.setParent(None)
                    fr = self.LoadCard(service, username, password, plus, 'card2_' + str(len(self.lista_cr) - 1))
                    self.lista_cr[num]["card2"] = {"frame":fr[0]}
                    self.LoadTextFields("card2", fr[1])
                    self.lista_cr[num]["card2"]["cont"] = self.cont if not keyb else keyb
                    self.cont += 1
                    self.lista_cr[num]["card2"]["vbox"] = fr[0].layout()
                    self.lista_cr[num]["hbox"].addWidget(self.lista_cr[num]["card2"]["frame"], Qt.AlignRight)
                   
                elif len(ogg) == 4 and len(self.lista_cr) == num + 1:
                    self.lista_cr.append({"hbox":hbox})
                    self.lista_cr[num + 1]["frame_hbox"] = frame_hbox
                    fr = self.LoadCard(service, username, password, plus, 'card1_' + str(len(self.lista_cr) - 1))
                    self.lista_cr[num + 1]["card1"] = {"frame":fr[0]}
                    self.lista_cr[num + 1]["card1"]["cont"] = self.cont if not keyb else keyb
                    self.cont += 1
                    self.LoadTextFields("card1", fr[1])
                    self.lista_cr[num + 1]["hbox"].addWidget(self.lista_cr[num + 1]["card1"]["frame"], Qt.AlignRight)
                    self.ProvCardo()
                    self.lista_cr[num + 1]["hbox"].addWidget(self.prov_card, Qt.AlignRight)
                    self.lista_cr[num + 1]["frame_hbox"].setLayout(self.lista_cr[num + 1]["hbox"])
                    self.lista_cr[num + 1]["card1"]["vbox"] = fr[0].layout()
                    self.vbox.addWidget(self.lista_cr[num + 1]["frame_hbox"])
                    break
        else:
            if not self.parent.k_eng.database["salvataggi"]:
                self.nos.move(-3000, 250)
            self.lista_cr.append({"hbox":hbox})
            self.lista_cr[0]["frame_hbox"] = frame_hbox
            fr = self.LoadCard(service, username, password, plus, 'card1_' + str(len(self.lista_cr) - 1))
            self.lista_cr[0]["card1"] = {"frame":fr[0]}
            self.lista_cr[0]["card1"]["cont"] = self.cont if not keyb else keyb
            self.cont += 1
            self.LoadTextFields("card1", fr[1])
            self.lista_cr[0]["hbox"].addWidget(self.lista_cr[0]["card1"]["frame"], Qt.AlignRight)
            self.lista_cr[0]["frame_hbox"].setLayout(self.lista_cr[0]["hbox"])
            self.vbox.addWidget(self.lista_cr[0]["frame_hbox"])
            self.lista_cr[0]["card1"]["vbox"] = fr[0].layout()

        QtCore.QTimer.singleShot(30, self.ScrollBottom)
        
    def ScrollBottom(self):
        try:
            last = self.vbox.itemAt(self.vbox.count()-1).widget()
            self.scroll.ensureWidgetVisible(last)
        except:
            None

    def LoadTextFields(self, card, items):
        self.lista_cr[len(self.lista_cr) - 1][card]["edit1"] = items[0]
        self.lista_cr[len(self.lista_cr) - 1][card]["edit2"] = items[1]
        self.lista_cr[len(self.lista_cr) - 1][card]["edit3"] = items[2]
        
    def ProvCardo(self):
        self.prov_card = QFrame(self)
        self.prov_card.setFixedSize(230, 290)
        self.prov_card.setStyleSheet("background-color: transparent;")

    def Salva(self, servizio, username, password):
        self.plus = False
        self.cont = 0
        self.but.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;")
        self.but.setObjectName("button")
        self.parent.k_eng.AddNewSave(servizio, username, password)
        self.RemoveAllItems()
        self.ProvCardo()
        self.LettAddCards()

    def SalvaMod(self, vbox, ser, use, pas, ind):
        self.parent.k_eng.ModSave(ser.text(), use.text(), pas.text(), ind)
        vbox.itemAt(vbox.count() - 1).widget().setParent(None)
        vbox.setSpacing(15)
        ser.setReadOnly(True)
        use.setReadOnly(True)
        pas.setReadOnly(True)
        self.mod = [False, "", "", ""]

    def Annulla(self):
        self.but.setObjectName("button")
        self.but.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;")
        self.plus = False
        if "card2" in self.lista_cr[len(self.lista_cr)-1]:
            self.lista_cr[len(self.lista_cr)-1]["card2"]["frame"].setParent(None)
            if len(self.lista_cr) > 1:
                self.ProvCardo()
                self.lista_cr[len(self.lista_cr)-1]["hbox"].addWidget(self.prov_card, Qt.AlignRight)
            del self.lista_cr[len(self.lista_cr)-1]["card2"]
        else:
            self.lista_cr[len(self.lista_cr)-1]["frame_hbox"].setParent(None)
            self.lista_cr.pop(len(self.lista_cr)-1)
        if not self.parent.k_eng.database["salvataggi"]:
            self.nos.move(300, 250)
        

    def AnnullaMod(self, vbox, ser, use, pas):
        vbox.itemAt(vbox.count() - 1).widget().setParent(None)
        vbox.setSpacing(15)
        ser.setText(self.mod[1])
        use.setText(self.mod[2])
        pas.setText(self.mod[3])
        ser.setReadOnly(True)
        use.setReadOnly(True)
        pas.setReadOnly(True)
        self.mod = [False, "", "", ""]

    def Elimina(self, but):
        if not self.botfr[0]:
            but.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid #8F6AAF; padding: 10px;") 
            but.setObjectName("None")
            self.botfr[0] = not self.botfr[0]
            self.botfr[1] = "del"
            self.botfr[2] = "#F9BBBE"
            self.botfr[3] = "./Media/card1_del.jpg"
        elif self.botfr[1] == "del":
            but.setObjectName("button")
            self.botfr[0] = not self.botfr[0]
            self.botfr[1] = ""

    def EliminaCard(self, tag):
        
        self.lol = Pop(1)
        self.lol.exec_()

        if self.lol.valore == 0:
            self.cont = 0
            card = tag.split("_")[0]
            ind = int(tag.split("_")[1])
            cont = self.lista_cr[ind][card]["cont"]

            self.RemoveAllItems()
            
            self.parent.k_eng.DeleteCard(cont)
            
            self.ProvCardo()
            self.LettAddCards()

    def Modifica(self, but):
        if not self.botfr[0]:
            but.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid #8F6AAF; padding: 10px;") 
            but.setObjectName("None")
            self.botfr[0] = not self.botfr[0]
            self.botfr[1] = "mod"
            self.botfr[2] = "#DDFFFE"
            self.botfr[3] = "./Media/card1_mod.jpg"
        elif self.botfr[1] == "mod" and self.mod[0] == False:
            but.setObjectName("button")
            self.botfr[0] = not self.botfr[0]
            self.botfr[1] = ""

    def ModificaClick(self, tag):
        if self.mod[0] == False:
            self.mod[0] = True
            card = tag.split("_")[0]
            ind = int(tag.split("_")[1])
            cont = self.lista_cr[ind][card]["cont"]
            cre = [self.lista_cr[ind][card]["edit1"], self.lista_cr[ind][card]["edit2"], self.lista_cr[ind][card]["edit3"]]
            cre[0].setReadOnly(False)
            cre[1].setReadOnly(False)
            cre[2].setReadOnly(False)
            self.mod = [True, cre[0].text(), cre[1].text(), cre[2].text()]
            self.ColorFrameEdit(self.lista_cr[ind][card]["frame"], "none", "./Media/card1.jpg")
            self.LoadCardButtons(self.lista_cr[ind][card]["vbox"], cre[0], cre[1], cre[2], [True, cont])

    def RemoveAllItems(self):   
        for cont in range(len(self.lista_cr)):
            self.lista_cr[cont]["frame_hbox"].setParent(None)
        self.lista_cr = []
        
    def LettAddCards(self):
        for ogg in self.parent.k_eng.database["salvataggi"]:
            servizio = self.parent.k_eng.Decryption(self.parent.k_eng.database["salvataggi"][ogg]["servizio"])
            username = self.parent.k_eng.Decryption(self.parent.k_eng.database["salvataggi"][ogg]["username"])
            password = self.parent.k_eng.Decryption(self.parent.k_eng.database["salvataggi"][ogg]["password"])
            if servizio != False and username != False and password != False:
                self.AddCards(servizio, username, password, False, False)
            else:
                self.AddCards("corrupt!", "corrupt!", "corrupt!", False, False)
        if not self.parent.k_eng.database["salvataggi"]:
            self.nos.move(300, 275)
        else:
            self.nos.move(-3000, 275)
            self.search_bar.setText("")

    def SearchBar(self):
        self.search_bar = QLineEdit(self)
        self.search_bar.setStyleSheet("border-radius: 5px; border: 1px solid #BAB6BA; padding: 7px 7px; background-color:#F3F3FD ")
        self.search_bar.setMinimumWidth(400)
        self.search_bar.setObjectName("search_bar")
        self.search_bar.installEventFilter(self)
        self.search_bar.move(20, 20)
        self.search_button = QPushButton(self)
        self.search_button.setIcon(QIcon("./Media/search.png"))
        self.search_button.setIconSize(QtCore.QSize(20, 20))
        self.search_button.setStyleSheet("background-color:#F3F3FD; border: none;")
        self.search_button.move(390, 25)
    
    def AddNos(self):
        self.nos = QLabel("Ancora nessun salvataggio", self)
        self.nos.setFont(QFont("Courgette", 18,weight=QtGui.QFont.Bold))

    def AddPix(self):
        pix = QPixmap("./Media/error.png")
        self.labp = QLabel(None)
        self.labp.setPixmap(pix)
        self.labp.setStyleSheet("padding-left: 240px;")
        
    def AddButtons(self):
        vbox = QVBoxLayout()
        frame = QFrame(self)
        frame.setLayout(vbox)

        self.but = QPushButton()
        self.but.setIcon(QIcon("./Buttons/plus.png"))
        self.but.setIconSize(QtCore.QSize(40,40))
        but1 = QPushButton()
        but1.setIcon(QIcon("./Buttons/compose.png"))
        but1.setIconSize(QtCore.QSize(40,40))
        but2 = QPushButton()
        but2.setIcon(QIcon("./Buttons/delete.png"))
        but2.setIconSize(QtCore.QSize(40,40))
        but3 = QPushButton()
        but3.setIcon(QIcon("./Buttons/exit.png"))
        but3.setIconSize(QtCore.QSize(40,40))

        self.but.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;") 
        but1.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;") 
        but2.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;") 
        but3.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;") 

        self.but.installEventFilter(self)
        but1.installEventFilter(self)
        but2.installEventFilter(self)
        but3.installEventFilter(self)
        
        self.but.setObjectName("button")
        but1.setObjectName("button")
        but2.setObjectName("button")
        but3.setObjectName("button")

        self.but.clicked.connect(lambda: self.AddCards(None, None, None, True, False) if self.plus == False and self.botfr[0] == False  else None)
        but3.clicked.connect(self.Exit)
        but2.clicked.connect(lambda: self.Elimina(but2) if self.botfr[1] != "mod" and self.plus == False else None)
        but1.clicked.connect(lambda: self.Modifica(but1) if self.botfr[1] != "del" and self.plus == False else None)
        
        vbox.addWidget(self.but)
        vbox.addWidget(but1)
        vbox.addWidget(but2)
        vbox.addWidget(but3)

        vbox.setSpacing(30)

        frame.setGeometry(15, 65, 100, 475)

    def Exit(self):
        self.parent.LoadAccesso()

    def eventFilter(self, ogg, event):
        if event.type() == QEvent.Enter:
            if ogg.objectName() == "button":
                ogg.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid #8F6AAF; padding: 10px;") 
            elif ogg.objectName()[0:4] == "card" and self.botfr[0] == True and self.mod[0] == False:
                self.ColorFrameEdit(ogg, self.botfr[2], self.botfr[3])
            elif ogg.objectName() == "salva" or ogg.objectName() == "annulla":
                ogg.setStyleSheet("background-color: #8F6AAF; color: white; border-radius: 5px; font-size: 13px; padding: 3px;")
        elif event.type() == QEvent.Leave:
            if ogg.objectName() == "button":
                ogg.setStyleSheet("background-color: #F3F2FD; border-radius: 5px; border: 1px solid #BAB6BA; padding: 10px;")
            elif ogg.objectName()[0:4] == "card" and self.botfr[0] == True and self.mod[0] == False:
                if not isinstance(ogg, QLineEdit) and not isinstance(ogg, PasswordEdit):
                    color = "none"
                    img = "./Media/card1.jpg"
                else:
                    color = self.botfr[2]
                    img = self.botfr[3]
                self.ColorFrameEdit(ogg, color, img)
            elif ogg.objectName() == "salva" or ogg.objectName() == "annulla":
                ogg.setStyleSheet("background-color: #763AAC; color: white; border-radius: 5px; font-size: 13px; padding: 3px;")
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if ogg.objectName()[0:4] == "card" and self.botfr[0] == True:
                if self.botfr[1] == "mod":
                    self.ModificaClick(ogg.objectName())
                elif self.botfr[1] == "del":    
                    QtCore.QTimer.singleShot(30, lambda: self.EliminaCard(ogg.objectName()))
        if event.type() == QtCore.QEvent.KeyRelease:
            if ogg.objectName() == "search_bar":
                if self.search_bar.text() != "":
                    self.Search()
                    self.kk = True
                elif self.kk:
                    self.labp.setParent(None)
                    self.update()
                    self.kk = False
                    self.RemoveAllItems()
                    self.ProvCardo()
                    self.cont = 0
                    self.LettAddCards()
                    
        return False

    def Search(self):
        self.RemoveAllItems()
        self.ProvCardo()
        self.cont = 0
        lista = self.parent.k_eng.SearchEngine(self.search_bar.text().lower())
        for ogg in lista:
            self.AddCards(ogg[0], ogg[1], ogg[2], False, ogg[3])
        if not lista:
            self.labp.setParent(self)
            self.update()
            self.vbox.addWidget(self.labp)
            self.nos.move(-3000, 250)
        else:
            self.labp.setParent(None)
            self.update()


    def ColorFrameEdit(self, ogg, color, image):
        self.lista_cr[int(ogg.objectName().split("_")[1])][ogg.objectName().split("_")[0]]["frame"].setStyleSheet('QFrame#' + ogg.objectName() + '{background-image: url(' + image + '); background-repeat: no-repeat;}')
        self.lista_cr[int(ogg.objectName().split("_")[1])][ogg.objectName().split("_")[0]]["edit1"].setStyleSheet("background-color: " + color + "; border-bottom: 2px solid #AC3AA5; padding-bottom: 5px;")
        self.lista_cr[int(ogg.objectName().split("_")[1])][ogg.objectName().split("_")[0]]["edit2"].setStyleSheet("background-color: " + color + "; border-bottom: 2px solid #AC3AA5; padding-bottom: 5px;")
        self.lista_cr[int(ogg.objectName().split("_")[1])][ogg.objectName().split("_")[0]]["edit3"].setStyleSheet("background-color: " + color + "; border-bottom: 2px solid #AC3AA5; padding-bottom: 5px;")

class Engine(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Kyps") 
        self.setWindowIcon(QtGui.QIcon("./Media/padlock.png"))
        self.setIconSize(QtCore.QSize(512,512))
        self.k_eng = importlib.import_module("KypsEngine").Engine()
        self.LoadAccesso()

    def LoadAccesso(self):
        self.AccOgg = Accesso(self.k_eng, self)
        self.setFixedSize(315, 450)
        self.setCentralWidget(self.AccOgg)
        self.AccOgg.b2.clicked.connect(self.LoadIscrizione)
        self.AccOgg.b1.clicked.connect(self.AccOgg.Accesso)
        self.show()

    def LoadIscrizione(self):
        self.IscrOgg = Iscrizione(self)
        self.setCentralWidget(self.IscrOgg)
        self.IscrOgg.b2.clicked.connect(self.LoadAccesso)
        self.show()

    def LoadSchermataPrincipale(self):
        self.SchrPr = SchermataPrincipale(self)
        self.setFixedSize(800,560)
        self.setCentralWidget(self.SchrPr)
        self.show()

    def eventFilter(self, ogg, event):
        
        if event.type() == QEvent.Enter:
            ogg.setStyleSheet("background-color:#E188D8; color: white; border: none; border-radius: 5px; padding: 5px 5px;")
        elif event.type() == QEvent.Leave:
            ogg.setStyleSheet("background-color:#E17BD6; color: white; border: none; border-radius: 5px; padding: 5px 5px;")

        return False

class Pop(QDialog):
    def __init__(self, mode, parent = None):
        super().__init__(parent)

        self.setFixedSize(430, 200)
        self.valore = -1
        
        #FRAME COLORATO 
        frame = QFrame(self)
        frame.setStyleSheet('background-image: url("./Media/pop.jpg"); background-repeat: no-repeat;')
        frame.setGeometry(0, 0, 430, 200)

        #FRAME2 BIANCO
        frame2 = QFrame(self)
        frame2.setStyleSheet("background-color: white;")
        frame2.setGeometry(10, 10, 410, 180)

        self.setWindowTitle("Kyps") 
        self.setWindowIcon(QtGui.QIcon("./Media/padlock.png"))

        if mode == 0:
            self.Iscrizione()
        elif mode == 1:
            self.Delete()
  
    def Delete(self):
        self.but1 = QPushButton("Si", self)
        self.but1.setStyleSheet("QPushButton:hover{background-color:#E188D8;} QPushButton{background-color:#E17BD6;color: white; border: none; border-radius: 5px; padding: 5px 5px;} ")
        self.but1.resize(80, 30)
        self.but1.clicked.connect(lambda: self.SiNo(0))
        self.but2 = QPushButton("No", self)
        self.but2.setStyleSheet("QPushButton:hover{background-color:#E188D8;} QPushButton{background-color:#E17BD6;color: white; border: none; border-radius: 5px; padding: 5px 5px;} ")
        self.but2.resize(80, 30)
        self.but2.clicked.connect(lambda: self.SiNo(1))
        self.label = QLabel("Sicuro di eliminare?", self)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Roboto", 11))
        self.label.move(120,75)
        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("./Media/question.png"))
        self.lab.move(40, 48)
        self.lab.resize(64,64)
        self.but1.move(220, 150)
        self.but2.move(320, 150)

    def Iscrizione(self):
        self.but1 = QPushButton("OK", self)
        self.but1.setStyleSheet("QPushButton:hover{background-color:#E188D8;} QPushButton{background-color:#E17BD6;color: white; border: none; border-radius: 5px; padding: 5px 5px;} ")
        self.but1.resize(80, 30)
        self.but1.clicked.connect(self.Ok)
        self.label = QLabel("Iscrizione completata!", self)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Roboto", 11))
        self.label.move(120,75)
        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("./Media/check.png"))
        self.lab.move(40, 48)
        self.lab.resize(64,64)
        self.but1.move(320, 150)

    def Ok(self):
        self.accept()

    def SiNo(self, mode):
        self.valore = mode
        self.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("./Media/Roboto-Regular.ttf")
    QtGui.QFontDatabase.addApplicationFont("./Media/Courgette-Regular.ttf")
    App.setStyle("Fusion")
    App.setStyleSheet(stylesheet)
    eng = Engine()
    sys.exit(App.exec_())