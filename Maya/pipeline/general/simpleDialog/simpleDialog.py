"""

__author__ = 'cargoyle'

"""
from PyQt4 import QtGui, QtCore
import sip
import maya.OpenMayaUI as apiUI

def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class sdWindow(QtGui.QDialog):
    """

    """

    def __init__(self, parent=getMayaWindow()):

        # initialize the QWidget
        QtGui.QDialog.__init__(self, parent)

        self.nameData = ""

        nameLabel = QtGui.QLabel("Name:")
        self.nameEdit = QtGui.QLineEdit()
        nameBox = QtGui.QHBoxLayout()
        nameBox.addStretch(1)
        nameBox.addWidget(nameLabel)
        nameBox.addWidget(self.nameEdit)

        self.acceptButton = QtGui.QPushButton('Accept')
        self.acceptButton.clicked.connect(lambda: self.accepted())

        self.cancelButton = QtGui.QPushButton('Cancel')
        self.cancelButton.clicked.connect(lambda: self.rejected())

        actionBox = QtGui.QHBoxLayout()
        actionBox.addStretch(1)
        actionBox.addWidget(self.acceptButton)
        actionBox.addWidget(self.cancelButton)

        dialogBox = QtGui.QVBoxLayout()
        dialogBox.addLayout(nameBox)
        dialogBox.addLayout(actionBox)

        self.setLayout(dialogBox)

        self.show()

    def accepted(self):
        print "accepted"

        self.nameData = str(self.nameEdit.text())
        self.accept()

    def rejected(self):
        print "rejected"
        self.reject()

def sdWinInit():
    print "hey, dialog coming up"

    window = sdWindow()
    returnCode = window.exec_()
    if returnCode == QtGui.QDialog.Accepted:
        # get the data
        print window.nameData
