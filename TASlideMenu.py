############################################################################
## Autor    : Marcel Nogueira d' Eurydice
## Empresa  : Eyetec
## Descricao:
############################################################################

from TASlide    import *
from TASVG      import TASVG

from PyQt4 import QtCore, QtGui

class TASlideMenu(TASlide):
    """
    """

    _layoutType     = None
    _optList        = []
    _examType       = None
    _maskIndex      = -1
    _maskSet        = False
    _currentPos     = 0
    _acceptDistance = QtGui.QMatrix(0.7,0,0,0.7,0,0)

    def __init__(self,width=1200,height=800,layoutIndex=0):
        """

        Arguments:
        - `width`:
        - `height`:
        """
        super(TASlideMenu,self).__init__(width,height,layoutIndex)

        self._anim = QtGui.QGraphicsItemAnimation()
        self._timeLine = QtCore.QTimeLine(200)
        self._timeLine.setFrameRange(0, 100)
        self._anim.setTimeLine(self._timeLine)

        self.setSelectorPositions()

        self._examType = "Menu"
        self._optMode  = "fixed"

        self.listFiles()

        self.setSquareLayout()
        self.drawOptotypes()


    def listFiles(self):
        """

        """
        self.menu        = "/home/eyetec/images/menu/menu.svg"
        #self.menuOptions = "/home/eyetec/images/menu/menu-options.svg"
        self.selector    = "/home/eyetec/images/menu/selector.svg"



    def setSelectorPositions(self):
        """

        """
        self._selctPosList = [0,245,530,780,1050,1320]




    def nextSlide(self):
        """

        """
        if self._timeLine.state()==0:
            oldPos = self._currentPos
            self._currentPos = (self._currentPos+1)%len(self._selctPosList)
            self.animateSelector(oldPos,self._currentPos)

    def previousSlide(self):
        """

        """
        if self._timeLine.state()==0:
            oldPos = self._currentPos
            self._currentPos = (self._currentPos-1)%len(self._selctPosList)
            self.animateSelector(oldPos,self._currentPos)


    def getSelection(self):
        """
        """
        return {
            0 : "Distance",
            1 : "Calibration",
            2 : "ScreenSaver",
            3 : "DisplayImage",
	    4 : "ScreenOnOff",
            5 : "SaveConf"
            }[self._currentPos]

    def drawOptotypes(self):
        """

        """

        self._optList.append(TASVG(self.menu))

        self._selectorObj = TASVG(self.selector)
        self._selectorObj.setPos(0,550)
        self._anim.setItem(self._selectorObj)

        self._optList.append(self._selectorObj)

        #self._optList.append(TASVG(self.menuOptions))

    def animateSelector(self,oldPos,brandNew):
        """

        Arguments:
        - `oldPos`:
        - `brandNew`:
        """
        if self._timeLine.state()==0:
            xPos0 = self._selctPosList[oldPos]
            xPos1 = self._selctPosList[brandNew]

            self._anim.setPosAt(0,QtCore.QPointF(xPos0, 550))
            self._anim.setPosAt(1,QtCore.QPointF(xPos1, 550))
            self._timeLine.start()



    def update(self):
        """

        """
        for i in range(12):
            self._optList[i].setExam(self._examType)
            self._optList[i].draw()


    def hide(self):
        """

        """
        for opt in self._optList:
            opt.hide()

    def show(self):
        """

        """
        for opt in self._optList:
            opt.show()
