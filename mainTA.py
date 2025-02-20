#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
## Autor    : Marcel Nogueira d' Eurydice
## Empresa  : Eyetec
## Descricao:
############################################################################

from TAScreen import TAView
from TAExamScene import TAExamScene

# from PyQt4.QtCore import Qt,QTimer,QObject,SIGNAL
# from PyQt4.QtGui import QGraphicsView,QMatrix,QBrush,QImage,QBrush,QColor,QApplication
from PyQt4.QtGui import QApplication

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    scene = TAExamScene("Child")

    view = TAView(scene)

    view.setWindowTitle("Eyetec-TA")
    view.showFullScreen()

    view.updateSettings()

    sys.exit(app.exec_())
