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
            'line_paral_1' : 'line_paral_2',
            'line_paral_2' : 'default',
            'line_orth_1' : 'line_orth_2',
            'line_orth_2' : 'default',
            'line_angle_1' : 'line_angle_2',
            'line_angle_2' : 'line_angle_3',
            'line_angle_3' : 'default',
            'line_hor' : 'default',
            'line_ver' : 'default',
            'point_to_line_1' : 'point_to_line_2',
            'point_to_line_2' : 'default',
        }
        # Что делать с кликом в зависимости от текущего состояния
        self.click_funcs = {
            'default' : self.doNothingClick,
            'point_drawing' : self.pointDrawing,
            'line_drawing_1' : self.lineDrawing1,
            'line_drawing_2' : self.lineDrawing2,
            'dot_coinc_1' : self.dotCoinc1,
            'dot_coinc_2' : self.dotCoinc2,
            'dot_dist_1' : self.dotDist1,
            'dot_dist_2' : self.dotDist2,
            'line_paral_1' : self.lineParal1,
            'line_paral_2' : self.lineParal2,
            'line_orth_1' : self.lineOrth1,
            'line_orth_2' : self.lineOrth2,
            'line_angle_1' : self.lineAngle1,
            'line_angle_2' : self.lineAngle2,
            'line_hor' : self.lineHor,
            'line_ver' : self.lineVer,
            'point_to_line_1' : self.pointToLine1,
            'point_to_line_2' : self.pointToLine2,
        }
        # Что делать с введенным текстом в зависимости от текущего состояния
        self.enter_funcs = {
            'default' : self.doNothingEnter,
            'dot_dist_3' : self.dotDist3,
            'line_angle_3' : self.lineAngle3,
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
            res = func(x, y)
            if res == -1:
                print('ERROR')
                self.setState('default')
            else:
                self.state = self.next_states[self.state]

    def takeEnter(self, enter_text):
        # Если есть подходящая функция - обрабатываем
        if self.state in self.enter_funcs:
            func = self.enter_funcs[self.state]
            func(enter_text)
            if res == -1:
                print('ERROR')
                self.setState('default')
            else:
                self.state = self.next_states[self.state]

    ### Функции для обработки клика
    def doNothingClick(self, arg1, arg2):
        pass

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
        if self.gc.dc_fp == -1:
            return -1
        self.gc.addPointToSelected(self.gc.dc_fp)
        return 0

    def dotCoinc2(self, x, y):
        self.gc.dc_sp = self.gc.findClosePoint(x, y)
        if self.gc.dc_sp == -1:
            return -1
        self.gc.addDotCoinc(self.gc.dc_fp, self.gc.dc_sp)
        #print(self.gc.constraints_idxs)
        self.gc.dropSelected()
        return 0

    def dotDist1(self, x, y):
        self.gc.fp = self.gc.findClosePoint(x, y)
        if self.gc.fp == -1:
            return -1
        self.gc.addPointToSelected(self.gc.fp)
        return 0

    def dotDist2(self, x, y):
        self.gc.sp = self.gc.findClosePoint(x, y)
        if self.gc.sp == -1:
            return -1
        self.gc.addPointToSelected(self.gc.sp)
        return 0

    def lineParal1(self, x, y):
        self.gc.fl = self.gc.findCloseLine(x, y)
        if self.gc.fl == -1:
            return -1
        self.gc.addLineToSelected(self.gc.fl)
        return 0

    def lineParal2(self, x, y):
        self.gc.sl = self.gc.findCloseLine(x, y)
        if self.gc.sl == -1:
            return -1
        #self.gc.addLineToSelected(self.gc.sl)
        self.gc.addLineParal(self.gc.fl, self.gc.sl)
        self.gc.dropSelected()
        return 0

    def lineOrth1(self, x, y):
        self.gc.fl = self.gc.findCloseLine(x, y)
        if self.gc.fl == -1:
            return -1
        self.gc.addLineToSelected(self.gc.fl)
        return 0

    def lineOrth2(self, x, y):
        self.gc.sl = self.gc.findCloseLine(x, y)
        if self.gc.sl == -1:
            return -1
        self.gc.addLineOrth(self.gc.fl, self.gc.sl)
        self.gc.dropSelected()
        return 0

    def lineAngle1(self, x, y):
        self.gc.fl = self.gc.findCloseLine(x, y)
        if self.gc.fl == -1:
            return -1
        self.gc.addLineToSelected(self.gc.fl)
        return 0

    def lineAngle2(self, x, y):
        self.gc.sl = self.gc.findCloseLine(x, y)
        if self.gc.fl == -1:
            return -1
        self.gc.addLineToSelected(self.gc.sl)
        return 0

    def lineHor(self, x, y):
        self.gc.fl = self.gc.findCloseLine(x, y)
        if self.gc.fl == -1:
            return -1
        self.gc.addLineHor(self.gc.fl)
        return 0

    def lineVer(self, x, y):
        self.gc.fl = self.gc.findCloseLine(x, y)
        if self.gc.fl == -1:
            return -1
        self.gc.addLineVer(self.gc.fl)
        return 0

    def pointToLine1(self, x, y):
        self.gc.fp = self.gc.findClosePoint(x, y)
        if self.gc.fp == -1:
            return -1
        self.gc.addPointToSelected(self.gc.fp)
        return 0

    def pointToLine2(self, x, y):
        self.gc.sl = self.gc.findCloseLine(x, y)
        if self.gc.sl == -1:
            return -1
        self.gc.addPointToLine(self.gc.fp, self.gc.sl)
        self.gc.dropSelected()
        return 0
    ###

    ### Функции для обработки введенного текста
    def doNothingEnter(self, arg):
        pass

    def dotDist3(self, dist_str):
        dist = float(dist_str)
        print(dist)
        self.gc.addDotDist(self.gc.fp, self.gc.sp, dist)
        print(self.gc.constraints_idxs)
        print(self.gc.constraints_values)
        self.gc.dropSelected()

    def lineAngle3(self, dist_str):
        angle = float(dist_str)
        print(angle)
        self.gc.addLineAngle(self.gc.fl, self.gc.sl, angle)
        print(self.gc.constraints_idxs)
        print(self.gc.constraints_values)
        self.gc.dropSelected()
