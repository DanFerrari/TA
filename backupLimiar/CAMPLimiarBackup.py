import sys, math, time
from PyQt5.QtCore import Qt, QTimer, QEventLoop, QThread
from PyQt5.QtGui import QBrush, QColor, QPen, QKeyEvent, QFont
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QWidget, QLabel

class MinhaJanela(QGraphicsView):
    def __init__(self):
        super().__init__()
        # Variáveis para controle de exibição
        self.areaTrabalhoX = 1000
        self.areaTrabalhoY = 1000
        self.scene_width = 1920
        self.scene_height = 1080
        # Variáveis para conversão de coordenadas
        self.resolucaoX = 0.250
        self.resolucaoY = 0.242
        # Variáveis para controle de cores
        self.tomDeCinzaArea = 120
        self.tomDeCinzaCena = 100
        # Variáveis para controle de posição
        self.sairAplicacao = False
        self.distanciaPacienteTela = 200
        self.inicializarCena()
        self.fixacaoDiamante()
        self.setupLabels()
        self.TemResposta = False

    def setupLabels(self):
        self.labelIntensidade = QLabel("Intensidade:  0", self)
        self.labelIntensidade.setStyleSheet("QLabel { color : preto; font-size: 38px; }")
        self.labelIntensidade.setGeometry(10, 10, 400, 80)
        self.labelLimiarFoveal = QLabel("Limiar Foveal: 0", self)
        self.labelLimiarFoveal.setStyleSheet("QLabel { color : white; font-size: 38px; }")
        self.labelLimiarFoveal.setGeometry(10, 100, 400, 30)

    def plotaAreaExame(self, larguraMM=100, alturaMM=100, cor=Qt.white):
        tamanhoX = larguraMM / self.resolucaoX
        tamanhoY = larguraMM / self.resolucaoY
        retangulo = QGraphicsRectItem(self.scene_width / 2 - tamanhoX / 2, self.scene_height / 2 - tamanhoY / 2, tamanhoX, tamanhoY)
        retangulo.setBrush(QBrush(cor))
        retangulo.setPen(QPen(Qt.NoPen))
        self.scene.addItem(retangulo)

    def plotaXYANGResp(self, xg, yg, tamanhoPonto, cor, db=35, tempoExposicaoEstimulo=1000, tempoRespostaPaciente=1000):
        resposta = self.esperar_tecla_ou_timer(tempo_maximo_paciente=tempoRespostaPaciente)
        self.labelIntensidade.setText("Intensidade:  " + str(db))
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
        return resposta

    def removePonto(self):
        self.scene.removeItem(self.ponto)

    def plotaXYANG(self, xg, yg, tamanhoPonto, cor, db=35):
        self.xPontoAtual = xg
        self.yPontoAtual = yg
        pontoRes = tamanhoPonto / self.resolucaoX
        xrad = math.radians(abs(xg))
        xmm = self.distanciaPacienteTela * math.tan(xrad)
        yrad = math.radians(abs(yg))
        ymm = self.distanciaPacienteTela * math.tan(yrad)
        x = xmm / self.resolucaoX
        y = ymm / self.resolucaoY

        if xg < 0:
            x = -x
        if yg < 0:
            y = -y

        x = x + self.scene_width / 2 - pontoRes / 2
        y = y + self.scene_height / 2 - pontoRes / 2

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
        UV = 0
        AT = 0
        UNV = 0
        NC = 0
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

        while not limiarok and not self.sairAplicacao:
            status = ''
            primeiro = True
            AT = 25
            while status != '=' and not self.sairAplicacao:
                resposta = self.plotaXYANGResp(xg=0, yg=0, tamanhoPonto=tamanhoPonto, cor=Qt.white, db=AT, tempoExposicaoEstimulo=tempoExposicao, tempoRespostaPaciente=2000)
                viu = 2 if resposta else 1

                match viu:
                    case 1:
                        if AT <= 0:
                            AT = -1
                            status = '='
                            continue
                        UNV = AT
                        if primeiro:
                            primeiro = False
                            NC = 0
                            UV = 0
                            Delta = Dbig
                            AT -= Delta
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
                                AT -= Delta
                                status = '+'
                                continue
                        else:
                            AT -= Delta
                            status = '+'
                            continue
                    case 2:
                        UV = AT
                        if primeiro:
                            primeiro = False
                            NC = 0
                            UNV = 35
                            Delta = Dbig
                            AT += Delta
                            status = '-'
                            continue
                        if status == '+':
                            NC += 1
                            Delta = Dsmall
                            if NC >= 2:
                                status = '='
                                AT = (UV + UNV) / 2
                                continue
                            else:
                                AT += Delta
                                status = '-'
                                continue
                        else:
                            AT += Delta
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
        self.plotaAreaExame(600, 600, QColor(120, 120, 120, 255))

    def esperar_tecla_ou_timer(self, tempo_maximo_paciente=1000):
        self.tecla_pressionada = None
        self.loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(self.loop.quit)
        timer.start(tempo_maximo_paciente)
        self.loop.exec_()
        return self.tecla_pressionada

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.tecla_pressionada = True
        elif event.key() == Qt.Key_Escape:
            self.sairAplicacao = True
            self.tecla_pressionada = False
        else:
            self.tecla_pressionada = False
        if self.loop and self.loop.isRunning():
            self.loop.quit()

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
