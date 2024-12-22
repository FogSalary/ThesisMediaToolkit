# -*- coding: utf-8 -*-
"""
@ProjectName: ffmpeg_dev
@FileName:  main
@Autor:  victor
@Date:  2023/12/14 0:13
"""

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ffmpeg_pro import Ui_MainWindow

class videoPro(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(videoPro, self).__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = videoPro()
    w.show()
    sys.exit(app.exec_())