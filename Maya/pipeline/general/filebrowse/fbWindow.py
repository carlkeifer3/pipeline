"""

__author__ = 'cargoyle'

"""
import logging

from PyQt4 import QtGui, QtCore
import os
import sip
import maya.OpenMayaUI as apiUI
import pipeline.general.filebrowse.thumbview as tv
import pipeline.general.filebrowse.imageview as iv
import pipeline.general.filebrowse.dialogs as dia
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

        self.log =logging.getLogger("phototonic_Logger")
        self.log.setLevel(logging.debug)

        # locate the directory where all of the images for the ui live
        ScriptDir = pm.internalVar(uad=True)
        self.imgDirectory = str(ScriptDir+"/scripts/pipeline/general/filebrowse/images/")

        self.setObjectName("FileBrowser")
        self.fbLayout = QtGui.QHBoxLayout(self)
        #self.fbLayout.addStretch(1)
        #self.fbLayout.setContentsMargins(0,0,0,0)
        #self.fbLayout.setSpacing(10)


        self.readSettings()
        self.createThumbView()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createFSTree()
        self.createBookmarks()
        self.createImageView()
        #self.UpdateExternalApps()
        self.loadShortcuts()
        self.setupDocks()

        self.restoreGeometry(g.GData.appSettings.value("Geometry").toByteArray())
        self.restoreState(g.GData.appSettings.value("WindowState").toByteArray())
        self.setWindowIcon(QtGui.QIcon(self.imgDirectory+"phototonic.png"))

        self.fbLayout.addWidget(self.thumbView)
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.fbLayout)
        self.setCentralWidget(self.centralWidget)

        # internal class variable time
        self.copyCutCount = 0
        self.copyMoveToDialog = 0
        self.colorsDialog = 0
        self.cropDialog = 0
        self.initComplete = True
        #self.thumbView.busy = False
        self.currentHistoryIdx = -1
        self.needHistory = True
        self.interfaceDisabled = False

        self.doFindDuplicates = False
        self.refreshThumbs(True)

        #self.setLayout(self.fbLayout)

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
        self.log.debug("fbWindow.createThumbView")
        self.log.info("Building the ThumbView")
        import pipeline.general.filebrowse.thumbview as tv

        self.thumbView = tv.thumbView(self)
        #self.thumbView.load()
        #print "thumbview should be built"
        #self.fbLayout.addWidget(self.thumbView)

        self.iiDock = QtGui.QDockWidget("Image Info", self)
        self.iiDock.setObjectName("ImageInfo")
        #self.iiDock.setWidget(self.thumbView)

        #self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.iiDock)
        self.log.info("ThumbView should be built")

    def AddMenuSeparator(self):
        """

        :return:
        """
        self.log.debug("fbWindow.addMenuSeparator")
        separator = QtCore.QAction(self)
        separator.setSeparator(True)
        self.addAction(separator)

    def createImageView(self):
        """

        :return:
        """
        logging.info("fbWindow.createImageView()")
        logging.info("Creating the Image View")
        import pipeline.general.filebrowse.imageview as iv

        self.imageView = iv.imageView()

        self.imageView.ImagePopUpMenu = QtGui.QMenu()

        ## Widget Actions
        self.imageView.addAction(self.slideShowAction)
        self.imageView.addAction(self.nextImageAction)
        self.imageView.addAction(self.prevImageAction)
        self.imageView.addAction(self.firstImageAction)
        self.imageView.addAction(self.lastImageAction)
        self.imageView.addAction(self.randomImageAction)
        self.imageView.addAction(self.zoomInAct)
        self.imageView.addAction(self.zoomOutAct)
        self.imageView.addAction(self.origZoomAct)
        self.imageView.addAction(self.resetZoomAct)
        self.imageView.addAction(self.rotateRightAct)
        self.imageView.addAction(self.rotateLeftAct)
        self.imageView.addAction(self.freeRotateRight)
        self.imageView.addAction(self.freeRotateLeftAct)
        self.imageView.addAction(self.flipHAct)
        self.imageView.addAction(self.flipVAct)
        self.imageView.addAction(self.cropAct)
        self.imageView.addAction(self.cropToSelectionAct)
        self.imageView.addAction(self.resizeAct)

    def createActions(self):
        """

        :return:
        """
        self.log.debug("creating all actions for the file browser")
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

        #if self.thumbView.thumbsSortFlags & QDir.time:
        #    self.actTime.setChecked(True)
        #elif self.thumbView.thumbsSortFlags & Qdir.Size:
        #    self.actSize.setChecked(True)
        #elif self.thumbView.thumbsSortFlags & QDir.Type:
        #    self.actType.setChecked(True)
        #else:
        #    self.actName.setChecked(True)
        #self.actReverse.setChecked(self.thumbView.thumbsSortFlags & QDir.reversed)

        self.actShowHidden = QtGui.QAction("Show Hidden Files", self)
        self.actShowHidden.setCheckable(True)
        self.actShowHidden.setChecked(g.GData.showHiddenFiles)
        self.actShowHidden.triggered.connect(lambda: self.showHiddenFiles())

        self.actShowLabels = QtGui.QAction("Show Labels", self)
        self.actShowLabels.setCheckable(True)
        self.actShowLabels.setChecked(g.GData.showLabels)
        self.actShowLabels.triggered.connect(lambda: self.showLabels())

        self.actSmallIcons = QtGui.QAction("Small Icons", self)
        self.actSmallIcons.setCheckable(True)
        self.actSmallIcons.setChecked(g.GData.smallIcons)

        self.actLockDocks = QtGui.QAction("Hide Docks Title Bar", self)
        self.actLockDocks.setCheckable(True)
        self.actLockDocks.setChecked(g.GData.LockDocks)
        self.actLockDocks.triggered.connect(lambda: self.lockDocks())

        self.actShowViewerToolbars = QtGui.QAction("Show Toolbar", self)
        self.actShowViewerToolbars.setCheckable(True)
        self.actShowViewerToolbars.setChecked(g.GData.imageToolbarFullScreen)
        self.actShowViewerToolbars.triggered.connect(lambda: self.toggleImageToolbar())

        # Thumbnail view actions
        self.actClassic = QtGui.QAction("Classic Thumbs", self)
        self.actCompact = QtGui.QAction("Compact", self)
        self.actSquarish = QtGui.QAction("Squarish", self)
        self.actClassic.triggered.connect(lambda: self.setClassicThumbs())
        self.actCompact.triggered.connect(lambda: self.setCompactThumbs())
        self.actSquarish.triggered.connect(lambda: self.setSquareishThumbs())
        self.actClassic.setCheckable(True)
        self.actCompact.setCheckable(True)
        self.actSquarish.setCheckable(True)
        #self.actClassic.setChecked(g.GData.thumbsLayout == self.thumbView.Classic)
        #self.actCompact.setChecked(g.GData.thumbsLayout == self.thumbView.Compact)
        #self.actSquarish.setChecked(g.GData.thumbsLayout == self.thumbView.Squares)

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

        self.createDirAction = QtGui.QAction("New Folder", self)
        self.createDirAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"new_Folder.png")))
        self.createDirAction.triggered.connect(lambda: self.createSubDirectory())

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

        self.nextImageAction = QtGui.QAction("Next", self)
        self.nextImageAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"Next.png")))
        self.nextImageAction.triggered.connect(lambda: self.loadNextImage())

        self.prevImageAction = QtGui.QAction("Previous", self)
        self.prevImageAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"back.png")))
        self.prevImageAction.triggered.connect(lambda: self.loadPrevImage())

        self.firstImageAction = QtGui.QAction("First", self)
        self.firstImageAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"first.png")))
        self.firstImageAction.triggered.connect(lambda: self.loadFirstImage())

        self.lastImageAction = QtGui.QAction("Last", self)
        self.lastImageAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"last.png")))
        self.lastImageAction.triggered.connect(lambda: self.loadLastImage())

        self.randomImageAction = QtGui.QAction("Random", self)
        self.randomImageAction.triggered.connect(lambda: self.loadRandomImage())

        self.openAction = QtGui.QAction("Open", self)
        self.openAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"open.png")))
        self.openAction.triggered.connect(lambda: self.openOp())

        self.showClipboardAction = QtGui.QAction("Load Clipboard", self)
        self.showClipboardAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"new.png")))
        self.showClipboardAction.triggered.connect(lambda: self.newImage())

        self.openWithSubMenu = QtGui.QMenu("Open With")
        self.openWithMenuAct = QtGui.QAction("Open With", self)
        self.openWithMenuAct.setMenu(self.openWithSubMenu)
        self.chooseAppAct = QtGui.QAction("Manage External Applications", self)
        self.chooseAppAct.triggered.connect(lambda: self.chooseExternalApp())

        self.addBookmarkAction = QtGui.QAction("Add Bookmark", self)
        self.addBookmarkAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"new_Bookmark.png")))
        self.addBookmarkAction.triggered.connect(lambda: self.addNewBookmark())

        self.removeBookmarkAction = QtGui.QAction("Remove Bookmark", self)
        self.removeBookmarkAction.setIcon(QtGui.QIcon(str(self.imgDirectory+"delete.png")))

        self.zoomOutAct = QtGui.QAction("Zoom Out", self)
        self.zoomOutAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom_out.png")))
        self.zoomOutAct.triggered.connect(lambda: self.zoomOut())

        self.zoomInAct = QtGui.QAction("Zoom In", self)
        self.zoomInAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"Zoom_in.png")))
        self.zoomInAct.triggered.connect(lambda: self.zoomIn())

        self.resetZoomAct = QtGui.QAction("Reset Zoom", self)
        self.resetZoomAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom.png")))
        self.resetZoomAct.triggered.connect(lambda: self.resetZoom())

        self.origZoomAct = QtGui.QAction("Original Size", self)
        self.origZoomAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"zoom1.png")))
        self.origZoomAct.triggered.connect(lambda: self.origZoom())

        self.keepZoomAct = QtGui.QAction("Keep Zoom", self)
        self.keepZoomAct.setCheckable(True)
        self.keepZoomAct.triggered.connect(lambda: self.keepZoom())

        self.rotateLeftAct = QtGui.QAction("Rotate 90 degree CCW", self)
        self.rotateLeftAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"rotate_left.png")))
        self.rotateLeftAct.triggered.connect(lambda: self.rotateLeft())

        self.rotateRightAct = QtGui.QAction("Rotate 90 degree CW", self)
        self.rotateRightAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"rotate_right.png")))
        self.rotateRightAct.triggered.connect(lambda: self.rotateRight())

        self.flipHAct = QtGui.QAction("Object-Flip-Horizontal", self)
        self.flipHAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"flipH.png")))
        self.flipHAct.triggered.connect(lambda: self.flipHoriz())

        self.flipVAct = QtGui.QAction("Object-Flip-Vertical", self)
        self.flipVAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"flipV.png")))
        self.flipVAct.triggered.connect(lambda: self.flipVert())

        self.cropAct = QtGui.QAction("Cropping", self)
        self.cropAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"crop.png")))
        self.cropAct.triggered.connect(lambda: self.cropImage())

        self.cropToSelectionAct = QtGui.QAction("Crop to Selection", self)
        self.cropToSelectionAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"crop.png")))

        self.resizeAct = QtGui.QAction("Scale Image", self)
        self.resizeAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"scale.png")))
        self.resizeAct.triggered.connect(lambda: self.scaleImage())

        self.freeRotateLeftAct = QtGui.QAction("Rotate 1 degree CCW", self)
        self.freeRotateLeftAct.triggered.connect(lambda:self.freeRotateLeft())

        self.freeRotateRight = QtGui.QAction("Rotate 1 degree CW", self)
        self.freeRotateRight.triggered.connect(lambda: self.freeRotateRight())

        self.colorsAct = QtGui.QAction("Colors", self)
        self.colorsAct.setIcon(QtGui.QIcon(str(self.imgDirectory+"colors.png")))
        self.colorsAct.triggered.connect(lambda: self.showColorsDialog())

        self.findDupesAction = QtGui.QAction("Find Duplicate Images", self)
        self.findDupesAction.triggered.connect(lambda: self.findDupesAction)

        self.mirrorDisabledAct = QtGui.QAction("Disable", self)
        self.mirrorDualAct = QtGui.QAction("Dual", self)
        self.mirrorTripleAct = QtGui.QAction("Triple", self)
        self.mirrorVDualAct = QtGui.QAction("Dual Vertical", self)
        self.mirrorQuadAct = QtGui.QAction("Quad", self)

        self.mirrorDisabledAct.setCheckable(True)
        self.mirrorQuadAct.setCheckable(True)
        self.mirrorTripleAct.setCheckable(True)
        self.mirrorDualAct.setCheckable(True)
        self.mirrorVDualAct.setCheckable(True)
        self.mirrorDisabledAct.triggered.connect(lambda: self.setMirrorDisabled())
        self.mirrorDualAct.triggered.connect(lambda: self.setMirrorDual())
        self.mirrorTripleAct.triggered.connect(lambda: self.setMirrorTriple())
        self.mirrorVDualAct.triggered.connect(lambda: self.setMirrorVDual())
        self.mirrorQuadAct.triggered.connect(lambda: self.setMirrorQuad())

        self.keepTransformAct = QtGui.QAction("Lock Transformations", self)
        self.keepTransformAct.setCheckable(True)
        self.keepTransformAct.triggered.connect(lambda: self.keepTransformClicked())

        self.moveLeftAct = QtGui.QAction("Move Left", self)
        self.moveLeftAct.triggered.connect(lambda: self.moveLeft())
        self.moveRightAct = QtGui.QAction("Move Right", self)
        self.moveRightAct.triggered.connect(lambda: self.moveRight())
        self.moveUpAct = QtGui.QAction("Move Up", self)
        self.moveUpAct.triggered.connect(lambda: self.moveUp())
        self.moveDownAct = QtGui.QAction("Move Down", self)
        self.moveDownAct.triggered.connect(lambda: self.moveDown())

        self.invertSelectionAct = QtGui.QAction("Invert Selection", self)
        self.invertSelectionAct.triggered.connect(lambda: self.invertSelection())

        self.filterImagesFocusAct = QtGui.QAction("Filter by Name", self)
        self.filterImagesFocusAct.triggered.connect(lambda: self.filterImagesFocus())
        self.setPathFocusAct = QtGui.QAction("Set Path", self)
        self.setPathFocusAct.triggered.connect(lambda: self.setPathFocus())

    def createMenus(self):
        """

        :return:
        """
        self.log.info("creating the menus")
        self.menubar = QtGui.QMenuBar(self)
        self.fileMenu = QtGui.QMenu("&File", self.menubar)
        self.fileMenu.addAction(self.subFoldersAction)
        self.fileMenu.addAction(self.createDirAction)
        self.fileMenu.addAction(self.showClipboardAction)
        self.fileMenu.addAction(self.addBookmarkAction)
        self.fileMenu.addSeparator()
        # probably won't add this. but who knows.
        # I would like to use this widget as a dockable widget
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = QtGui.QMenu("&Edit", self.menubar)
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.copyToAction)
        self.editMenu.addAction(self.moveToAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.selectAllAction)
        self.editMenu.addAction(self.invertSelectionAct)
        #addAction("filterImagesFocusAct")
        #addAction("setPathFocusAct")
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.settingsAction)

        self.goMenu = QtGui.QMenu("&Go", self.menubar)
        self.goMenu.addAction(self.goBackAction)
        self.goMenu.addAction(self.goFrwdAction)
        self.goMenu.addAction(self.goUpAction)
        self.goMenu.addAction(self.goHomeAction)
        self.goMenu.addSeparator()
        self.goMenu.addAction(self.thumbsGoTopAct)
        self.goMenu.addAction(self.thumbsGoBottomAct)

        self.viewMenu = QtGui.QMenu("&View", self.menubar)
        self.viewMenu.addAction(self.slideShowAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.thumbsZoomInAct)
        self.viewMenu.addAction(self.thumbsZoomOutAct)
        self.sortMenu = self.viewMenu.addAction("Sort By")
        self.sortTypesGroup = QtGui.QActionGroup(self)
        self.sortTypesGroup.addAction(self.actName)
        self.sortTypesGroup.addAction(self.actTime)
        self.sortTypesGroup.addAction(self.actSize)
        self.sortTypesGroup.addAction(self.actType)
        #self.sortMenu.addActions(self.sortTypesGroup.actions())
        #self.sortMenu.addSeparator()
        #self.sortMenu.addActions("actReverse")
        self.viewMenu.addSeparator()

        #self.thumbsLayoutGroup = QtGui.QActionGroup(self)
        #self.thumbsLayoutGroup.addAction(self.actClassic)
        #self.thumbsLayoutGroup.addAction(self.actCompact)
        #self.thumbsLayoutGroup.addAction(self.actSquarish)
        #self.viewMenu.addAction(self.thumbsLayoutGroup.actions())
        #self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.refreshAction)


        self.toolsMenu = QtGui.QMenu("&Tools", self.menubar)
        self.toolsMenu.addAction(self.findDupesAction)

        self.menubar.addSeparator()
        self.helpMenu = QtGui.QMenu("&Help", self.menubar)
        self.helpMenu.addAction(self.aboutAction)

        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.goMenu)
        self.menubar.addMenu(self.viewMenu)
        self.menubar.addMenu(self.toolsMenu)
        self.menubar.addMenu(self.helpMenu)
        self.setMenuBar(self.menubar)

        # thumbView Context menu
        self.thumbView.addAction(self.openAction)
        self.thumbView.addAction(self.openWithMenuAct)
        self.thumbView.addAction(self.cutAction)
        self.thumbView.addAction(self.copyAction)
        self.thumbView.addAction(self.pasteAction)
        #self.addMenuSeparator(self.thumbView)
        self.thumbView.addAction(self.copyToAction)
        self.thumbView.addAction(self.moveToAction)
        self.thumbView.addAction(self.renameAction)
        self.thumbView.addAction(self.deleteAction)
        #self.addMenuSeparator(self.thumbView)
        self.thumbView.addAction(self.selectAllAction)
        self.thumbView.addAction(self.invertSelectionAct)
        self.thumbView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.menubar.setVisible(True)

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
        self.editToolBar.toggleViewAction().triggered.connect(lambda: self.setEditToolBarVisibility())

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
        self.pathComplete = QtGui.QCompleter(self)
        self.pathCompleteDirMod = QtGui.QDirModel()
        self.pathCompleteDirMod.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.pathComplete.setModel(self.pathCompleteDirMod)
        self.pathBar.setCompleter(self.pathComplete)
        self.pathBar.setMinimumWidth(200)
        self.pathBar.setMaximumWidth(300)
        self.pathBar.returnPressed.connect(lambda: self.goPathBarDir())

        self.goToolBar.addWidget(self.pathBar)
        self.goToolBar.addAction(self.subFoldersAction)
        self.goToolBar.toggleViewAction().triggered.connect(lambda: self.setGoToolBarVisibility())

        # View Toolbar
        self.viewToolBar = self.addToolBar("View")
        self.viewToolBar.setObjectName("View")
        self.viewToolBar.addAction(self.slideShowAction)
        self.viewToolBar.addAction(self.thumbsZoomInAct)
        self.viewToolBar.addAction(self.thumbsZoomOutAct)

        # Filter Bar
        self.filterAct = QtGui.QAction("Filter", self)
        self.filterAct.setIcon(QtGui.QIcon(self.imgDirectory+"zoom.png"))
        self.filterAct.triggered.connect(lambda: self.setThumbsFilter())
        self.filterBar = QtGui.QLineEdit()
        self.filterBar.setMinimumWidth(100)
        self.filterBar.setMaximumWidth(200)
        self.filterBar.returnPressed.connect(lambda: self.setThumbsFilter())
        self.filterBar.textChanged.connect(lambda: self.clearThumbsFilter())

        self.viewToolBar.addSeparator()
        self.viewToolBar.addWidget(self.filterBar)
        self.viewToolBar.addAction(self.settingsAction)
        #self.viewToolBar.toggleViewAction().triggered.connect(lambda: self.setViewToolBarVisibility())

        # Image
        self.imageToolBar = self.addToolBar("Image")
        self.imageToolBar.setObjectName("Image")
        self.imageToolBar.addAction(self.prevImageAction)
        self.imageToolBar.addAction(self.nextImageAction)
        self.imageToolBar.addAction(self.firstImageAction)
        self.imageToolBar.addAction(self.lastImageAction)
        self.imageToolBar.addAction(self.slideShowAction)
        self.imageToolBar.addSeparator()
        self.imageToolBar.addAction(self.saveAction)
        self.imageToolBar.addAction(self.saveAsAction)
        self.imageToolBar.addAction(self.deleteAction)
        self.imageToolBar.addSeparator()
        self.imageToolBar.addAction(self.resizeAct)
        self.imageToolBar.addAction(self.rotateRightAct)
        self.imageToolBar.addAction(self.rotateLeftAct)
        self.imageToolBar.addAction(self.flipHAct)
        self.imageToolBar.addAction(self.flipVAct)
        self.imageToolBar.addAction(self.cropAct)
        self.imageToolBar.addAction(self.colorsAct)
        self.imageToolBar.setVisible(True)

        self.imageToolBar.toggleViewAction().triggered.connect(lambda: self.setImageToolBarVisibility())

        self.setToolbarIconSize()

    def setToolbarIconSize(self):
        print "setting Toolbar icon size"

    def createStatusBar(self):
        self.log.debug("creating Status bar")

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
        logging.info("creating filesystem tree")
        import pipeline.general.filebrowse.fstree as fs

        self.fsDock = QtGui.QDockWidget("File System", self)
        self.fsDock.setObjectName("File System")

        self.fsTree = fs.FSTree(self.fsDock)
        self.fsDock.setWidget(self.fsTree)

        self.fsDock.toggleViewAction().triggered.connect(lambda: self.setFsDockVisibility())
        #self.fsDock.visibilityChanged.connect(lambda: self.setFsDockVisibility())
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.fsDock)

        #Context Menu
        self.fsTree.addAction(self.openAction)
        self.fsTree.addAction(self.createDirAction)
        self.fsTree.addAction(self.renameAction)
        self.fsTree.addAction(self.deleteAction)
        #self.fsTree.addSeparator()
        self.fsTree.addAction(self.pasteAction)
        #self.fsTree.addSeparator()
        self.fsTree.addAction(self.openWithMenuAct)
        self.fsTree.addAction(self.addBookmarkAction)
        self.fsTree.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.fsTree.clicked.connect(lambda: self.goSelectedDir())

    def createBookmarks(self):
        logging.info("creating bookmarks window")
        import pipeline.general.filebrowse.bookmarks as bm

        self.bmDock = QtGui.QDockWidget("Bookmarks", self)
        self.bmDock.setObjectName("Bookmarks")
        self. bookmarks = bm.BookMarks(self.bmDock)
        self.bmDock.setWidget(self.bookmarks)



        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.bmDock)

        self.bookmarks.addAction(self.pasteAction)
        self.bookmarks.addAction(self.removeBookmarkAction)
        self.bookmarks.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def sortThumbnails(self):
        print "sorting thumbnails"

    def reload(self):
        print "reload"

    def setIncludeSubFolders(self):
        logging.debug("set Include SubFolders")
        g.GData.includeSubFolders = self.subFoldersAction.isChecked()
        self.refreshThumbs(False)

    def refreshThumbs(self, scrollToTop):
        logging.info("refresh Thumbs")
        self.thumbView.setNeedScroll(scrollToTop)
        QtCore.QTimer.singleShot(0, lambda: self.reloadThumbsSlot())
        QtCore.QTimer.singleShot(100, lambda: self.selectRecentThumb())

    def setClassicThumbs(self):
        logging.info("setting classic thumbs view")
        #g.GData.thumbsLayout = self.tl.Classic

    def setCompactThumbs(self):
        print "setting compact thumbs view"

    def setSquareishThumbs(self):
        print "setting Square thumbs view"

    def showHiddenFiles(self):
        print "showing hidden files"

    def toggleImageToolbar(self):
        logging.info("toggling Image Toolbar")
        self.imageToolBar.setVisible(self.actShowViewerToolbars.isChecked())
        g.GData.imageToolbarFullScreen = self.actShowViewerToolbars.isChecked()

    def showLabels(self):
        print "showing Labels"

    def about(self):
        print " displaying about message"
        aboutString = QtCore.QString("<h2>Phototonic v1.5 for maya</h2>"\
            "<p>ImageViewer and Organizer</p>"\
            "QT v"\
            "<p><a href=\"http://oferkv.github.io/phototonic\">"+"Bug reports"+"</a></p>"\
            "<p><a href=\"https://github.com/oferkv/phototonic/issues\">"+"Bug reports"+"</a></p>"\
		    "<p>Copyright &copy; 2013-2014 Ofer Kashayov (oferkv@live.com)</p>"\
		    "Contributors / Code:<br>"\
		    "Christopher Roy Bratusek (nano@jpberlin.de)<br><br>"\
            "Carl Keifer: Maya Port (cargoyle@hotmail.com)<br><br>"\
		    "Contributors / Translations:"\
		    "<table><tr><td>Czech:</td><td>Pavel Fric (pavelfric@seznam.cz)</td></tr>"\
		    "<tr><td>French:</td><td>David Geiger (david.david@mageialinux-online.org)</td></tr>"\
		    "<tr><td></td><td>Adrien Daugabel (adrien.d@mageialinux-online.org)</td></tr>"\
		    "<tr><td></td><td>Raomi Verschelde (akien@mageia.org)</td></tr>"\
		    "<tr><td>German:</td><td>Jonathan Hooverman (jonathan.hooverman@gmail.com)</td></tr>"\
		    "<tr><td>Polish:</td><td>Robert Wojew\u00F3dzki (robwoj44@poczta.onet.pl)</td></tr>"\
		    "<tr><td>Russian:</td><td>Ilya Alexandrovich (yast4ik@gmail.com)</td></tr></table>"\
		    "<p>Phototonic is licensed under the GNU General Public License version 3</p>")

        QtGui.QMessageBox.about(self, "About Phototonic", aboutString)

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
        logging.info("loading preferences window")
        if g.GData.slideShowActive:
            self.slideShow()
        #self.imageView.setCursorHiding(False)
        dialog = dia.settingsDialog(self)

        #if dialog.exec():
        #     self.thumbView.setThumbColors()
        #     g.GData.imageZoomFactor = 1.0
        #del dialog

    def toggleFullScreen(self):
        print "Toggle Full Screen Mode"

    def selectAllThumbs(self):
        logging.info("selecting all thumbs")
        self.thumbView.selectAll()

    def copyOrCutThumbs(self, copy):
        logging.info("copy or cut thumbs")
        g.GData.copyCutIdxList = self.thumbView.selectionModel().selectedIndexes()
        g.GData.copyCutFileList.clear()
        for f in g.GData.copyCutIdxList:
            g.GData.copyCutFileList.append(self.thumbView.thumbModel.item(f.row()).data(self.thumbView.fileNameRole).toString())
            self.copyCutCount +=1
        g.GData.copyOp = copy
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
        #if self.thumbView.thumbSize < self.ThumbMaxSize:
        self.thumbView.thumbSize += 25
        self.thumbsZoomInAct.setEnabled(True)
        # check the thumbs to make sure we don't go over the max size
        #if self.thumbView.thumbSize == self.ThumbMaxSize:
        #    self.thumbsZoomInAct.setEnabled(False)
        logging.info("Thumbs have been enlarged to: " + str(self.thumbView.thumbSize))
        self.refreshThumbs(False)

    def thumbsZoomOut(self):
        #if self.thumbView.thumbSize < self.ThumbMinSize:
        self.thumbView.thumbSize -= 25
        self.thumbsZoomOutAct.setEnabled(True)
        # check the thumbs to make sure we don't go over the max size
        #if self.thumbView.thumbSize == self.ThumbMinSize:
        #    self.thumbsZoomOutAct.setEnabled(False)
        logging.info("Thumbs have been shrunk to: " + str(self.thumbView.thumbSize))
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
        logging.info("fbWindow.showColorsDialog()")
        logging.info("Showing colors dialog")

        if g.GData.slideShowActive:
            self.slideShow()

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

    def isValidPath(self, path):
        logging.info("fbWindow.isValidPath()")
        logging.info("is this path Valid")

        checkPath = QtCore.QDir(path)
        if checkPath.exists() == False:
            if checkPath.isReadable() == False:
                return False

        return True

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

        #g.GData.copyCutIdxList.clear()
        #g.GData.copyCutFileList.clear()
        self.pasteAction.setEnabled(False)
        self.thumbView.loadVisibleThumbs(0)

    def updateCurrentImage(self):
        print "update current Image"

    def deleteViewerImage(self):
        print "deleteViewerImage"

    def deleteOp(self):
        print "Deleting"

    def goTo(self, path):
        logging.info(str("going to QDir "+path))
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
        logging.info("fbWindow.goPathBarDir()")
        logging.info("go to the directory indicated by the path bar")

        self.thumbView.setNeedScroll(True)

        self.checkPath = QtCore.QDir(self.pathBar.text())
        if self.checkPath.exists() == False:
            if self.checkPath.isReadable():

                self.msgBox = QtGui.QMessageBox()
                self.msgBox.critical(self, "Error", "Invalid Path: "+ self.pathBar.text())
                self.pathBar.setText(self.thumbView.currentViewDir)
                return
        self.thumbView.currentViewDir = self.pathBar.text()
        self.refreshThumbs(True)
        self.selectCurrentViewDir()

    def bookmarkClicked(self, item, col):
        logging.info("bookmark selected")
        self.goTo(item.toolTip(col))

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
        logging.info(" goto home directory")
        self.goTo(QtCore.QDir.homePath())

    def setCopyCutActions(self):
        print "setting the cut and copy actions"

    def changeActionsBySelection(self):
        print "changing actions by selection"

    def UpdateActions(self):
        print "Updating Actions"

    def writeSettings(self):
        logging.info("Writing Settings")
        #if g.GData.layoutMode

        #g.GData.appSettings.setValue("ThumbsSortFlags", int(self.thumbView.thumbSortFlags))
        g.GData.appSettings.setValue("ThumbsZoomVal", int(self.thumbView.thumbSize))
        g.GData.appSettings.setValue("isFullScreen", bool(g.GData.isFullScreen))
        g.GData.appSettings.setValue("backgroundColor", g.GData.backgroundColor)
        logging.info("Background Color" + str(g.GData.backgroundColor))
        g.GData.appSettings.setValue("backgroundThumbColor", g.GData.thumbsBackgroundColor)
        #logging.info("Background Thumb Color" + str(g.GData.thumbsBackgroundColor))
        g.GData.appSettings.setValue("textThumbColor", g.GData.thumbsTextColor)
        #logging.info("Text Thumb Color" + str(g.GData.thumbsTextColor))
        g.GData.appSettings.setValue("thumbSpacing", g.GData.thumbsSpacing)
        logging.info("Thumbs Spacing " + str(g.GData.thumbsSpacing))
        g.GData.appSettings.setValue("thumbsPagesReadahead", int(g.GData.thumbPagesReadahead))
        g.GData.appSettings.setValue("thumbLayout", int(g.GData.thumbsLayout))
        g.GData.appSettings.setValue("exitInsteadOfClose", int(g.GData.exitInsteadofClose))
        g.GData.appSettings.setValue("enableAnimations", bool(g.GData.enableAnimations))
        g.GData.appSettings.setValue("exifRotationEnabled", bool(g.GData.exifRotationEnabled))
        g.GData.appSettings.setValue("reverseMouseBehavior", bool(g.GData.reverseMouseBehavior))
        g.GData.appSettings.setValue("showHiddenFiles", bool(g.GData.showHiddenFiles))
        g.GData.appSettings.setValue("wrapImageList", bool(g.GData.wrapImageList))
        g.GData.appSettings.setValue("imageZoomFactor", g.GData.imageZoomFactor)
        g.GData.appSettings.setValue("shouldMaximize", bool(self.isMaximized()))
        g.GData.appSettings.setValue("defaultSaveQuality", g.GData.defaultSaveQuality)
        g.GData.appSettings.setValue("noEnlargeSmallThumb", bool(g.GData.noEnlargeSmallThumbs))
        g.GData.appSettings.setValue("slideShowDelay", g.GData.slideShowDelay)
        g.GData.appSettings.setValue("slideShowRandom", bool(g.GData.slideShowRandom))
        g.GData.appSettings.setValue("editToolBarVisible", bool(self.editToolbarVisible))
        g.GData.appSettings.setValue("goToolBarVisible", bool(self.goToolBarVisible))
        g.GData.appSettings.setValue("viewToolBarVisible", bool(self.viewToolBarVisible))
        g.GData.appSettings.setValue("imageToolBarVisible", bool(self.imageToolBarVisible))
        g.GData.appSettings.setValue("fsDockVisible", bool(g.GData.fsDockVisible))
        g.GData.appSettings.setValue("iiDockVisible", bool(g.GData.iiDockVisible))
        g.GData.appSettings.setValue("pvDockVisible", bool(g.GData.pvDockVisible))
        #g.GData.appSettings.setValue("startupDir", int(g.GData.startupDir))
        g.GData.appSettings.setValue("specifiedStartDir", g.GData.specifiedStartDir)
        g.GData.appSettings.setValue("thumbsBackImage", g.GData.thumbsBackImage)
        #g.GData.appSettings.setValue("lastDir", g.GData.startupDir == g.GData.rememberLastDir)

        g.GData.appSettings.setValue("enableImageInfoFS", bool(g.GData.enableImageInfoFS))
        g.GData.appSettings.setValue("showLabels", bool(g.GData.showLabels))
        g.GData.appSettings.setValue("smallIcons", bool(g.GData.smallIcons))
        g.GData.appSettings.setValue("LockDocks", bool(g.GData.LockDocks))
        g.GData.appSettings.setValue("imageToolbarFullScreen", bool(g.GData.imageToolbarFullScreen))

        logging.info("settings Written exiting Cleanly")


    def readSettings(self):
        logging.info("Reading Settings")
        self.initComplete = False
        self.needThumbsRefresh = False

        if not g.GData.appSettings.contains("thumbsZoomVal"):
            logging.info(" app settings not found")
            self.resize(800, 600)
            g.GData.appSettings.setValue("thumbsSortFlags", int(0))
            g.GData.appSettings.setValue("thumbsZoomVal", 150)
            g.GData.appSettings.setValue("isFullScreen", False)
            g.GData.appSettings.setValue("backgroundColor", QtGui.QColor(25, 25, 25))
            g.GData.appSettings.setValue("backgroundThumbColor", QtGui.QColor(200, 200, 200))
            g.GData.appSettings.setValue("textThumbColor", QtGui.QColor(25, 25, 25))
            g.GData.appSettings.setValue("thumbSpacing", 10)
            g.GData.appSettings.setValue("thumbPagesReadahead", 2)
            g.GData.appSettings.setValue("thumbsLayout", g.GData.thumbsLayout)
            g.GData.appSettings.setValue("zoomOutFlags", 1)
            g.GData.appSettings.setValue("zoomInFlags", 0)
            g.GData.appSettings.setValue("wrapImageList", False)
            g.GData.appSettings.setValue("exitInsteadOfClose", 0)
            g.GData.appSettings.setValue("imageZoomFactor", 1.0)
            g.GData.appSettings.setValue("defaultSaveQuality", 100)
            g.GData.appSettings.setValue("noEnlargeSmallThumb", True)
            g.GData.appSettings.setValue("enableAnimations", True)
            g.GData.appSettings.setValue("exifRotationEnabled", True)
            g.GData.appSettings.setValue("referseMouseBehavior", False)
            g.GData.appSettings.setValue("showHiddenFiles", False)
            g.GData.appSettings.setValue("slideShowDelay", 5)
            g.GData.appSettings.setValue("slideShowRandom", False)
            g.GData.appSettings.setValue("editToolBarVisible", True)
            g.GData.appSettings.setValue("goToolBarVisible", True)
            g.GData.appSettings.setValue("viewToolBarVisible", True)
            g.GData.appSettings.setValue("imageToolBarVisible", False)
            g.GData.appSettings.setValue("fsDockVisible", True)
            g.GData.appSettings.setValue("bmDockVisible", True)
            g.GData.appSettings.setValue("iiDockVisible", True)
            g.GData.appSettings.setValue("pvDockVisible", False)
            g.GData.appSettings.setValue("enableImageInfoFS", False)
            g.GData.appSettings.setValue("showLabels", True)
            g.GData.appSettings.setValue("smallIcons", False)
            g.GData.appSettings.setValue("LockDocks", True)
            g.GData.appSettings.setValue("imageToolbarFullScreen", False)
            #g.GData.bookmarkPaths.insert(QtCore.QDir.homePath())

        logging.debug("store loaded setting in memory")
        g.GData.backgroundColor = QtGui.QColor(g.GData.appSettings.value("backgroundColor"))
        #logging.info("Background Color: "+str(g.GData.backgroundColor))
        g.GData.exitInsteadofClose = g.GData.appSettings.value("exitInsteadOfClose").toBool()
        #logging.info("Exit instead of Close: "+str(g.GData.exitInsteadofClose))
        g.GData.enableAnimations = g.GData.appSettings.value("enableAnimations").toBool()
        #logging.info("Enable Animations: "+str(g.GData.enableAnimations))
        g.GData.exifRotationEnabled = g.GData.appSettings.value("exifRotationEnabled").toBool()
        #logging.info("Exif Rotations Enabled: "+str(g.GData.exifRotationEnabled))
        g.GData.exifThumbRotationEnabled = g.GData.appSettings.value("exifThumbRotationEnabled").toBool()
        #logging.info("Exif Thumbnail Rotations Enabled: "+str(g.GData.exifThumbRotationEnabled))
        g.GData.reverseMouseBehavior = g.GData.appSettings.value("reverseMouseBehavior").toBool()
        #logging.info("Reverse Mouse Behavior: "+str(g.GData.reverseMouseBehavior))
        g.GData.showHiddenFiles = g.GData.appSettings.value("showHiddenFiles").toBool()
        #logging.info("Showing Hidden Files: "+str(g.GData.showHiddenFiles))
        g.GData.wrapImageList = g.GData.appSettings.value("wrapImageList").toBool()
        #logging.info("Wrap Image List: "+str(g.GData.wrapImageList))
        trashf = g.GData.appSettings.value("imageZoomFactor").toFloat()
        g.GData.imageZoomFactor = trashf[0]
        #logging.info("Image Zoom Factor: "+str(g.GData.imageZoomFactor))
        trashi = g.GData.appSettings.value("zoomOutFlags").toInt()
        g.GData.zoomOutFlags = trashi[0]
        #logging.info("Zoom Out Flags: "+str(g.GData.zoomOutFlags))
        trashi = g.GData.appSettings.value("zoomInFlags").toInt()
        g.GData.zoomInFlags = trashi[0]
        #logging.info("Zoom In Flags: "+str(g.GData.zoomInFlags))
        g.GData.rotation = 0
        g.GData.keepTransform = False
        self.shouldMaximize = g.GData.appSettings.value("shouldMaximize").toBool()
        #logging.info("Should Maximize: "+str(self.shouldMaximize))
        g.GData.flipH = False
        g.GData.flipV = False
        trashi =  g.GData.appSettings.value("defaultSaveQuality").toInt()
        g.GData.defaultSaveQuality = trashi[0]
        #logging.info("Default Image Save Quality: "+str(g.GData.defaultSaveQuality))
        g.GData.noEnlargeSmallThumbs = g.GData.appSettings.value("noEnlargeSmallThumb").toBool()
        #logging.info("No Enlarge Small Thumb: "+str(g.GData.noEnlargeSmallThumbs))
        trashi = g.GData.appSettings.value("slideShowDelay").toInt()
        g.GData.slideShowDelay = trashi[0]
        #logging.info("Slide Show Delay: "+str(g.GData.slideShowDelay))
        g.GData.slideShowRandom = g.GData.appSettings.value("slideShowRandom").toBool()
        #logging.info("Slide Show Random: "+str(g.GData.slideShowRandom))
        g.GData.slideShowActive = False
        #logging.info("Slide Show Active: "+str(g.GData.slideShowActive))
        self.editToolbarVisible = g.GData.appSettings.value("editToolBarVisible").toBool()
        #logging.info("Edit ToolBar Visible: "+str(self.editToolbarVisible))
        self.goToolBarVisible = g.GData.appSettings.value("goToolBarVisible").toBool()
        #logging.info("Go ToolBar Visible: "+str(self.goToolBarVisible))
        self.viewToolBarVisible = g.GData.appSettings.value("viewToolBarVisible").toBool()
        #logging.info("View ToolBar Visible: "+str(self.viewToolBarVisible))
        self.imageToolBarVisible = g.GData.appSettings.value("imageToolBarVisible").toBool()
        #logging.info("Image ToolBar Visible: "+str(self.imageToolBarVisible))
        g.GData.fsDockVisible = g.GData.appSettings.value("fsDockVisible").toBool()
        #logging.info("Fs Dock Visible: "+str(g.GData.fsDockVisible))
        g.GData.bmDockVisible = g.GData.appSettings.value("bmDockVisible").toBool()
        #logging.info("Bm Dock Visible: "+str(g.GData.bmDockVisible))
        g.GData.iiDockVisible = g.GData.appSettings.value("iiDockVisible").toBool()
        #logging.info("Ii Dock Visible: "+str(g.GData.iiDockVisible))
        g.GData.pvDockVisible = g.GData.appSettings.value("pvDockVisible").toBool()
        #logging.info("Pv Dock Visible: "+str(g.GData.pvDockVisible))
        trashi = g.GData.appSettings.value("startupDir").toInt()
        g.GData.startupDir = trashi[0]
        #logging.info("Startup Directory: "+str(g.GData.startupDir))
        g.GData.specifiedStartDir = g.GData.appSettings.value("specifiedStartDir").toString()
        #logging.info("specified Start Directory: "+str(g.GData.specifiedStartDir))
        g.GData.thumbsBackImage = g.GData.appSettings.value("thumbsBackImage").toString()
        #logging.info("Thumbs Background Image: "+str(g.GData.thumbsBackImage))
        trashi =  g.GData.appSettings.value("thumbSpacing").toInt()
        g.GData.thumbsSpacing = trashi[0]
        #logging.info("Thumb Spacing: "+ str(g.GData.thumbsSpacing))
        g.GData.enableImageInfoFS = g.GData.appSettings.value("enableImageInfoFS").toBool()
        #logging.info("Enable Image Info Fs: "+str(g.GData.enableImageInfoFS))
        g.GData.showLabels = g.GData.appSettings.value("showLabels").toBool()
        #logging.info("Show Labels: "+str(g.GData.showLabels))
        g.GData.smallIcons = g.GData.appSettings.value("smallIcons").toBool()
        #logging.info("Small Icons: "+str(g.GData.smallIcons))
        g.GData.LockDocks = g.GData.appSettings.value("LockDocks").toBool()
        #logging.info("Lock Docks: "+str(g.GData.LockDocks))
        g.GData.imageToolbarFullScreen = g.GData.appSettings.value("imageToolbarFullScreen").toBool()
        #logging.info("Image Toolbar Full Screen: "+str(g.GData.imageToolbarFullScreen))

        #g.GData.appSettings.beginGroup("externalApps")
        #extApps = g.GData.appSettings.childKeys()
        #i = 0
        #while i < extApps.size():
        #    g.GData.externalApps[extApps.at(i)] = g.GData.appSettings.value(extApps.at(i).toString())
        #    i +=1
        #g.GData.appSettings.endGroup()

        #g.GData.appSettings.beginGroup("CopyMoveToPaths")
        #paths = g.GData.appSettings.childKeys()
        #i = 0
        #while i < paths.size():
        #    g.GData.bookmarkPaths.insert(g.GData.appSettings.value(paths.at(i).toString()))
        #    i +=1
        #g.GData.appSettings.endGroup()

        logging.info("settings Read, program continuing")


    def setupDocks(self):
        logging.info("fbWindow.setupDocks()")
        logging.info("setting up the docks")

        self.pvDock = QtGui.QDockWidget("Viewer", self)
        self.pvDock.setObjectName("Viewer")

        self.imageViewContainer = QtGui.QVBoxLayout(self)
        self.imageViewContainer.setContentsMargins(0, 0, 0, 0)
        self.imageViewContainer.addWidget(self.imageView)
        self.imageViewContainerWidget = QtGui.QWidget()
        self.imageViewContainerWidget.setLayout(self.imageViewContainer)

        self.pvDock.setWidget(self.imageViewContainerWidget)
        #self.pvDock.toggleViewAction().triggered.connect(lambda: self.setPvDockVisibility())
        #self.pvDock.visiblityChanged().connect(lambda: self.setPvDockVisibility())
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.pvDock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.iiDock)

        self.fsDockOrigWidget = self.fsDock.titleBarWidget()
        self.bmDockOrigWidget = self.bmDock.titleBarWidget()
        self.iiDockOrigWidget = self.iiDock.titleBarWidget()
        self.pvDockOrigWidget = self.pvDock.titleBarWidget()
        self.fsDockEmptyWidget = QtGui.QWidget()
        self.bmDockEmptyWidget = QtGui.QWidget()
        self.iiDockEmptyWidget = QtGui.QWidget()
        self.pvDockEmptyWidget = QtGui.QWidget()
        self.lockDocks()

        self.setDockOptions(self.AllowNestedDocks)
        logging.info("Dock setup complete loading program window")

    def lockDocks(self):
        print "locking all docked items"

    def createPopupMenu(self):
        print "creating popup menus"

    def loadShortcuts(self):
        print "loading shortcuts"

    def closeEvent(self, event):
        logging.info("close Event")
        self.thumbView.abort()
        self.writeSettings()

        event.accept()

    def setStatus(self):
        print "setting Status"

    def mouseDoubleClickEvent(self, event):
        print "mouse has been double clicked"

    def mousePressEvent(self, event):
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
        #QtCore.QTimer.singleShot(0,self.reloadThumbsSlot())
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

    def wheelEvent(self, event):
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

    def setInterfaceEnabled(self, enable):
        logging.info("setting the interface to enabled")

        ## Actions
        self.colorsAct.setEnabled(enable)

    def addNewBookmark(self):
        logging.info("fbWindow.addNewBookmark()")
        logging.info("getting selected path and calling addBookmark()")

        self.addBookmark(self.getSelectedPath())

    def addBookmark(self, path):
        logging.info("fbWindow.addBookmark()")
        logging.info("adding bookmark for: %s, to global data"% path)
        g.GData.bookmarkPaths.append(path)
        logging.info("Reloading bookmarks window")
        self.bookmarks.reloadBookmarks()


    def findDuplicateImages(self):
        print "finding duplicate Images"

def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()