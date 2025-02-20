#!/usr/bin/python
############################################################################
## Autor     : Marcel Nogueira d' Eurydice
## Empresa   : Eyetec
## Descricao :
## Modificado: Klausner Augusto
## Motivo    : Uma notificacao mais rapida
############################################################################
import glob

from TASlideDisplayImage import TASlideDisplayImage
from TASlideSquare  import TASlideSquare
from TASlideClock   import TASlideClock
from TASlideEDTRS   import TASlideEDTRS
from TASlideSVG     import TASlideSVG
from TASlidePNGList import TASlidePNGList
from TASlideSVGList import TASlideSVGList
from TASlideTwoPics import TASlideTwoPics
from TASlideAnimate import TASlideAnimate
from TASlideHBar    import TASlideHBar
from TASlideVBar    import TASlideVBar

from TASlideMenu    import TASlideMenu
from TAExamSettings import TAExamSettings
from TANotify       import TANotify


from PyQt4.QtCore import Qt
from PyQt4.QtGui  import QGraphicsScene,QBrush
from PyQt4.QtSvg  import QGraphicsSvgItem

import os

class TAExamScene(QGraphicsScene):
    """
    """
    _actualSlide = None
    _slideNumber = 0
    _NSlides     = 0
    _slideDict   = {}
    _visibility  = True

    def __init__(self,exam,width=1280,height=800):
        """
        """
        super(TAExamScene, self).__init__()

        self._width  = width
        self._height = height

        self.setSceneRect(0,0,width,height)
        self.setItemIndexMethod(TAExamScene.NoIndex)

        self.setBackgroundBrush(Qt.white)

        self._exam = exam

        self._layout = "square"
        self._examSettings = TAExamSettings()

        self.RGMask = QGraphicsSvgItem("/home/eyetec/images/redgreen.svg")
        self.RGMask.hide()
        self.RGMask.setPos(-10000+width/2,-6250+height/2)
        self.addItem(self.RGMask)

        self.createSlide("square-0",layoutIndex=0)
        self.createSlide("square-1",layoutIndex=1)
        self.createSlide("square-2",layoutIndex=2)
        self.createSlide("square-3",layoutIndex=3)
        #self.createSlide("square-4",layoutIndex=4)

        self.createSlide("HOTV",layoutIndex=2)
        self._slideDict["HOTV"].setExam("HOTV")
        self._slideDict["HOTV"]._optMode="fixed"


        self.createSlide("Clock",layoutIndex=0)
        self.createSlide("EDTRS",layoutIndex=0)
        self.createSlide("Animate",layoutIndex=0)

        # Menu
        self.createSlide("Menu",layoutIndex=0)
        self.createSlide("Calibration",layoutIndex=0,slideType="SVGList")
        self._slideDict["Calibration"]._acceptDistance=True

        ###
        self.createSlide("hBar",layoutIndex=0)
        self.createSlide("vBar",layoutIndex=0)

        self.createSlide("4Balls",layoutIndex=0,slideType="SVG",background=Qt.black)
        self.createSlide("FixPoint",layoutIndex=0,slideType="SVG",background=Qt.black)
        self.createSlide("Amsler",layoutIndex=0,slideType="SVG")
        self.createSlide("RedGreen",layoutIndex=0,slideType="SVG")
        self.createSlide("Ishihara",layoutIndex=0,slideType="PNG")
        self.createSlide("3D",layoutIndex=0,slideType="PNG")

        self.createSlide("Semafore",layoutIndex=0,slideType="SVGList")
        self.createSlide("Tortion",layoutIndex=0,slideType="SVGList")
        self.createSlide("Cylinder",layoutIndex=0,slideType="SVGList")


        # self.createSlide("cylinder",layoutIndex=0)
        self.createSlide("Glaucoma",layoutIndex=0,slideType="Transition")
        self.createSlide("Cataracta",layoutIndex=0,slideType="Transition")

        self.createSlide("Help",layoutIndex=0,slideType="PNG")
        self.createSlide("Info",layoutIndex=0,slideType="PNG")


        self._notify = TANotify()
        item = self._notify.getItem()
        self.addItem(item)
        item.hide()

        self._actualSlide = "square-0"
        self._slideDict[self._actualSlide].show()

        self._actualExam = "Letter"

    def slideAccpetDistance(self):
        """

        """
        return self._slideDict[self._actualSlide].acceptDistance()



    def createSlide(self,slideName=None,layoutIndex=0,slideType=None,background=Qt.white):
        """

        Arguments:
        - `self`:
        """
        if slideName == None:
            slideName = "slide-%02d"%self._NSlides

        if slideName == "Clock":
            slide = TASlideClock(layoutIndex=layoutIndex)
        elif slideName == "EDTRS":
            slide = TASlideEDTRS(layoutIndex=layoutIndex)
        elif slideName == "Animate":
            slide = TASlideAnimate(layoutIndex=layoutIndex)
        elif slideName == "hBar":
            slide = TASlideHBar(layoutIndex=layoutIndex)
        elif slideName == "vBar":
            slide = TASlideVBar(layoutIndex=layoutIndex)
        elif slideType == "SVG":
            slide = TASlideSVG(layoutIndex=layoutIndex,slideName=slideName,background=background)
        elif slideType == "SVGList":
            slide = TASlideSVGList(layoutIndex=layoutIndex,slideName=slideName)
        elif slideType == "PNG":
            slide = TASlidePNGList(layoutIndex=layoutIndex,slideName=slideName)
        elif slideType == "Transition":
            slide = TASlideTwoPics(layoutIndex=layoutIndex,directory=slideName)
        elif slideName == "Menu":
            slide = TASlideMenu(layoutIndex=layoutIndex)
        else:
            slide = TASlideSquare(layoutIndex=layoutIndex)

        self._slideDict[slideName]=slide
        self._drawSlide(slideName)

        slide.hide()

    def createCustomSlide(self,layoutIndex=0,background=Qt.white, path=None):


        slide = TASlideDisplayImage(layoutIndex=layoutIndex, path=path)

        self._slideDict["DisplayImage"] = slide
        self._drawSlide("DisplayImage")

        slide.hide()

    def deleteSlideFromSlidDict(self, slideName):
        del self._slideDict[slideName]

    def updateSSquareSize(self, size):
        for slide in self._slideDict:
            if isinstance(self._slideDict[slide], TASlideSquare) or isinstance(self._slideDict[slide], TASlideEDTRS):
                self._slideDict[slide].updateOptotypeSizes(size)

    def _drawSlide(self,slideName="slide-00"):
        """

        Arguments:
        - `self`:
        """

        for item in self._slideDict[slideName].getOptotypes():
            self.addItem(item)

        for item in self._slideDict[slideName].getScale():
            self.addItem(item)

        self._actualSlide = slideName


    def _drawMask(self):
        """

        Arguments:
        - `self`:
        """

        pass

    def loadExam(self,exam):
        """

        Arguments:
        - `self`:
        - `exam`:
        """

        examType = exam

        if examType in ["Child","Child2","Letter","Number","Landolt","EChart"]:
            examType = "square-0"

        # Different Slides accessed by the same key

        if exam=="Child" and self._actualExam=="Child":
            exam = "Child2"
        if exam=="vBar" and self._actualExam=="vBar":
            exam = "hBar"
        if exam=="FixPoint" and self._actualExam=="FixPoint":
            exam = "Amsler"
        if exam=="Cataracta" and self._actualExam=="Cataracta":
            exam = "Glaucoma"
            self.notify(u" ")
        elif exam == "Cataracta":
            self.notify(u" ")
        if exam=="Ishihara" and self._actualExam=="Ishihara":
            exam = "Semafore"
        elif exam=="Ishihara" and self._actualExam=="Semafore":
            os.system("python game.pyc")

        optMode =  self._slideDict[examType]._optMode

        if optMode == "fixed":
            self._slideDict[self._actualSlide].hide()
            self._actualSlide = exam
            self._slideDict[self._actualSlide].show()
        else:
            self._slideDict[self._actualSlide].hide()
            self._actualSlide = "square-0"
            self._slideDict[self._actualSlide].show()


            for slide in self._slideDict.values():
                if slide._examType != "HOTV":
                    slide.setExam(exam)


        self._slideDict[self._actualSlide].reset()
        self._actualExam = exam


    def setExam(self,exam):
        """

        Arguments:
        - `self`:
        - `exam`:
        """
        self.loadExam(exam)

        self._examSettings.resetCycle()

    def reset(self):
        """
        """
        self._slideDict[self._actualSlide].reset()
