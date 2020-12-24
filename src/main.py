#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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

        self.setGeometry(100, 100, 1800, 900)
        self.setWindowTitle('lab1 CAD')

        ### Для отрисовки поля
        self.frame_ox = 150
        self.frame_oy = 0
        self.frame_target = QRectF(self.frame_ox, self.frame_oy, 1210+self.frame_ox, 810+self.frame_oy)
        self.frame_source = QRectF(0.0, 0.0, 1210.0, 810.0)
        self.base_image = QImage("base.png")
        self.frame_image = QImage("base_frame.png")

        ### Лист справа
        self.lw = QListWidget(self)
        self.lw.resize(QSize(200, 808))
        self.lw.move(1535, 0)
        self.lw.itemClicked.connect(lambda item: self.itemClickedList(item))

        ### Текстовая полосочка
        self.qle = QLineEdit(self)
        self.qle.resize(QSize(200, 23))
        self.qle.move(self.frame_ox, 850+self.frame_oy)
        # Кнопка к ней
        enter_btn = QPushButton('Ввод', self)
        enter_btn.clicked.connect(lambda: self.enterButton())
        enter_btn.resize(btn_size)
        enter_btn.move(self.frame_ox + 200, 850+self.frame_oy)

        ### Кнопочки слева
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
        solve_btn = QPushButton('Рассчитать', self)
        solve_btn.clicked.connect(lambda: self.solveButton())
        solve_btn.resize(btn_size)
        solve_btn.move(0, 400)
        #
        point_drawing_btn = QPushButton('Отрисовка точек', self)
        point_drawing_btn.clicked.connect(lambda: self.pointDrawingButton())
        point_drawing_btn.resize(btn_size)
        point_drawing_btn.move(0, 520)
        #
        line_drawing_btn = QPushButton('Отрисовка линий', self)
        line_drawing_btn.clicked.connect(lambda: self.lineDrawingButton())
        line_drawing_btn.resize(btn_size)
        line_drawing_btn.move(0, 550)
        #
        grid_drawing_btn = QPushButton('Отрисовка сетки', self)
        grid_drawing_btn.clicked.connect(lambda: self.gridDrawingButton())
        grid_drawing_btn.resize(btn_size)
        grid_drawing_btn.move(0, 580)
        #
        self.show()

    ### Ивенты
    # Нажатие мыши
    def mousePressEvent(self, event):
        # Проверяем, попали ли мы в рамку
        if  (event.x() < self.frame_target.left() + 3) or\
            (event.x() > self.frame_target.right() - 3) or\
            (event.y() > self.frame_target.bottom() - 8) or\
            (event.y() < self.frame_target.top()):
            print('out click X:', event.x(), 'Y:', event.y())
            return;
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
        painter.setRenderHint(QPainter.Antialiasing, True)
        # Отрисовка поля
        if sc.draw_grid:
            painter.drawImage(self.frame_target, self.base_image, self.frame_source);
        else:
            painter.drawImage(self.frame_target, self.frame_image, self.frame_source);
        # Отрисовка обычных точек
        pen = QPen()
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

        # Выводим все ограничения в лист
        self.printConstraintsToList()
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

    def gridDrawingButton(self):
        if self.sc.draw_grid:
            self.sc.draw_grid = False
        else:
            self.sc.draw_grid = True
        print('sc.draw_grid ', self.sc.draw_grid)
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
        if (self.sc.getState() != 'line_paral_1' and
            self.sc.getState() != 'line_paral_2'):
            self.sc.setState('line_paral_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def lineOrthButton(self):
        if (self.sc.getState() != 'line_orth_1' and
            self.sc.getState() != 'line_orth_2'):
            self.sc.setState('line_orth_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def lineAngleButton(self):
        if (self.sc.getState() != 'line_angle_1' and
            self.sc.getState() != 'line_angle_2' and
            self.sc.getState() != 'line_angle_3'):
            self.sc.setState('line_angle_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def lineHorButton(self):
        if (self.sc.getState() != 'line_hor'):
            self.sc.setState('line_hor')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def lineVerButton(self):
        if (self.sc.getState() != 'line_ver'):
            self.sc.setState('line_ver')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def pointToLineButton(self):
        if (self.sc.getState() != 'point_to_line_1' and
            self.sc.getState() != 'point_to_line_2'):
            self.sc.setState('point_to_line_1')
            print(self.sc.getState())
        else:
            self.sc.setState('default')
            print(self.sc.getState())
        self.update()

    def solveButton(self):
        self.gc.satisfy_constraints()
        self.update()

    ### Обработчики для листа
    def itemClickedList(self, item):
        self.sc.setState('select_constrain')
        constr_idx = int(item.text().split('|', 1)[0]) - 1
        self.sc.selectConstrain(constr_idx)
        self.update()

    def printConstraintsToList(self):
        self.lw.clear()
        values = self.gc.constraints_values
        for i, constr_i in enumerate(self.gc.constraints_idxs):
            if constr_i[0] == 0:
                self.lw.addItem(str(i + 1) + ' | полож. т. ' + str(constr_i[1]) + '\t | ' + str(values[i, 0]) + str(values[i, 1]))
            elif constr_i[0] == 1:
                self.lw.addItem(str(i + 1) + ' | совп. т. ' + str(constr_i[1]) + ' и ' + str(constr_i[2]))
            elif constr_i[0] == 2:
                self.lw.addItem(str(i + 1) + ' | расст. т. ' + str(constr_i[1]) + ' и ' + str(constr_i[2]) + '\t | ' + str(values[i, 0]))
            elif constr_i[0] == 3:
                self.lw.addItem(str(i + 1) + ' | прлл. л. ' + str(constr_i[1]) + ' и ' + str(constr_i[2]))
            elif constr_i[0] == 4:
                self.lw.addItem(str(i + 1) + ' | перп. л. ' + str(constr_i[1]) + ' и ' + str(constr_i[2]))
            elif constr_i[0] == 5:
                self.lw.addItem(str(i + 1) + ' | угол. л. ' + str(constr_i[1]) + ' и ' + str(constr_i[2]) + '\t | ' + str(values[i, 0]))
            elif constr_i[0] == 6:
                self.lw.addItem(str(i + 1) + ' | гориз. л. ' + str(constr_i[1]))
            elif constr_i[0] == 7:
                self.lw.addItem(str(i + 1) + ' | верт. л. ' + str(constr_i[1]))
            elif constr_i[0] == 8:
                self.lw.addItem(str(i + 1) + ' | прндл. т. ' + str(constr_i[1]) + ' л. ' + str(constr_i[2]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
