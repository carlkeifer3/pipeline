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
        #import os
        import pipeline.general.filebrowse.thumbview as tv

        self.path = "D:/bank/reference/"
        #self.directory = os.listdir(self.path)
        #self.path = QtCore.QDir()
        #self.path.setPath("D:/bank/reference/")

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

        #def createThumbView(self):
        self.thumbView = tv.thumbView(self.fbWin)
        #self.thumbView.thumbsDir.setPath(self.path)
        self.thumbView.load()
        print "thumbview should be built"
        #self.tlist = QtGui.QListView(self)
        #self.tmodel = QtGui.QStandardItemModel(self.tlist)
        #self.tlist.setModel(self.tmodel)
        #self.tlist.setViewMode(QtGui.QListView.IconMode)
        #self.tlist.setGeometry(QtCore.QRect(0, 0, 800, 390))
        #images = self.path.entryInfoList()
        #for image in images:
        #    self.tItem = QtGui.QStandardItem()
        #    #self.tItem.setText(str(image))
        #    self.tItem.setIcon(QtGui.QIcon(image.filePath()))
        #    self.tmodel.appendRow(self.tItem)

        #self.list = QtGui.QListWidget(self)
        #self.list.setGeometry(QtCore.QRect(0, 0, 250, 400))
        #for image in self.directory:
        #    self.list.addItem(str(self.path + image))

        #self.fbLayout.addWidget(self.list)
        self.fbLayout.addWidget(self.thumbView)
        #self.fbLayout.addWidget(self.tlist)
        self.setLayout(self.fbLayout)



def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()