"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as G

class settingsDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        # initialize the QlistView
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Preferences")

        self.GData = g.GData()

        ## Image Viewer Options
        ## Zoom Large Images
        self.fitLargeGroupBox = QtGui.QGroupBox("Fit Large Images")
        self.fitLargeRadios = []
        self.fitLargeRadios.append(QtGui.QRadioButton("Disable"))
        self.fitLargeRadios.append(QtGui.QRadioButton("By width and height"))
        self.fitLargeRadios.append(QtGui.QRadioButton("By width"))
        self.fitLargeRadios.append(QtGui.QRadioButton("By height"))
        self.fitLargeVbox = QtGui.QVBoxLayout()
        for radio in self.fitLargeRadios:
            self.fitLargeVbox.addWidget(radio)
            radio.setChecked(False)

        self.fitLargeVbox.addStretch(1)
        self.fitLargeGroupBox.setLayout(self.fitLargeVbox)
        self.fitLargeRadios[self.GData.zoomOutFlags].setChecked(True)

