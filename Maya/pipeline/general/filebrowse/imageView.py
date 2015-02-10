"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class ImageView(QtGui.QWidget):

    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)

        self.cursorIsHidden = False
        self.moveImageLocked = False