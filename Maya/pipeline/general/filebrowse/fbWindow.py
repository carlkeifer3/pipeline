"""

__author__ = 'cargoyle'

"""
import logging

from PyQt4 import QtGui, QtCore
import os
import sip
import maya.OpenMayaUI as apiUI
import pipeline.general.filebrowse.thumbview as tv
import pipeline.general.filebrowse.GData as g

def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


class fbWindow(QtGui.QMainWindow):
    """


    """

    def __init__(self, parent=getMayaWindow()):
        import os
        import pymel.core as pm

        # initialize the QWidget
        QtGui.QWidget.__init__(self, parent)

        self.GData = g.GData()

        self.GData.appSettings = QtCore.QSettings("photonic", "photonic_103")

        # locate the directory where all of the images for the ui live
        ScriptDir = pm.internalVar(uad=True)
        self.imgDirectory = str(ScriptDir+"/scripts/pipeline/general/filebrowse/images/")

        self.setObjectName("FileBrowser")
        self.fbLayout = QtGui.QHBoxLayout(self)
        #self.fbLayout.addStretch(1)
        #self.fbLayout.setContentsMargins(0,0,0,0)
        self.fbLayout.setSpacing(10)

        # internal class variable time
        self.copyCutCount = 0
        self.copyMoveToDialog = 0
        self.colorsDialog = 0
        self.cropDialog = 0
        self.initComplete = True

        self.needHistory = True
        self.interfaceDisabled = False

        self.readSettings()
        self.createThumbView()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createFSTree()
        self.createBookmarks()
        #self.createImageView()
        #self.UpdateExternalApps()
        #self.loadShortcuts()
        #self.setupDocks()

        self.setLayout(self.fbLayout)

    def handleStartupArgs(self):
        """

        :return:
        """
        cliImageLoaded = False

