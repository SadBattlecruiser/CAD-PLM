#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import *
#from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtCore import *
from flagsclass import *
#import numpy as np


class MyApp(QWidget):
    def __init__(self):
        self.flags = FlagsClass()       # Хранилище флагов состояний
        self.points = []                # Лист точек
        self.lines = []                 # Лист линий
        super().__init__()
        self.initUI()

    def initUI(self):
        wow_btn = QPushButton('WOW', self)
        wow_btn.clicked.connect(lambda: self.printButton('test'))
        wow_btn.resize(wow_btn.sizeHint())
        wow_btn.move(50, 50)
        #
        line_btn = QPushButton('Line', self)
        line_btn.clicked.connect(lambda: self.lineButton())
        line_btn.resize(line_btn.sizeHint())
        line_btn.move(0, 0)
        #
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('lab1 CAD')
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
        # Если сейчас рисуем линию
        if self.flags.in_line_draw:
            if self.flags.line_first_point:
                self.first_point = event.pos()
                self.flags.line_first_point = False
            else:
                self.second_point = event.pos()
                self.lines.append(QLineF(self.first_point, self.second_point))
                self.flags.line_first_point = True
        # Иначе просто ставим точку
        else:
            self.points.append(event.pos())
        self.update()

    # Отвечает за отрисовку всего
    def paintEvent(self, event):
        painter = QPainter(self)
        #painter.drawPixmap(self.rect(), self._image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen()
        # Отрисовка обычных точек
        if self.flags.draw_points:
            pen.setWidth(6)
            painter.setPen(pen)
            for point_i in self.points:
                painter.drawPoint(point_i)
        # Отрисовка обычных линий
        if self.flags.draw_lines:
            pen.setWidth(3)
            painter.setPen(pen)
            for line_i in self.lines:
                painter.drawLine(line_i)
        # Отрисовка первой точки линии, если она уже задана
        if self.flags.in_line_draw and not self.flags.line_first_point:
            pen.setWidth(6)
            pen.setColor(QColor(255,0,0))
            painter.setPen(pen)
            painter.drawPoint(self.first_point)
            pen.setColor(QColor(0,0,0))
            painter.setPen(pen)
    ###


    ### Обработчики
    def printButton(self, name):
        print(name)

    def lineButton(self):
        self.flags.change_in_line_draw()
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
