#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

#from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtWidgets import *
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

        self.setGeometry(150, 150, 800, 800)
        self.setWindowTitle('lab1 CAD')

        ### Текстовая полосочка
        self.qle = QLineEdit(self)
        self.qle.resize(QSize(200, 23))
        self.qle.move(100, 700)
        #qle.textChanged[str].connect(lambda: self.onChanged)
        #qle.returnPressed.connect(lambda: self.onChanged)
        # Кнопка к ней
        enter_btn = QPushButton('Ввод', self)
        enter_btn.clicked.connect(lambda: self.enterButton())
        enter_btn.resize(btn_size)
        enter_btn.move(300, 700)

        ### Кнопочки cktdf
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
        point_drawing_btn = QPushButton('Отрисовка точек', self)
        point_drawing_btn.clicked.connect(lambda: self.pointDrawingButton())
        point_drawing_btn.resize(btn_size)
        point_drawing_btn.move(0, 60)
        #
        line_drawing_btn = QPushButton('Отрисовка линий', self)
        line_drawing_btn.clicked.connect(lambda: self.lineDrawingButton())
        line_drawing_btn.resize(btn_size)
        line_drawing_btn.move(0, 90)
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
        line_hor_btn = QPushButton('Горизонт. прямой', self)
        line_hor_btn.clicked.connect(lambda: self.lineHorButton())
        line_hor_btn.resize(btn_size)
        line_hor_btn.move(0, 300)
        #
        line_ver_btn = QPushButton('Вертикал. прямой', self)
        line_ver_btn.clicked.connect(lambda: self.lineVerButton())
        line_ver_btn.resize(btn_size)
        line_ver_btn.move(0, 330)
        #
        point_to_line_btn = QPushButton('Принадл. точки прямой', self)
        point_to_line_btn.clicked.connect(lambda: self.pointToLineButton())
        point_to_line_btn.resize(btn_size)
        point_to_line_btn.move(0, 360)
        #
        self.show()

    ### Ивенты
    # Нажатие мыши
    def mousePressEvent(self, event):
        print('click X:', event.x(), 'Y:', event.y())
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
        if sc.draw_points:
            pen.setWidth(6)
            painter.setPen(pen)
            for point_i in gc.points:
                painter.drawPoint(point_i[0], point_i[1])
        # Отрисовка обычных линий
        if sc.draw_lines:
            pen.setWidth(3)
            painter.setPen(pen)
            for line_i in gc.lines:
                fp_idx, sp_idx = line_i
                painter.drawLine(gc.points[fp_idx,0], gc.points[fp_idx,1],
                                 gc.points[sp_idx,0], gc.points[sp_idx,1])
        # Отрисовка выбранных точек и линий
        pen.setWidth(6)
        pen.setColor(QColor(50,50,255))
        painter.setPen(pen)
        for point_i in gc.selected_points:
            painter.drawPoint(point_i[0], point_i[1])
        pen.setWidth(3)
        painter.setPen(pen)
        for line_i in gc.selected_lines:
            fp_idx, sp_idx = line_i
            painter.drawLine(gc.points[fp_idx,0], gc.points[fp_idx,1],
                             gc.points[sp_idx,0], gc.points[sp_idx,1])
        pen.setColor(QColor(0,0,0))
        painter.setPen(pen)
        # Иногда надо отрисовать точечку красным
        pen.setWidth(6)
        pen.setColor(QColor(255,0,0))
        painter.setPen(pen)
        if sc.getState() == 'line_drawing_2':
            painter.drawPoint(gc.fp_x, gc.fp_y)
        #elif (sc.getState() == 'dot_coinc_2' or
        #      sc.getState() == 'dot_dist_2'):
        #    painter.drawPoint(gc.points[gc.fp, 0], gc.points[gc.fp, 1])
        pen.setColor(QColor(0,0,0))
        painter.setPen(pen)
    ###

    ### Обработчики кнопочек
    def enterButton(self):
        print('enterButton()')
        self.sc.takeEnter(self.qle.text())
        self.qle.clear()
        self.update()

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

    def pointDrawingButton(self):
        if self.sc.draw_points:
            self.sc.draw_points = False
        else:
            self.sc.draw_points = True
        print('sc.draw_points ', self.sc.draw_points)
        self.update()

    def lineDrawingButton(self):
        if self.sc.draw_lines:
            self.sc.draw_lines = False
        else:
            self.sc.draw_lines = True
        print('sc.draw_lines ', self.sc.draw_lines)
        self.update()

    def testButton(self):
        #print(self.points)
        self.update()

    def dotCoincButton(self):
        #print('dotCoincButton()')
        if (self.sc.getState() != 'dot_coinc_1' and
            self.sc.getState() != 'dot_coinc_2'):
            self.sc.setState('dot_coinc_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def dotDistButton(self):
        #print('dotDistButton()')
        if (self.sc.getState() != 'dot_dist_1' and
            self.sc.getState() != 'dot_dist_2' and
            self.sc.getState() != 'dot_dist_3'):
            self.sc.setState('dot_dist_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
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

    def lineHorButton(self):
        print('lineHorButton()')
        self.update()

    def lineVerButton(self):
        print('lineVerButton()')
        self.update()

    def pointToLineButton(self):
        print('pointToLineButton()')
        self.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
