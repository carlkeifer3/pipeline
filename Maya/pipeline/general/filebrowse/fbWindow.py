"""

__author__ = 'cargoyle'

"""
import logging

from PyQt4 import QtGui, QtCore
import sip
import maya.OpenMayaUI as apiUI


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class fbWindow(QtGui.QMainWindow):
    """


    """

    def __init__(self, parent=getMayaWindow()):
        super(fbWindow, self).__init__(parent)
        import os
        import pipeline.general.filebrowse.thumbview as tv

        self.path = "d:/bank/reference/"
        self.directory = os.listdir(self.path)



        self.setObjectName("FileBrowser")
        self.fbWin = QtGui.QWidget()
        self.fbLayout = QtGui.QHBoxLayout()
        self.fbLayout.setContentsMargins(0,0,0,0)
        self.fbLayout.setSpacing(0)

        # internal class variable time
        self.copyMoveToDialog = 0
        self.colorsDialog = 0
        self.cropDialog = 0
        self.initComplete = True

        self.needHistory = True
        self.interfaceDisabled = False

        self.thumbView = tv.thumbView()
        """
        self.pixLayout = QtGui.QGridLayout()
        # here is where I want to add my thumbnail squares
        row = 0
        col = 0
        for image in self.directory:
            file = str(self.path+image)
            print file
            self.label = QtGui.QLabel(self)
            self.pixmap = QtGui.QPixmap(file)
            #pixmap = pixmap.scaled(600, 600)
            self.label.setPixmap(self.pixmap)
            self.pixLayout.addWidget(self.label, row, col)
            col+=1
            if col >= 6:
                row+=1
                col=0
        """

        self.fbLayout.addWidget(self.fbWin)
        self.setLayout(self.fbLayout)



def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()