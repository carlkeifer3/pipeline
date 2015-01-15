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

        if self.currentIndex.isValid() && self.thumbViewModel.rowCount() > 0:
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




    def initThumbs(self):

        self.thumbFileInfoList = self.thumbsDir.entryInfoList()


        for currThumb = 0; currThumb < self.thumbFileInfoList.size; ++currThumb:
            thumbFileInfo = self.thumbFileInfoList.at(currThumb)
            thumbIitem = QtGui.QStandardItem()
            thumbIitem.setData(self.thumbFileInfo.filePath(), FileNameRole)

            self.thumbViewModel.appendRow(thumbIitem)

