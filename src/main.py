#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from flagsclass import *
#import numpy as np


class MyApp(QWidget):
    def __init__(self):
        self.flags = FlagsClass()       # Хранилище флагов состояний
        self.points = []                # Лист обычных точек
        self.lines = []                 # Лист обычных линий
        self.selected_points = []       # Лист выбранных точек
        self.selected_lines = []        # Лист выбранных линий
        super().__init__()
        self.initUI()

    def initUI(self):
        line_btn = QPushButton('Line draw', self)
        line_btn.clicked.connect(lambda: self.lineButton())
        line_btn.resize(line_btn.sizeHint())
        line_btn.move(0, 0)
        #
        point_pos_btn = QPushButton('Point pos', self)
        point_pos_btn.clicked.connect(lambda: self.pointPosButton())
        point_pos_btn.resize(point_pos_btn.sizeHint())
        point_pos_btn.move(0, 30)
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
        f = self.flags
        # Если сейчас рисуем линию
        if f.in_line_draw:
            if f.line_first_point:
                self.first_point = event.pos()
                f.line_first_point = False
            else:
                self.second_point = event.pos()
                self.lines.append(QLineF(self.first_point, self.second_point))
                f.line_first_point = True
        # Если сейчас выбираем точку
        elif f.in_select_point:
            #self.selected_points.append(self.findClosePoint(event.pos()))
            self.selected_points.append(event.pos())
            pass
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
        # Отрисовка выбранных точек и линий
        pen.setWidth(6)
        pen.setColor(QColor(100,150,50))
        painter.setPen(pen)
        for point_i in self.selected_points:
            painter.drawPoint(point_i)
        pen.setWidth(3)
        painter.setPen(pen)
        for line_i in self.selected_lines:
            painter.drawLine(line_i)
        pen.setColor(QColor(0,0,0))
        painter.setPen(pen)
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
    def lineButton(self):
        self.selected_points = []
        self.selected_lines = []
        self.flags.change_in_line_draw()
        self.update()

    def pointPosButton(self):
        self.selected_points = []
        self.selected_lines = []
        self.flags.change_in_point_pos()
        self.update()

    def findClosePoint(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
