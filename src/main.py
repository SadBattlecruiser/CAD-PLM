#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np

from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from flagsclass import *



class MyApp(QWidget):
    def __init__(self):
        self.flags = FlagsClass()                       # Хранилище флагов состояний
        self.points = np.empty([0, 2])                  # Лист обычных точек
        self.lines = []                                 # Лист обычных линий
        self.selected_points = np.empty([0, 2])         # Лист выбранных точек
        self.selected_lines = []                        # Лист выбранных линий
        super().__init__()
        self.initUI()
        print('MyApp constructor')

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
        point_pos_btn = QPushButton('test', self)
        point_pos_btn.clicked.connect(lambda: self.testButton())
        point_pos_btn.resize(point_pos_btn.sizeHint())
        point_pos_btn.move(0, 60)
        #
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('lab1 CAD')
        self.show()

    ### Ивенты
    # Нажатие мыши
    def mousePressEvent(self, event):
        print(event)
        print('X:', event.x(), 'Y:', event.y())
        f = self.flags
        # Если сейчас рисуем линию
        if f.in_line_draw:
            if f.line_first_point:
                self.first_point = np.array([event.x(), event.y()])
                f.line_first_point = False
            else:
                self.second_point = np.array([event.x(), event.y()])
                self.lines.append(QLineF(self.first_point[0], self.first_point[1], self.second_point[0], self.second_point[1]))
                f.line_first_point = True
        # Если сейчас выбираем точку
        elif f.in_select_point:
            cls_idx = self.findClosePoint(event.x(), event.y())
            self.selected_points = np.vstack([self.selected_points, self.points[cls_idx]])
        # Иначе просто ставим точку
        else:
            #self.points.append(event.pos())
            self.points = np.vstack([self.points, [event.x(), event.y()]])
        self.update()

    # Этого достаточно, чтобы ловить кнопку
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print('esc')

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
                painter.drawPoint(point_i[0], point_i[1])
        # Отрисовка обычных линий
        if self.flags.draw_lines:
            pen.setWidth(3)
            painter.setPen(pen)
            for line_i in self.lines:
                painter.drawLine(line_i)
        # Отрисовка выбранных точек и линий
        pen.setWidth(6)
        pen.setColor(QColor(50,50,255))
        painter.setPen(pen)
        for point_i in self.selected_points:
            painter.drawPoint(point_i[0], point_i[1])
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
            painter.drawPoint(self.first_point[0], self.first_point[1])
            pen.setColor(QColor(0,0,0))
            painter.setPen(pen)
    ###


    ### Обработчики
    def lineButton(self):
        self.selected_points = np.empty([0, 2])
        self.selected_lines = []
        self.flags.change_in_line_draw()
        self.update()

    def pointPosButton(self):
        self.selected_points = np.empty([0, 2])
        self.selected_lines = []
        self.flags.change_in_point_pos()
        self.update()

    def testButton(self):
        print(self.points)
        self.update()


    ### Вспомогательное
    def findClosePoint(self, x, y):
        if (self.points.size == 0):
            print('ERROR: self.points.size == 0 in findClosePoints')
            return -1
        dist = np.sqrt(np.power(self.points[:,0] - x, 2) + np.power(self.points[:,1] - y, 2))
        return np.argmin(dist)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
