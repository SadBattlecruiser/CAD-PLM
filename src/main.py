#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
#from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QCoreApplication

#import numpy as np

class MyApp(QWidget):
    def __init__(self):
        self.points = []
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

    ### Ивенты
    # Этого достаточно, чтобы ловить кнопку
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print('esc')
    # Нажатие мыши
    def mousePressEvent(self, event):
        print(event)
        print('X:', event.x(), 'Y:', event.y())
        #self.drawPoint(event.pos())
        self.points.append(event.pos())
        self.update()

    def paintEvent(self, paint_event):
        painter = QPainter(self)
        #painter.drawPixmap(self.rect(), self._image)
        pen = QPen()
        pen.setWidth(4)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPoint(300, 300)
        #painter.drawLine(100, 100, 400, 400)
        for pos in self.points:
            painter.drawPoint(pos)
    ###

    ### Обработчики
    def printButton(self, name):
        print(name)

    #def drawPoint(self, pos, color=Qt.black):
    #    painter = QPainter(self)
    #    pen = QPen(color, 3)
    #    painter.setPen(pen)
    #    painter.drawPoint(pos)

    #def drawLine(self, color='black'):
    #    painter = QPainter(self)
    #    pen = QPen(Qt.red, 3)
    #    painter.setPen(pen)
    #    painter.drawLine(10, 10, self.rect().width() -10 , 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
