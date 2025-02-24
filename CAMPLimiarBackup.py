# #!/usr/bin/python3
# import sys, math
# from PyQt5.QtCore import Qt, QTimer, QEventLoop
# from PyQt5.QtGui import QBrush, QColor, QPen, QKeyEvent, QFont
# from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QWidget,QLabel

# class CAMPLimiarFoveal(QGraphicsView):
#     def __init__(self):
#         super(CAMPLimiarFoveal, self).__init__()
#        # Flag para indicar que estamos no teste inicial
#         self.modoTesteInicial = True
#         # Parâmetros do teste:
#         self.incrementoDB = 5        # incremento de 5 dB por resposta
#         self.max_dB = 45
#         self.dBInicial = 0         # inicia em 0 dB (estímulo máximo visível)
#         # Variáveis de controle do trial
#         self.dBAtual = None          # nível atual (em dB)
#         self.last_validated_dB = None   # último nível em que o usuário respondeu
#         self.numTentativas = 0              # contador de ciclos

#         # Timers do teste inicial
#         self.timerTesteInicial = QTimer()
#         self.timerTesteInicial.setSingleShot(True)
#         self.timerTesteInicial.timeout.connect(self.terminouTempo)
#         # variáveis para controle de resposta        
#         self.alreadyPressed = False
#         self.spacePressed = False        
#         # variáveis para controle de exibição
#         self.areaTrabalhoX = 1000
#         self.areaTrabalhoY = 1000
#         self.scene_width = 1920
#         self.scene_height = 1080
#         # variáveis para conversão de coordenadas
#         self.resolucaoX = 0.250
#         self.resolucaoY = 0.242
#         # variáveis para controle de cores        
#         self.tomDeCinzaArea = 120
#         self.tomDeCinzaCena = 100
#         # variáveis para controle de posição
#         self.xPontoAtual = 0
#         self.yPontoAtual = 0   
#         self.view = None
#         self.distanciaPacienteTela = 200	
#         self.viuEstimulo = False	     
       
        
     
                
#         self.inicializarCena()
#         self.plotaAreaExame(600,600,QColor(self.tomDeCinzaArea, self.tomDeCinzaArea, self.tomDeCinzaArea, 255))   
#         self.fixacaoDiamante()
#         self.iniciarTeste()
        
#     def dBParaIntensidade(self, dB):
#         db = max(0, min(35, dB))
#         brilho = 255 * (1 - db / 35)
#         return int(brilho)

        
    
#     def keyPressEvent(self, event):
#         self.alreadyPressed = False
#         if event.key() == Qt.Key_Space:
#             if self.ComecouTimer == True and self.alreadyPressed == False:
#                 self.plotaXYANG(xg=self.xPontoAtual, yg=self.yPontoAtual, tamanhoPonto=3, cor=QColor(self.tomDeCinzaArea,self.tomDeCinzaArea,self.tomDeCinzaArea,255), db=self.dBAtual)
#                 self.spacePressed = True
#                 self.alreadyPressed = True 
#                 self.timerTesteInicial.stop()
#                 self.label = QLabel("Apertei", self)
#                 self.label.setStyleSheet("QLabel { color : white; font-size: 24px; }")
#                 self.label.setAlignment(Qt.AlignCenter)
#                 self.label.setGeometry(self.scene_width // 2 - 50, self.scene_height // 2 - 12, 100, 24)
#                 self.label.show()
                   
      
            
       
#     def iniciarTeste(self):
#         self.xPontoAtual = 0
#         self.yPontoAtual = 0
#         self.dBAtual = 0
#         self.plotaXYANG(xg=self.xPontoAtual, yg=self.yPontoAtual, tamanhoPonto=3, cor=Qt.white, db=self.dBAtual)
#         self.timerTesteInicial.start(2000)
#         self.ComecouTimer = True
        
    
#     def inicializarCena(self):        
#         self.scene = QGraphicsScene()
#         self.scene.setSceneRect(0, 0, self.scene_width, self.scene_height)
#         self.scene.setBackgroundBrush(QColor(self.tomDeCinzaCena, self.tomDeCinzaCena, self.tomDeCinzaCena, 255))
#         self.setScene(self.scene)      
        

