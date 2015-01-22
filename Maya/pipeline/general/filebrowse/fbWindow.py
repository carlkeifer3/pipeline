"""

__author__ = 'cargoyle'

"""
import logging

from PyQt4 import QtGui, QtCore
import sip
import maya.OpenMayaUI as apiUI
import pipeline.general.filebrowse.thumbview as tv

def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


class fbWindow(QtGui.QMainWindow):
    """


    """

    def __init__(self, parent=getMayaWindow()):
        super(fbWindow, self).__init__(parent)
        #import os

        # this is just for now, I want to use QDirectory
        # preferred image locations like this will be
        # captured in qsettings
        self.path = "D:/bank/reference/"
        #self.directory = os.listdir(self.path)

        self.setObjectName("FileBrowser")
        self.resize(810, 390)
        self.fbWin = QtGui.QWidget(self)
        self.fbLayout = QtGui.QVBoxLayout(self.fbWin)
        self.fbLayout.addStretch(1)
        self.fbLayout.setContentsMargins(0,0,0,0)
        self.fbLayout.setSpacing(0)

        # internal class variable time
        self.copyMoveToDialog = 0
        self.colorsDialog = 0
        self.cropDialog = 0
        self.initComplete = True

        self.needHistory = True
        self.interfaceDisabled = False

        # create our views
        self.createThumbView()

        #self.list = QtGui.QListWidget(self)
        #self.list.setGeometry(QtCore.QRect(0, 0, 250, 400))
        #for image in self.directory:
        #    self.list.addItem(str(self.path + image))

        #self.fbLayout.addWidget(self.list)

        self.setLayout(self.fbLayout)


    def createThumbView(self):
        import pipeline.general.filebrowse.thumbview as tv

        self.thumbView = tv.thumbView(self)
        self.thumbView.thumbsDir.setPath(self.path)
        self.thumbView.setGeometry(QtCore.QRect(0, 0, 800, 390))
        self.thumbView.load()
        print "thumbview should be built"
        self.fbLayout.addWidget(self.thumbView)





def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()