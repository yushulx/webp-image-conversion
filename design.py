# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 989)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1600, 848))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionOpen_File = QAction(MainWindow)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.actionOpen_Folder = QAction(MainWindow)
        self.actionOpen_Folder.setObjectName(u"actionOpen_Folder")
        self.actionExport_template = QAction(MainWindow)
        self.actionExport_template.setObjectName(u"actionExport_template")
        self.actionEnter_License_Key = QAction(MainWindow)
        self.actionEnter_License_Key.setObjectName(u"actionEnter_License_Key")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_barcode = QGroupBox(self.centralwidget)
        self.groupBox_barcode.setObjectName(u"groupBox_barcode")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_barcode.sizePolicy().hasHeightForWidth())
        self.groupBox_barcode.setSizePolicy(sizePolicy2)
        self.groupBox_barcode.setMinimumSize(QSize(400, 220))
        self.groupBox_barcode.setSizeIncrement(QSize(0, 0))
        self.horizontalSlider = QSlider(self.groupBox_barcode)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(20, 90, 371, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.label_2 = QLabel(self.groupBox_barcode)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 10, 131, 71))
        font = QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.pushButton = QPushButton(self.groupBox_barcode)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(60, 150, 111, 51))
        self.label_slider = QLabel(self.groupBox_barcode)
        self.label_slider.setObjectName(u"label_slider")
        self.label_slider.setGeometry(QRect(150, 10, 131, 71))
        self.label_slider.setFont(font)
        self.pushButton_all = QPushButton(self.groupBox_barcode)
        self.pushButton_all.setObjectName(u"pushButton_all")
        self.pushButton_all.setGeometry(QRect(240, 150, 111, 51))

        self.gridLayout.addWidget(self.groupBox_barcode, 0, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        self.label.setMinimumSize(QSize(800, 800))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        self.label.setMouseTracking(True)

        self.gridLayout.addWidget(self.label, 0, 1, 5, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.listWidget = QListWidget(self.groupBox)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 20, 381, 671))
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.groupBox, 1, 2, 4, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1600, 21))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuAbout.addAction(self.actionOpen_File)
        self.menuAbout.addAction(self.actionOpen_Folder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WebP Conversion", None))
#if QT_CONFIG(accessibility)
        MainWindow.setAccessibleName(QCoreApplication.translate("MainWindow", u"WebP Conversion", None))
#endif // QT_CONFIG(accessibility)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionOpen_File.setText(QCoreApplication.translate("MainWindow", u"Open File...", None))
        self.actionOpen_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Folder...", None))
        self.actionExport_template.setText(QCoreApplication.translate("MainWindow", u"Save Template", None))
        self.actionEnter_License_Key.setText(QCoreApplication.translate("MainWindow", u"Enter License Key", None))
        self.groupBox_barcode.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"WebP Quality:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Convert Selected", None))
        self.label_slider.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pushButton_all.setText(QCoreApplication.translate("MainWindow", u"Convert All", None))
        self.label.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

