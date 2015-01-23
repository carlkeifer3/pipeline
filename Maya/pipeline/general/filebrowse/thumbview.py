"""

__author__ = 'cargoyle'

"""
from PyQt4 import QtGui, QtCore

class thumbView(QtGui.QListView):

    def __init__(self, parent=None):
        import os

        # initialize the QlistView
        QtGui.QListView.__init__(self, parent)
        #self. currentRow = 0

        # setting up the list view to display icons nicely
        self.setViewMode(QtGui.QListView.IconMode)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setWordWrap(True)
        self.setDragEnabled(True)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.thumbModel = QtGui.QStandardItemModel(self)
        #self.thumbViewModel.setSortRole()
        self.setModel(self.thumbModel)

        self.scrollbar = self.verticalScrollBar()
        self.scrollbar.setValue = 0
        self.scrollbar.valueChanged.connect(lambda:self.loadVisibleThumbs(self.scrollbar.value()))

        self.thumbSize = 100

        self.thumbsDir = QtCore.QDir()
        #self.fileFilters = QtCore.QStringList

    def setThumbColors(self):
        self.bgColor = QtCore.QString("background: rgb(%1, %2, %3)")

    def selectCurrentIndex(self):

        if self.currentIndex.isValid() & self.thumbViewModel.rowCount() > 0:
            self.tview.scrollTo(self.currentIndex)
            self.tview.setCurrentIndex(self.currentIndex)

    def getSingleSelectionFilename(self):
        if self.tview.selectionModel().selectedIndexes().size() == 1:
            return self.thumbViewModel.item(self.tview.selectionModel())
        return("")

    def getNextRow(self):
        if self.currentRow == self.thumbViewModel.rowCount() -1:
            return -1
        return self.currentRow + 1

    def getPrevRow(self):
        if self.currentRow == 0:
            return -1
        return self.currentRow -1

    def getLastRow(self):
        return self.thumbViewModel.rowCount()-1

    def getRandomRow(self):
        import random
        return random.randrange(self.thumbViewModel.rowCount()-1)

    def setCurrentRow(self, row):
        if row >= 0:
            self.currentRow = row
        else:
            self.currentRow = 0

    def setImageviewWindowTitle(self):
        title = self.thumbViewModel.item(self.currentRow).data(self.fileNameRole).toString()
        self.tview.setWindowTitle(title)

    def setCurrentIndexByName(self, fileName):
        self.indexList = self.thumbModel.match(self.thumbModel.index(0,0), self.fileNameRole, fileName)
        if self.indexList.size():
            self.currentIndex = indexList[0]
            self.setCurrentRow(self.currentIndex.row())
            self.setRowHidden(self.currentIndex.row(). False)
            return True
        return False

    def setCurrentIndexByRow(self, ):
        idx = self.thumbModel.indexFromItem(self.thumbModel.item(row))
        if idx.isValid():
            self.currentIndex = idx
            self.setCurrentRow(idx.row())
            return True
        return False

    #def updateExifInfo(self, imageFullPath):

    def HandleSelectionChanged(self, QItemSelection):
        indexesList = self.tview.selectionModel().selectedIndexes()
        nSelected = indexesList.size()

        if nSelected == 1:
            imageFullPath = self.thumbViewModel.item(indexesList.first().row().data(self.fileNameRole).toString())

        self.updateThumbSelection()

    def loadVisibleThumbs(self, scrollbarValue):
        #print "scrollbar moved"

        self.lastScrollBarValue = 0

        #if gdata.thumbsLayout == "Compact":
        # scrolledForward = True
        #else:
        scrolledForward = bool(scrollbarValue)

        self.lastScrollBarValue = scrollbarValue

        first = self.getFirstVisibleThumb()
        last = self.getLastVisibleThumb()
        if first < 0 | last < 0:
            return

        if scrolledForward == True:
            print "scrolled"


    def getFirstVisibleThumb(self):
        idx = QtCore.QModelIndex()
        currThumb = 0
        if self.thumbModel.rowCount() > currThumb:
            idx = self.thumbModel.indexFromItem(self.thumbModel.item(currThumb))
            #if self.viewport().rect().contains()
            currThumb =+ 1

        return -1

    def getLastVisibleThumb(self):
        return 4

    def isThumbVisible(self, idx):
        """
        :param idx:
        :return:
        """

    def updateThumbsCount(self):
        """
        :return:
        """
        print "updating thumbs count"

    def updateThumbsSelection(self):
        """
        :return:
        """

    def loadPrepare(self):
        """
        :return:
        """
        thumbAspect = 1.33
        thumbHeight = self.thumbSize * thumbAspect
        thumbWidth = self.thumbSize * thumbAspect
        self.setIconSize(QtCore.QSize(thumbWidth, thumbHeight))

        # skipping filtered search for now

        #self.thumbsDir.setPath(self.currentViewDir)
        self.thumbModel.clear()

    def load(self):

        self.loadPrepare()
        self.initThumbs()
        self.updateThumbsCount()
        self.loadVisibleThumbs()

    def initThumbs(self):

        self.thumbFileInfoList = self.thumbsDir.entryInfoList()
         #print self.thumbFileInfoList
        for thumbFileInfo in self.thumbFileInfoList:
            thumbIitem = QtGui.QStandardItem()
            #thumbIitem.setText(str(thumbFileInfo))
            thumbIitem.setIcon(QtGui.QIcon(thumbFileInfo.filePath()))
            self.thumbModel.appendRow(thumbIitem)
