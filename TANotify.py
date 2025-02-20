############################################################################
## Autor      : Marcel Nogueira d' Eurydice
## Empresa    : Eyetec
## Descricao  :
## Modificacao: Klausner Augusto
## Motivo:    : Uma notificacao mais rapido
############################################################################

from TAText import TAText

from random import randint

from PyQt4.QtCore import QTimer, QObject, SIGNAL, Qt


class TANotify(object):
    """ """

    _obj = None

    def __init__(self, color=None, width=1280, height=800, layoutIndex=0):
        """
        Arguments:
        - `width`:
        - `height`:
        """
        self._width = width
        self._height = height

        self._timer = QTimer()
        self._timer.setSingleShot(True)
        QObject.connect(self._timer, SIGNAL("timeout()"), self.hide)

        if not color:
            self._color = Qt.blue

        self.drawNotify()

    def setMatrix(self, matrix):
        """

        Arguments:
        - `matrix`:
        """

        m11 = matrix.m11()

        self._obj.setMatrix(matrix)

        self._obj.setPos(
            50 - (m11 - 1) * (self._width / 2.0 - 50) + 0.1,
            (self._height) - 50 + (m11 - 1) * (self._height / 2.0 - 50) + 0.1,
        )

    def drawNotify(self):
        """

        Arguments:
        - `self`:
        """
        self._obj = TAText(size=15, fontFamily="URW Gothic L")

        self._obj.setPos(50, (self._height) - 50)

        self._obj.setColor(self._color)

    def setText(self, text="", color=None):
        """ """
        if color:
            self._obj.setColor(color)
        else:
            self._obj.setColor(self._color)

        self._obj.setText(text)

    def update(self):
        """

        Arguments:
        - `self`:
        """
        self._obj.draw()

    def hide(self):
        """

        Arguments:
        - `self`:
        """
        self._obj.hide()

    def show(self):
        """

        Arguments:
        - `self`:
        """
        self._obj.show()
        self._timer.start(3500)

    def showQuick(self):
        """

        Arguments:
        - `self`:
        """
        self._obj.show()
        self._timer.start(300)

    def getItem(self):
        return self._obj
