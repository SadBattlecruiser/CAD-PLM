#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geometryclass import *

class StateClass():
    def __init__(self, geometry):
        self.draw_points = True             # Отрисовывать ли точки
        self.draw_lines = True              # Отрисовывать ли линии
        self.gc = geometry
        self.setState('default')
        # Какое состояние следующее в зависимости от текущего состояния
        # Здесь все возможные состояния
        self.next_states = {
            'default' : 'default',
            'point_drawing' : 'point_drawing',
            'line_drawing_1' : 'line_drawing_2',
            'line_drawing_2' : 'line_drawing_1',
            'dot_coinc_1' : 'dot_coinc_2',
            'dot_coinc_2' : 'default',
            'dot_dist_1' : 'dot_dist_2',
            'dot_dist_2' : 'dot_dist_3',
            'dot_dist_3' : 'default',
        }
        # Что делать с кликом в зависимости от текущего состояния
        self.click_funcs = {
            'default' : self.doNothing,
            'point_drawing' : self.pointDrawing,
            'line_drawing_1' : self.lineDrawing1,
            'line_drawing_2' : self.lineDrawing2,
            'dot_coinc_1' : self.dotCoinc1,
            'dot_coinc_2' : self.dotCoinc2,
            'dot_dist_1' : self.dotDist1,
            'dot_dist_2' : self.dotDist2,
        }
        # Что делать с введенным текстом в зависимости от текущего состояния
        self.enter_funcs = {
            'default' : self.doNothing,
            'dot_dist_3' : self.dotDist3,
        }
        print('StateClass constructor')

    def getState(self):
        return self.state

    def setState(self, state):
        # Если мы здесь, вполне могло быть нажатие кнопки
        # При этом прошлые стейты могли не закончится - почисти
        self.gc.dropSelected()
        self.state = state

    def takeClick(self, x, y):
        # Если есть подходящая функция - обрабатываем
        if self.state in self.click_funcs:
            func = self.click_funcs[self.state]
            func(x, y)
            self.state = self.next_states[self.state]

    def takeEnter(self, enter_text):
        # Если есть подходящая функция - обрабатываем
        if self.state in self.enter_funcs:
            func = self.enter_funcs[self.state]
            func(enter_text)
            self.state = self.next_states[self.state]

    ### Функции для обработки клика
    def pointDrawing(self, x, y):
        self.gc.addPoint(x,y)

    def lineDrawing1(self, x, y):
        self.gc.fp_x = x
        self.gc.fp_y = y

    def lineDrawing2(self, x, y):
        self.gc.ld_sp_x = x
        self.gc.ld_sp_y = y
        self.gc.addLine(self.gc.fp_x, self.gc.fp_y,
                        self.gc.ld_sp_x, self.gc.ld_sp_y)

    def dotCoinc1(self, x, y):
        self.gc.dc_fp = self.gc.findClosePoint(x, y)
        self.gc.addPointToSelected(self.gc.dc_fp)

    def dotCoinc2(self, x, y):
        self.gc.dc_sp = self.gc.findClosePoint(x, y)
        self.gc.addDotCoinc(self.gc.dc_fp, self.gc.dc_sp)
        print(self.gc.constraints_idxs)
        self.gc.dropSelected()

    def dotDist1(self, x, y):
        self.gc.fp = self.gc.findClosePoint(x, y)
        self.gc.addPointToSelected(self.gc.fp)

    def dotDist2(self, x, y):
        self.gc.sp = self.gc.findClosePoint(x, y)
        self.gc.addPointToSelected(self.gc.sp)

    def doNothing(self, arg1, arg2):
        pass
    ###

    ### Функции для обработки введенного текста
    def doNothing(self, arg):
        pass

    def dotDist3(self, dist_str):
        dist = float(dist_str)
        print(dist)
        self.gc.addDotDist(self.gc.fp, self.gc.sp, dist)
        print(self.gc.constraints_idxs)
        print(self.gc.constraints_values)
        self.gc.dropSelected()
