#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#from flagsclass import *
from geometryclass import *
from stateclass import *


# Этот класс отвечает за обработку ивентов - нажатий кнопок, отрисовку и др.
class MyApp(QWidget):
    def __init__(self):
        self.gc = GeometryClass()            # Отвечает за работу с геометрией
        self.sc = StateClass(self.gc)        # Отвечает за смену состояний программы
        super().__init__()
        self.initUI()
        print('MyApp constructor')

    def initUI(self):
        btn_size = QSize(125, 23)

        point_btn = QPushButton('Точка', self)
        point_btn.clicked.connect(lambda: self.pointButton())
        point_btn.resize(btn_size)
        point_btn.move(0, 0)
        #
        line_btn = QPushButton('Линия', self)
        line_btn.clicked.connect(lambda: self.lineButton())
        line_btn.resize(btn_size)
        line_btn.move(0, 30)
        #
        point_pos_btn = QPushButton('Point pos', self)
        point_pos_btn.clicked.connect(lambda: self.pointPosButton())
        point_pos_btn.resize(btn_size)
        point_pos_btn.move(0, 60)
        #
        line_pos_btn = QPushButton('Line pos', self)
        line_pos_btn.clicked.connect(lambda: self.linePosButton())
        line_pos_btn.resize(btn_size)
        line_pos_btn.move(0, 90)
        #
        dot_coinc_btn = QPushButton('Совпадение точек', self)
        dot_coinc_btn.clicked.connect(lambda: self.dotCoincButton())
        dot_coinc_btn.resize(btn_size)
        dot_coinc_btn.move(0, 150)
        #
        dot_dist_btn = QPushButton('Расст. между точками', self)
        dot_dist_btn.clicked.connect(lambda: self.dotDistButton())
        dot_dist_btn.resize(btn_size)
        dot_dist_btn.move(0, 180)
        #
        line_paral_btn = QPushButton('Паралл. прямых', self)
        line_paral_btn.clicked.connect(lambda: self.lineParalButton())
        line_paral_btn.resize(btn_size)
        line_paral_btn.move(0, 210)
        #
        line_orth_btn = QPushButton('Перпенд. прямых', self)
        line_orth_btn.clicked.connect(lambda: self.lineOrthButton())
        line_orth_btn.resize(btn_size)
        line_orth_btn.move(0, 240)
        #
        line_angle_btn = QPushButton('Угол между прямыми', self)
        line_angle_btn.clicked.connect(lambda: self.lineAngleButton())
        line_angle_btn.resize(btn_size)
        line_angle_btn.move(0, 270)
        #
        self.setGeometry(150, 150, 800, 800)
        self.setWindowTitle('lab1 CAD')
        print(dot_dist_btn.sizeHint())
        self.show()

    ### Ивенты
    # Нажатие мыши
    def mousePressEvent(self, event):
        print(event)
        print('X:', event.x(), 'Y:', event.y())
        self.sc.takeClick(event.x(), event.y())
        self.update()

    # Этого достаточно, чтобы ловить кнопку
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print('esc')

    # Отвечает за отрисовку всего
    def paintEvent(self, event):
        gc = self.gc
        sc = self.sc
        painter = QPainter(self)
        #painter.drawPixmap(self.rect(), self._image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen()
        # Отрисовка обычных точек
        if sc.draw_points_:
            pen.setWidth(6)
            painter.setPen(pen)
            for point_i in gc.points:
                painter.drawPoint(point_i[0], point_i[1])
        # Отрисовка обычных линий
        if sc.draw_lines_:
            pen.setWidth(3)
            painter.setPen(pen)
            for line_i in gc.lines:
                fp_idx, sp_idx = line_i
                painter.drawLine(gc.points[fp_idx,0], gc.points[fp_idx,1],
                                 gc.points[sp_idx,0], gc.points[sp_idx,1])
        # Отрисовка первой точки линии, если она уже задана
        if sc.getState() == 'line_drawing_2':
            pen.setWidth(6)
            pen.setColor(QColor(255,0,0))
            painter.setPen(pen)
            painter.drawPoint(gc.ld_fp_x_, gc.ld_fp_y_)
            pen.setColor(QColor(0,0,0))
            painter.setPen(pen)
    ###


    ### Обработчики
    def pointButton(self):
        #print('pointButton()')
        if self.sc.getState() != 'point_drawing':
            self.sc.setState('point_drawing')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def lineButton(self):
        #print('lineButton()')
        if (self.sc.getState() != 'line_drawing_1' and
            self.sc.getState() != 'line_drawing_2'):
            self.sc.setState('line_drawing_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def pointPosButton(self):
        #self.selected_points = np.empty([0, 2])
        #self.selected_lines = np.empty([0, 2], dtype=int)
        #self.flags.change_in_point_pos()
        self.update()

    def linePosButton(self):
        #self.selected_points = np.empty([0, 2])
        #self.selected_lines = np.empty([0, 2], dtype=int)
        #self.flags.change_in_line_pos()
        self.update()

    def testButton(self):
        #print(self.points)
        self.update()

    def dotCoincButton(self):
        print('dotCoincButton()')
        self.update()

    def dotDistButton(self):
        print('dotDistButton()')
        self.update()

    def lineParalButton(self):
        print('lineParalButton()')
        self.update()

    def lineOrthButton(self):
        print('lineOrthButton()')
        self.update()

    def lineAngleButton(self):
        print('lineAngleButton()')
        self.update()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
