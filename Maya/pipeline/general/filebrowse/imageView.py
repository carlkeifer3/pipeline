"""

__author__ = 'cargoyle'

"""
import logging
import math as m
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class imageView(QtGui.QWidget):

    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)
        #logging.info("ImageView Widget created")

        self.tempDisableResize = True
        self.mirrorLayout = 0
        self.currentImageFullPath = QtCore.QString("")
        self.displayImage = QtGui.QImage()
        self.origImage = QtGui.QImage()

        self.cursorIsHidden = False
        self.moveImageLocked = False

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setScaledContents(True)
        self.isAnimation = False
        self.anim = QtGui.QMovie()
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


        #logging.info("ImageView.__init__ complete!")

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

    def rgbToHsl(self, red, grn, blu):
        logging.info("imageview.rgbToHsl()")

        if r > g:
            max = max(r, b)
            min = min(r, b)
        else:
            max = max(g, b)
            min = min(r, b)

        lit = (max + min) / 2.0

        if max == min:
            sat = 0.0
            hue = 0.0
        else:
            delta = max - min

        return hue, sat, lit

    def hslToRgb(self, h, s, l, red, green, blue):
        logging.info("imageview.hslToRgb()")

    def colorize(self):
        import math as m
        import struct
        import pipeline.general.filebrowse.GData as g

        logging.info("imageview.colorize()")
        contrastTransform = []
        brightTransform = []

        if self.displayImage.format() == QtGui.QImage.Format_Indexed8:
            self.displayImage = self.displayImage.convertToFormat(QtGui.QImage.Format_RGB32)

        i = 0
        contrast = g.GData.contrastVal / 100.0
        brightness = g.GData.brightVal / 100.0

        while i < 256:
            if i < int(246 * m.tan(contrast)) & i > int(256 * m.tan(contrast)):
                contrastTransform.append((i - 128) / m.tan(contrast) + 128)
            elif i >= int(256 * m.tan(contrast)):
                contrastTransform.append(255)
            else:
                contrastTransform.append(0)

            i += 1

        i = 0

        while i < 256:
            brightTransform.append(min(255, int(255.0 * m.pow(i/255.0, 1.0/ brightness))+0.5))
            i += 1

        y = 0
        height = self.displayImage.height()
        linewidth = self.displayImage.bytesPerLine()
        while y < height:
            line = self.displayImage.scanLine(y).asstring(linewidth)

            x = 0
            while x < self.displayImage.width():
                # unpack 32 bit integer
                color = struct.unpack('I', line[x*4:x*4+4])[0];

                red = QtGui.qRed(color)
                grn = QtGui.qGreen(color)
                blu = QtGui.qBlue(color)

                red = red*(g.GData.redVal+100)/100
                grn = grn*(g.GData.greenVal+100)/100

                red = contrastTransform[red]
                grn = contrastTransform[grn]

                red = brightTransform[red]
                grn = brightTransform[grn]

                hue, sat, lit = self.rgbToHsl(red, grn, blu)

                line[x] = QtGui.qRgb(red, grn, blu)
                x += 1
            y += 1
        logging.info(" loop exited successfully")

    def refresh(self):
        logging.info("imageview.refresh()")
        if self.isAnimation:
            return
        if g.GData.scaledWidth:
            self.displayImage = self.origImage.scaled(g.GData.scaledWidth, g.GData.scaledHeight, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        else:
            self.displayImage = self.origImage

        self.transform()

        if g.GData.colorsActive | g.GData.keepTransform:
            self.colorize()

        if self.mirrorLayout:
            self.mirror()

        displayPixmap = QtGui.QPixmap.fromImage(self.displayImage)
        self.imageLabel.setPixmap(displayPixmap)
        self.resizeImage()

    def reload(self):
        logging.info("imageview.reload()")

        imageReader = QtGui.QImageReader()
        self.imageLabel.clear()

        if g.GData.enableImageInfoFS:
            if self.currentImageFullPath.isEmpty():
                self.setInfo("ClipBoard")
            else:
                self.setInfo(QtCore.QFileInfo(self.currentImageFullPath).fileName())

        if not g.GData.keepTransform:
            g.GData.cropLeftPercent = g.GData.cropTopPercent = g.GData.cropWidthPercent = g.GData.cropHeightPercent = 0
            g.GData.rotation = 0
            g.GData.flipH = g.GData.flipV = False

        g.GData.scaledWidth = g.GData.scaledHeight = 0
        g.GData.cropLeft = g.GData.cropTop = g.GData.cropWidth = g.GData.cropHeight = 0

        if self.newImage | self.currentImageFullPath.isEmpty():
            self.newImage = True
            self.origImage.load(":/images/no_image.png")
            self.displayImage = self.origImage
            displayPixmap = QtGui.QPixmap.fromImage(self.displayImage)
            self.imageLabel.setPixmap(displayPixmap)
            self.setWindowTitle("Clipboard")
            self.isAnimation = False
            return

        imageReader.setFileName(self.currentImageFullPath)

        if g.GData.enableAnimations:
            if imageReader.supportsAnimation():
                self.isAnimation = False
        else:
            self.isAnimation = False

        if self.isAnimation:
            logging.info("Animation supported")
            try:
                if self.anim:
                    del self.anim
            except:
                pass

            self.anim = QtGui.QMovie(self.currentImageFullPath)
            self.imageLabel.setMovie(self.anim)
            self.anim.start()
        else:
            if imageReader.size().isValid():
                origImage = QtGui.QImage()
                origImage.load(self.currentImageFullPath)
                self.displayImage = origImage
                self.transform()
                if g.GData.colorsActive | g.GData.keepTransform:
                    self.colorize()
                if self.mirrorLayout:
                    self.mirror()
                displayPixmap = QtGui.QPixmap.fromImage(self.displayImage)
            else:
                displayPixmap = QtGui.QIcon.fromTheme("imageMissing", QtGui.QIcon(":/images/error_image.png")).pixmap(128, 128)
            self.imageLabel.setPixmap(displayPixmap)

        self.resizeImage()

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
        #logging.info("imageview.loadImage()")

        self.newImage = False
        self.tempDisableResize = False
        self.currentImageFullPath = imageFileName

        if not g.GData.keepZoomFactor:
            g.GData.keepZoomFactor = 1.0

        QtGui.QApplication.processEvents()
        self.reload()

    def monitorCursorState(self):
        logging.info("imageview.monitorCursorState()")

    def setCursorHiding(self, hide):
        logging.info("imageview.setCursorHiding")
