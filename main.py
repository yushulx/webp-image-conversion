#!/usr/bin/env python3

import sys
from PySide2.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog
from PySide2.QtCore import QFile, QTimer, QEvent
from PySide2.QtWidgets import *
from design import Ui_MainWindow

import os
import cv2

from PySide2.QtCore import QObject, QThread, Signal

class MainWindow(QMainWindow):

    def __init__(self, license):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        
        # Initialization
        self._all_images = {}
        self._all_webps = {}
        self.current_file = None
        self._pixmap = None
        self._path = os.path.dirname(os.path.realpath(__file__))

        self.ui.actionOpen_File.triggered.connect(self.openFile)
        self.ui.actionOpen_Folder.triggered.connect(self.openFolder)
        self.ui.horizontalSlider.valueChanged.connect(self.onSliderChanged)
        self.ui.pushButton.clicked.connect(self.convertOne)
        self.ui.pushButton_all.clicked.connect(self.convertAll)
        self.ui.listWidget.currentItemChanged.connect(self.currentItemChanged)

    def convert(self, filename):
        if (filename is None):
            return
        else:
            if not filename.endswith('.web'):
                frame = cv2.imread(filename)
                webp_file = filename.split('.')[0] + '.webp'
                self.addImage(webp_file)
                quality = int(self.ui.label_slider.text())
                cv2.imwrite(webp_file, frame, [cv2.IMWRITE_WEBP_QUALITY, quality])

    def convertAll(self):
        if (self.current_file is None):
            self.showMessageBox('Error', "No item selected")
        else:
            for filename in self._all_images:
                self.convert(filename)

            self.showMessageBox('WebP Conversion', "Done!")

    def convertOne(self):
        if (self.current_file is None):
            self.showMessageBox('Error', "No item selected")
            return False
        else:
            self.convert(self.current_file)
            self.showMessageBox('WebP Conversion', "Done!")
            

    def onSliderChanged(self):
        self.ui.label_slider.setText(str(self.ui.horizontalSlider.value()))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        filename = urls[0].toLocalFile()
        if os.path.isdir(filename):
            self.appendFolder(filename)
        else:
            self.appendFile(filename)
        event.acceptProposedAction()
        self.showImage(self.current_file)

    def addImage(self, filename):
        if filename.endswith('.webp'):
            if filename not in self._all_webps:
                item = QListWidgetItem()
                item.setText(filename)
                self.ui.listWidget.addItem(item)
                self._all_webps[filename] = None
        else:
            if filename not in self._all_images:
                item = QListWidgetItem()
                item.setText(filename)
                self.ui.listWidget.addItem(item)
                self._all_images[filename] = None
            
        self.current_file = filename
        self.ui.statusbar.showMessage(filename)

    def appendFile(self, filename):
        self.addImage(filename)

    def currentItemChanged(self, current, previous):
        filename = current.text()
        self.appendFile(filename)
        self.showImage(self.current_file)

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File',
                                               self._path, "Barcode images (*)")
        if filename is None or filename[0] == '':
            self.showMessageBox('Open File...', "No file selected")
            return

        filename = filename[0]
        self.appendFile(filename)
        self.showImage(self.current_file)

    def appendFolder(self, folder):
        if os.path.isdir(folder):
            files = os.listdir(folder)
            for file in files:
                filepath = os.path.join(folder, file)
                if not os.path.isdir(filepath):
                    self.appendFile(filepath)
                else:
                    self.appendFolder(filepath)
        else:
            self.appendFile(folder)

    def openFolder(self):
        dir = QFileDialog.getExistingDirectory(self, 'Open Folder',
                                               self._path, QFileDialog.ShowDirsOnly)
        if dir is '':
            self.showMessageBox('Open Folder...', "No folder selected")
            return

        self.appendFolder(dir)
        self.showImage(self.current_file)

    def resizeImage(self, pixmap):
        lwidth = self.ui.label.width()
        pwidth = pixmap.width()
        lheight = self.ui.label.height()
        pheight = pixmap.height()

        wratio = pwidth * 1.0 / lwidth
        hratio = pheight * 1.0 / lheight

        if pwidth > lwidth or pheight > lheight:
            if wratio > hratio:
                lheight = pheight / wratio
            else:
                lwidth = pwidth / hratio

            scaled_pixmap = pixmap.scaled(lwidth, lheight)
            return scaled_pixmap
        else:
            return pixmap

    def showImage(self, filename):
        frame = cv2.imread(filename)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self._pixmap = self.resizeImage(pixmap)
        self.ui.label.setPixmap(self._pixmap)
        return frame

    def showMessageBox(self, title, content):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(content)
        msgBox.exec_()

    def closeEvent(self, event):
    
        msg = "Close the app?"
        reply = QMessageBox.question(self, 'Message', 
                        msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    window = MainWindow(license)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()