"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore


class InfoView(QtGui.QTableView):

    def __init__(self, parent = None):

        QtGui.QTableView.__init__(self,parent)
        logging.info("InfoView Class instantiated")

        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(self.verticalHeader().minimumSectionSize())
        self.horizontalHeader().setVisible(False)
        #self.horizontalHeader().setSectionResizeMode()
        self.setShowGrid(False)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setTabKeyNavigation(False)

        self.infoModel = QtGui.QStandardItemModel(self)
        self.setModel(self.infoModel)

        ## infoview menu
        self.infoMenu = QtGui.QMenu("")
        self.copyAction = QtGui.QAction("Copy", self)
        #self.copyAction.triggered.connect(lambda: self.copyEntry)
        self.infoMenu.addAction(self.copyAction)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        logging.info("InfoView Class Init complete")

    def showInfoViewMenu(self, pt):
        logging.info("infoview.showInfoViewMenu()")

        selectedEntry = self.indexAt(pt)
        if selectedEntry.isValid():
            self.infoMenu.popup(self.viewport().maptoGlobal(pt))

    def clear(self):
        logging.info("infoview.clear()")
        self.infoModel.clear()

    def addEntry(self, key, value):
        logging.info("infoview.addEntry()")

        atRow = self.infoModel.rowCount()
        itemKey = QtGui.QStandardItem(key)
        self.infoModel.insertRow(atRow, itemKey)
        if not value.isEmpty():
            itemVal = QtGui.QStandardItem(value)
            itemVal.setToolTip(value)
            self.infoModel.setItem(atRow, itemVal)

    def addTitleEntry(self, title):
        logging.info("infoview.addTitleEntry()")

        atRow = self.infoModel.rowCount()
        itemKey = QtGui.QStandardItem(title)
        self.infoModel.insertRow(atRow, itemKey)

        boldFont = QtGui.QFont.boldFont()
        boldFont.setBold(True)
        itemKey.setData(boldFont, QtCore.Qt.FontRole)

    def copyEntry(self):
        logging.info("infoview.copyEntry()")

        if self.selectedEntry().isValid():
            QtCore.QApplication.clipboard.setText(infoModel.itemFromIndex(self.selectedEntry()).toolTip())