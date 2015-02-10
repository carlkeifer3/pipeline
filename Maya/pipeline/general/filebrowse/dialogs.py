"""

__author__ = 'cargoyle'

"""
import logging
from PyQt4 import QtGui, QtCore
import pipeline.general.filebrowse.GData as g

class settingsDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        # initialize the QlistView
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Preferences")

        ## Image Viewer Options
        ## Zoom Large Images
        self.fitLargeGroupBox = QtGui.QGroupBox("Fit Large Images")
        self.fitLargeRadios = []
        self.fitLargeRadios.append(QtGui.QRadioButton("Disable"))
        self.fitLargeRadios.append(QtGui.QRadioButton("By width and height"))
        self.fitLargeRadios.append(QtGui.QRadioButton("By width"))
        self.fitLargeRadios.append(QtGui.QRadioButton("By height"))
        self.fitLargeRadios.append(QtGui.QRadioButton("Stretch disproportionately"))

        self.fitLargeVbox = QtGui.QVBoxLayout()
        for radio in self.fitLargeRadios:
            self.fitLargeVbox.addWidget(radio)
            radio.setChecked(False)

        self.fitLargeVbox.addStretch(1)
        self.fitLargeGroupBox.setLayout(self.fitLargeVbox)
        self.fitLargeRadios[g.GData.zoomOutFlags].setChecked(True)

        ## Zoom small images
        self.fitSmallGroupBox = QtGui.QGroupBox("Fit Small Images")
        self.fitSmallRadios = []
        self.fitSmallRadios.append(QtGui.QRadioButton("Disable"))
        self.fitSmallRadios.append(QtGui.QRadioButton("By width and height"))
        self.fitSmallRadios.append(QtGui.QRadioButton("By width"))
        self.fitSmallRadios.append(QtGui.QRadioButton("By height"))
        self.fitSmallRadios.append(QtGui.QRadioButton("Stretch disproportionately"))
        self.fitSmallVbox = QtGui.QVBoxLayout()
        for radio in self.fitSmallRadios:
            self.fitSmallVbox.addWidget(radio)
            radio.setChecked(False)

        self.fitSmallVbox.addStretch(1)
        self.fitSmallGroupBox.setLayout(self.fitSmallVbox)
        self.fitSmallRadios[g.GData.zoomInFlags].setChecked(True)

        ## ImageView background color
        self.backgroundColorLab = QtGui.QLabel("Background color: ")
        self.backgroundColorButton = QtGui.QToolButton()
        self.backgroundColorButton.setFixedSize(48,24)
        self.bgColBox = QtGui.QHBoxLayout()
        self.bgColBox.addWidget(self.backgroundColorLab)
        self.bgColBox.addWidget(self.backgroundColorButton)
        self.bgColBox.addStretch(1)
        self.backgroundColorButton.clicked.connect(lambda: self.pickColor())
        self.setButtonBgColor(g.GData.backgroundColor, self.backgroundColorButton)
        self.backgroundColorButton.setAutoFillBackground(True)
        self.bgColor = g.GData.backgroundColor

        ## Exit when opening image
        self.exitCliCb = QtGui.QCheckBox("Exit instead of closing, when image is loaded from the command line")
        self.exitCliCb.setChecked(g.GData.exitInsteadofClose)

        ## Wrap image list
        self.wrapListCb = QtGui.QCheckBox("Wrap image list when reachin last or first image")
        self.wrapListCb.setChecked(g.GData.wrapImageList)

        ## Save Quality
        self.saveQualityLab = QtGui.QLabel("Default quality when saving images: ")
        self.saveQualitySpin = QtGui.QSpinBox()
        self.saveQualitySpin.setRange(0, 100)
        self.saveQualitySpin.setValue(g.GData.defaultSaveQuality)
        self.saveQualityHbox = QtGui.QHBoxLayout()
        self.saveQualityHbox.addWidget(self.saveQualityLab)
        self.saveQualityHbox.addWidget(self.saveQualitySpin)
        self.saveQualityHbox.addStretch(1)

        ## Enable Animations
        self.enableAnimCb = QtGui.QCheckBox("Enable GIF animation")
        self.enableAnimCb.setChecked(g.GData.enableAnimations)

        ## Enable image Exif rotation
        self.enableExifCb = QtGui.QCheckBox("Rotate image according to Exif orientation")
        self.enableExifCb.setChecked(g.GData.exifRotationEnabled)

        ## Image Info
        self.imageInfoCb = QtGui.QCheckBox("Show image file name in full screen mode")
        self.imageInfoCb.setChecked(g.GData.enableImageInfoFS)

        ## Viewer options
        self.viewerOptsBox = QtGui.QVBoxLayout()
        self.zoomOptsBox = QtGui.QHBoxLayout()
        self.zoomOptsBox.setAlignment(QtCore.Qt.AlignTop)
        self.zoomOptsBox.addWidget(self.fitLargeGroupBox)
        self.zoomOptsBox.addWidget(self.fitSmallGroupBox)
        self.zoomOptsBox.addStretch(1)

        self.viewerOptsBox.addLayout(self.zoomOptsBox)
        self.viewerOptsBox.addLayout(self.bgColBox)
        self.viewerOptsBox.addWidget(self.enableExifCb)
        self.viewerOptsBox.addWidget(self.imageInfoCb)
        self.viewerOptsBox.addWidget(self.wrapListCb)
        self.viewerOptsBox.addWidget(self.enableAnimCb)
        self.viewerOptsBox.addLayout(self.saveQualityHbox)
        self.viewerOptsBox.addWidget(self.exitCliCb)
        self.viewerOptsBox.addStretch(1)

        ## thumbView background color
        self.bgThumbTxtLab = QtGui.QLabel("Background color: ")
        self.colThumbButton = QtGui.QToolButton()
        self.colThumbButton.setFixedSize( 48, 24)
        self.bgThumbColBox = QtGui.QHBoxLayout()
        self.bgThumbColBox.addWidget(self.bgThumbTxtLab)
        self.bgThumbColBox.addWidget(self.colThumbButton)
        self.colThumbButton.clicked.connect(lambda: self.pickThumbsColor())
        self.setButtonBgColor(g.GData.thumbsBackgroundColor, self.colThumbButton)
        self.colThumbButton.setAutoFillBackground(True)
        self.thumbBgColor = g.GData.thumbsBackgroundColor

        ## thumbview text color
        self.txtThumbTxtLab = QtGui.QLabel("\tLabel color: ")
        self.colThumbTextButton = QtGui.QToolButton()
        self.colThumbTextButton.setFixedSize( 48, 24)
        self.bgThumbColBox.addWidget(self.txtThumbTxtLab)
        self.bgThumbColBox.addWidget(self.colThumbTextButton)
        self.bgThumbColBox.addStretch(1)
        self.colThumbTextButton.clicked.connect(lambda: self.pickThumbsTextColor())
        self.setButtonBgColor(g.GData.thumbsTextColor, self.colThumbTextButton)
        self.colThumbTextButton.setAutoFillBackground(True)
        self.thumbTextColor = g.GData.thumbsTextColor

        ## thumbview background image
        self.thumbsBackImageLab = QtGui.QLabel("Background Image: ")
        self.thumbsBackImageEdit = QtGui.QLineEdit()
        #self.thumbsBackImageEdit.setClearButtonEnabled(True)

        self.chooseThumbsBackImageButton = QtGui.QToolButton()
        #self.chooseThumbsBackImageButton.setIcon(QtCore.QIcon.fromTheme("document-open", QtCore.QIcon(":/images/open.png")))
        self.chooseThumbsBackImageButton.setFixedSize( 26, 26)
        self.chooseThumbsBackImageButton.setIconSize( QtCore.QSize(16, 16))
        #self.chooseThumbsBackImageButton.clicked.connect(self.pickBgImage)

        self.thumbsBackImageEditBox = QtGui.QHBoxLayout()
        self.thumbsBackImageEditBox.addWidget(self.thumbsBackImageLab)
        self.thumbsBackImageEditBox.addWidget(self.thumbsBackImageEdit)
        self.thumbsBackImageEditBox.addWidget(self.chooseThumbsBackImageButton)
        self.thumbsBackImageEditBox.addStretch(1)
        self.thumbsBackImageEdit.setText(g.GData.thumbsBackImage)

        ## thumbnail spacing
        self.thumbSpacingLab = QtGui.QLabel("Add space between thumbnails: ")
        self.thumbSpacingSpin = QtGui.QSpinBox()
        self.thumbSpacingSpin.setRange(0, 15)
        #logging.info("Thumbnail Spacing will be set to: "+str(g.GData.thumbsSpacing))
        self.thumbSpacingSpin.setValue(g.GData.thumbsSpacing)
        self.thumbSpacingHbox = QtGui.QHBoxLayout()
        self.thumbSpacingHbox.addWidget(self.thumbSpacingLab)
        self.thumbSpacingHbox.addWidget(self.thumbSpacingSpin)
        self.thumbSpacingHbox.addStretch(1)

        ## Do not enlarge small thumbs
        self.noSmallThumbCb = QtGui.QCheckBox("Show original size of images smaller than the thumbnail size")
        self.noSmallThumbCb.setChecked(g.GData.noEnlargeSmallThumbs)

        ##thumbnail pages to read ahead
        self.thumbPagesLab = QtGui.QLabel("Number of thumbnail pages to read ahead: ")
        self.thumbPagesSpin = QtGui.QSpinBox()
        self.thumbPagesSpin.setRange(1, 10)
        self.thumbPagesSpin.setValue(g.GData.thumbPagesReadahead)
        self.thumbPagesHbox = QtGui.QHBoxLayout()
        self.thumbPagesHbox.addWidget(self.thumbPagesLab)
        self.thumbPagesHbox.addWidget(self.thumbPagesSpin)
        self.thumbSpacingHbox.addStretch(1)

        self.enableExifCb = QtGui.QCheckBox("Rotate thumbnails according to Exif orientation")
        self.enableExifCb.setChecked(g.GData.exifRotationEnabled)

        ## Thumbnail options
        self.thumbsOptBox = QtGui.QVBoxLayout()
        self.thumbsOptBox.addLayout(self.bgThumbColBox)
        self.thumbsOptBox.addWidget(self.thumbsBackImageEdit)
        self.thumbsOptBox.addLayout(self.thumbSpacingHbox)
        #self.thumbsOptBox.addWidget(self.enableThumbExifCb)
        self.thumbsOptBox.addLayout(self.thumbPagesHbox)
        self.thumbsOptBox.addWidget(self.noSmallThumbCb)
        self.thumbsOptBox.addStretch(1)

        ## Slide show delay
        self.slideDelayLab = QtGui.QLabel("Delay Between slides in seconds: ")
        self.slideDelaySpin = QtGui.QSpinBox()
        self.slideDelaySpin.setRange(1, 3600)
        self.slideDelaySpin.setValue(g.GData.slideShowDelay)
        self.slideDelayHbox = QtGui.QHBoxLayout()
        self.slideDelayHbox.addWidget(self.slideDelayLab)
        self.slideDelayHbox.addWidget(self.slideDelaySpin)
        self.slideDelayHbox.addStretch(1)

        ## Slide Show Random
        self.slideRandomCb = QtGui.QCheckBox("Show random images")
        self.slideRandomCb.setChecked(g.GData.slideShowRandom)

        ## Slide Show options
        self.slideShowVbox = QtGui.QVBoxLayout()
        self.slideShowVbox.addLayout(self.slideDelayHbox)
        self.slideShowVbox.addWidget(self.slideRandomCb)
        self.slideShowVbox.addStretch(1)

        ## Startup Directory
        self.startupDirGroupBox = QtGui.QGroupBox("Startup Folder")
        self.startupDirRadios = []
        self.startupDirRadios.append(QtGui.QRadioButton("Default, or Specified by command line argument."))
        self.startupDirRadios.append(QtGui.QRadioButton("Remember last"))
        self.startupDirRadios.append(QtGui.QRadioButton("Specify:"))

        self.startupDirEdit = QtGui.QLineEdit()
        self.startupDirEdit.setClearButtonEnabled = True
        self.startupDirEdit.setMinimumWidth(300)
        self.startupDirEdit.setMaximumWidth(400)

        self.chooseStartupDirButton = QtGui.QToolButton()
        self.chooseStartupDirButton.setIcon(QtGui.QIcon.fromTheme("document-open", QtGui.QIcon(":/images/open.png")))
        self.chooseStartupDirButton.setFixedSize(26, 26)
        self.chooseStartupDirButton.setIconSize(QtCore.QSize(16, 16))
        self.chooseStartupDirButton.clicked.connect(lambda: self.pickStartupDir())

        self.startupDirEditBox = QtGui.QHBoxLayout()
        self.startupDirEditBox.addWidget(self.startupDirRadios[2])
        self.startupDirEditBox.addWidget(self.startupDirEdit)
        self.startupDirEditBox.addWidget(self.chooseStartupDirButton)
        self.startupDirEditBox.addStretch(1)

        self.startupDirVbox = QtGui.QVBoxLayout()
        for radio in self.startupDirRadios:
            self.startupDirVbox.addWidget(radio)
            radio.setChecked(False)

        self.startupDirVbox.addLayout(self.startupDirEditBox)
        self.startupDirVbox.addStretch(1)
        self.startupDirGroupBox.setLayout(self.startupDirVbox)
        #if g.GData.startupDir == g.GData.specifiedStartDir:

        self.startupDirEdit.setText(g.GData.specifiedStartDir)

        ## Keyboard shortcuts widgets
        self.keysCombo = QtGui.QComboBox()
        #self.keyLine = QtGui.keyGrabLineEdit(self.keysCombo)
        #self.keyLine.textChanged.connect()

        ## Mouse settings
        self.reverseMouseCb = QtGui.QCheckBox("Swap mouse left-click and middle-click actions")
        self.reverseMouseCb.setChecked(g.GData.reverseMouseBehavior)

        ## Keyboard and mouse
        self.keyboardGrp = QtGui.QGroupBox("Keyboard Shortcuts")
        self.keyboardHbox = QtGui.QHBoxLayout()
        self.keyboardHbox.addWidget(self.keysCombo)
        #self.keyboardHbox.addWidget(self.keyLine)
        self.keyboardHbox.addStretch(1)
        self.keyboardGrp.setLayout(self.keyboardHbox)

        self.generalVbox = QtGui.QVBoxLayout()
        self.generalVbox.addWidget(self.keyboardGrp)
        self.generalVbox.addWidget(self.reverseMouseCb)
        self.generalVbox.addWidget(self.startupDirGroupBox)

        ## Confirmation buttons
        self.buttonsHbox = QtGui.QHBoxLayout()
        self.okButton = QtGui.QPushButton("OK!")
        #self.okButton.setIcon(QtCore.QIcon.fromTheme("dialog-ok"))
        #self.okButton.setSizePolicy(QtCore.QSize.QSizePolicy.fixed, QtCore.QSize.QSizePolicy.fixed)
        self.okButton.clicked.connect(lambda: self.saveSettings())
        self.closeButton = QtGui.QPushButton("Cancel")
        #self.closeButton.setIcon(QtCore.QIcon.fromTheme("dialog-cancel"))
        #self.closeButton.setSizePolicy(QtCore.QSizePolicy.fixed, QtCore.QSizePolicy.fixed)
        self.closeButton.clicked.connect(lambda: self.abort())
        self.buttonsHbox.addWidget(self.closeButton, 1, QtCore.Qt.AlignRight)
        self.buttonsHbox.addWidget(self.okButton, 0, QtCore.Qt.AlignRight)

        ## Tabs
        self.tabs = QtGui.QTabWidget()

        self.viewerSettings = QtGui.QWidget()
        self.viewerSettings.setLayout(self.viewerOptsBox)
        self.tabs.addTab(self.viewerSettings, "Viewer")

        self.thumbSettings = QtGui.QWidget()
        self.thumbSettings.setLayout(self.thumbsOptBox)
        self.tabs.addTab(self.thumbSettings, "thumbnails")

        self.slideSettings = QtGui.QWidget()
        self.slideSettings.setLayout(self.slideShowVbox)
        self.tabs.addTab(self.slideSettings, "Slide Show")

        self.generalSettings = QtGui.QWidget()
        self.generalSettings.setLayout(self.generalVbox)
        self.tabs.addTab(self.generalSettings, "General")

        self.mainVbox = QtGui.QVBoxLayout()
        self.mainVbox.addWidget(self.tabs)
        self.mainVbox.addLayout(self.buttonsHbox)
        self.setLayout(self.mainVbox)
        self.show()

        logging.info("Preferences window initialized")

    def saveSettings(self):
        logging.info("OK clicked, writing settings to GData")

        for radio in self.fitLargeRadios:
            if radio.isChecked():
                g.GData.appSettings.setValue("zoomOutFlags", g.GData.zoomOutFlags)

        for radio in self.fitSmallRadios:
            if radio.isChecked():
                g.GData.appSettings.setValue("zoomInFlags", g.GData.zoomInFlags)

        g.GData.backgroundColor = self.bgColor
        g.GData.thumbsBackgroundColor = self.thumbBgColor
        g.GData.thumbsTextColor = self.thumbTextColor
        g.GData.thumbsBackImage = self.thumbsBackImageEdit.text()
        g.GData.thumbsSpacing = self.thumbSpacingSpin.value()
        logging.info("Thumbnail Spacing: " + str(g.GData.thumbsSpacing))
        g.GData.thumbPagesReadahead = self.thumbPagesSpin.value()
        g.GData.exitInsteadofClose = self.exitCliCb.isChecked()
        g.GData.wrapImageList = self.wrapListCb.isChecked()
        g.GData.defaultSaveQuality = self.saveQualitySpin.value()
        g.GData.slideShowDelay = self.slideDelaySpin.value()
        g.GData.slideShowRandom = self.slideRandomCb.isChecked()
        g.GData.enableAnimations = self.enableAnimCb.isChecked()
        g.GData.exifRotationEnabled = self.enableExifCb.isChecked()
        g.GData.reverseMouseBehavior = self.reverseMouseCb.isChecked()

        if self.startupDirRadios[0].isChecked():
            g.GData.startupDir = g.GData.defaultDir
        elif self.startupDirRadios[1].isChecked():
            g.GData.startupDir = g.GData.rememberLastDir
        else:
            g.GData.startupDir = g.GData.specifiedStartDir
            g.GData.specifiedStartDir = self.startupDirEdit.text()


        self.accept()
        logging.info("Settings Written, continuing")

    def abort(self):
        logging.info("Cancel clicked, aborting preferences window")
        self.reject()

    def pickColor(self):
        logging.info("Pick Bg color clicked, selecting color swatch for background Color")
        userColor = QtGui.QColorDialog.getColor(g.GData.backgroundColor)
        if userColor.isValid():
            self.setButtonBgColor(userColor, self.backgroundColorButton)
            self.bgColor = userColor

    def setButtonBgColor(self, color, button):
        logging.info("Setting buttons background color")
        style = "background: rgb(%i, %i, %i)" % (color.red(), color.green(), color.blue())
        button.setStyleSheet(style)

    def pickThumbsColor(self):
        logging.info("Picking the Thumb Color")
        userColor = QtGui.QColorDialog.getColor(g.GData.thumbsBackgroundColor)
        if userColor.isValid():
            self.setButtonBgColor(userColor, self.colThumbButton)
            self.thumbBgColor = userColor

    def pickThumbsTextColor(self):
        logging.info("Picking the thumbs text color")
        userColor = QtGui.QColorDialog.getColor(g.GData.thumbsTextColor)
        if userColor.isValid():
            self.setButtonBgColor(userColor, self.colThumbTextButton)
            self.thumbTextColor = userColor

    def pickStartupDir(self):
        logging.info("pick Startup Directory")
        dirName = QtGui.QFileDialog.getExistingDirectory(caption="Choose a startup folder", directory="", options=QtGui.QFileDialog.ShowDirsOnly)
        self.startupDirEdit.setText(dirName)