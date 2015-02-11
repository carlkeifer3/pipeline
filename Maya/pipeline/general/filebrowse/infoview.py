"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore


class InfoView(QtGui.QWidget):

    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self,parent)
        logging.info("InfoView Class instantiated")

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(self.verticalHeader().minimumSectionSize())
        self.horizontalHeader().setVisible(False)
        #self.horizontalHeader().setSectionResizeMode()
        self.setShowGrid(False)



        self.infoModel = QtGui.QStandardItemModel(self)
        self.setModel(self.infoModel)


        logging.info("InfoView Class Init complete")