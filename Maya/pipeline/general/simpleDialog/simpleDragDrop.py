"""

__author__ = 'cargoyle'

"""
import sys
from PyQt4 import QtGui, QtCore

class DragFromWidget(QtGui.QDockWidget):

    def __init__(self, parent=None):
        super(DragFromWidget, self).__init__(parent=parent)
        self.layout().addWidget(QtGui.QLabel("Label!"))

class DragToWidget(QtGui.QDockWidget):

    def __init__(self, parent=None):
        super(DragToWidget, self).__init__(parent=parent)
        self.setAcceptDrops(True)

class SandboxApp(QtGui.QWidget):

    def __init__(self, *args, **kwargs):
        super(SandboxApp, self).__init(*args)
        self.mainWindow = mainWindow()
        self.mainWindow.show()


class mainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent=parent)
        self.setDockOptions(QtGui.QMainWindow.AllowNestedDocks| QtGui.QMainWindow.AnimatedDocks)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, DragFromWidget())
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, DragToWidget())

def main():
    app = SandboxApp(sys.argv)
    sys.exit(app.exec_())