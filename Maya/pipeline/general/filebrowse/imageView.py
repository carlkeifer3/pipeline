"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class ImageView(QtGui.QWidget):

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
        self.scrlArea.verticalSrollBar().blockSignals(True)
        self.scrlArea.hoizontalScrollBar().blockSignals(True)
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
        self.infoLabel.setStyleSheet(QtGui.QLabel("background-color: black; color: white; border-radius: 3px"))

        self.feedbackLabel = QtGui.QLabel()
        self.feedbackLabel.setVisible(False)
        self.feedbackLabel.setMargin(3)



        logging.info("ImageView.__init__ complete!")



