#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################################
import sys, random,math
from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import (QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,
                         QGraphicsTextItem, QBrush, QColor, QPen, QApplication,
                         QPushButton, QGraphicsProxyWidget, QFont,QGraphicsRectItem)
# Importa a classe do exame com matriz (por exemplo, CAMPExame)
from CAMPExame import CAMPExame

class CAMPLimiarFoveal:
    def __init__(self):
        # Flag para indicar que estamos no teste inicial
        self.initialTestMode = True
        # Parâmetros do teste:
        self.dBIncrement = 5        # incremento de 5 dB por resposta
        self.max_dB = 45
        self.initial_dB = 0         # inicia em 0 dB (estímulo máximo visível)
        # Variáveis de controle do trial
        self.current_dB = None          # nível atual (em dB)
        self.last_validated_dB = None   # último nível em que o usuário respondeu
        self.numTrials = 0              # contador de ciclos

        # Timers do teste inicial
        self.initialTestTimer = QTimer()
        self.initialTestTimer.setSingleShot(True)
        self.initialTestTimer.timeout.connect(self.onInitialTestTimeout)

        # Timer para o cronômetro de preparação (5 s)
        self.prepTimer = QTimer()
        self.prepTimer.setInterval(1000)  # 1 segundo
        self.prepTimer.timeout.connect(self.updateCountdown)
        self.countdown = 5

        # Para garantir que em cada ciclo apenas 1 pressionamento seja considerado:
        self.alreadyPressed = False
	
        self.spacePressed = False

        # Parâmetros da cena:
        self.areaTrabalhoX = 1000
        self.areaTrabalhoY = 1000
        self.resolucaoX = 0.250
        self.resolucaoY = 0.242
        self.scene_width = 1920
        self.scene_height = 1080
        self.colorSetTest = QColor(255,255,255,100)
        self.tomDeCinzaArea = 120
        self.tomDeCinzaCena = 100
            # Aqui definimos o atributo view (inicialmente None)
        self.view = None
        self.initializeScene()

        self.plotaAreaExame(widthMM = 250, heightMM = 250, cor = QColor(self.tomDeCinzaArea,self.tomDeCinzaArea,self.tomDeCinzaArea,255))
        #self.runPreparationPhase()
        self.distanciaPacienteTela = 200	
        self.drawCenterPoint()	

        self.timer = QTimer()
        self.timerParou = False
        self.timer.timeout.connect(self.checkResponse)
        self.view.keyPressEvent = self.handleKeyPress
        self.viuEstimulo = False
	

	
    def plotaAreaExame(self, widthMM=100, heightMM=100, cor=Qt.white):
    	

       tamanhoX = widthMM / self.resolucaoX
       tamanhoY = heightMM / self.resolucaoY
       
       rect = QGraphicsRectItem(self.scene_width / 2 - tamanhoX / 2,self.scene_height / 2 - tamanhoY / 2, tamanhoX, tamanhoY)
       rect.setBrush(QBrush(cor))
       rect.setPen(QPen(Qt.NoPen))
       self.scene.addItem(rect)
       
       
    def drawCenterPoint(self):
        """Desenha um ponto amarelo no centro da tela"""       	
	point = QGraphicsEllipseItem( self.scene_width / 2 - 5,self.scene_height / 2 - 5, 10,10)
        point.setBrush(QBrush(Qt.yellow))
        point.setPen(QPen(Qt.NoPen))
        self.scene.addItem(point)
    def plotaXYANG(self,xg,yg,tamanhoPonto,color):
	pontoRes = tamanhoPonto / self.resolucaoX
	xrad = math.radians(xg)
	tangenteAng = math.tan(xrad)
	xmm = self.distanciaPacienteTela * tangenteAng
	yrad = math.radians(yg)
	tangenteAng = math.tan(yrad)
	ymm = self.distanciaPacienteTela * tangenteAng
       	
	x = xmm / self.resolucaoX		
	y = ymm / self.resolucaoY

	point = QGraphicsEllipseItem(x + self.scene_width / 2 - pontoRes / 2, y + self.scene_height / 2 - pontoRes / 2, pontoRes,pontoRes)
        point.setBrush(QBrush(color))
        point.setPen(QPen(Qt.NoPen))
        self.scene.addItem(point)
     
    def testaPontoXYG(self, xang, yang, tamanhoPonto, color, tempo):
       	self.spacePressed = False
        self.plotaXYANG(xg=xang, yg=yang, tamanhoPonto=tamanhoPonto, color=color) 
	self.timer.start(tempo)
	
	   
        

    def handleKeyPress(self,event):
	if event.key() == Qt.Key_Space:
           self.spacePressed = True
	   self.timer.stop()	
           self.checkResponse()
	
    def checkResponse(self):
	timerParou = True	
	if self.spacePressed:
	   viuEstimulo = True
	   
        else:
	   self.viuEstimulo = False
	

	
    def setView(self, view):
        """Define a referência para a QGraphicsView."""
        self.view = view

    def initializeScene(self):
        """Configura a cena com tamanho fixo (1900x1000) centralizada numa tela de 1920x1080."""
        self.scene = QGraphicsScene()
        offset_x = (1920 - self.scene_width) // 2
        offset_y = (1080 - self.scene_height) // 2
        self.scene.setSceneRect(offset_x, offset_y, self.scene_width, self.scene_height)
        self.scene.setBackgroundBrush(QColor(self.tomDeCinzaCena,self.tomDeCinzaCena,self.tomDeCinzaCena,255))

    def runPreparationPhase(self):
        """Exibe um cronômetro de 5 segundos para preparação."""
        self.scene.clear()
        self.countdownText = QGraphicsTextItem("Prepare-se: 5")
        self.countdownText.setDefaultTextColor(QColor(0,0,255))
        font = QFont()
        font.setPointSize(40)
        self.countdownText.setFont(font)
        self.countdownText.setPos(self.scene_width/2 - 100, self.scene_height/2 - 50)
        self.scene.addItem(self.countdownText)
        self.countdown = 5
        self.prepTimer.start()

    def updateCountdown(self):
        """Atualiza o cronômetro a cada segundo."""
        self.countdown -= 1
        self.countdownText.setPlainText("Prepare-se: " + str(self.countdown))
        if self.countdown == 0:
            self.prepTimer.stop()
            self.scene.removeItem(self.countdownText)
            self.runInitialThresholdTest()

    def runInitialThresholdTest(self):
        """Inicia o teste inicial: desenha o círculo, plota o estímulo e inicia o timer de 1 s."""
        self.scene.clear()
        center_x = self.scene_width / 2
        center_y = self.scene_height / 2
        circle_radius = 200  # diâmetro 400
        circle = QGraphicsEllipseItem(center_x - circle_radius, center_y - circle_radius, 400, 400)
        circle.setBrush(QBrush(QColor(200,200,200)))
        circle.setPen(QPen(Qt.red))
        self.scene.addItem(circle)
        self.stimulusPoint = QGraphicsEllipseItem(center_x - 10, center_y - 10, 20, 20)
        self.updateStimulusAppearance(self.initial_dB)
        self.stimulusPoint.setPen(QPen(Qt.NoPen))
        self.scene.addItem(self.stimulusPoint)
        self.numTrials += 1
        self.current_dB = self.initial_dB
        self.last_validated_dB = None
        self.alreadyPressed = False
        self.initialTestTimer.start(1000)

    def updateStimulusAppearance(self, dB):
        """Atualiza a aparência do estímulo com base no nível (dB)."""
        intensity = self.dBToIntensity(dB)
        color = QColor(255,255,255, int(255 * intensity))
        if self.stimulusPoint is not None:
            self.stimulusPoint.setBrush(QBrush(color))

    def dBToIntensity(self, dB):
        intensity = 1 - (dB/float(self.max_dB))
        return max(0, intensity)

    def onInitialTestSpacePressed(self):
        """Quando o usuário pressiona Espaço, registra a resposta e aumenta o nível em 5 dB."""
        if self.stimulusPoint is None:
            return
        if not self.alreadyPressed:
            self.alreadyPressed = True
            self.last_validated_dB = self.current_dB
            self.scene.removeItem(self.stimulusPoint)
            self.stimulusPoint = None
            self.current_dB += self.dBIncrement
            if self.current_dB > self.max_dB:
                self.current_dB = self.max_dB
            QTimer.singleShot(100, self.startInitialTestCycle)

    def startInitialTestCycle(self):
        """Replota o estímulo com o novo nível e reinicia o timer."""
        if not self.initialTestMode:
            return
        self.scene.clear()
        center_x = self.scene_width / 2
        center_y = self.scene_height / 2
        circle_radius = 200
        circle = QGraphicsEllipseItem(center_x - circle_radius, center_y - circle_radius, 400, 400)
        circle.setBrush(QBrush(QColor(200,200,200)))
        circle.setPen(QPen(Qt.NoPen))
        self.scene.addItem(circle)
        self.stimulusPoint = QGraphicsEllipseItem(center_x - 10, center_y - 10, 20, 20)
        self.updateStimulusAppearance(self.current_dB)
        self.stimulusPoint.setPen(QPen(Qt.NoPen))
        self.scene.addItem(self.stimulusPoint)
        self.alreadyPressed = False
        self.initialTestTimer.start(1000)

    def onInitialTestTimeout(self):
        """Se o tempo expirar sem resposta, finaliza o teste e define o limiar como o último nível validado."""
        finalThreshold = self.last_validated_dB if self.last_validated_dB is not None else self.initial_dB
        self.finishInitialTest(finalThreshold)

    def finishInitialTest(self, threshold):
        """Finaliza o teste, exibindo o limiar e um menu final com as opções de Reiniciar e Continuar."""
        self.initialTestMode = False
        self.initialTestTimer.stop()
        self.scene.clear()
        thresholdText = QGraphicsTextItem("Limiar: {:.0f} dB".format(threshold))
        thresholdText.setDefaultTextColor(QColor(0,0,255))
        font = QFont()
        font.setPointSize(60)
        thresholdText.setFont(font)
        thresholdText.setPos(self.scene_width/2 - 250, self.scene_height/2 - 150)
        self.scene.addItem(thresholdText)
        self.createFinalMenu(threshold)

    def createFinalMenu(self, threshold):
        """Cria o menu final com as opções 'Reiniciar' e 'Continuar'."""
        self.finalMenuSelection = 0  # 0: Reiniciar, 1: Continuar
        fontOption = QFont()
        fontOption.setPointSize(40)
        self.optionRestart = QGraphicsTextItem("Reiniciar")
        self.optionRestart.setFont(fontOption)
        self.optionRestart.setPos(self.scene_width/2 - 200, self.scene_height/2 + 50)
        self.optionContinue = QGraphicsTextItem("Continuar")
        self.optionContinue.setFont(fontOption)
        self.optionContinue.setPos(self.scene_width/2 + 50, self.scene_height/2 + 50)
        self.scene.addItem(self.optionRestart)
        self.scene.addItem(self.optionContinue)
        self.updateFinalMenuAppearance()

    def updateFinalMenuAppearance(self):
        """Atualiza a aparência das opções do menu final conforme a seleção."""
        if self.finalMenuSelection == 0:
            self.optionRestart.setDefaultTextColor(QColor(0,0,255))
            self.optionContinue.setDefaultTextColor(QColor(0,0,0))
        else:
            self.optionRestart.setDefaultTextColor(QColor(0,0,0))
            self.optionContinue.setDefaultTextColor(QColor(0,0,255))

    def moveSelectionLeft(self):
        """Muda a seleção para 'Reiniciar'."""
        if not self.initialTestMode:
            self.finalMenuSelection = 0
            self.updateFinalMenuAppearance()

    def moveSelectionRight(self):
        """Muda a seleção para 'Continuar'."""
        if not self.initialTestMode:
            self.finalMenuSelection = 1
            self.updateFinalMenuAppearance()

    def selectFinalMenuOption(self):
        """Executa a opção selecionada do menu final."""
        if not self.initialTestMode:
            if self.finalMenuSelection == 0:
                self.restartTest()
            else:
                self.continueExam()

    def restartTest(self):
        """Reinicia o teste inicial."""
        self.initialTestMode = True
        self.current_dB = self.initial_dB
        self.last_validated_dB = None
        self.alreadyPressed = False
        self.runPreparationPhase()

    def continueExam(self):
	    self.scene.clear()
	    exame = CAMPExame(self.last_validated_dB if self.last_validated_dB is not None else self.initial_dB)
	    if self.view is not None:
		self.view.setScene(exame.scene)
	    else:
		self.scene = exame.scene
	    print("Continuando para o exame com matriz...")



    def onSpacePressed(self):
        """Método chamado a partir da view quando a tecla Espaço é pressionada."""
        if self.initialTestMode:
            if self.initialTestTimer.isActive():
                self.initialTestTimer.stop()
                self.onInitialTestSpacePressed()
        else:
            # No menu final, espaço não faz nada; navegação se dá com as setas e Enter.
            pass

class CustomGraphicsView(QGraphicsView):
    def __init__(self, exam, *args, **kwargs):
        super(CustomGraphicsView, self).__init__(*args, **kwargs)
        self.exam = exam

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if self.exam.initialTestMode:
            if event.key() == Qt.Key_Space:
                self.exam.onSpacePressed()
        else:
            if event.key() == Qt.Key_Left:
                self.exam.moveSelectionLeft()
            elif event.key() == Qt.Key_Right:
                self.exam.moveSelectionRight()
            elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
                self.exam.selectFinalMenuOption()
        super(CustomGraphicsView, self).keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    exam = CAMPLimiarFoveal()
    window = CustomGraphicsView(exam)
    exam.setView(window)
    window.setScene(exam.scene)
    window.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window.setAlignment(Qt.AlignCenter)
    window.showFullScreen()
    sys.exit(app.exec_())

