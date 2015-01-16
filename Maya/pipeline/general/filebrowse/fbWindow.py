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


        #def createThumbView(self):
        self.thumbView = tv.thumbView()
        self.thumbView.thumbsDir.setPath(self.path)
        self.thumbView.load()
        print "thumbview should be built"

        self.fbLayout.addWidget(self.thumbView)
        self.setLayout(self.fbLayout)



def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()