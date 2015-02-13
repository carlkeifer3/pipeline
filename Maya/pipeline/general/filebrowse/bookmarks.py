"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class BookMarks(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        import os
        import pymel.core as pm

        # initialize the QlistView
        QtGui.QTreeWidget.__init__(self, parent)

        self.GData = g.GData()

        #locate the directory where all of the images for the UI live
        ScriptDir = pm.internalVar(uad = True)
        self.imgDirectory = str(ScriptDir+"/scripts/pipeline/general/filebrowse/images/")

        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.reloadBookmarks()

    def reloadBookmarks(self):
        #logging.info("bookmarks.reloadBookmarks()")
        #logging.info("reloading Bookmarks")
        self.clear()
        bmList = g.GData.bookmarkPaths
        for model in bmList:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, QtCore.QFileInfo(model).fileName())
            item.setIcon(0, QtGui.QIcon(self.imgDirectory+"bookmarks.png"))
            item.setToolTip(0, model)
            self.insertTopLevelItem(0, item)
            #logging.info("bookmark "+QtCore.QFileInfo(model).fileName()+" has been added to list of bookmarks")


    def resizeTreeColumn(self):
        logging.info("resizing Tree Column")
        self.resizeColumnToContents(0)

    def removeBookmark(self):
        logging.info("bookmarks.removeBookmark()")
        logging.info("remove the bookmark: "+ self.selectedItems()[0].toolTip(0))
        g.GData.bookmarkPaths.remove(self.selectedItems()[0].toolTip(0))
        self.reloadBookmarks()


    def dragEnterEvent(self, event):
        logging.info("bookmarks.dragEnterEvent()")
        logging.info("Drag enter event")

        selectedDirs = self.selectionModel().selectedRows()
        if len(selectedDirs) > 0:
            self.dndOrigSelection = selectedDirs[0]

        event.acceptProposedAction

    def dragMoveEvent(self, event):
        logging.info("bookmarks.dragMoveEvent()")
        logging.info("Drag move event")

        self.setCurrentIndex(self.indexAt(event.pos()))

    def dropEvent(self, event):
        logging.info("bookmarks.dropEvent()")
        logging.info("Drop event")

        if event.source():
            fstreeStr = QtCore.QString("FSTree")
            dirOp = bool(event.source().metaObject().className() == fstreeStr)
            self.emit(dropOp(event.keyboardModifiers, dirOp, event.mimeData().urls()[0].toLocalFile()))