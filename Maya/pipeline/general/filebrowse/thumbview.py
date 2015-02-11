"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import Qt, QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class thumbView(QtGui.QListView):

    def __init__(self, parent=None):
        import os
        import pipeline.general.filebrowse.infoview as iv


        #logging.debug("initialize the QlistView")
        QtGui.QListView.__init__(self, parent)
        #self. currentRow = 0

        #logging.info("Get the global Settings Data for use by thumbView class")

        self.r = g.UserRoles()

        g.GData.thumbsBackgroundColor = QtGui.QColor(g.GData.appSettings.value("backgroundThumbColor"))
        g.GData.thumbsTextColor = QtGui.QColor(g.GData.appSettings.value("textThumbColor"))



        self.thumbSize = g.GData.appSettings.value("thumbsZoomVal").toInt()[0]
        logging.info(self.thumbSize)

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
        #self.scrollbar.valueChanged.connect(lambda:self.loadVisibleThumbs( self.scrollbar.value()))

        self.lastScrollBarValue = 0

        self.busy = True

        self.fileNameRole = 1

        self.abortOp = False
        self.isNeedScroll = False
        self.currentViewDir = QtCore.QString("")

        self.setThumbColors()

        self.infoView = iv.InfoView()
        self.thumbsDir = QtCore.QDir()
        self.fileFilters = QtCore.QStringList("")

        self.selectionModel().selectionChanged.connect(lambda: self.HandleSelectionChanged())

    def setNeedScroll(self, needScroll):
        isneedScroll = needScroll

    def setThumbColors(self):
        logging.info("thumbView.setThumbColors()")
        color = g.GData.thumbsBackgroundColor
        self.bgColor = QtCore.QString("background-color: rgb(%i, %i, %i)" % (color.red(), color.green(), color.blue()))
        self.bgImage = QtCore.QString("background-image: url("+g.GData.thumbsBackImage+")")
        self.bgSetting = QtCore.QString("background-attachment: fixed")

        self.setStyleSheet(self.bgColor)
        self.setStyleSheet(self.bgImage)
        #self.setStyleSheet(self.bgSetting)

        scrollBarOigPal = self.scrollbar.palette()
        thumbViewOrigPal = self.palette()
        thumbViewOrigPal.setColor(QtGui.QPalette().Text, g.GData.thumbsTextColor)
        self.setPalette(thumbViewOrigPal)
        self.scrollbar.setPalette(scrollBarOigPal)

    def selectCurrentIndex(self):
        logging.info("thumbview.selectCurrentIndex()")
        if self.currentIndex.isValid() & self.thumbModel.rowCount() > 0:
            self.scrollTo(self.currentIndex)
            self.setCurrentIndex(self.currentIndex)

    def getSingleSelectionFilename(self):
        logging.info("thumbview.getSingleSelectionFilename()")
        if self.selectionModel().selectedIndexes().size() == 1:
            return self.thumbModel.item(self.selectionModel().selectedIndexes().first().row().data(self.r.fileNameRole).toString())
        return("")

    def getNextRow(self):
        logging.info("thumbview.getNextRow()")
        if self.currentRow == self.thumbModel.rowCount() -1:
            return -1
        return self.currentRow + 1

    def getPrevRow(self):
        logging.info("thumbview.getPrevRow")
        if self.currentRow == 0:
            return -1
        return self.currentRow -1

    def getLastRow(self):
        logging.info("thumbview.getLastRow()")
        return self.thumbModel.rowCount()-1

    def getRandomRow(self):
        logging.info("thumbview.getRandomRow()")
        import random
        return random.randrange(self.thumbModel.rowCount()-1)

    def getCurrentRow(self):
        logging.info("thumbview.getCurrentRow()")
        return self.currentRow

    def setCurrentRow(self, row):
        logging.info("thumbview.setCurrentRow()")
        if row >= 0:
            self.currentRow = row
        else:
            self.currentRow = 0

    def setImageviewWindowTitle(self):
        logging.info("thumbview.setImageviewWindowTitle()")
        title = self.thumbModel.item(self.currentRow).data(self.r.fileNameRole).toString()
        self.setWindowTitle(title)

    def setCurrentIndexByName(self, fileName):
        logging.info("thumbview.setCurrentIndexByName()")
        self.indexList = self.thumbModel.match(self.thumbModel.index(0,0), self.r.fileNameRole, fileName)
        if self.indexList.size():
            self.currentIndex = self.indexList[0]
            self.setCurrentRow(self.currentIndex.row())
            self.setRowHidden(self.currentIndex.row(). False)
            return True
        return False

    def setCurrentIndexByRow(self, row):
        logging.info("thumbview.setCurrentIndexByRow()")
        idx = self.thumbModel.indexFromItem(self.thumbModel.item(row))
        if idx.isValid():
            self.currentIndex = idx
            self.setCurrentRow(idx.row())
            return True
        return False

    def updateExifInfo(self, imageFullPath):
        logging.info("thumbview.updateExifInfo()")
        import exifread



    def HandleSelectionChanged(self):
        #logging.info("thumbView.HandleSelectionChanged()")
        indexesList = self.selectionModel().selectedIndexes()
        nSelected = len(indexesList)

        self.infoView.clear()
        if nSelected == 1:
            imageFullPath = self.thumbModel.item(indexesList[0].row()).data(self.r.fileNameRole).toString()
            #self.imageInfoReader.setFileName(imageFullPath)

            imageInfo = QtCore.QFileInfo(imageFullPath)
            self.infoView.addTitleEntry("General: ")

            key = "File Name"
            val = imageInfo.fileName()
            self.infoView.addEntry(key, val)

            key = "Location"
            val = imageInfo.path()
            self.infoView.addEntry(key, val)

            key = "Size"
            val = QtCore.QString.number(imageInfo.size())
            self.infoView.addEntry(key, val)

            key = "Modified"
            val = imageInfo.lastModified().toString(QtCore.Qt.SystemLocaleShortDate)
            self.infoView.addEntry(key, val)



        self.updateThumbsSelection()

    #def startDrag(self, dropActions):
    #    print "starting drag action"

    def abort(self):
        self.abortOp = True

    def loadVisibleThumbs(self, scrollbarValue):
        logging.info("thumbView.loadVisibleThumbs()")
        #logging.info("Scrollbar Moved, recheck for visible Thumbnails")

        #if gdata.thumbsLayout == "Compact":
        # scrolledForward = True
        #else:
        scrolledForward = bool(scrollbarValue)

        self.lastScrollBarValue = scrollbarValue

        first = self.getFirstVisibleThumb()
        last = self.getLastVisibleThumb()

        logging.info("First thumbnail found: "+ str(first))
        logging.info("Last thumbnail found: "+ str(last))
        logging.info(" currently displaying "+str((last-first)+1)+" thumbnails.")
        if first < 0 | last < 0:
            return

        if scrolledForward == True:
            last = (last - first) * (g.GData.thumbPagesReadahead + 1)
            if last >= self.thumbModel.rowCount():
                last = self.thumbModel.rowCount() -1

        else:
            first = (last -first) * (g.GData.thumbPagesReadahead +1)
            if first < 0:
                first = 0

            last += 10
            if last >= self.thumbModel.rowCount():
                last = self.thumbModel.rowCount()-1

        if self.thumbsRangeFirst == first & self.thumbsRangeLast == last:
            return

        self.thumbsRangeFirst = first
        self.thumbsRangeLast = last

        logging.info("preparing to load the range of thumbs")
        index = self.thumbModel.index(first, 0)
        logging.info("First thumbnail "+ self.thumbModel.data(index).toString())
        index = self.thumbModel.index(last, 0)
        logging.info("Last thumbnail: "+ self.thumbModel.data(index).toString())

        self.loadThumbsRange()

    def getFirstVisibleThumb(self):
        logging.info("thumbView.getFirstVisibleThumb()")
        #logging.info("get first visible thumb")
        currThumb = 0
        logging.info("Investigating "+str(self.thumbModel.rowCount())+" rows")
        while currThumb < int(self.thumbModel.rowCount()):
            #logging.info("Looking for first thumbnail in list of thumbs")
            idx = self.thumbModel.index(currThumb, 0)
            if self.viewport().rect().contains(QtCore.QPoint(0, self.visualRect(idx).y() + self.visualRect(idx).height() + 1)):
                #index = self.thumbModel.index(currThumb, 0)
                #logging.info("First thumbnail "+ str(self.thumbModel.data(index).toString()))
                return idx.row()
            currThumb += 1

        return -1

    def getLastVisibleThumb(self):
        """

        :return:
        """
        logging.info("thumbView.getLastVisibleThumb()")
        #logging.info("get last visible thumbnail")
        currThumb = int(self.thumbModel.rowCount())-1
        logging.info("Investigating "+str(currThumb)+" rows")
        while currThumb >= 0:
            #logging.info("Looking for last Thumbnail in list of thumbs")
            idx = self.thumbModel.indexFromItem(self.thumbModel.item(currThumb))
            if self.viewport().rect().contains(QtCore.QPoint(0, self.visualRect(idx).y() + self.visualRect(idx).height() + 1)):
                index = self.thumbModel.index(currThumb, 0)
                logging.info("Last thumbnail: "+ str(self.thumbModel.data(index).toString()))
                return idx.row()
            currThumb -= 1
            #print "currThumb: "+ str(currThumb)
        #print "nothing found exit -1"
        return -1

    def isThumbVisible(self, idx):
        """
        :param idx:
        :return:
        """
        print "is thumbnail "+str(idx)+" visible"

    def updateThumbsCount(self):
        """
        :return:
        """
        print "updating thumbs count"

    def updateThumbsSelection(self):
        """
        :return:
        """
        #logging.info("thumbView.updateThumbsSelection()")
        #logging.info("update thumbnail selection")
        nSelected = len(self.selectionModel().selectedIndexes())

        if not nSelected:
            state = str(self.thumbModel.rowCount())+" Images"
        elif nSelected >= 1:
            state = "Selected "+str(nSelected)+" of "+str(self.thumbModel.rowCount())+" images"
        else:
            return

        logging.info(state)


    def loadPrepare(self):
        """
        :return:
        """
        #logging.info("thumbView.loadPrepare()")
        #logging.info("preparing to load thumbnails")
        thumbAspect = 1.33
        thumbHeight = float(self.thumbSize) * thumbAspect
        thumbWidth = self.thumbSize * thumbAspect
        self.setIconSize(QtCore.QSize(thumbWidth, thumbHeight))

        self.fileFilters.clear()
        self.fileFilters.append("*.BMP")
        self.fileFilters.append("*.GIF")
        self.fileFilters.append("*.ICO")
        self.fileFilters.append("*.JPEG")
        self.fileFilters.append("*.JPG")
        self.fileFilters.append("*.MNG")
        self.fileFilters.append("*.PBM")
        self.fileFilters.append("*.PNG")
        self.fileFilters.append("*.PPM")
        self.fileFilters.append("*.SVG")
        self.fileFilters.append("*.SVGZ")
        self.fileFilters.append("*.TGA")
        self.fileFilters.append("*.TIF")
        self.fileFilters.append("*.TIFF")
        self.fileFilters.append("*.WBMP")
        self.fileFilters.append("*.XBM")
        self.fileFilters.append("*.XPM")
        self.fileFilters.append("*.JPE")

        self.thumbsDir.setNameFilters(self.fileFilters)
        self.thumbsDir.setFilter(QtCore.QDir.Files)
        #if g.GData.showHiddenFiles:
        #    self.thumbsDir.setFilter(self.thumbsDir.filters() | QtCore.QDir.hidden)
        self.thumbsDir.setPath(self.currentViewDir)
        self.thumbModel.clear()

        self.setSpacing(g.GData.thumbsSpacing)

        self.abortOp = False

        self.thumbsRangeFirst = -1
        self.thumbsRangeLast = -1

    def load(self):
        #logging.info("thumbview.load()")

        self.loadPrepare()
        self.initThumbs()
        #self.updateThumbsCount()
        #self.loadVisibleThumbs(0)

    def loadDuplicates(self):
        logging.info("thumbView.loadDuplicates")

    def initThumbs(self):
        logging.info("thumbView.initThumbs()")
        self.thumbFileInfoList = self.thumbsDir.entryInfoList()
        currThumb = 0
        #emptyPixMap = QtGui.QPixmap()
        #hintSize = QtCore.QSize()

        #emptyPixMap.fromImage(self.emptyImg).scaled(self.thumbWidth,self.thumbHeight)

        for thumbFileInfo in self.thumbFileInfoList:
            #logging.info("adding %s to the model" % thumbFileInfo.filePath())
            thumbIitem = QtGui.QStandardItem()
            thumbIitem.setData(False, role=g.UserRoles.loadedRole)
            thumbIitem.setData(currThumb, role=g.UserRoles.sortRole)
            thumbIitem.setData(thumbFileInfo.filePath(), role=g.UserRoles.fileNameRole)
            ## add
            thumbIitem.setData(thumbFileInfo.fileName(), role=QtCore.Qt.DisplayRole)

            thumbIitem.setTextAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            thumbIitem.setText(thumbFileInfo.fileName())
            #thumbIitem.setIcon(QtGui.QIcon("D:/Nedry.png"))
            #logging.info("Ah, Ah, Ah, you didn't say the magic word")
            thumbIitem.setIcon(QtGui.QIcon(thumbFileInfo.filePath()))

            self.thumbModel.appendRow(thumbIitem)
            currThumb += 1

    def updateFoundDupeState(self):
        logging.info("thumbview.updateFoundDupeState")

    def findDupes(self):
        logging.info("thumbView.findDupes")

    def loadThumbsRange(self):
        logging.info("thumbView.loadThumbsRange")

        painter =  QtGui.QPainter()

        thumbReader = QtGui.QImageReader()

        self.inProgress = True
        currRowCount = self.thumbModel.rowCount()

        currThumb = self.thumbsRangeFirst

        if currThumb < 0:
            currThumb = 0

        while currThumb <= self.thumbsRangeLast:


            imageFileName = self.thumbModel.item(currThumb).data(role=self.r.fileNameRole).toString()



            self.thumbModel.item(currThumb).setIcon(QtGui.QIcon(imageFileName))
            #self.thumbModel.item(currThumb).setIcon(QtGui.QIcon("D:/Nedry.png"))

            logging.info(imageFileName+", Should now be loaded.")
            self.thumbModel.item(currThumb).setData(True, role=self.r.loadedRole)
            QtGui.qApp.processEvents()
            self.update(self.thumbModel.index(currThumb,0))
            currThumb += 1
        painter.restore()
        painter.end()


    def addThumb(self):
        logging.info("thumbView.addThumb")

    #def wheelEvent(self, event):
    #    logging.info("thumbView.wheelEvent")

    #def mousePressEvent(self, event):
    #    logging.info("thumbView.mousePressEvent")

    #    if g.GData.reverseMouseBehavior & event.button() == QtCore.Qt.MiddleButton:
    #
    #        if self.selectionModel().selectedIndexes.size() == 1:
    #            emit (doubleClicked(self.selectionModel().selectedIndexes().first))

    def invertSelection(self):
        logging.info("thumbView.invertSelection")