#     def fixacaoCentral(self):
#         self.plotaXYANG(xg=0, yg=0, tamanhoPonto=3, cor=Qt.yellow)
 
#     def fixacaoDiamante(self):
#         self.plotaXYANG(xg=0, yg=6, tamanhoPonto=2, cor=Qt.yellow)
#         self.plotaXYANG(xg=6, yg=0, tamanhoPonto=2, cor=Qt.yellow)
#         self.plotaXYANG(xg=-6, yg=0, tamanhoPonto=2, cor=Qt.yellow)
#         self.plotaXYANG(xg=0, yg=-6, tamanhoPonto=2, cor=Qt.yellow)
 
#     def plotaAreaExame(self, larguraMM=100, alturaMM=100, cor=Qt.white):    	
#         tamanhoX = larguraMM / self.resolucaoX
#         tamanhoY = alturaMM / self.resolucaoY       
#         retangulo = QGraphicsRectItem(self.scene_width / 2 - tamanhoX / 2, self.scene_height / 2 - tamanhoY / 2, tamanhoX, tamanhoY)
#         retangulo.setBrush(QBrush(cor))
#         retangulo.setPen(QPen(Qt.NoPen))
#         self.scene.addItem(retangulo)
       
#     def plotaXYANG(self, xg, yg, tamanhoPonto, cor, db=35):
#         self.xPontoAtual = xg
#         self.yPontoAtual = yg
#         pontoRes = tamanhoPonto / self.resolucaoX
        
#         if xg < 0:
#             xrad = math.radians(xg * -1)
#             tangenteAng = math.tan(xrad)
#             xmm = self.distanciaPacienteTela * tangenteAng
#         else:
#             xrad = math.radians(xg)
#             tangenteAng = math.tan(xrad)
#             xmm = self.distanciaPacienteTela * tangenteAng
        
#         if yg < 0:
#             yrad = math.radians(yg * -1)
#             tangenteAng = math.tan(yrad)
#             ymm = self.distanciaPacienteTela * tangenteAng
#         else:
#             yrad = math.radians(yg)        
#             tangenteAng = math.tan(yrad)
#             ymm = self.distanciaPacienteTela * tangenteAng
                
#         x = xmm / self.resolucaoX		
#         y = ymm / self.resolucaoY
        
#         if xg < 0 and yg < 0:                  
#             x = -x + self.scene_width / 2 - pontoRes / 2
#             y = y + self.scene_height / 2 - pontoRes / 2
          
#         if xg < 0 and yg >= 0:
#             x = -x + self.scene_width / 2 - pontoRes / 2
#             y = -y + self.scene_height / 2 - pontoRes / 2
           
#         if xg >= 0 and yg < 0:
#             x = x + self.scene_width / 2 - pontoRes / 2
#             y = y + self.scene_height / 2 - pontoRes / 2          
            
#         if xg >= 0 and yg >= 0:  
#             y = -y + self.scene_height / 2 - pontoRes / 2
#             x = x + self.scene_width / 2 - pontoRes / 2
        
#         ponto = QGraphicsEllipseItem(x, y, pontoRes, pontoRes)
        
#         intensidade = self.dBParaIntensidade(db)
        
#         if cor == Qt.white:
#             cor = QColor(255, 255, 255, intensidade)
        
#         ponto.setBrush(QBrush(cor))
#         ponto.setPen(QPen(Qt.NoPen))
#         self.scene.addItem(ponto)     
    
   

        
#     def terminouTempo(self):
#         print("Tempo esgotado")
#         self.plotaXYANG(xg=self.xPontoAtual, yg=self.yPontoAtual, tamanhoPonto=3, cor=QColor(self.tomDeCinzaArea,self.tomDeCinzaArea,self.tomDeCinzaArea,255), db=self.dBAtual)
#         self.timerTesteInicial.stop()   
#         self.label1 = QLabel("Tempo esgotado", self)
#         self.label1.setStyleSheet("QLabel { color : white; font-size: 24px; }")
#         self.label1.setAlignment(Qt.AlignCenter)
#         self.label1.setGeometry(self.scene_width // 2 - 100, self.scene_height // 2 - 12, 200, 24)
#         self.label1.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     view = CAMPLimiarFoveal()           
#     view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#     view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#     view.setAlignment(Qt.AlignCenter)    
#     view.showFullScreen()
#     view.keyPressEvent = CAMPLimiarFoveal().keyPressEvent
#     sys.exit(app.exec_())

