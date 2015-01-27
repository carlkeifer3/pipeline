"""

__author__ = 'cargoyle'

"""
from PyQt4 import QtGui, QtCore

class GData():
    appSettings = QtCore.QSettings()
    layoutMode = 0
    zoomInFlags = 0
    zoomOutFlags = 0
    backgroundColor = QtGui.QColor()
    thumbsBackgroundColor = QtGui.QColor()
    thumbsTextColor = QtGui.QColor()
    thumbsLayout = 0
    thumbsSpacing = 0
    thumbPagesReadahead = 0
    exitInsteadofClose = False
    wrapImageList = False
    enableAnimations = False
    imageZoomFactor = 0.0
    keepZoomFactor = False
    rotation = 0
    keepTransform = False
    flipH = False
    flipV = False
    scaledWidth = 0
    scaledHeight = 0
    defaultSaveQuality = 0
    cropLeft = 0
    cropTop = 0
    cropWidth = 0
    cropHeight = 0
    cropLeftPercent = 0
    cropTopPercent = 0
    cropWidthPercent = 0
    cropHeightPercent = 0
    noEnlargeSmallThumbs = False
    slideShowDelay = 0
    slideShowRandom = False
    slideShowActive = False
    actionKeys = QtCore.QMap()
    hueVal = 0
    saturationVal = 0
    lightnessVal = 0
    contrastVal = 0
    brightVal = 0
    redVal = 0
    greenVal = 0
    blueVal = 0
    colorsActive = True
    colorizeEnabled = False
    hueRedChannel = True
    hueGreenChannel = True
    hueBlueChannel = True
    exifRotationEnabled = False
    exifThumbRotationEnabled = False
    includeSubFolders = False
    showHiddenFiles = False
    imageToolbarFullScreen = False
    externalApps = QtCore.QMap()
    bookmarkPaths = QtCore.QSet()
    reverseMouseBehavior = False
    copyCutIdxList = QtCore.QStringList()
    copyOp = False
    copyCutFileList = QtCore.QStringList()
    isFullScreen = False
    dialogLastX = 0
    dialogLastY = 0
    # I don't know what this is.
    #startupDir StartupDir
    specifiedStartDir = QtCore.QString()
    enableImageInfoFS = False
    showLabels = False
    smallIcons = False
    LockDocks = False
    fsDockVisible = True
    bmDockVisible = True
    iiDockVisible = True
    pvDockVisible = False
    ivDockVisible = False
    thumbsBackImage = QtCore.QString()

