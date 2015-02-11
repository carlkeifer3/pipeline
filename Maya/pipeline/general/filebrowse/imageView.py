"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class imageView(QtGui.QWidget):

    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)
        logging.info("ImageView Widget created")
        self.cursorIsHidden = False
        self.moveImageLocked = False

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setScaledContents(True)
        self.isAnimation = False
        self.anim = 0
        self.setPalette(QtGui.QPalette(g.GData.backgroundColor))

        self.mainVLayout = QtGui.QVBoxLayout()
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        self.mainVLayout.addWidget(self.imageLabel)

        self.scrlArea = QtGui.QScrollArea()
        self.scrlArea.setContentsMargins(0, 0, 0, 0)
        self.scrlArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrlArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrlArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrlArea.verticalScrollBar().blockSignals(True)
        self.scrlArea.horizontalScrollBar().blockSignals(True)
        self.scrlArea.setFrameStyle(0)
        self.scrlArea.setLayout(self.mainVLayout)
        self.scrlArea.setWidgetResizable(True)

        self.scrollLayout = QtGui.QVBoxLayout()
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.scrollLayout.addWidget(self.scrlArea)
        self.setLayout(self.scrollLayout)

        self.infoLabel = QtGui.QLabel()
        self.infoLabel.setVisible(False)
        self.infoLabel.setMargin(3)
        self.infoLabel.move(10, 10)
        self.infoLabel.setStyleSheet("background-color: black; color: white; border-radius: 3px")

        self.feedbackLabel = QtGui.QLabel()
        self.feedbackLabel.setVisible(False)
        self.feedbackLabel.setMargin(3)
        self.feedbackLabel.setStyleSheet("background-color: black; color: white; border-radius: 3px")

        self.infoEffect = QtGui.QGraphicsOpacityEffect()
        self.infoEffect.setOpacity(0.5)
        self.infoLabel.setGraphicsEffect(self.infoEffect)
        self.feedbackEffect = QtGui.QGraphicsOpacityEffect()
        self.feedbackEffect.setOpacity(0.5)
        self.feedbackLabel.setGraphicsEffect(self.feedbackEffect)

        self.mouseMovementTimer = QtCore.QTimer()

        g.GData.cropLeft = g.GData.cropTop = g.GData.cropWidth = g.GData.cropHeight = 0
        g.GData.cropLeftPercent = g.GData.cropTopPercent = g.GData.cropWidthPercent = g.GData.cropHeightPercent = 0

        g.GData.hueVal = 0
        g.GData.saturationVal = 100
        g.GData.lightnessVal = 100
        g.GData.hueRedChannel = True
        g.GData.hueGreenChannel = True
        g.GData.hueBlueChannel = True

        g.GData.contrastVal = 78
        g.GData.brightVal = 100

        g.GData.dialogLastX = g.GData.dialogLastY = 0

        self.newImage = False
        self.cropBand = 0


        logging.info("ImageView.__init__ complete!")

    def getHeightByWidth(self, imgWidth, imgHeight, newWidth):
        logging.info("imageview.getHeightByWidth()")
        logging.info("")

    def getWidthByHeight(self, imgHeigth, imgWidth, newHeight):
        logging.info("imageview.getWidthByHeight()")
        logging.info("")

    def calcZoom(self, size):
        logging.info("imageview.calcZoom")
        return size * g.GData.imageZoomFactor

    def resizeImage(self):
        logging.info("imageview.resizeImage()")

    def resizeEvent(self, event):
        logging.info("imageview.resizeEvent()")

    def showEvent(self, event):
        logging.info("imageview.showEvent()")

    def centerImage(self, imgSize):
        logging.info("imageview.centerImage()")

    def rotateByExifRotation(self, image, imageFullPath):
        logging.info("imageview.rotateByExifRotation")

    def transform(self):
        logging.info("imageview.transform()")

    def mirror(self):
        logging.info("imageview.mirror()")

    def bound0_255(self, val):
        logging.info("imageview.bound0_255()")

    def hslValue(self, n1, n2, hue):
        logging.info("imageview.hslValue()")

    def rgbToHsl(self, r, g, b, hue, sat, light):
        logging.info("imageview.rgbToHsl()")

        if r > g:
            max = max(r, b)
            min = min(r, b)
        else:
            max = max(g, b)
            min = min(r, b)

        l = (max + min) / 2.0

        if max == min:
            s = 0.0
            h = 0.0
        else:
            delta = max - min

    def hslToRgb(self, h, s, l, red, green, blue):
        logging.info("imageview.hslToRgb()")

    def colorize(self):
        logging.info("imageview.colorize()")

    def refresh(self):
        logging.info("imageview.refresh()")

    def reload(self):
        logging.info("imageview.reload()")

    def setInfo(self, infoString):
        logging.info("imageview.setInfo")
        self.infoLabel.setText(infoString)
        self.infoLabel.adjustSize()

    def unsetFeedback(self):
        logging.info("imageview.unsetFeedback()")
        self.feedbackLabel.setText("")
        self.feedbackLabel.setVisible(False)

    def setFeedback(self, feedbackSrting):
        logging.info("imageview.setFeedback()")
        self.feedbackLabel.setText(feedbackSrting)
        self.feedbackLabel.setVisible(True)

        if self.infoLabel.isVisible():
            margin = self.infoLabel.height() + 15
        else:
            margin = 10

        self.feedbackLabel.move(10, margin)
        self.feedbackLabel.adjustSize()
        QtCore.QTimer.singleShot(3000, self.unsetFeedback())

    def loadImage(self, imageFileName):
        logging.info("imageview.loadImage()")

    def monitorCursorState(self):
        logging.info("imageview.monitorCursorState()")

    def setCursorHiding(self, hide):
        logging.info("imageview.setCursorHiding")