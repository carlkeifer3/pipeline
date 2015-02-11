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
        logging.info("bookmarks.reloadBookmarks()")
        logging.info("reloading Bookmarks")
        self.clear()
        bmList = g.GData.bookmarkPaths
        for model in bmList:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, QtCore.QFileInfo(model).fileName())
            item.setIcon(0, QtGui.QIcon(self.imgDirectory+"bookmarks.png"))
            item.setToolTip(0, model)
            self.insertTopLevelItem(0, item)
            logging.info("bookmark "+QtCore.QFileInfo(model).fileName()+" has been added to list of bookmarks")


    def resizeTreeColumn(self):
        logging.info("resizing Tree Column")
        self.resizeColumnToContents(0)

    def removeBookmark(self):
        logging.info("remove the selected bookmark")
        selectedDirs = self.selectionModel().selectedRows()

    def dragEnterEvent(self, event):
        logging.info("Drag enter event")

    def dragMoveEvent(self, event):
        logging.info("Drag move event")

    def dropEvent(self, event):
        logging.info("Drop event")