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

        self.path = "D:/bank/reference/"
        self.directory = os.listdir(self.path)



        self.setObjectName("FileBrowser")
        self.resize(810, 390)
        self.fbWin = QtGui.QWidget()
        self.fbLayout = QtGui.QVBoxLayout()
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


        self.SaveRig = QtGui.QPushButton(self)
        self.SaveRig.setGeometry(QtCore.QRect(410, 320, 141, 61))
        self.SaveRig.setObjectName("SaveRig")
        self.SaveRig.setText("Save Rig")

        #def createThumbView(self):
        self.thumbView = tv.thumbView()
        #self.thumbView.thumbsDir.setPath(self.path)
        self.thumbView.setPath(self.path)
        self.thumbView.setGeometry(QtCore.QRect(0,0,800,319))
        self.thumbView.load()
        print "thumbview should be built"
        #self.tlist = QtGui.QListView(self)
        #self.tmodel = QtGui.QStandardItemModel(self.tlist)
        #self.tlist.setModel(self.tmodel)
        #self.tlist.setViewMode(QtGui.QListView.IconMode)
        #self.tlist.setGeometry(QtCore.QRect(0, 0, 800, 319))
        #thumbWidth = 100 * 2
        #self.tlist.setIconSize(QtCore.QSize(thumbWidth, thumbWidth))
        #for image in self.directory:
        #    self.tItem = QtGui.QStandardItem()
        #    #self.tItem.setText(str(image))
        #    self.tItem.setIcon(QtGui.QIcon(str(self.path+image)))
        #    self.tmodel.appendRow(self.tItem)

        #self.list = QtGui.QListWidget(self)
        #self.list.setGeometry(QtCore.QRect(0, 0, 250, 400))
        #for image in self.directory:
        #    self.list.addItem(str(self.path + image))

        #self.fbLayout.addWidget(self.list)
        self.fbLayout.addWidget(self.thumbView)
        self.fbLayout.addWidget(self.tlist)
        self.fbLayout.addWidget(self.SaveRig)
        self.setLayout(self.fbLayout)



def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()