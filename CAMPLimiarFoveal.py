#!/usr/bin/python3
import sys,math
from PyQt5.QtCore import Qt,QTimer,QEventLoop
from PyQt5.QtGui import QBrush, QColor, QPen,QKeyEvent
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,QGraphicsRectItem,QWidget

class BallView(QGraphicsView):
    def __init__(self):
        super(BallView, self).__init__()
        
        #variaveis para controle de resposta        
        self.alreadyPressed = False
        self.spacePressed = False        
        #variaveis para controle de exibicao
        self.areaTrabalhoX = 1000
        self.areaTrabalhoY = 1000
        self.scene_width = 1920
        self.scene_height = 1080
        #variaveis para conversao de coordenadas
        self.resolucaoX = 0.250
        self.resolucaoY = 0.242
        #variaveis para controle de cores        
        self.tomDeCinzaArea = 120
        self.tomDeCinzaCena = 100
        #variaveis para controle de posicao
        self.xPontoAtual = 0
        self.yPontoAtual = 0   
        self.view = None
        
        #variaveis para controle de tempo
        # self.timerParou = False
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.checkResponse)    
        # self.timer.setSingleShot(True)
        self.initializeScene()
        self.plotaAreaExame(widthMM = 250, heightMM = 250, cor = QColor(self.tomDeCinzaArea,self.tomDeCinzaArea,self.tomDeCinzaArea,255))        
        self.distanciaPacienteTela = 200	
        
        #inicializacao fixacao diamante limiar foveal teste
        self.fixacaoDiamante()
        self.testaPontoXYG(xang=15, yang=15, tamanhoPonto=2, color=Qt.white, tempo=2000,db=0)  
        self.resposta = self.esperar_tecla_ou_timer(2000) 
        # Enquanto a tecla não for pressionada e o timer ainda estiver ativo,
        # processa os eventos da aplicação
        if self.resposta == "timeout":
            print("Tempo máximo atingido antes de qualquer tecla ser pressionada.")
        else:
            print(f"Tecla '{self.resposta}' foi pressionada antes do tempo acabar!")      
        self.testaPontoXYG(xang=-15, yang=15, tamanhoPonto=2, color=Qt.white, tempo=2000,db=10)
        self.testaPontoXYG(xang=-15, yang=-15, tamanhoPonto=2, color=Qt.white, tempo=2000,db=20)
        self.testaPontoXYG(xang=15, yang=-15, tamanhoPonto=2, color=Qt.white, tempo=2000,db=25)

        self.viuEstimulo = False	
        
        self.UV = 0
        self.AT = 0
        
    def initializeScene(self):        
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, self.scene_width, self.scene_height)
        self.scene.setBackgroundBrush(QColor(self.tomDeCinzaCena,self.tomDeCinzaCena,self.tomDeCinzaCena,255))
        self.setScene(self.scene)
        
    def db_to_brightness(self,db):
        """
        Converte um nível em dB para um valor de brilho (0 a 255).
        0 dB corresponde a brilho 255 (máxima visibilidade)
        e 35 dB corresponde a brilho 0 (mínimo brilho).
        """
        # Garante que o valor de dB esteja entre 0 e 35
        db = max(0, min(35, db))
        brightness = 255 * (1 - db/35)
        return int(brightness)

    def fixacaoCentral(self):
        self.plotaXYANG(xg=0, yg=0, tamanhoPonto=3, color=Qt.yellow)
 
    def fixacaoDiamante(self):
        self.plotaXYANG(xg=0, yg=6, tamanhoPonto=2, color=Qt.yellow)
        self.plotaXYANG(xg=6 ,yg=0, tamanhoPonto=2, color=Qt.yellow)
        self.plotaXYANG(xg=-6, yg=0, tamanhoPonto=2, color=Qt.yellow)
        self.plotaXYANG(xg=0, yg=-6, tamanhoPonto=2, color=Qt.yellow)
 
    def plotaAreaExame(self, widthMM=100, heightMM=100, cor=Qt.white):    	

       tamanhoX = widthMM / self.resolucaoX
       tamanhoY = heightMM / self.resolucaoY       
       rect = QGraphicsRectItem(self.scene_width / 2 - tamanhoX / 2,self.scene_height / 2 - tamanhoY / 2, tamanhoX, tamanhoY)
       rect.setBrush(QBrush(cor))
       rect.setPen(QPen(Qt.NoPen))
       self.scene.addItem(rect)
       
    def plotaXYANG(self,xg,yg,tamanhoPonto,color,db = 35):
        
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
        
        point = QGraphicsEllipseItem(x, y, pontoRes,pontoRes)
        
        intensidade  = self.db_to_brightness(db)
        
        if(color == Qt.white):
            color = QColor(255,255,255,intensidade)
        
        point.setBrush(QBrush(color))
        point.setPen(QPen(Qt.NoPen))
        self.scene.addItem(point)
        
    def testaPontoXYG(self, xang, yang, tamanhoPonto, color, tempo,db):      
        # self.spacePressed = False
        self.plotaXYANG(xg=xang, yg=yang, tamanhoPonto=tamanhoPonto, color=color,db=db)         
        # self.timerParou = False
        # self.timer.start(tempo)   
        
   
    def esperar_tecla_ou_timer(self,tempo_maximo=3000):
        """Pausa a execução e espera uma tecla ser pressionada ou o tempo limite estourar."""        
        app = QApplication.instance()  # Usa a aplicação já existente
        if not app:
            raise RuntimeError("O QApplication precisa estar rodando!")
        loop = QEventLoop()  # Cria um loop de eventos para bloquear a execução
        tecla_pressionada = {"valor": None}  # Dicionário mutável para armazenar a tecla pressionada

    # Configura um timer para encerrar o loop após o tempo limite
    def timeout(self):
        if self.tecla_pressionada["valor"] is None:  # Só registra timeout se nenhuma tecla foi pressionada antes
            self.tecla_pressionada["valor"] = "timeout"
        self.loop.quit()  # Sai do loop e desbloqueia a execução

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(timeout)
        timer.start(tempo_maximo)

    # Função para capturar a tecla pressionada
    def keyPressEvent(self,event: QKeyEvent):
        self.tecla_pressionada["valor"] = event.text()  # Salva a tecla pressionada
        self.loop.quit()  # Sai do loop e desbloqueia a execução

        # Conecta o evento de tecla à aplicação principal
        app.installEventFilter(EventFilter(self.tecla_pressionada, loop))

        self.loop.exec_()  # Bloqueia a execução aqui até que uma tecla seja pressionada ou o tempo acabe

        app.removeEventFilter(EventFilter)  # Remove o filtro de eventos depois do uso

        return self.tecla_pressionada["valor"]  # Retorna a tecla pressionada ou 'timeout'
    #self.plotaXYANG(xg=self.xPontoAtual, yg=self.yPontoAtual, tamanhoPonto=4, color=QColor(self.tomDeCinzaArea,self.tomDeCinzaArea,self.tomDeCinzaArea,255)) 
        
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Space:
    #         self.spacePressed = True
    #         self.timer.stop()
    #         self.checkResponse()
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Space:
    #         self.spacePressed = True
    #         self.timer.stop()
    #         self.checkResponse()
    #     # Chama a implementação padrão, se necessário:
    #     super(YourWidgetClass, self).keyPressEvent(event)
        
    # def runNextTestPoint(self):
    #     # Adicione a lógica para determinar o próximo ponto a ser testado
    #     # Exemplo:
    #     next_points = [
    #         (15, 15, 2, Qt.white, 2000,0),
    #         (-15, 15, 2, Qt.white, 2000,10),
    #         (-15, -15, 2, Qt.white, 2000,20),
    #         (15, -15, 2, Qt.white, 2000,30)
    #     ]
    #     if hasattr(self, 'current_point_index'):
    #         self.current_point_index += 1
    #     else:
    #         self.current_point_index = 0

    #     if self.current_point_index < len(next_points):
    #         xang, yang, tamanhoPonto, color, tempo,db = next_points[self.current_point_index]
    #         self.testaPontoXYG(xang=xang, yang=yang, tamanhoPonto=tamanhoPonto, color=color, tempo=tempo,db=db)


class EventFilter:
    """Filtro de eventos para capturar teclas pressionadas."""
    def __init__(self, tecla_pressionada, loop):
        self.tecla_pressionada = tecla_pressionada
        self.loop = loop

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            self.tecla_pressionada["valor"] = event.text()
            self.loop.quit()
            return True  # Indica que o evento foi tratado
        return False  # Continua processando outros eventos normalmente
 
        
  
    def checkResponse(self):
        self.timerParou = True     
        if self.spacePressed:
            self.viuEstimulo = True
            self.plotaXYANG(xg=self.xPontoAtual, yg=self.yPontoAtual, tamanhoPonto=4, color=Qt.green)
        else:
            self.viuEstimulo = False
            self.plotaXYANG(xg=self.xPontoAtual, yg=self.yPontoAtual, tamanhoPonto=4, color=Qt.red)
        self.timer.stop()
        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = BallView()           
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setAlignment(Qt.AlignCenter)    
    view.showFullScreen()
    sys.exit(app.exec_())