#        self._slideDict[self._actualSlide].show()

    def randomizeSlide(self):
        """

        """

        self._slideDict[self._actualSlide].randomize()



    def cleanSlide(self):
        """

        """
        for item in self._slideDict[self._actualSlide].getOptotypes():
            self.removeItem(item)


    def nextSlide(self):
        """

        Arguments:
        - `self`:
        """


        if self._actualSlide[:6] == "square":
            self._slideDict[self._actualSlide].hide()
            self._slideDict[self._actualSlide].randomize()

            self._actualSlide = self._examSettings.getNextSlide(self._layout)

            self._slideDict[self._actualSlide].randomize()
            self._slideDict[self._actualSlide].show()

        else:
            self._slideDict[self._actualSlide].nextSlide()

    def previousSlide(self):
        """

        Arguments:
        - `self`:
        """

        if self._actualSlide[:6] == "square":
            self._slideDict[self._actualSlide].hide()
            self._slideDict[self._actualSlide].randomize()

            self._actualSlide = self._examSettings.getPreviousSlide(self._layout)

            self._slideDict[self._actualSlide].randomize()
            self._slideDict[self._actualSlide].show()

        else:
            self._slideDict[self._actualSlide].previousSlide()

    def setVisible(self):
        self._visibility = True
        self.setForegroundBrush(QBrush(Qt.black,Qt.NoBrush))

    def toggleVisibility(self):
        """

        Arguments:
        - `self`:
        """
        self._visibility = bool((self._visibility+1)%2)


        if self._visibility:
            self.showSlide()

        #     self._slideDict[self._actualSlide].show()
        #     # self.setForegroundBrush(QBrush(Qt.black,Qt.NoBrush))
        # else:
        #     self._slideDict[self._actualSlide].hide()
        #     # self.setForegroundBrush(Qt.black)



    def hideSlide(self):
        """
        """
        self._slideDict[self._actualSlide].hide()

    def updateSSquareSize(self, size):
        for slide in self._slideDict:
            if isinstance(self._slideDict[slide], TASlideSquare) or isinstance(self._slideDict[slide], TASlideEDTRS):
                self._slideDict[slide].updateOptotypeSizes(size)

    def showSlide(self):
        """
        """
        self.previousMask()
        self.nextMask()

    def hideMask(self):
        """

        Arguments:
        - `self`:
        """

        self._slideDict[self._actualSlide].show()


    def showMask(self):
        """

        Arguments:
        - `self`:
        """

        self._slideDict[self._actualSlide].setMask()


    def toggleRGMask(self):
        """
        """

        if self.RGMask.isVisible():
            self.RGMask.hide()
        else:
            self.RGMask.show()


    def showRGMask(self):
        """

        Arguments:
        - `self`:
        """
        self.RGMask.show()

    def hideRGMask(self):
        """

        Arguments:
        - `self`:
        """
        self.RGMask.hide()


    def showScale(self):
        """

        Arguments:
        - `self`:
        """
        self._slideDict[self._actualSlide].showScale()

    def hideScale(self):
        """

        Arguments:
        - `self`:
        """
        self._slideDict[self._actualSlide].hideScale()

    def nextMask(self):
        """

        Arguments:
        - `self`:
        """

        self._slideDict[self._actualSlide].nextMask()


    def previousMask(self):
        """

        Arguments:
        - `self`:
        """

        self._slideDict[self._actualSlide].previousMask()



    def applyOptContrast(self,opacity):
        """

        Arguments:
        - `self`:
        - `opacity`:
        """
        for item in self._slideDict[self._actualSlide].getOptotypes():
            item.setContrast(opacity)


        if self._actualSlide == "Clock":
            item.setContrast(opacity)

    def applyOptColor(self,color):
        """

        Arguments:
        - `self`:
        - `color`:
        """
        for item in self._slideDict[self._actualSlide].getOptotypes():
            item.setColor(color)

        for item in self._slideDict[self._actualSlide].getScale():
            item.setColor(color)


    def notify(self,text,color=None):
        """
        """
        self._notify.setText(text,color)
        self._notify.show()

    def notifyQuick(self,text,color=None):
        """
        """
        self._notify.setText(text,color)
        self._notify.showQuick()
	self._notify


    def getBackground(self):
        """

        """
        return self._slideDict[self._actualSlide].getBackground()

    def acceptBrightness(self):
        """

        """
        return self._slideDict[self._actualSlide].acceptBrightness()


    def acceptContrast(self):
        """

        """
        return self._slideDict[self._actualSlide].acceptContrast()

    def acceptNegative(self):
        """

        """
        return self._slideDict[self._actualSlide].acceptNegative()

    def acceptRedGreenFilter(self):
        """

        """
        return self._slideDict[self._actualSlide].acceptRedGreenFilter()


    def acceptYellBlueFilter(self):
        """

        """
        return self._slideDict[self._actualSlide].acceptYellBlueFilter()


    def setSlidefromBank(self,slide,status):
        """

        Arguments:
        - `slide`:
        - `status`:
        """

        if slide[:6]== "square":
            self.loadExam(status[1])
            self._slideDict[self._actualSlide].hide()
            self._actualSlide = slide
        else:
            self.loadExam(slide)

        # self._actualSlide = slide
        # self._slideDict[self._actualSlide].show()
        if status[2]:
            status[3] -= 1
            self._slideDict[slide].setStatus(status)
            self.nextMask()
            status[3] += 1
        else:
            self._slideDict[slide].setStatus(status)
