#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
## Autor     : Marcel Nogueira d' Eurydice
## Empresa   : Eyetec
## Descricao :
## Modificado: Klausner Augusto
## Motivo    : Mostrar um temporizador ao desligar
## Modificado: Lucas Castro
## Motivo    : Corrigido Bug Alterar distância. Legenda Glaucoma.
##             Exibir mensagem ao atualizar proteção de tela.
############################################################################
from TADisplayImage import TADisplayImage
from TAExamScene import TAExamScene
from TASettings  import TASettings
from TAScSaverManager import TAScSaverPicsUpdate
from TACPUCheck import TACPUCheck

from PyQt4.QtCore import Qt,QTimer,QObject,SIGNAL
from PyQt4.QtGui import QGraphicsView,QMatrix,QBrush,QImage,QBrush,QColor,QApplication

import os,pickle,time
import  OPi.GPIO as GPIO
#import RPi.GPIO as GPIO
import subprocess
import sys
import shutil
import thread

app = QApplication(sys.argv)


class TAView(QGraphicsView):
    """
    """

    optotype_size = 300

    def __init__(self,scene):
        """

        Arguments:
        -`scene`:
        """

	#psk_home = "SERIAL_NUMBER"
	#psk = subprocess.check_output("lshw -c network | grep -v '12345' | grep 'serial' | head -1 | sed 's/ //g'", shell=True).decode("utf-8")[:-1]

	#if psk_home == psk:
	#	print("sucess. continuing...")
	#else:
	#	shutil.rmtree('/home/eyetec', ignore_errors=True)
	#	sys.exit()

	
        self.blue = 'PD18'
        self.red = 'PL02'
        self.green = 'PL03'
        self.ir = 'PD26'
       # self.rele ='PL08'
	
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.SUNXI)   
        ## Use board pin numbering
        GPIO.setup(self.ir, GPIO.OUT)
        GPIO.output(self.ir,False)
        GPIO.setup(self.blue,GPIO.OUT)
        GPIO.output(self.blue,False)
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.output(self.red,False)
        GPIO.setup(self.green,GPIO.OUT)
        GPIO.output(self.green,False)
        #GPIO.setup(self.rele,GPIO.OUT)
        #GPIO.output(self.rele,self.releon)
        #Iniciando o led verde para ligado
        GPIO.output(self.green, True)


        #Variavel que verifica se está desligado
        self.off = False;
        #self.standby = False;
        super(TAView, self).__init__(scene)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._settings = TASettings()

        self.centerOn(0,0)

        self._distanceMatrix = self.matrix()

        #self._SDtimer = QTimer()
        #self._SDtimer.setSingleShot(True)

	#self._TimeEllapsed = QTimer()
	#self._TimeEllapsed.setSingleShot(True)
	#QObject.connect(self._TimeEllapsed, SIGNAL("timeout()"), self.Tick)
	#self._contagem = 22
	#self._cancelShutdown = False
	#self._loadingShutdown = False

        self._SUptimer = QTimer()
        self._SUptimer.setSingleShot(True)
        QObject.connect(self._SUptimer,SIGNAL("timeout()"),self.TARestart)

        self._SDtimerConfirm = QTimer()
        self._SDtimerConfirm.setSingleShot(True)

        self._holdBtPressTimer = QTimer()
        self._holdBtPressTimer.setSingleShot(True)

        # Menu Flags
        self._Menu = False
        self._distanceSetUp = False
        self._calibrationSetUp = False
        self._screensaverOnOff = False
        self._menuSuccess = True

        self._distance = 6.0
        self._factorCalibration = 1

        # Programing Banks

        self._Programming  = False
        self._bankSelected = False
        self._bankAccess   = False
        self._bankIndex    = 0

        self.loadDistance()
        self.loadCalibration()
        self.setDistance()
        self.loadBanks()


       # self.checkMachine()

    def checkMachine(self):
        cp = TACPUCheck()
        print
        if not cp.checkCPU():
            os.system("sudo shutdown -h now")
            exit()


    def setDistance(self):
        m11 = (self._distance/6.0)/self._factorCalibration
        self._distanceMatrix = QMatrix(m11,0,0,m11,0,0)
        self.setMatrix(self._distanceMatrix)
        self.scene()._notify.setMatrix(QMatrix(1.0/m11,0,0,1.0/m11,0,0))


    def changeDistance(self, sign):

        self._distance += sign*0.1

        if self._distance<=0.3:
            self._distance = 0.3

        if self._distance>=7.0:
            self._distance = 7.0


        m11 = (self._distance/6.0)/self._factorCalibration

        self._distanceMatrix = QMatrix(m11,0,0,m11,0,0)

        self.setMatrix(self._distanceMatrix)

        self.scene()._notify.setMatrix(QMatrix(1.1/m11,0,0,1.1/m11,0,0))
        self.scene().notify(u"Distância %.1f m. Pressione Enter para confirmar a alteração."%(self.matrix().m11()*6*self._factorCalibration))

    def changeCalibration(self, sign):

        m11 = self._distanceMatrix.m11()

        m11 += sign*0.01


        if m11<=0.2:
            m11= 0.2
        if m11>=1.8:
            m11=1.8

        self._distanceMatrix = QMatrix(m11,0,0,m11,0,0)

    def menuEvent(self,event):
        """
        Arguments:
        - `self`:
        - `event`:
        """
        if event.key() == Qt.Key_E: # Enter

            if self.scene()._actualSlide == "Menu":
                option = None
                option = self.scene()._slideDict[self.scene()._actualSlide].getSelection()

                if option:
                    self._menuOption = {
                        "Distance"    : self.setupDistance,
                        "Calibration" : self.setupCalibration,
                        "ScreenSaver" : self.setupScreenSaver,
                        "DisplayImage": self.setupDisplayImage,
			"ScreenOnOff" : self.setupScreenOnOff,
			"SaveConf"    : self.setupSave
                        }[option]
                    self._menuOption()
            else:
                self._menuOption()


        elif event.key() in [Qt.Key_Left,
                             Qt.Key_Right,]:

            if self._distanceSetUp:
                sign = {
                    Qt.Key_Left   : -1,
                    Qt.Key_Right  :  1
                    }[event.key()]
                self.changeDistance(sign)
            elif self._calibrationSetUp:
                sign = {
                    Qt.Key_Left   : -1,
                    Qt.Key_Right  :  1
                    }[event.key()]
                self.changeCalibration(sign)
            else:
                {
                    Qt.Key_Left  : self.scene().previousSlide,
                    Qt.Key_Right : self.scene().nextSlide,
                    }[event.key()]()
                option = None
                option = self.scene()._slideDict[self.scene()._actualSlide].getSelection()
                if option:
                    NOTIFICATION = {
                        "Distance"    : u"Selecione a distância de operação do equipamento.",
                        "Calibration" : u"Calibração da unidade de projeção dos optótipos.",
                        "ScreenSaver" : u"Aperte 'Entra' para copiar as imagens a serem exibidas.",
                        "DisplayImage": u"Aperte 'Entra' para exibir imagens continas no pendrive.",
		        "ScreenOnOff" : u"Aperte 'Entra' Ativar ou Desativar Protecao de tela.",
			"SaveConf"    : u"Aperte 'Entra' para salvar as alterações"
                        }[option]
                self.scene().notify(NOTIFICATION,Qt.black)

    def setupDistance(self):
        """
        """
        if self._distanceSetUp:
            self.scene().setExam("Menu")
            self._distanceSetUp = False

            #FILE = file("/home/eyetec/.TA3rdG/distance.pkl","w")
	    #os.system("sudo gedit /home/.TA3rdG/eyetec/distance.pkl")
            FILE = file("/home/eyetec/.TA3rdG/distance.pkl","w")
            pickle.dump(self._distance,FILE)
            FILE.close()
            self._menuSuccess = True
            #self.scene().notify(u"Sistema sera reinciado ",Qt.darkGreen)
            #thread.start_new_thread(self.TARestartAsync,()) 	
	    self.msgAlterado()	
	
        else:
            self.scene().setExam("HOTV")
            self._distanceSetUp = True
            self._menuSuccess = False



    def TARestartAsync(self):
         for i in range(0,200000):
             print(i)

         os.system("sudo shutdown -r now")
	
     
    def setupSave(self):
	self.scene().notify(u"Sistema será reinciado ",Qt.darkGreen)
        thread.start_new_thread(self.TARestartAsync,()) 	
	

    def setupCalibration(self):
        """
        """

        if self._calibrationSetUp:
            self.scene().setExam("Menu")

            self._factorCalibration = 1.0/self._distanceMatrix.m11()

            self._distance = self._oldDistance

            m11 = (self._distance/6.0)/self._factorCalibration
            self._distanceMatrix = QMatrix(m11,0,0,m11,0,0)
            self.scene()._notify.setMatrix(QMatrix(1.0/m11,0,0,1.0/m11,0,0))

            #FILE = file("/home/eyetec/.TA3rdG/calibration.pkl","w")
            FILE = file("/home/eyetec/.TA3rdG/calibration.pkl","w")
            pickle.dump(self._factorCalibration,FILE)
            FILE.close()

            self._calibrationSetUp = False
            self._menuSuccess = True
            #self.scene().notify(u"Sistema sera reinciado ",Qt.darkGreen)
            #thread.start_new_thread(self.TARestartAsync,()) 
	    self.msgAlterado()

        else:

            self.scene().setExam("Calibration")
            self._calibrationSetUp  = True
            self._oldDistance    = self._distance
            self._distance       = 6.0

            m11 = 1.0/self._factorCalibration
            self._distanceMatrix = QMatrix(m11,0,0,m11,0,0)
            self.setMatrix(self._distanceMatrix)
            self._menuSuccess = False
            #self.updateSettings()


    def setupScreenSaver(self):
        """
        """
        self.scene()._notify.setMatrix(QMatrix(1,0,0,1,0,0))
        self.scene().notify(u"Atualização de imagens iniciada...    ")
        app.processEvents()

        sc = TAScSaverPicsUpdate()
        if sc.checkPicsDirectory():
            self.scene().notify(u"Imagens de proteção atualizadas.")
            os.system("sync")
            #self.scene().notify(u"Sistema sera reinciado ",Qt.darkGreen)
            #thread.start_new_thread(self.TARestartAsync,()) 
	    self.msgAlterado()
        else:
            self.scene().notify(u"Não foi possível atualizar as imagens de proteção de tela. Dados não encontrados.",Qt.red)


    def setupDisplayImage(self):
        """
        """
        su = TADisplayImage()
		       
        if su.checkPicsDirectory():

            self.scene().notify(u"", Qt.black)
            self.scene().createCustomSlide(path=su.picsDirectory)
        
            self._Menu = False
            self._bankAccess = False

            self._settings.unsetMask()

            self.scene().setExam("Menu")
            self.scene().setExam("DisplayImage")


        else:
            self.scene().notify(u"Não foi possível mostrar imagens do pendrive. Imagens não encontradas.",Qt.red)      

  
    def setupScreenOnOff(self):
         """
         """
                  
         #self.scene().notify(u"Ligando ")
         #app.processEvents()
  	

         word='mode:off'
	 with open("/home/eyetec/.xscreensaver","r") as fp:
             if word in fp.read():
	        achou = 1
             else:
                achou = 0

         if  achou ==0 :
  	    os.system("sed -i 's/mode:one/mode:off/g' /home/eyetec/.xscreensaver")
            self.scene().notify(u"Protecao de tela  DESLIGADA ")

         else:
	    os.system("sed -i 's/mode:off/mode:one/g' /home/eyetec/.xscreensaver")
            self.scene().notify(u"Protecao de tela LIGADA TEMPO 10 MIN")
        


    def TARestart(self):
        """

        Arguments:
        - `self`:
        """
        self.scene().notify(u"Sistema será reinciado ",Qt.darkGreen)
        time.sleep(0.05)
        os.system("sudo shutdown -r +1")

    def msgAlterado(self):
        self.scene().notify(u"Foram detectadas alterações no sistema.Pressione Enter no botão salvar para aplica-las.",Qt.red)    	

    def keyPressEvent(self,event):
        """

        Arguments:
        - `self`:
        """
    	GPIO.output(self.ir,True)
    	time.sleep(0.05)
    	GPIO.output(self.ir,False)
        
	if self.off == True:
            #os.system("sudo /opt/vc/bin/tvservice -p; sudo chvt 6; sudo chvt 7;")
            #os.system("sudo xset dpms force on")
            os.system("sudo echo on> /sys/class/drm/card0-HDMI-A-1/status")
            
            #os.system("sudo systemctl suspend;")
            self.scene().setVisible()
            self.off = False
            GPIO.output(self.green,True)
            GPIO.output(self.red,False)
            self.scene().setExam("Letter")

        if 1==1:
            #not self._holdBtPressTimer.isActive():
            #self._holdBtPressTimer.start(200)

            if  self._menuSuccess and  event.key() == Qt.Key_Y and self.off == False:
                #os.system("sudo /opt/vc/bin/tvservice -o")
                #os.system("sudo xset +dpms")

                GPIO.output(self.red,True)
                GPIO.output(self.green, False)
		
		#for i in range(1):
		#  os.system("sudo xset dpms force off;")
	
		os.system("sudo echo off> /sys/class/drm/card0-HDMI-A-1/status")
       	        #time.sleep(4)               
                #os.system("sudo shutdown -h now")		
		#print('respondeu o controle')
                self.off = True
                #GPIO.output(self.rele,False)
                #self.releon = False

            elif self._menuSuccess and event.key() in [Qt.Key_Z,
                                 Qt.Key_X,
                                 Qt.Key_C,
                                 Qt.Key_V,
                                 Qt.Key_B,
                                 Qt.Key_A,
                                 Qt.Key_S,
                                 Qt.Key_D,
                                 Qt.Key_F,
                                 Qt.Key_1,
                                 Qt.Key_2,
                                 Qt.Key_3,
                                 Qt.Key_4,
                                 Qt.Key_5,
                                 Qt.Key_6,
                                 Qt.Key_7,
                                 Qt.Key_8,
                                 Qt.Key_9,
                                 Qt.Key_0,
                                 Qt.Key_H,
                                 Qt.Key_U,
			         Qt.Key_T
                                 ]:
                exam = {
                    Qt.Key_Z : "Child" ,
                    Qt.Key_X : "Letter",
                    Qt.Key_C : "Number",
                    Qt.Key_V : "Landolt",
                    Qt.Key_B : "EChart",
                    Qt.Key_A : "Clock",
                    Qt.Key_S : "EDTRS",
                    Qt.Key_D : "HOTV",
                    Qt.Key_F : "Animate",
                    Qt.Key_1 : "4Balls",
                    Qt.Key_2 : "Amsler",
                    Qt.Key_3 : "Ishihara",
                    Qt.Key_4 : "FixPoint",
                    Qt.Key_5 : "RedGreen",
                    Qt.Key_6 : "vBar",
                    Qt.Key_7 : "3D",
                    Qt.Key_8 : "Tortion",
                    Qt.Key_9 : "Cataracta",
                    Qt.Key_0 : "Cylinder",
                    Qt.Key_H : "Help",
                    Qt.Key_U : "Info",
		    Qt.Key_Q : "Letter"
                    }[event.key()]

                self._Menu       = False
                self._bankAccess = False

                self._settings.unsetMask()
                self.scene().setExam(exam)

                if ("DisplayImage" in self.scene()._slideDict):
                    self.scene().deleteSlideFromSlidDict("DisplayImage")
            elif  self._menuSuccess and  event.key() == Qt.Key_M: # Menu

                self._Menu = True

                self._settings.unsetMask()
                self.scene().setExam("Menu")

            elif self._menuSuccess and event.key() == Qt.Key_F10:
                caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',"..","inicia_campo.sh"))
                os.execvp("bash", ["bash", caminho])

            elif self._menuSuccess and event.key() == Qt.Key_J:  # Change Optotypes Sizes

                self._settings.toggleScale

                # possible states sizes of the optotype
                if self.optotype_size == 300:
                    self.optotype_size = 150
                elif self.optotype_size == 150:
                    self._settings.setScale(False)
                    self.optotype_size = 1
                else:
                    self._settings.setScale(True)
                    self.optotype_size = 300

                self.updateSettings()

                self.scene().updateSSquareSize(self.optotype_size)
                self.update()


            elif  event.key() == Qt.Key_E: # Enter
                if self._Menu:
                    self.menuEvent(event)
                elif self._Programming:
                    self.appendSlideinBank()


            elif event.key() in [Qt.Key_Left,
                                 Qt.Key_Right,]:

                if not self._Menu and not self._bankAccess:
                    {
                        Qt.Key_Left  : self.scene().previousSlide,
                        Qt.Key_Right : self.scene().nextSlide,
                        }[event.key()]()

                    self._settings.unsetMask()

                elif self._Menu:
                    self.menuEvent(event)
                elif self._bankAccess:
                    self.bankAccessEvent(event)

            elif self._menuSuccess and not "DisplayImage" in self.scene()._slideDict and event.key() in [Qt.Key_Up,
                                 Qt.Key_Down]:
                changeMask = {
                    Qt.Key_Up    : self.scene().previousMask,
                    Qt.Key_Down  : self.scene().nextMask,
                    }[event.key()]

                self._settings.setMask()
                changeMask()

            elif self._menuSuccess and  event.key() in [Qt.Key_K,
                                 Qt.Key_L,
                                 Qt.Key_I,
                                 Qt.Key_O,
                                 Qt.Key_G,
                                 Qt.Key_Y,
                                 Qt.Key_N,
                                 Qt.Key_T
                                 ]:
                {
                    Qt.Key_K       : self.decreaseContrast,
                    Qt.Key_L       : self.increaseContrast,
                    Qt.Key_I       : self.decreaseBrightness,
                    Qt.Key_O       : self.increaseBrightness,
                    Qt.Key_G       : self._settings.toggleRGBYMask,
                    Qt.Key_N       : self._settings.toggleNegative,
                    Qt.Key_T       : self.reset
                    }[event.key()]()

                self.updateSettings()

            elif self._menuSuccess and  event.key() == Qt.Key_P:
                if self._Programming:
                    self.saveBank()
                else:
                    self._Programming = True
                    self.scene().notify(u"Programando:",Qt.darkGreen)

            elif self._menuSuccess and  event.key() in [Qt.Key_F1,
                                 Qt.Key_F2,
                                 Qt.Key_F3,
                                 Qt.Key_F4
                                 ]:

                self._prgBank = {Qt.Key_F1 : "P1",
                                 Qt.Key_F2 : "P2",
                                 Qt.Key_F3 : "P3",
                                 Qt.Key_F4 : "P4"
                                 }[event.key()]
                if self._Programming:
                    if not self._bankSelected:
                        self.programBank()
                else:
                    self.accessBank()

           #elif event.key() == Qt.Key_Q: # Liga Glare
                #if self.releon  == False:
                        #GPIO.output(self.rele,True)
                        #self.releon = True
                #else:
                        #GPIO.output(self.rele,False)
                        #self.releon = False

            else:
                if self.scene()._actualSlide != "Clock":
                    self.scene().randomizeSlide()

            if not self._Menu and not self._menuSuccess:
                self._distance = self._oldDistance
                m11 = (self._distance/6.0)
                self._distanceMatrix = QMatrix(m11,0,0,m11,0,0)
                self.scene()._notify.setMatrix(QMatrix(1.1/m11,0,0,1.1/m11,0,0))
                self._menuSuccess      = True
                self._distanceSetUp    = False
                self._calibrationSetUp = False
            self.updateSettings()


    def loadDistance(self):
        """
        """
        if os.path.isfile("/home/eyetec/.TA3rdG/distance.pkl"):
            FILE = file("/home/eyetec/.TA3rdG/distance.pkl","r")
            self._distance = pickle.load(FILE)
            FILE.close()
        else:
            self._distance = 6.0


    def loadCalibration(self):
        """
        """
        if os.path.isfile("/home/eyetec/.TA3rdG/calibration.pkl"):
            FILE = file("/home/eyetec/.TA3rdG/calibration.pkl","r")
            self._factorCalibration = pickle.load(FILE)
            FILE.close()
        else:
            self._factorCalibration = 1.0



    def loadBanks(self):
        """
        """
        if os.path.isfile("/home/eyetec/.TA3rdG/savedbank.pkl"):
            FILE = file("/home/eyetec/.TA3rdG/savedbank.pkl","r")
            self._programmingBank = pickle.load(FILE)
            FILE.close()
        else:
            self._programmingBank = {
            "P1" : [],
            "P2" : [],
            "P3" : [],
            "P4" : []
            }


    def saveBank(self):
        """
        """

        FILE = file("/home/eyetec/.TA3rdG/savedbank.pkl","w")
        pickle.dump(self._programmingBank,FILE)
        FILE.close()
        self._Programming  = False
        self._bankSelected = False

        N = len(self._programmingBank[self._prgBank])
        self.scene().notify(u"%d slides gravados no banco %s."%(N,self._prgBank),Qt.darkGreen)
        self.scene().notify(u"Sistema sera reinciado ",Qt.darkGreen)
        thread.start_new_thread(self.TARestartAsync,()) 


    def programBank(self):
        """
        """
        self.scene().notify(u"Banco %s selecionado."%self._prgBank,Qt.darkGreen)
        self._programmingBank[self._prgBank] = []
        self._bankSelected = True

    def accessBank(self):
        """
        """
        self._bankIndex  = 0
        self.loadBankSlide()

        self._bankAccess = True

    def appendSlideinBank(self):
        """
        """

        slide       = self.scene()._actualSlide
        slideStatus = self.scene()._slideDict[slide].getStatus()
        settings    = self._settings.getSettings()

        self._programmingBank[self._prgBank].append([slide,slideStatus,settings])

        N = len(self._programmingBank[self._prgBank])
        self.scene().notify(u"%d⁰ Slide incluído no banco %s."%(N,self._prgBank),Qt.darkGreen)

    def bankAccessEvent(self,event):
        """
        Arguments:
        - `event`:
        """
        direction = {
            Qt.Key_Left   : -1,
            Qt.Key_Right  :  1
            }[event.key()]
        if len(self._programmingBank[self._prgBank])>0:
            self._bankIndex = (self._bankIndex+direction)%len(self._programmingBank[self._prgBank])
            self.loadBankSlide()

    def loadBankSlide(self):
        """
        Arguments:
        - `self`:
        """
