"""

__author__ = 'cargoyle'

"""
from PyQt4 import QtGui, QtCore

class FSTree(QtGui.QTreeView):

    def __init__(self, parent=None):
        import os

        # initialize the QlistView
        QtGui.QTreeView.__init__(self, parent)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)


        self.fsModel = QtGui.QFileSystemModel(self)
        self.fsModel.setRootPath("")
        #self.setModelFlags()

        self.setModel(self.fsModel)

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

        self.setHeaderHidden(True)