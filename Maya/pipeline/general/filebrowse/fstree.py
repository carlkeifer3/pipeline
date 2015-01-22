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
        self.setDragDropMode(QtCore.QAbstractItemView.InternalMove)

        self.fsModel = QtCore.QFileSystemModel(self)
        self.fsModel.setRootPath("")
        #self.setModelFlags()

        self.setModel(self.fsModel)