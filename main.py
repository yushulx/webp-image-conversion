#!/usr/bin/env python3

'''
Usage:
   app.py <license.txt>
'''

import sys
from PySide2.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QInputDialog
from PySide2.QtCore import QFile, QTimer, QEvent
from PySide2.QtWidgets import *
from design import Ui_MainWindow

import os
import cv2

from PySide2.QtCore import QObject, QThread, Signal

class Worker(QObject):
    finished = Signal()
    progress = Signal(object)

    def __init__(self, manager, capture):
        super(Worker, self).__init__()
        self._cap = capture
        self.isRunning = True

    def run(self):
        print('Running worker thread...')
        # while self.isRunning:
        #     try:
        #         results = self._barcodeManager.decodeLatestFrame()

        #         if  results != None:
        #             self.progress.emit(results)
        #     except Exception as e:
        #         print(e)
        #         break

        print('Quit worker thread...')
        self.finished.emit()


class MainWindow(QMainWindow):
    useQThread = True
    

    def __init__(self, license):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        
        # Initialization
        self._all_data = {}
        self.current_file = None
        self.frame = None

        # The current path.
        self._path = os.path.dirname(os.path.realpath(__file__))
        
        # Load file
        self.ui.actionOpen_File.triggered.connect(self.openFile)

        # Load directory
        self.ui.actionOpen_Folder.triggered.connect(self.openFolder)

        self.ui.horizontalSlider.valueChanged.connect(self.onSliderChanged)

        self.ui.pushButton.clicked.connect(self.convertOne)
        self.ui.pushButton_2.clicked.connect(self.convertAll)

        ## List widget
        self.ui.listWidget.currentItemChanged.connect(self.currentItemChanged)
        self._pixmap = None


    def convertAll(self):
        if (self.current_file is None):
            self.showMessageBox('Error', "No item selected")
        else:
            # webp_file = self.current_file.split('.')[0] + '.webp'
            # quality = int(self.ui.label_3.text())
            # if not os.path.exists(webp_file):
            #     self.ui.listWidget.addItem(webp_file)

            # cv2.imwrite(webp_file, self.frame, [cv2.IMWRITE_WEBP_QUALITY, quality]) 
            for filename in self._all_data:
                img = cv2.imread(filename)
                webp_file = filename.split('.')[0] + '.webp'
                quality = int(self.ui.label_3.text())
                if not os.path.exists(webp_file):
                    self.ui.listWidget.addItem(webp_file)

                cv2.imwrite(webp_file, img, [cv2.IMWRITE_WEBP_QUALITY, quality])

            self.showMessageBox('WebP Conversion', "Done!")

    def convertOne(self, filename=None):
        if (self.current_file is None):
            self.showMessageBox('Error', "No item selected")
        else:
            webp_file = self.current_file.split('.')[0] + '.webp'
            quality = int(self.ui.label_3.text())
            if not os.path.exists(webp_file):
                self.ui.listWidget.addItem(webp_file)

            cv2.imwrite(webp_file, self.frame, [cv2.IMWRITE_WEBP_QUALITY, quality])
            self.showMessageBox('WebP Conversion', "Done!")
            

    def onSliderChanged(self):
        self.ui.label_3.setText(str(self.ui.horizontalSlider.value()))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        filename = urls[0].toLocalFile()
        self.loadFile(filename)
        event.acceptProposedAction()

    def loadFile(self, filename):
        self.ui.statusbar.showMessage(filename)
        item = QListWidgetItem()
        item.setText(filename)
        self.ui.listWidget.addItem(item)
        self._all_data[filename] = None

        self.frame = cv2.imread(filename)
        self.showResults(self.frame)
        self.current_file = filename

    def appendFile(self, filename):
       
        if filename not in self._all_data:
            self.loadFile(filename)

    def currentItemChanged(self, current, previous):
        filename = current.text()
        self.current_file = filename
        self.ui.statusbar.showMessage(filename)
        self.showResults(cv2.imread(filename))

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File',
                                               self._path, "Barcode images (*)")
        if filename is None or filename[0] == '':
            # self.showMessageBox('Open File...', "No file selected")
            return

        filename = filename[0]
        self.appendFile(filename)

    def process_folder(self, folder):
        if os.path.isdir(folder):
            files = os.listdir(folder)
            for file in files:
                filepath = os.path.join(folder, file)
                if not os.path.isdir(filepath):
                    self.process_file(filepath)
                else:
                    self.process_folder(filepath)
        else:
            self.process_file(folder)

    def process_file(self, filename):
        self.appendFile(filename)

    def openFolder(self):
        dir = QFileDialog.getExistingDirectory(self, 'Open Folder',
                                               self._path, QFileDialog.ShowDirsOnly)
        if dir is '':
            # self.showMessageBox('Open Folder...', "No folder selected")
            return

        self.process_folder(dir)

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

    def showResults(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self._pixmap = self.resizeImage(pixmap)
        self.ui.label.setPixmap(self._pixmap)

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
    try:
        with open(sys.argv[1]) as f:
            license = f.read()
    except:
        license = ""

    app = QApplication(sys.argv)

    window = MainWindow(license)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    print(__doc__)
    main()