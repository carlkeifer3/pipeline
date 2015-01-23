"""

__author__ = 'cargoyle'

"""
from PyQt4 import QtGui, QtCore

class BookMarks(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        import os

        # initialize the QlistView
        QtGui.QTreeWidget.__init__(self, parent)

        self.setAcceptDrops(True)