import sys, math,time
from PyQt5.QtCore import Qt, QTimer, QEventLoop,QThread
from PyQt5.QtGui import QBrush, QColor, QPen, QKeyEvent, QFont
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QWidget,QLabel

class MinhaJanela(QGraphicsView):
    def __init__(self):
        super().__init__() 

        # variáveis para controle de exibição
        self.areaTrabalhoX = 1000
        self.areaTrabalhoY = 1000
        self.scene_width = 1920
        self.scene_height = 1080
        # variáveis para conversão de coordenadas
        self.resolucaoX = 0.250
        self.resolucaoY = 0.242
        # variáveis para controle de cores        
        self.tomDeCinzaArea = 120
        self.tomDeCinzaCena = 100
        # variáveis para controle de posição 
        self.sairAplicacao = False
        self.distanciaPacienteTela = 200	
        self.inicializarCena()
        self.fixacaoDiamante()
        self.setupLabels()
        self.TemResposta = False
    
    
    
    def setupLabels(self):
        # self.labelAngX = QLabel("AngX:0", self)
        # self.labelAngX.setStyleSheet("QLabel { color : white; font-size: 24px; }")
        # self.labelAngX.setGeometry(10, 10, 200, 30)
        
        # self.labelAngY = QLabel("AngY:0", self)
        # self.labelAngY.setStyleSheet("QLabel { color : white; font-size: 24px; }")
        # self.labelAngY.setGeometry(10, 50, 200, 30)
        
        
        # self.labelNumCruz = QLabel("Número de cruzamentos:0", self)
        # self.labelNumCruz.setStyleSheet("QLabel { color : white; font-size: 24px; }")
        # self.labelNumCruz.setGeometry(10, 130, 300, 30)
        # self.labelStatus = QLabel("Status:NA", self)
        # self.labelStatus.setStyleSheet("QLabel { color : white; font-size: 24px; }")
        # self.labelStatus.setGeometry(10, 210, 200, 30)
           
        # self.labelUAV = QLabel("Última atenuação vista:0", self)
        # self.labelUAV.setStyleSheet("QLabel { color : white; font-size: 24px; }")
        # self.labelUAV.setGeometry(10, 250, 300, 30)
        
        self.labelIntensidade = QLabel("Intensidade:  0", self)
        self.labelIntensidade.setStyleSheet("QLabel { color : preto; font-size: 38px; }")
        self.labelIntensidade.setGeometry(10, 10, 400, 80)
      
        # self.labelViu = QLabel("Viu:NA", self)
        # self.labelViu.setStyleSheet("QLabel { color : white; font-size: 24px; }")
        # self.labelViu.setGeometry(10, 170, 200, 30)
        
        
        self.labelLimiarFoveal = QLabel("Limiar Foveal: 0", self)
        self.labelLimiarFoveal.setStyleSheet("QLabel { color : white; font-size: 38px; }")
        self.labelLimiarFoveal.setGeometry(10, 100, 400, 30)
        
    
        
        
    def plotaAreaExame(self, larguraMM=100, alturaMM=100, cor=Qt.white):    	
        tamanhoX = larguraMM / self.resolucaoX
        tamanhoY = alturaMM / self.resolucaoY       
        retangulo = QGraphicsRectItem(self.scene_width / 2 - tamanhoX / 2, self.scene_height / 2 - tamanhoY / 2, tamanhoX, tamanhoY)
        retangulo.setBrush(QBrush(cor))
        retangulo.setPen(QPen(Qt.NoPen))
        self.scene.addItem(retangulo)    
        
        
        
        
        
    def plotaXYANGResp(self, xg, yg, tamanhoPonto, cor, db=35,tempoExposicaoEstimulo = 1000, tempoRespostaPaciente = 1000):
   
        resposta = self.esperar_tecla_ou_timer(tempo_maximo_paciente = tempoRespostaPaciente) # Espera até 5 segundos  
        self.labelIntensidade.setText("Intensidade:  "+str(db))
        self.labelIntensidade.setStyleSheet("QLabel { color : white; font-size: 38px; }")
        
        self.plotaXYANG(xg, yg, tamanhoPonto, cor, db)

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.plotaXYANG(xg=0, yg=0, tamanhoPonto=5, cor=QColor(self.tomDeCinzaArea, self.tomDeCinzaArea, self.tomDeCinzaArea, 255)))
        timer.start(200)
      
        if resposta:
                       
            self.labelIntensidade.setStyleSheet("QLabel { color : green; font-size: 38px; }")
            
        else:
            
            self.labelIntensidade.setStyleSheet("QLabel { color : red; font-size: 38px; }")
            
        # self.loop = QEventLoop()  # Cria um loop para bloquear a execução

 
        # timer = QTimer()
        # timer.setSingleShot(True)
        # timer.timeout.connect(self.loop.quit)  # Sai do loop quando o tempo acabar
        # timer.start(500)


        # Executa o loop de eventos (bloqueia a execução até que algo aconteça)
        # self.loop.exec_()    
        return resposta  
        
        
    def removePonto(self):
        self.scene.removeItem(self.ponto)
        
        
    def plotaXYANG(self, xg, yg, tamanhoPonto, cor, db=35):
        self.xPontoAtual = xg
        self.yPontoAtual = yg
        pontoRes = tamanhoPonto / self.resolucaoX
        
        if xg < 0:
            xrad = math.radians(xg * -1)
            tangenteAng = math.tan(xrad)
            xmm = self.distanciaPacienteTela * tangenteAng
        else:
            xrad = math.radians(xg)
            tangenteAng = math.tan(xrad)
            xmm = self.distanciaPacienteTela * tangenteAng
        
        if yg < 0:
            yrad = math.radians(yg * -1)
            tangenteAng = math.tan(yrad)
            ymm = self.distanciaPacienteTela * tangenteAng
        else:
            yrad = math.radians(yg)        
            tangenteAng = math.tan(yrad)
            ymm = self.distanciaPacienteTela * tangenteAng
                
        x = xmm / self.resolucaoX		
        y = ymm / self.resolucaoY
        
        if xg < 0 and yg < 0:                  
            x = -x + self.scene_width / 2 - pontoRes / 2
            y = y + self.scene_height / 2 - pontoRes / 2
          
        if xg < 0 and yg >= 0:
            x = -x + self.scene_width / 2 - pontoRes / 2
            y = -y + self.scene_height / 2 - pontoRes / 2
           
        if xg >= 0 and yg < 0:
            x = x + self.scene_width / 2 - pontoRes / 2
            y = y + self.scene_height / 2 - pontoRes / 2          
            
        if xg >= 0 and yg >= 0:  
            y = -y + self.scene_height / 2 - pontoRes / 2
            x = x + self.scene_width / 2 - pontoRes / 2
        
        
        ponto = QGraphicsEllipseItem(x, y, pontoRes, pontoRes)
        
        intensidade = self.dBParaIntensidade(db)
        
        if cor == Qt.white:
            cor = QColor(255, 255, 255, intensidade)
        
        ponto.setBrush(QBrush(cor))
        ponto.setPen(QPen(Qt.NoPen))
        self.scene.addItem(ponto)     
       
       
      
    
    def dBParaIntensidade(self, dB):
        db = max(0, min(35, dB))
        brilho = 255 * (1 - db / 35)
        return int(brilho)
        


    def calculaLimiarFoveal(self):
        UV=0
        AT=0
        UNV=0
        NC=0
        Delta = 0
        viu = 0 
        Dbig = 3
        Dsmall = 2
        limiarok = False
        status = ''
        limiar = 0.1
        primeiro = True
        tempoExposicao = 200
        tamanhoPonto = 3
        self.sairAplicacao = False
        self.fixacaoDiamante()
        limiarok = False
        
        while limiarok == False and self.sairAplicacao == False:
            
        
            status = ''
            primeiro = True
            AT = 25
            while status != '=' and self.sairAplicacao == False:
               
                resposta = self.plotaXYANGResp(xg = 0,yg = 0,tamanhoPonto= tamanhoPonto,cor = Qt.white,db= AT,tempoExposicaoEstimulo = tempoExposicao, tempoRespostaPaciente = 2000)
               
                                                
                if resposta:
                    viu = 2
                else:   
                    viu = 1
                    
              
                match viu:
                    case 1:
                        if AT <= 0:
                            AT = -1 
                            status = '='                            
                            continue
                                               
                        UNV = AT 
                        if primeiro == True:
                            primeiro = False
                            NC = 0
                            UV = 0
                            Delta = Dbig
                            AT = AT - Delta
                            status = '+'
                            continue
                        if status == '-':
                            NC += 1
                            Delta = Dsmall
                            if NC >= 2:
                                status = '='
                                AT = (UV + UNV) / 2
                                continue
                            else:            
                                AT = AT - Delta
                                status = '+'
                                continue
                        else:
                            AT = AT - Delta        
                            status = '+'
                            continue
                            
                        
                    case 2:
                        UV = AT
                        if primeiro == True:
                            primeiro = False
                            NC = 0
                            UNV = 35
                            Delta = Dbig
                            AT = AT + Delta
                            status = '-'
                            continue
                            
                        if status == '+':
                            NC =+ 1
                            Delta = Dsmall
                            
                            if NC >= 2:
                                status = '='
                                AT = (UV + UNV) / 2
                                continue
                                
                            else:
                                AT = AT + Delta
                                status = '-' 
                                continue
                                
                                   

                        else:
                            AT = AT + Delta
                            status = '-'
                            continue
                            
                
                        
                if AT > 40:
                    AT = 35    
            
            
            limiar = AT
            self.labelIntensidade.setStyleSheet("QLabel { color : black; font-size: 38px; }")
            limiarok = True
            self.labelLimiarFoveal.setText(f"Limiar Foveal= {limiar}")

                
                

    

            
        
      
    
        

    def inicializarCena(self):        
         self.scene = QGraphicsScene()
         self.scene.setSceneRect(0, 0, 1920, 1080)
         self.scene.setBackgroundBrush(QColor(120, 120, 120, 255))         
         self.setScene(self.scene) 
         self.plotaAreaExame(600,600,QColor(120, 120, 120, 255))    

    def esperar_tecla_ou_timer(self, tempo_maximo_paciente= 1000):
        """Pausa a execução até uma tecla ser pressionada ou o tempo acabar."""
        self.tecla_pressionada = None
        self.loop = QEventLoop()  # Cria um loop para bloquear a execução

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(self.loop.quit)  # Sai do loop quando o tempo acabar
        timer.start(tempo_maximo_paciente)

        self.loop.exec_()

        # Executa o loop de eventos (bloqueia a execução até que algo aconteça)
       
        
        return self.tecla_pressionada  # Retorna a tecla pressionada ou None se o tempo acabar

    def keyPressEvent(self, event: QKeyEvent):
        """Captura a tecla pressionada e sai do loop de espera."""
   
        if event.key() == Qt.Key_Space:
            self.tecla_pressionada = True
        elif event.key() == Qt.Key_Escape:
            self.sairAplicacao = True
            self.tecla_pressionada = False
        else:
            self.tecla_pressionada = False
        
        if self.loop and self.loop.isRunning():
            self.loop.quit()  # Sai do loop assim que a tecla for pressionada
            
            
    def fixacaoDiamante(self):
        self.plotaXYANG(xg=0, yg=6, tamanhoPonto=2, cor=Qt.yellow)
        self.plotaXYANG(xg=6, yg=0, tamanhoPonto=2, cor=Qt.yellow)
        self.plotaXYANG(xg=-6, yg=0, tamanhoPonto=2, cor=Qt.yellow)
        self.plotaXYANG(xg=0, yg=-6, tamanhoPonto=2, cor=Qt.yellow)
    
      
 

# === Fluxo do Programa ===
app = QApplication(sys.argv)
janela = MinhaJanela()
janela.showFullScreen()
janela.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
janela.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
janela.setAlignment(Qt.AlignCenter)  


janela.calculaLimiarFoveal()







sys.exit(app.exec_())
