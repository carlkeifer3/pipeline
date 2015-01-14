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

        self.thumbViewModel = QtGui.QStandardItemModel(self)
