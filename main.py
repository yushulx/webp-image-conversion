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

class Worker(QObject):
    finished = Signal()
    progress = Signal(object)

    def __init__(self, files, quality):
        super(Worker, self).__init__()
        self.files = files
        self.total = len(files)
        self.isRunning = True
        self.quality = quality

    def run(self):
        print('Running worker thread...')
        count = 0
        keys = list(self.files.keys())
        while self.isRunning and len(self.files) > 0:
            filename = keys[count]
            count += 1
            print(filename)
            frame = cv2.imread(filename)
            webp_file = filename.split('.')[0] + '.webp'
            cv2.imwrite(webp_file, frame, [cv2.IMWRITE_WEBP_QUALITY, self.quality])
            self.progress.emit((webp_file, count, self.total))
            self.files.pop(filename)

        print('Quit worker thread...')
        self.finished.emit()

class MainWindow(QMainWindow):

    def __init__(self):
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
        self.progress_dialog = None
        self.worker = None
        self.isProcessing = False

        self.ui.actionOpen_File.triggered.connect(self.openFile)
        self.ui.actionOpen_Folder.triggered.connect(self.openFolder)
        self.ui.horizontalSlider.valueChanged.connect(self.onSliderChanged)
        self.ui.pushButton.clicked.connect(self.convertOne)
        self.ui.pushButton_all.clicked.connect(self.convertAll)
        self.ui.listWidget.currentItemChanged.connect(self.currentItemChanged)

    def reportProgress(self, data):
        filename, completed, total = data
        self.addImage(filename)
        if not self.isProcessing:
            return

        progress = completed
        self.progress_dialog.setLabelText(str(completed) +"/"+ str(total))
        self.progress_dialog.setValue(progress)
        if completed == total:
            self.onProgressDialogCanceled()
            self.showMessageBox('WebP Conversion', "Done!")

    def onProgressDialogCanceled(self):
        self.isProcessing = False
        self.worker.isRunning = False
        self.progress_dialog.cancel()

    def runLongTask(self):
        if (len(self._all_images) == 0):
            return
            
        self.isProcessing = True
        self.progress_dialog = QProgressDialog('Progress', 'Cancel', 0, len(self._all_images), self)
        self.progress_dialog.setLabelText('Progress')
        self.progress_dialog.setCancelButtonText('Cancel')
        self.progress_dialog.setRange(0, len(self._all_images))
        self.progress_dialog.setValue(0)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.show()
        self.progress_dialog.canceled.connect(self.onProgressDialogCanceled)

        self.thread = QThread()
        self.worker = Worker(self._all_images, int(self.ui.label_slider.text()))
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

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
            # for filename in self._all_images:
            #     self.convert(filename)

            # self.showMessageBox('WebP Conversion', "Done!")
            self.runLongTask()

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
        self.showImage(filename)

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
        directory = QFileDialog.getExistingDirectory(self, 'Open Folder',
                                               self._path, QFileDialog.ShowDirsOnly)
        if directory is '':
            self.showMessageBox('Open Folder...', "No folder selected")
            return

        self.appendFolder(directory)
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()