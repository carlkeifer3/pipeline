"""

__author__ = 'cargoyle'

"""
import logging
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
        self.fsModel.setFilter(QtCore.QDir.AllDirs|QtCore.QDir.NoDotAndDotDot)

        self.setModel(self.fsModel)

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

        #self.expanded.connect(lambda: self.resizeTreeColumn())
        #self.collapsed.connect(lambda: self.resizeTreeColumn())

        self.setHeaderHidden(True)


    def getCurrentIndex(self):
        logging.info("fsTree.getCurrentIndex()")
        return self.selectedIndexes.first()

    def resizeTreeColumn(self):
        logging.info("fsTree.resizeTreeColumn()")
        self.resizeColumnToContents(0)

    def dragEnterEvent(self, event):
        logging.info("fsTree.dragEnterEvent()")
        selectedDirs = self.selectionModel().selectedRows()
        if len(selectedDirs) > 0:
            self.dndOrigSelection = selectedDirs[0]
            event.acceptProposedAction()

    def dropEvent(self, event):
        logging.info("fsTree.dropEvent()")
        if event.source():
            fsTreeStr = QtCore.QString("FSTree")
            dirOp = event.source().metaObject().className() == fsTreeStr
            emit.dropOp(event.keyboardModifiers(), dirOp, event.mimeData().urls().at(0).toLocalFile)
            self.setCurrentIndex(self.dndOrigSelection)

    def setModelFlags(self):
        logging.info("fsTree.setModelFlags()")
        self.fsModel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        if g.GData.showHiddenFiles:
            self.fsModel.setFilter(self.fsModel.filter() | QtCore.QDir.Hidden)