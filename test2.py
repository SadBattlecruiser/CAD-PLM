#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        qbtn = QPushButton('WOW', self)
        #qbtn.clicked.connect(QCoreApplication.instance().quit)
        # Принтим надпись в консольку
        qbtn.clicked.connect(lambda: self.printButton('test'))
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Button Test')
        self.show()

    def printButton(self, name):
        print(name)

    # Этого достаточно, чтобы ловить кнопку
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print('esc')

    # Нажатие мши
    def mousePressEvent(self, event):
        print(event)

    def drawLine(self, color='black'):
        painter = QPainter(self)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() -10 , 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
