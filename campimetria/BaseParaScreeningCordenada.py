import sys, random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QBrush, QColor, QPen, QFont
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsView,
    QApplication,
    QGraphicsLineItem,
)


class CAMPExame:
    def __init__(self, threshold=0):
        """Inicializa a cena e a matriz de pontos"""
        self.threshold = threshold
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.showFullScreen()

        # Define a área da cena e cor de fundo
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())
        self.scene.setBackgroundBrush(QColor(255, 255, 255))

        # Lista de pontos excluídos
        self.excluded_points = {
            0,
            10,
            20,
            1,
            11,
            2,
            7,
            18,
            8,
            9,
            19,
            29,
            70,
            80,
            90,
            81,
            91,
            92,
            97,
            88,
            98,
            99,
            89,
            79,
        }
        self.viewed_points = set()

        self.last_intensity = 10
        self.createMatrix()
        random.shuffle(self.points)

        self.currentPointIndex = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.validatePoint)

        self.view.keyPressEvent = self.handleKeyPress
        self.view.show()

        self.drawCenterCross()
        self.plotNextPoint()

    def drawCenterCross(self):
        """Desenha uma cruz vermelha no centro da tela"""
        center_x = self.scene.width() / 2
        center_y = self.scene.height() / 2
        size = 10

        line1 = QGraphicsLineItem(center_x - size, center_y, center_x + size, center_y)
        line2 = QGraphicsLineItem(center_x, center_y - size, center_x, center_y + size)

        pen = QPen(QColor(255, 0, 0), 2)
        line1.setPen(pen)
        line2.setPen(pen)

        self.scene.addItem(line1)
        self.scene.addItem(line2)

    def plotPoint(self, x, y, size=10, point_id=None, color=None):
        """Plota um ponto com a cor definida"""
        if point_id in self.excluded_points:
            return

        color = color if color else QColor(255, 255, 255)
        point = QGraphicsEllipseItem(x, y, size, size)
        point.setBrush(QBrush(color))
        point.setPen(QPen(Qt.NoPen))
        self.scene.addItem(point)
        self.view.viewport().update()

    def createMatrix(self):
        """Cria uma matriz 10x10 e posiciona no centro da tela"""
        self.scene.clear()
        self.drawCenterCross()

        num_rows, num_cols = 10, 10
        point_size = 10
        spacing = 100
        total_matrix_size = num_rows * (point_size + spacing) - spacing
        start_x = (self.scene.width() - total_matrix_size) // 2
        start_y = (self.scene.height() - total_matrix_size) // 2

        self.points = []
        point_id = 0
        for i in range(num_rows):
            for j in range(num_cols):
                if point_id in self.excluded_points:
                    point_id += 1
                    continue

                x = start_x + j * (point_size + spacing)
                y = start_y + i * (point_size + spacing)
                self.points.append((x, y, point_id))
                point_id += 1

    def plotNextPoint(self):
        """Plota o próximo ponto"""
        if self.currentPointIndex < len(self.points):
            x, y, point_id = self.points[self.currentPointIndex]
            self.currentPoint = point_id
            self.plotPoint(
                x, y, size=10, point_id=point_id, color=QColor(255, 255, 255)
            )
            self.timer.start(1500)  # Tempo para resposta do usuário
        else:
            self.showFinalMap()

    def handleKeyPress(self, event):
        """Registra a resposta do usuário"""
        if self.currentPointIndex < len(self.points):
            if event.key() == Qt.Key_Space:
                self.viewed_points.add(self.currentPoint)
            self.validatePoint()

    def validatePoint(self):
        """Valida o ponto e passa para o próximo"""
        self.scene.clear()
        self.drawCenterCross()
        self.currentPointIndex += 1
        self.plotNextPoint()

    def showFinalMap(self):
        """Mostra o mapa final com os pontos vistos (verdes) e não vistos (vermelhos)"""
        self.scene.clear()
        num_rows, num_cols = 10, 10
        point_size = 10
        spacing = 100
        total_matrix_size = num_rows * (point_size + spacing) - spacing
        start_x = (self.scene.width() - total_matrix_size) // 2
        start_y = (self.scene.height() - total_matrix_size) // 2

        point_id = 0
        for i in range(num_rows):
            for j in range(num_cols):
                if point_id in self.excluded_points:
                    point_id += 1
                    continue

                x = start_x + j * (point_size + spacing)
                y = start_y + i * (point_size + spacing)
                color = (
                    QColor(0, 255, 0)
                    if point_id in self.viewed_points
                    else QColor(255, 0, 0)
                )
                self.plotPoint(x, y, size=10, point_id=point_id, color=color)
                point_id += 1

        self.drawLegend()
        self.view.viewport().update()

    def drawLegend(self):
        """Desenha a legenda ao lado do mapa"""
        legend_x = self.scene.width() + 600
        legend_y = 100

        green_box = QGraphicsEllipseItem(legend_x, legend_y, 10, 10)
        green_box.setBrush(QBrush(QColor(0, 255, 0)))
        self.scene.addItem(green_box)

        red_box = QGraphicsEllipseItem(legend_x, legend_y + 60, 10, 10)
        red_box.setBrush(QBrush(QColor(255, 0, 0)))
        self.scene.addItem(red_box)

        font = QFont("Arial", 10)
        seen_text = self.scene.addText("Visto", font)
        seen_text.setPos(legend_x + 10, legend_y - 5)

        unseen_text = self.scene.addText("Nao Visto", font)
        unseen_text.setPos(legend_x + 10, legend_y + 55)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exame = CAMPExame(threshold=0)
    sys.exit(app.exec_())
