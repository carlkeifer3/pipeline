"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class multiFileView(QtGui.QListView):

    def __init__(self, parent=None):

        #logging.debug("initialize the QlistView")
        QtGui.QListView.__init__(self, parent)

        self.r = g.UserRoles()

        g.GData.thumbsBackgroundColor = QtGui.QColor(g.GData.appSettings.value("backgroundThumbColor"))
        g.GData.thumbsTextColor = QtGui.QColor(g.GData.appSettings.value("textThumbColor"))

        # setting up the list view to display icons nicely
        self.setViewMode(QtGui.QListView.IconMode)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setFixedSize(800, 100)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.thumbModel = QtGui.QStandardItemModel(self)
        #self.thumbViewModel.setSortRole()
        self.setModel(self.thumbModel)

        self.setFileViewColors()


    def setFileViewColors(self):
        #logging.info("multiFileView.setFileViewColors()")
        color = g.GData.thumbsBackgroundColor
        self.bgColor = QtCore.QString("background-color: rgb(%i, %i, %i)" % (color.red(), color.green(), color.blue()))

        self.setStyleSheet(self.bgColor)