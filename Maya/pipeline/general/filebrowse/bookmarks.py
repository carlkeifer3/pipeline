"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class BookMarks(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        import os
        import pymel.core as pm

        # initialize the QlistView
        QtGui.QTreeWidget.__init__(self, parent)

        self.GData = g.GData()

        #locate the directory where all of the images for the UI live
        ScriptDir = pm.internalVar(uad = True)
        self.imgDirectory = str(ScriptDir+"/scripts/pipeline/general/filebrowse/images/")

        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setDragDropMode(QtGui.QAbstractItemView.DropOnly)