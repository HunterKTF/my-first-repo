# File: main.py
# For ui updates: pyside6-uic mainwindow.ui > myui.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Slot
import pydub
from pydub import AudioSegment
from pydub.playback import play
from myui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, AudioSegment, pydub)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