#        N = len(self._programmingBank[self._prgBank])
#       self.scene().notify(u"Slide (%d/%d) do banco %s."%(self._bankIndex+1,N,self._prgBank),Qt.darkGreen)
        if len(self._programmingBank[self._prgBank])>0:
            slide,status,settings = self._programmingBank[self._prgBank][self._bankIndex]
            self.scene().setSlidefromBank(slide,status)
            self._settings.setSettings(settings)
            self.updateSettings()
        else:
            self._bankAccess = False


    def reset(self):
        """
        """
        self._settings.reset()
        self.scene().reset()


    #def standBy(self):
    #    """
    #
    #    Arguments:
    #    - `self.`:
    #    """
    #	if self._loadingShutdown == False:
    #	     self.scene().toggleVisibility()
    #	     self._loadingShutdown = True
    #	     self.Tick()


    #def Tick(self):
#	"""
#	"""
#
#	self.scene().notifyQuick(u"Sistema desligando em %d segundos. Pressione outra tecla para abortar."%(self._contagem / 4), Qt.red)
#	if self._contagem > 0 and self._cancelShutdown == False :
#	    self._contagem = self._contagem - 1
#	    self._TimeEllapsed.start(250)
#	else :
#	    self._contagem = 22
#	    self._cancelShutdown = False
#	    self._loadingShutdown = False

    def decreaseContrast(self):
        if self.scene().acceptContrast():
            self._settings.decreaseContrast()

            contrast = self._settings.getContrast()

            self.scene().notify("Contraste %3d %%"%(contrast))

    def increaseContrast(self):
        if self.scene().acceptContrast():
            self._settings.increaseContrast()

            contrast = self._settings.getContrast()

            self.scene().notify("Contraste %3d %%"%(contrast))

    def decreaseBrightness(self):
        if self.scene().acceptBrightness():
            self._settings.decreaseBrightness()

            brightness = self._settings.getBrightness()

            self.scene().notify("Brilho %3d %%"%(brightness))

    def increaseBrightness(self):
        if self.scene().acceptBrightness():
            self._settings.increaseBrightness()

            brightness = self._settings.getBrightness()

            self.scene().notify("Brilho %3d %%"%(brightness))


    def updateSettings(self):
        """

        Arguments:
        - `self`:
        """

        distMatrix = self.scene().slideAccpetDistance()
        if distMatrix == True:
            self.setMatrix(self._distanceMatrix)
        else:
            self.setMatrix(distMatrix)

        contrast   = self._settings.getContrast()
        brightness = self._settings.getBrightness()

        contrP  = int(255*(100-contrast)/100.0)
        brightP = int(255*brightness/100.0)

        self.scene().applyOptColor(Qt.black)

        self.setBackgroundBrush(self.scene().getBackground())

        color = QColor(contrP,contrP,contrP)

        self.scene().applyOptContrast(contrast/100.0)


        if not self.scene().acceptRedGreenFilter():
            self._settings.hideRGMask()

        if not self.scene().acceptNegative():
            self._settings.hideNegative()



        if self._settings.isRGMaskSet():
            self.scene().showRGMask()
            #self.scene().hideMask()
        else:
            self.scene().hideRGMask()

        if self._settings.isBYMaskSet():
            self.scene().hideRGMask()
            self.setBackgroundBrush(QBrush(QColor(255,255,0)))
            self.scene().applyOptColor(Qt.blue)
            #self.scene().hideMask()

        if self._settings.isNegative():
            self.scene().hideRGMask()
            self.setBackgroundBrush(QBrush(Qt.black))
            self.scene().applyOptColor(Qt.white)


        if self._settings.isMaskSet():
            self.scene().showMask()
        else:
            self.scene().hideMask()

        if self._settings.isScaleSet():
            self.scene().showScale()
        else:
            self.scene().hideScale()

        if self.scene()._visibility:
            if not self._settings.isBYMaskSet() and not self._settings.isNegative():
                self.setBackgroundBrush(self.scene().getBackground())
        else:
            self.scene().hideRGMask()
            self.scene().hideSlide()
            self.setBackgroundBrush(Qt.black)

if __name__ == '__main__':

    scene = TAExamScene("Child")
    view = TAView(scene)
    view.setWindowTitle("Eyetec-TA")
    view.showFullScreen()

    view.updateSettings()

    sys.exit(app.exec_())
