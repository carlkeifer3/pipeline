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

        # initialize the QWidget
        QtGui.QWidget.__init__(self, parent)

        # this is just for now, I want to use QDirectory
        # preferred image locations like this will be
        # captured in qsettings
        self.path = "D:/bank/reference/"
        self.directory = os.listdir(self.path)

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

        # create our views
        self.createThumbView()
        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.list = QtGui.QListWidget(self)
        self.list.setGeometry(QtCore.QRect(0, 70, 240, 370))
        for image in self.directory:
            self.list.addItem(str(self.path + image))

        self.fbLayout.addWidget(self.list)

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
        directory = "C:/Users/cargoyle/Documents/maya/scripts/pipeline/general/filebrowse"

        self.thumbsZoomInAct = QtGui.QAction("Enlarge Thumbnails", self)
        self.thumbsZoomInAct.setIcon(QtGui.QIcon(str(directory+"/images/zoom_in.png")))

        self.thumbsZoomOutAct = QtGui.QAction("Shrink Thumbnails", self)
        self.thumbsZoomOutAct.setIcon(QtGui.QIcon(str(directory+"/images/zoom_out.png")))

        self.cutAction = QtGui.QAction("Cut", self)
        self.cutAction.setIcon(QtGui.QIcon(str(directory+"/images/cut.png")))

        self.copyAction = QtGui.QAction("Copy", self)
        self.copyAction.setIcon(QtGui.QIcon(str(directory+"/images/copy.png")))


        self.deleteAction = QtGui.QAction("Delete", self)
        self.deleteAction.setIcon(QtGui.QIcon(str(directory+"/images/delete.png")))

        self.refreshAction = QtGui.QAction("Reload", self)
        self.refreshAction.setIcon(QtGui.QIcon(str(directory+"/images/refresh.png")))

        self.subFoldersAction = QtGui.QAction("Include Sub-Folders", self)
        self.subFoldersAction.setIcon(QtGui.QIcon(str(directory+"/images/tree.png")))

        self.pasteAction = QtGui.QAction("Paste Here", self)
        self.pasteAction.setIcon(QtGui.QIcon(str(directory+"/images/paste.png")))

        self.goBackAction = QtGui.QAction("Back", self)
        self.goBackAction.setIcon(QtGui.QIcon(str(directory+"/images/back.png")))

        self.goFrwdAction = QtGui.QAction("Forward", self)
        self.goFrwdAction.setIcon(QtGui.QIcon(str(directory+"/images/next.png")))

        self.goUpAction = QtGui.QAction("Up", self)
        self.goUpAction.setIcon(QtGui.QIcon(str(directory+"/images/up.png")))

        self.goHomeAction = QtGui.QAction("Home", self)
        self.goHomeAction.setIcon(QtGui.QIcon(str(directory+"/images/home.png")))

        self.slideShowAction = QtGui.QAction("Slide Show", self)
        self.slideShowAction.setIcon(QtGui.QIcon(str(directory+"/images/play.png")))

        self.showClipboardAction = QtGui.QAction("Load Clipboard", self)
        self.showClipboardAction.setIcon(QtGui.QIcon(str(directory+"/images/new.png")))

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

def fbWinInit():
    myWindow = fbWindow()
    myWindow.show()