"""

__author__ = 'cargoyle'

"""
import logging

from PyQt4 import QtGui, QtCore
import sip
import maya.OpenMayaUI as apiUI
import pipeline.general.filebrowse.thumbview as tv

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

        # this is just for now, I want to use QDirectory
        # preferred image locations like this will be
        # captured in qsettings
        self.path = "D:/bank/reference/"
        self.directory = os.listdir(self.path)

        # locate the directory where all of the images for the ui live
        ScriptDir = pm.internalVar(uad=True)
        self.imgDirectory = str(ScriptDir+"/scripts/pipeline/general/filebrowse/images/")

        self.setObjectName("FileBrowser")
        self.resize(810, 460)
        self.fbLayout = QtGui.QHBoxLayout(self)
        #self.fbLayout.addStretch(1)
        #self.fbLayout.setContentsMargins(0,0,0,0)
        self.fbLayout.setSpacing(10)

        # internal class variable time
        self.copyMoveToDialog = 0
        self.colorsDialog = 0
        self.cropDialog = 0
        self.initComplete = True

        self.needHistory = True
        self.interfaceDisabled = False

        #self.readSettings()
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


    #def event(self, QtCore.QEvent()):
    #    """
    #    """

    def createThumbView(self):
        import pipeline.general.filebrowse.thumbview as tv

        self.thumbView = tv.thumbView(self)
        self.thumbView.thumbsDir.setPath(self.path)
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

    def createActions(self):
        """

        :return:
        """
        self.thumbsZoomInAct = QtGui.QAction("Enlarge Thumbnails", self)
        self.thumbsZoomInAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom_in.png")))
        self.thumbsZoomInAct.triggered.connect(lambda:self.thumbsZoomIn())


        self.thumbsZoomOutAct = QtGui.QAction("Shrink Thumbnails", self)
        self.thumbsZoomOutAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom_out.png")))
        self.thumbsZoomOutAct.triggered.connect(lambda: self.thumbsZoomOut())

        self.cutAction = QtGui.QAction("Cut", self)
        self.cutAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"cut.png")))

        self.copyAction = QtGui.QAction("Copy", self)
        self.copyAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"copy.png")))


        self.deleteAction = QtGui.QAction("Delete", self)
        self.deleteAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"delete.png")))

        self.refreshAction = QtGui.QAction("Reload", self)
        self.refreshAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"refresh.png")))

        self.subFoldersAction = QtGui.QAction("Include Sub-Folders", self)
        self.subFoldersAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"tree.png")))

        self.pasteAction = QtGui.QAction("Paste Here", self)
        self.pasteAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"paste.png")))

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

        self.showClipboardAction = QtGui.QAction("Load Clipboard", self)
        self.showClipboardAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"new.png")))

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

    def refreshThumbs(self, scrollToTop):
        self.thumbView.setNeedScroll(scrollToTop)
        QtCore.QTimer.singleShot(0, lambda: self.reloadThumbsSlot())

    def about(self):
        print " displaying about message"

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

    def goTo(self, path):
        print str("going to QDir "+path)
        self.fsTree.setCurrentIndex(self.fsTree.fsModel.index(path))
        self.thumbView.currentViewDir = path
        # this is not the right directory, just trying to get this to work
        self.thumbView.thumbsDir.setPath(path)
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
        print " goto home directory"
        self.goTo(QtCore.QDir.homePath())

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

    def getSelectedPath(self):
        logging.info("getting the path selected in fsTree")
        selectedDirs = self.fsTree.selectionModel().selectedRows()
        if selectedDirs.size() && selectedDirs[0].isValid():
            dirInfo = QtCore.QFileInfo(self.fsTree.fsModel.filePath(selectedDirs[0]))
            return dirInfo.absoluteFilePath()
        else:
            return ""

    def goSelectedDir(self):
        logging.info("go to the directory selected in the tree widget")
        self.thumbView.setNeedScroll(True)
        selectedPath = self.getSelectedPath()
        self.thumbView.currentViewDir = selectedPath
        self.thumbView.thumbsDir.setPath(selectedPath)
        self.refreshThumbs(True)

def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()