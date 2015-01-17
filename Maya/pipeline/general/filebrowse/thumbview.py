"""

__author__ = 'cargoyle'

"""
from PyQt4 import QtGui, QtCore

class thumbView(QtGui.QListView):

    def __init__(self,):
        # these variables should be global data

        # these variables are local to the class
        self.tview = QtGui.QListView()
        self. currentRow = 0

        # setting up the list view to display icons nicely
        self.tview.setViewMode(QtGui.QListView.IconMode)
        self.tview.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tview.setResizeMode(QtGui.QListView.Adjust)
        self.tview.setWordWrap(True)
        self.tview.setDragEnabled(True)
        self.tview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.thumbViewModel = QtGui.QStandardItemModel(self.tview)
        #self.thumbViewModel.setSortRole()
        self.tview.setModel(self.thumbViewModel)

        self.thumbsDir = QtCore.QDir()
        self.fileFilters = QtCore.QStringList

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
        self.indexList = self.thumbViewModel.match(self.thumbViewModel.index(0,0), self.fileNameRole, fileName)
        if self.indexList.size():
            self.currentIndex = indexList[0]
            self.setCurrentRow(self.currentIndex.row())
            self.setRowHidden(self.currentIndex.row(). False)
            return True
        return False

    def setCurrentIndexByRow(self, ):
        idx = self.thumbViewModel.indexFromItem(self.thumbViewModel.item(row))
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

    def isThumbVisible(self, idx):
        """
        :param idx:
        :return:
        """

    def updateThumbsCount(self):
        """
        :return:
        """

    def updateThumbsSelection(self):
        """
        :return:
        """

    def loadPrepare(self):
        """
        :return:
        """
        thumbAspect = 1.33
        thumbHeight = map(QtCore.QSize(), 200)
        thumbWidth = QtCore.QSize()
        self.tview.setIconSize(thumbHeight)

        # skipping filtered search for now

        #self.thumbsDir.setPath(self.currentViewDir)
        self.thumbViewModel.clear()

    def load(self):

        self.loadPrepare()
        self.initThumbs()
        self.updateThumbsCount()
        #self.loadVisibleThumbs()

    def initThumbs(self):

        self.thumbFileInfoList = self.thumbsDir.entryInfoList()

        currThumb = 0
        while  currThumb < len(self.thumbFileInfoList):
            thumbFileInfo = self.thumbFileInfoList[currThumb]
            thumbIitem = QtGui.QStandardItem()
            #Icon = QtGui.QIcon()
            #Icon.QFileIconProvider.icon(thumbFileInfo)
            thumbIitem.setIcon(QtGui.QIcon(thumbFileInfo))


            self.thumbViewModel.appendRow(thumbIitem)
            currThumb+=1