#    def event(self, event):
#        print "event"
#        # this is really messed up
#        # also the C++ code has a recursive call
#        #if event.type() == QtCore.QEvent.ActivationChange():
#        #    print "activation change"
#
#        # do not run this, its in the C++ code but python doesn't like it
#        # return self.event(event)
#        return event

    def createThumbView(self):
        import pipeline.general.filebrowse.thumbview as tv

        self.thumbView = tv.thumbView(self)
        self.thumbView.load()
        print "thumbview should be built"
        self.fbLayout.addWidget(self.thumbView)

        self.iiDock = QtGui.QDockWidget("Image Info", self)
        self.iiDock.setObjectName("ImageInfo")
        self.iiDock.setWidget(self.thumbView)

        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.iiDock)

    def AddMenuSeparator(self):
        """

        :return:
        """
        separator = QtCore.QAction(self)
        separator.setSeparator(True)
        self.addAction(separator)

    def createImageView(self):
        """

        :return:
        """
        print "createImageView()"

    def createActions(self):
        """

        :return:
        """
        logging.debug("creating all actions for the file browser")
        self.thumbsGoTopAct = QtGui.QAction("Top", self)
        self.thumbsGoTopAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"top.png")))
        self.thumbsGoTopAct.triggered.connect(lambda: self.goTop())

        self.thumbsGoBottomAct = QtGui.QAction("Bottom", self)
        self.thumbsGoBottomAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"bottom.png")))

        self.closeImageAct = QtGui.QAction("Close Image", self)
        self.closeImageAct.triggered.connect(lambda: self.hideViewer())

        self.fullScreenAct = QtGui.QAction("Full Screen", self)
        self.fullScreenAct.setCheckable(True)
        self.fullScreenAct.triggered.connect(lambda: self.toggleFullScreen())

        self.settingsAction = QtGui.QAction("Preferences", self)
        self.settingsAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"settings.png")))
        self.settingsAction.triggered.connect(lambda: self.showSettings())

        self.exitAction = QtGui.QAction("Exit", self)
        self.exitAction.triggered.connect(lambda: self.close())

        self.thumbsZoomInAct = QtGui.QAction("Enlarge Thumbnails", self)
        self.thumbsZoomInAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom_in.png")))
        self.thumbsZoomInAct.triggered.connect(lambda:self.thumbsZoomIn())

        self.thumbsZoomOutAct = QtGui.QAction("Shrink Thumbnails", self)
        self.thumbsZoomOutAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom_out.png")))
        self.thumbsZoomOutAct.triggered.connect(lambda: self.thumbsZoomOut())

        self.cutAction = QtGui.QAction("Cut", self)
        self.cutAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"cut.png")))
        self.cutAction.triggered.connect(lambda: self.cutThumbs())
        self.cutAction.setEnabled(False)

        self.copyAction = QtGui.QAction("Copy", self)
        self.copyAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"copy.png")))
        self.copyAction.triggered.connect(lambda: self.copyThumbs())
        self.copyAction.setEnabled(False)

        self.copyToAction = QtGui.QAction("Copy to...", self)
        self.copyToAction.triggered.connect(lambda: self.copyImagesTo())

        self.moveToAction = QtGui.QAction("Move To...", self)
        self.moveToAction.triggered.connect(lambda: self.moveImagesTo())

        self.deleteAction = QtGui.QAction("Delete", self)
        self.deleteAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"delete.png")))
        self.deleteAction.triggered.connect(lambda: self.deleteOp())

        self.saveAction = QtGui.QAction("Save", self)
        self.saveAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"save.png")))

        self.saveAsAction = QtGui.QAction("Save As", self)
        self.saveAsAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"save_as.png")))

        self.copyImageAction = QtGui.QAction("Copy Image Data", self)
        self.pasteImageAction = QtGui.QAction("Paste Image Data", self)

        self.renameAction = QtGui.QAction("Rename", self)
        self.renameAction.triggered.connect(lambda: self.rename())

        self.selectAllAction = QtGui.QAction("Select All", self)
        self.selectAllAction.triggered.connect(lambda:self.selectAllThumbs())

        self.aboutAction = QtGui.QAction("About", self)
        self.aboutAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"about.png")))
        self.aboutAction.triggered.connect(lambda:self.about())

        # sort Actions
        self.actName = QtGui.QAction("Name", self)
        self.actTime = QtGui.QAction("Time", self)
        self.actSize = QtGui.QAction("Size", self)
        self.actType = QtGui.QAction("Type", self)
        self.actReverse = QtGui.QAction("Reverse", self)
        self.actName.setCheckable(True)
        self.actTime.setCheckable(True)
        self.actSize.setCheckable(True)
        self.actType.setCheckable(True)
        self.actReverse.setCheckable(True)
        self.actName.triggered.connect(lambda: self.sortThumbnails())
        self.actTime.triggered.connect(lambda: self.sortThumbnails())
        self.actSize.triggered.connect(lambda: self.sortThumbnails())
        self.actType.triggered.connect(lambda: self.sortThumbnails())
        self.actReverse.triggered.connect(lambda: self.sortThumbnails())


        self.refreshAction = QtGui.QAction("Reload", self)
        self.refreshAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"refresh.png")))
        self.refreshAction.triggered.connect(lambda: self.reload())

        self.subFoldersAction = QtGui.QAction("Include Sub-Folders", self)
        self.subFoldersAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"tree.png")))
        self.subFoldersAction.setCheckable(True)
        self.subFoldersAction.triggered.connect(lambda: self.setIncludeSubFolders())

        self.pasteAction = QtGui.QAction("Paste Here", self)
        self.pasteAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"paste.png")))
        self.pasteAction.triggered.connect(lambda: self.pasteThumbs())

        # missing createDirAction

        self.goBackAction = QtGui.QAction("Back", self)
        self.goBackAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"back.png")))
        self.goBackAction.triggered.connect(lambda:self.goBack())

        self.goFrwdAction = QtGui.QAction("Forward", self)
        self.goFrwdAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"next.png")))
        self.goFrwdAction.triggered.connect(lambda:self.goForward())

        self.goUpAction = QtGui.QAction("Up", self)
        self.goUpAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"up.png")))
        self.goUpAction.triggered.connect(lambda:self.goUp())

        self.goHomeAction = QtGui.QAction("Home", self)
        self.goHomeAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"home.png")))
        self.goHomeAction.triggered.connect(lambda:self.goHome())

        self.slideShowAction = QtGui.QAction("Slide Show", self)
        self.slideShowAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"play.png")))

        #missing actions

        self.showClipboardAction = QtGui.QAction("Load Clipboard", self)
        self.showClipboardAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"new.png")))
        self.showClipboardAction.triggered.connect(lambda: self.newImage())

        # missing several


    def createMenus(self):
        """

        :return:
        """
        print "creating the menus"
        self.menubar = QtGui.QMenuBar(self)
        self.fileMenu = QtGui.QMenu("&File", self.menubar)
        self.fileMenu.addAction("subFoldersAction")
        self.fileMenu.addAction("createDirectoryAction")
        self.fileMenu.addAction("showClipboardAction")
        self.fileMenu.addAction("addBookmarkAction")
        self.fileMenu.addSeparator()
        # probably won't add this. but who knows.
        # I would like to use this widget as a dockable widget
        self.fileMenu.addAction("exitAction")

        self.editMenu = QtGui.QMenu("&Edit", self.menubar)
        self.editMenu.addAction("cutAction")
        self.editMenu.addAction("copyAction")
        self.editMenu.addAction("copyToAction")
        self.editMenu.addAction("moveToAction")
        self.editMenu.addAction("pasteAction")
        self.editMenu.addAction("deleteAction")
        self.editMenu.addSeparator()
        self.editMenu.addAction("selectAllAction")
        self.editMenu.addAction("inverseSelectionAct")
        #addAction("filterImagesFocusAct")
        #addAction("setPathFocusAct")
        self.editMenu.addSeparator()
        self.editMenu.addAction("settingsAction")

        self.goMenu = QtGui.QMenu("&Go", self.menubar)
        self.goMenu.addAction("goBackAction")
        self.goMenu.addAction("goFrwdAction")
        self.goMenu.addAction("goUpAction")
        self.goMenu.addAction("goHomeAction")
        self.goMenu.addSeparator()
        self.goMenu.addAction("thumbsGoTopAct")
        self.goMenu.addAction("thumbsGoBottomAct")

        self.viewMenu = QtGui.QMenu("&View", self.menubar)
        self.viewMenu.addAction("slideShowAction")
        self.viewMenu.addSeparator()
        self.viewMenu.addAction("thumbsZoomInAct")
        self.viewMenu.addAction("thumbsZoomOutAct")
        self.sortMenu = self.viewMenu.addAction("Sort By")
        self.sortTypesGroup = QtGui.QActionGroup(self)
        self.sortTypesGroup.addAction("actName")
        self.sortTypesGroup.addAction("actTime")
        self.sortTypesGroup.addAction("actSize")
        self.sortTypesGroup.addAction("actType")
        #self.sortMenu.addActions(self.sortTypesGroup.actions())
        #self.sortMenu.addSeparator()
        #self.sortMenu.addActions("actReverse")
        self.viewMenu.addSeparator()


        self.toolsMenu = QtGui.QMenu("&Tools", self.menubar)
        self.toolsMenu.addAction("findDupesAction")

        self.menubar.addSeparator()
        self.helpMenu = QtGui.QMenu("&Help", self.menubar)
        self.helpMenu.addAction("aboutAction")




        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.goMenu)
        self.menubar.addMenu(self.viewMenu)
        self.menubar.addMenu(self.toolsMenu)
        self.menubar.addMenu(self.helpMenu)
        self.setMenuBar(self.menubar)

    def createToolBars(self):
        print "Creating the tool bars"
        #Edit Toolbar
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setObjectName("Edit")
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)
        self.editToolBar.addAction(self.deleteAction)
        self.editToolBar.addAction(self.showClipboardAction)

        # Navigation Toolbar
        self.goToolBar = self.addToolBar("Navigation")
        self.goToolBar.setObjectName("Navigation")
        self.goToolBar.addAction(self.goBackAction)
        self.goToolBar.addAction(self.goFrwdAction)
        self.goToolBar.addAction(self.goUpAction)
        self.goToolBar.addAction(self.goHomeAction)
        self.goToolBar.addAction(self.refreshAction)

        # Path Toolbar
        self.pathBar = QtGui.QLineEdit()

        # enter pathbar stuff here
        self.pathBar.setMinimumWidth(200)
        self.pathBar.setMaximumWidth(300)

        self.goToolBar.addWidget(self.pathBar)
        self.goToolBar.addAction(self.subFoldersAction)

        # View Toolbar
        self.viewToolBar = self.addToolBar("View")
        self.viewToolBar.setObjectName("View")
        self.viewToolBar.addAction(self.slideShowAction)
        self.viewToolBar.addAction(self.thumbsZoomInAct)
        self.viewToolBar.addAction(self.thumbsZoomOutAct)

    def setToolbarIconSize(self):
        print "setting Toolbar icon size"

    def createStatusBar(self):
        print "creating Status bar"

        self.statusBar = QtGui.QStatusBar()
        self.stateLabel = QtGui.QLabel("Initializing")
        self.statusBar.addWidget(self.stateLabel)

        self.busyMovie = QtGui.QMovie(str(self.imgDirectory+"busy.gif"))
        self.busyLabel = QtGui.QLabel(self)
        self.busyLabel.setMovie(self.busyMovie)
        self.statusBar.addWidget(self.busyLabel)
        self.busyLabel.setVisible(False)

        self.setStatusBar(self.statusBar)

    def createFSTree(self):
        print "creating filesystem tree"
        import pipeline.general.filebrowse.fstree as fs

        self.fsDock = QtGui.QDockWidget("File System", self)
        self.fsDock.setObjectName("File System")

        self.fsTree = fs.FSTree(self.fsDock)
        self.fsDock.setWidget(self.fsTree)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.fsDock)

        #Context Menu

        self.fsTree.clicked.connect(lambda: self.goSelectedDir())

    def createBookmarks(self):
        print "creating bookmarks window"
        import pipeline.general.filebrowse.bookmarks as bm

        self.bmDock = QtGui.QDockWidget("Bookmarks", self)
        self.bmDock.setObjectName("Bookmarks")

        self. bookmarks = bm.BookMarks(self.bmDock)
        self.bmDock.setWidget(self.bookmarks)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.bmDock)

    def sortThumbnails(self):
        print "sorting thumbnails"

    def reload(self):
        print "reload"

    def setIncludeSubFolders(self):
        print "set Include SubFolders"

    def refreshThumbs(self, scrollToTop):
        print "refresh Thumbs"
        self.thumbView.setNeedScroll(scrollToTop)
        QtCore.QTimer.singleShot(0, lambda: self.reloadThumbsSlot())

    def setClassicThumbs(self):
        print "setting classic thumbs view"

    def setCompactThumbs(self):
        print "setting compact thumbs view"

    def setSquareishThumbs(self):
        print "setting Square thumbs view"

    def showHiddenFiles(self):
        print "showing hidden files"

    def toggleImageToolbar(self):
        print "toggling Image Toolbar"

    def showLabels(self):
        print "showing Labels"

    def about(self):
        print " displaying about message"

    def filterImagesFocus(self):
        print "filtering ImagesFocus"

    def setPathFocus(self):
        print "setting Path Focus"

    def cleanupSender(self):
        print "cleanup Sender"

    def externalAppError(self):
        print "External Applications error"

    def runExternalApp(self):
        print "Running external Application"

    def updateExternalApps(self):
        print "updating External Application"

    def chooseExternalApp(self):
        print "Choose External Application"

    def showSettings(self):
        print "show settings"

    def toggleFullScreen(self):
        print "Toggle Full Screen Mode"

    def selectAllThumbs(self):
        logging.info("selecting all thumbs")
        self.thumbView.selectAll()

    def copyOrCutThumbs(self, copy):
        logging.info("copy or cut thumbs")
        self.GData.copyCutIdxList = self.thumbView.selectionModel().selectedIndexes()
        self.GData.copyCutFileList.clear()
        for f in self.GData.copyCutIdxList:
            self.GData.copyCutFileList.append(self.thumbView.thumbModel.item(f.row()).data(self.thumbView.fileNameRole).toString())
            self.copyCutCount +=1
        self.GData.copyOp = copy
        self.pasteAction.setEnabled(True)

    def cutThumbs(self):
        logging.info("cut Thumb to clipboard")
        self.copyOrCutThumbs(False)

    def copyThumbs(self):
        logging.info("copy thumb to clipboard")
        self.copyOrCutThumbs(True)

    def copyImagesTo(self):
        logging.info("copy images to")
        self.copyMoveImages(False)

    def moveImagesTo(self):
        logging.info("moving images to")
        self.copyMoveImages(True)

    def copyMoveImages(self, move):
        print "copy or move images"


    def thumbsZoomIn(self):
        print "Enlarge Thumbs"
        #if self.thumbView.thumbSize < self.ThumbMaxSize:
        self.thumbView.thumbSize += 25
        self.thumbsZoomInAct.setEnabled(True)
        # check the thumbs to make sure we don't go over the max size
        #if self.thumbView.thumbSize == self.ThumbMaxSize:
        #    self.thumbsZoomInAct.setEnabled(False)
        self.refreshThumbs(False)

    def thumbsZoomOut(self):
        print "shrink Thumbs"
        #if self.thumbView.thumbSize < self.ThumbMinSize:
        self.thumbView.thumbSize -= 25
        self.thumbsZoomOutAct.setEnabled(True)
        # check the thumbs to make sure we don't go over the max size
        #if self.thumbView.thumbSize == self.ThumbMinSize:
        #    self.thumbsZoomOutAct.setEnabled(False)
        self.refreshThumbs(False)

    def zoomOut(self):
        print "zooming out"

    def zoomIn(self):
        print "zooming In"

    def resetZoom(self):
        print "resetting zoom"

    def origZoom(self):
        print "original size"

    def keepZoom(self):
        print "keep zoom"

    def keepTransformClicked(self):
        print "keep transform clicked"

    def rotateLeft(self):
        print "rotating left"

    def rotateRight(self):
        print "rotate right"

    def flipVert(self):
        print "filipping Vertically"

    def flipHoiz(self):
        print "flipping Hoizontally"

    def cropImage(self):
        print "cropping Image"

    def scaleImage(self):
        print "scaling Image"

    def freeRotateLeft(self):
        print "Free rotate left"

    def freeRotateRight(self):
        print "Free rotate Right"

    def showColorsDialog(self):
        print "Show colors dialog"

    def moveRight(self):
        print "moving Image Right"

    def moveLeft(self):
        print "moving Image Left"

    def moveUp(self):
        print "moving Image Up"

    def moveDown(self):
        print "moving Image Down"

    def setMirrorDisabled(self):
        print "setting mirroring as disabled"

    def setMirrorDual(self):
        print "setting Mirror to Dual"

    def setMirrorTriple(self):
        print "setting Mirror triple"

    def setMirrorVDual(self):
        print "set mirror V Dual"

    def setMirrorQuad(self):
        print "set mirror quad"

    def isValidPath(self):
        print "is this path Valid"

    def pasteThumbs(self):
        print "paste thumbnails"
        if self.copyCutCount == 0:
            logging.debug("No thumbnails on clipboard")
            return

        destDir = 0
        # this will probably break later
        logging.debug("check if we have stored the selected Path")
        if self.copyMoveToDialog != 0:
            destDir = self.copyMoveToDialog.selectedPath()
        #else:


        #if not os.isvalidpath(destDir):
        #    msgBox = QtGui.QMessageBox()
        #    msgBox.critical("Error", str("can not Copy or Move to"+destDir))
        #    self.selectCurrentViewDir()
        #    return

        # I don't like this.
        # what if you want to past this item multiple times
        self.copyCutCount = 0

        #self.GData.copyCutIdxList.clear()
        #self.GData.copyCutFileList.clear()
        self.pasteAction.setEnabled(False)
        self.thumbView.loadVisibleThumbs(0)

    def updateCurrentImage(self):
        print "update current Image"

    def deleteViewerImage(self):
        print "deleteViewerImage"

    def deleteOp(self):
        print "Deleting"

    def goTo(self, path):
        print str("going to QDir "+path)
        self.fsTree.setCurrentIndex(self.fsTree.fsModel.index(path))
        self.thumbView.currentViewDir = path
        # this is not the right directory, just trying to get this to work
        self.thumbView.thumbsDir.setPath(path)
        self.refreshThumbs(True)

    def goSelectedDir(self):
        logging.info("getting the directory selected in the tree widget")
        self.thumbView.setNeedScroll(True)
        selectedPath = self.getSelectedPath()
        self.thumbView.currentViewDir = selectedPath
        self.thumbView.thumbsDir.setPath(selectedPath)
        self.refreshThumbs(True)

    def goPathBarDir(self):
        print "go to the directory indicated by the path bar"

    def bookmarkClicked(self):
        print "bookmark selected"

    def setThumbsFilter(self):
        print "setting thumbnails filter"

    def clearThumbsFilter(self):
        print "clearing thumbnails filter"

    def goBack(self):
        print "go back one directory"

    def goForward(self):
        print "go forward one directory"

    def goUp(self):
        print " go up one directory"

    def goHome(self):
        loggin.info(" goto home directory")
        self.goTo(QtCore.QDir.homePath())

    def setCopyCutActions(self):
        print "setting the cut and copy actions"

    def changeActionsBySelection(self):
        print "changing actions by selection"

    def UpdateActions(self):
        print "Updating Actions"

    def writeSettings(self):
        print "Writing Settings"

    def readSettings(self):
        logging.info("Reading Settings")
        self.initComplete = False
        self.needThumbsRefresh = False

        if self.GData.appSettings.contains("thumbsZoomVal"):
            self.resize(800,600)
            self.GData.appSettings.setValue("thumbsSortFlags", int(0))
            self.GData.appSettings.setValue("thumbsZoomVal", 150)
            self.GData.appSettings.setValue("isFullScreen", False)
            self.GData.appSettings.setValue("backgroundColor", QtGui.QColor(25, 25, 25))
            self.GData.appSettings.setValue("backgroundThumbColor", QtGui.QColor(200, 200, 200))
            self.GData.appSettings.setValue("textThumbColor", QtGui.QColor(25, 25, 25))
            self.GData.appSettings.setValue("thumbSpacing", 10)
            self.GData.appSettings.setValue("thumbPagesReadahead", 2)
            self.GData.appSettings.setValue("thumbsLayout", self.GData.thumbsLayout)
            self.GData.appSettings.setValue("zoomOutFlags", 1)
            self.GData.appSettings.setValue("zoomInFlags", 0)
            self.GData.appSettings.setValue("wrapImageList", False)
            self.GData.appSettings.setValue("exitInsteadOfClose", 0)
            self.GData.appSettings.setValue("imageZoomFactor", 1.0)
            self.GData.appSettings.setValue("defaultSaveQuality", 100)
            self.GData.appSettings.setValue("noEnlargeSmallThumb", True)
            self.GData.appSettings.setValue("enableAnimations", True)
            self.GData.appSettings.setValue("exifRotationEnabled", True)
            self.GData.appSettings.setValue("referseMouseBehavior", False)
            self.GData.appSettings.setValue("showHiddenFiles", False)
            self.GData.appSettings.setValue("slideShowDelay", 5)
            self.GData.appSettings.setValue("slideShowRandom", False)
            self.GData.appSettings.setValue("editToolBarVisible", True)
            self.GData.appSettings.setValue("goToolBarVisible", True)
            self.GData.appSettings.setValue("viewToolBarVisible", True)
            self.GData.appSettings.setValue("imageToolBarVisible", False)
            self.GData.appSettings.setValue("fsDockVisible", True)
            self.GData.appSettings.setValue("bmDockVisible", True)
            self.GData.appSettings.setValue("iiDockVisible", True)
            self.GData.appSettings.setValue("pvDockVisible", False)
            self.GData.appSettings.setValue("enableImageInfoFS", False)
            self.GData.appSettings.setValue("showLabels", True)
            self.GData.appSettings.setValue("smallIcons", False)
            self.GData.appSettings.setValue("LockDocks", True)
            self.GData.appSettings.setValue("imageToolbarFullScreen", False)
            self.GData.bookmarkPaths.insert(QtCore.QDir.homePath())

        self.GData.backgroundColor = self.GData.appSettings.value("backgroundColor")
        self.GData.exitInsteadofClose = self.GData.appSettings.value("exitInsteadOfClose").toBool()
        self.GData.enableAnimations = self.GData.appSettings.value("enableAnimations").toBool()
        self.GData.exifRotationEnabled = self.GData.appSettings.value("exifRotationEnabled").toBool()
        self.GData.exifThumbRotationEnabled = self.GData.appSettings.value("exifThumbRotationEnabled").toBool()
        self.GData.reverseMouseBehavior = self.GData.appSettings.value("reverseMouseBehavior").toBool()
        self.GData.showHiddenFiles = self.GData.appSettings.value("showHiddenFiles").toBool()
        self.GData.wrapImageList = self.GData.appSettings.value("wrapImageList").toBool()
        self.GData.imageZoomFactor = self.GData.appSettings.value("imageZoomFactor").toFloat()
        self.GData.zoomOutFlags = self.GData.appSettings.value("zoomOutFlags").toInt()
        self.GData.zoomInFlags = self.GData.appSettings.value("zoomInFlags").toInt()
        self.GData.rotation = 0
        self.GData.keepTransform = False
        self.shouldMaximize = self.GData.appSettings.value("shouldMaximize").toBool()
        self.GData.flipH = False
        self.GData.flipV = False
        self.GData.defaultSaveQuality = self.GData.appSettings.value("defaultSaveQuality").toInt()
        self.GData.noEnlargeSmallThumbs = self.GData.appSettings.value("noEnlargeSmallThumb").toBool()
        self.GData.slideShowDelay = self.GData.appSettings.value("slideShowDelay").toInt()
        self.GData.slideShowRandom = self.GData.appSettings.value("slideShowRandom").toBool()
        self.GData.slideShowActive = False
        self.editToolbarVisible = self.GData.appSettings.value("editToolBarVisible").toBool()
        self.goToolBarVisible = self.GData.appSettings.value("goToolBarVisible").toBool()
        self.viewToolBarVisible = self.GData.appSettings.value("viewToolBarVisible").toBool()
        self.imageToolBarVisible = self.GData.appSettings.value("imageToolBarVisible").toBool()
        self.GData.fsDockVisible = self.GData.appSettings.value("fsDockVisible").toBool()
        self.GData.bmDockVisible = self.GData.appSettings.value("bmDockVisible").toBool()
        self.GData.iiDockVisible = self.GData.appSettings.value("iiDockVisible").toBool()
        self.GData.pvDockVisible = self.GData.appSettings.value("pvDockVisible").toBool()
        self.GData.startupDir = self.GData.appSettings.value("startupDir").toInt()
        self.GData.specifiedStartDir = self.GData.appSettings.value("specifiedStartDir").toString()
        self.GData.thumbsBackImage = self.GData.appSettings.value("thumbsBackImage").toString()
        self.GData.enableImageInfoFS = self.GData.appSettings.value("enableImageInfoFS").toBool()
        self.GData.showLabels = self.GData.appSettings.value("showLabels").toBool()
        self.GData.smallIcons = self.GData.appSettings.value("smallIcons").toBool()
        self.GData.LockDocks = self.GData.appSettings.value("LockDocks").toBool()
        self.GData.imageToolbarFullScreen = self.GData.appSettings.value("imageToolbarFullScreen").toBool()

        #self.GData.appSettings.beginGroup("externalApps")
        #extApps = self.GData.appSettings.childKeys()
        #i = 0
        #while i < extApps.size():
        #    self.GData.externalApps[extApps.at(i)] = self.GData.appSettings.value(extApps.at(i).toString())
        #    i +=1
        #self.GData.appSettings.endGroup()

        #self.GData.appSettings.beginGroup("CopyMoveToPaths")
        #paths = self.GData.appSettings.childKeys()
        #i = 0
        #while i < paths.size():
        #    self.GData.bookmarkPaths.insert(self.GData.appSettings.value(paths.at(i).toString()))
        #    i +=1
        #self.GData.appSettings.endGroup()


    def setupDocks(self):
        print "setting up the docks"

    def lockDocks(self):
        print "locking all docked items"

    def createPopupMenu(self):
        print "creating popup menus"

    def loadShortcuts(self):
        print "loading shortcuts"

    def closeEvent(self):
        print "close Event"

    def setStatus(self):
        print "setting Status"

    def mouseDoubleClickEvent(self):
        print "mouse has been double clicked"

    def mousePressEvent(self):
        print "the mouse has been clicked"

    def newImage(self):
        print "creating a new Image"

    def setDocksVisibility(self):
        print "setting dock Visibility"

    def openOp(self):
        print "open operation"

    def setEditToolBarVisibility(self):
        print "setting the Edit Toolbar's visibility"


    def setGoToolBarVisibility(self):
        print "setting the Go Toolbar's Visibility"

    def setViewToolBarVisibility(self):
        print "setting the View Toolbar's Visibility"

    def setImageToolBarVisibility(self):
        print "setting the Image Toolbar's Visibility"

    def setFsDockVisibility(self):
        print "setting The File system Dock Visibility"

    def setBmDockVisibility(self):
        print "setting the Bookmark Dock Visibilty"

    def setIiDockVisibility(self):
        print "Setting the Thumbnail dock Visibility"

    def setPvDockVisibility(self):
        print "setting the Pv Dock Visibility"

    def showViewer(self):
        print "showing the Viewer"

    def showBusyStatus(self):
        print "Showing the Busy Status"

    def loadImageFromThumb(self):
        print "loading Image from thumbnail"

    def updateViewerImageBySelection(self):
        print "Updating Viewer image by selection"

    def loadImagefromCli(self):
        print "Loading Image from Cli"

    def slideShow(self):
        print "starting Slide show"

    def slideShowHandler(self):
        print "slide show handler"

    def selectThumbsByRow(self):
        print "selecting thumbs by row"

    def loadNextImage(self):
        print "Loading the next image"

    def loadPrevImage(self):
        print "Loading the previous image"

    def loadFirstImage(self):
        print "loading the first image"

    def loadLastImage(self):
        print "loading the last image"

    def loadRandomImage(self):
        print "loading a random image"

    def selectRecentThumb(self):
        print "selecting recent thumbnail"

    def setViewerKeyEventsEnabled(self):
        print "set viewer key events enabled"

    def updateIndexByViewerImage(self):
        print "update index by viewer image"

    def hideViewer(self):
        print "hide the viewer"

    def goBottom(self):
        print "Scroll Thumbnail view to the bottom"
        self.thumbView.scrollToBottom()

    def goTop(self):
        print "Scroll Thumbnail view to the top"
        self.thumbView.scrollToTop()

    def dropOp(self):
        print "drag item has been dropped"

    def selectCurrentViewDir(self):
        print "selecting currently viewed directory"

    def checkDirState(self):
        print "checking directory state"

    def recordHistory(self):
        print "record History"

    def reloadThumbsSlot(self):
        #if self.thumbView.busy:
        self.thumbView.abort()
        # QtCore.QTimer.singleShot(0,self.reloadThumbsSlot())
        self.thumbView.load()

    def setThumbViewWindowTitle(self):
        print "set the thumbnail view window title"

    def renameDir(self):
        print "renaming directory"

    def rename(self):
        print "rename"

    def deleteDir(self):
        print "delete directory"

    def createSubDirectory(self):
        print "creating Sub Directory"

    def getSelectedPath(self):
        logging.info("getting the path selected in fsTree")
        selectedDirs = self.fsTree.selectionModel().selectedRows()
        if selectedDirs[0].isValid():
            dirInfo = QtCore.QFileInfo(self.fsTree.fsModel.filePath(selectedDirs[0]))
            return dirInfo.absoluteFilePath()
        else:
            return ""

    def wheelEvent(self):
        print "mouse wheel event"

    def showNewImageWarning(self):
        print "showing a new Image Warning"

    def removeDirOp(self):
        print "removing directory Operation"

    def cleanupCropDialog(self):
        print "cleaning up the crop dialog"

    def cleanupScaleDialog(self):
        print "cleaning up the scale dialog"

    def cleanupColorsDialog(self):
        print "cleaning up the colors dialog"

    def setInterfaceEnabled(self):
        print "setting the interface to enabled"

    def addNewBookmark(self):
        print "adding a new bookmark"

    def addBookmark(self):
        print "adding bookmark"

    def findDuplicateImages(self):
        print "finding duplicate Images"

def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()