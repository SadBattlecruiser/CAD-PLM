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
        self.flags = FlagsClass()                                  # Хранилище флагов состояний
        self.points = np.empty([0, 2])                             # Каждая точка - x,y
        self.lines = np.empty([0, 2], dtype=int)                   # Каждая линия - p1_idx, p2_idx
        self.selected_points = np.empty([0, 2])                    # Лист выбранных точек
        self.selected_lines = np.empty([0, 2], dtype=int)          # Лист выбранных линий
        super().__init__()
        self.initUI()
        print('MyApp constructor')

    def initUI(self):
        btn_size = QSize(125, 23)

        line_btn = QPushButton('Line draw', self)
        line_btn.clicked.connect(lambda: self.lineButton())
        line_btn.resize(btn_size)
        line_btn.move(0, 0)
        #
        point_pos_btn = QPushButton('Point pos', self)
        point_pos_btn.clicked.connect(lambda: self.pointPosButton())
        point_pos_btn.resize(btn_size)
        point_pos_btn.move(0, 30)
        #
        line_pos_btn = QPushButton('Line pos', self)
        line_pos_btn.clicked.connect(lambda: self.linePosButton())
        line_pos_btn.resize(btn_size)
        line_pos_btn.move(0, 60)
        #
        test_pos_btn = QPushButton('test', self)
        test_pos_btn.clicked.connect(lambda: self.testButton())
        test_pos_btn.resize(btn_size)
        test_pos_btn.move(0, 90)
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
        line_orth_btn.clicked.connect(lambda: self.lineOrtButton())
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
        f = self.flags
        # Если сейчас рисуем линию
        if f.in_line_draw:
            if f.line_first_point:
                self.first_point = np.array([event.x(), event.y()])
                f.line_first_point = False
            else:
                self.second_point = np.array([event.x(), event.y()])
                fp_idx = self.points.shape[0]
                sp_idx = fp_idx + 1
                # Добавляем обе точки линии ко всем точкам
                self.points = np.vstack([self.points, np.vstack([self.first_point, self.second_point])])
                # Добавляем линию как индексы двух точек
                self.lines = np.vstack([self.lines, [fp_idx, sp_idx]])
                f.line_first_point = True
        # Если сейчас выбираем точку
        elif f.in_select_point:
            cls_idx = self.findClosePoint(event.x(), event.y())
            self.selected_points = np.vstack([self.selected_points, self.points[cls_idx]])
        # Если сейчас выбираем отрезок
        elif f.in_select_line:
            cls_idx = self.findCloseLine(event.x(), event.y())
            self.selected_lines = np.vstack([self.selected_lines, self.lines[cls_idx]])
        # Иначе просто ставим точку
        else:
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
                fp_idx, sp_idx = line_i
                painter.drawLine(self.points[fp_idx,0], self.points[fp_idx,1],
                                 self.points[sp_idx,0], self.points[sp_idx,1])
        # Отрисовка выбранных точек и линий
        pen.setWidth(6)
        pen.setColor(QColor(50,50,255))
        painter.setPen(pen)
        for point_i in self.selected_points:
            painter.drawPoint(point_i[0], point_i[1])
        pen.setWidth(3)
        painter.setPen(pen)
        for line_i in self.selected_lines:
            fp_idx, sp_idx = line_i
            painter.drawLine(self.points[fp_idx,0], self.points[fp_idx,1],
                             self.points[sp_idx,0], self.points[sp_idx,1])
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
        self.selected_lines = np.empty([0, 2], dtype=int)
        self.flags.change_in_line_draw()
        self.update()

    def pointPosButton(self):
        self.selected_points = np.empty([0, 2])
        self.selected_lines = np.empty([0, 2], dtype=int)
        self.flags.change_in_point_pos()
        self.update()

    def linePosButton(self):
        self.selected_points = np.empty([0, 2])
        self.selected_lines = np.empty([0, 2], dtype=int)
        self.flags.change_in_line_pos()
        self.update()

    def testButton(self):
        #print(self.points)
        self.update()

    def dotCoincButton(self):
        pass

    def dotDistButton(self):
        pass

    def lineParalButton(self):
        pass

    def lineOrthButton(self):
        pass

    def lineAngleButton(self):
        pass


    ### Вспомогательное
    # Ближайшая точка
    def findClosePoint(self, x, y):
        if (self.points.size == 0):
            print('ERROR: self.points.size == 0 in findClosePoints')
            return -1
        dist = np.sqrt(np.power(self.points[:,0] - x, 2) + np.power(self.points[:,1] - y, 2))
        return np.argmin(dist)

    # Ближайший отрезок
    def findCloseLine(self, x, y):
        if (self.lines.size == 0):
            print('ERROR: self.lines.size == 0 in findCloseLine')
            return -1
        tolerance = 20
        # Оставляем только те линии, в "рамку" которых попал курсор
        interes_idxs = []
        interes_fp_x = []
        interes_fp_y = []
        interes_sp_x = []
        interes_sp_y = []
        for i, line_i in enumerate(self.lines):
            fp_xi = self.points[line_i[0]][0]
            fp_yi = self.points[line_i[0]][1]
            sp_xi = self.points[line_i[1]][0]
            sp_yi = self.points[line_i[1]][1]
            if ((x < max([fp_xi, sp_xi]) + tolerance) and
                (x > min([fp_xi, sp_xi]) - tolerance) and
                (y < max([fp_yi, sp_yi]) + tolerance) and
                (y > min([fp_yi, sp_yi]) - tolerance)):
                interes_idxs.append(i)
                interes_fp_x.append(fp_xi)
                interes_fp_y.append(fp_yi)
                interes_sp_x.append(sp_xi)
                interes_sp_y.append(sp_yi)
        # Переводим в массивы для удобного счета
        fp_x = np.array(interes_fp_x)
        fp_y = np.array(interes_fp_y)
        sp_x = np.array(interes_sp_x)
        sp_y = np.array(interes_sp_y)
        # Для оставленных линий смотрим расстояние от клика до них
        # Формулу смотри в выводе в Wolfram
        numerator = np.abs(sp_x*fp_y - x*fp_y - fp_x*sp_y + x*sp_y + fp_x*y - sp_x*y)
        denominator = np.sqrt(np.power(fp_x,2) - 2 * fp_x * sp_x + np.power(sp_x,2) + np.power(fp_y-sp_y,2))
        dist = numerator / denominator
        # Индекс нужной линии в листе интересных
        interes_cls_idx = np.argmin(dist)
        return interes_idxs[interes_cls_idx]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
