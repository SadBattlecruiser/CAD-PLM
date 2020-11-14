#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geometryclass import *

class StateClass():
    def __init__(self, geometry):
        self.draw_points = True             # Отрисовывать ли точки
        self.draw_lines = True              # Отрисовывать ли линии
        self.gc = geometry
        self.setState('default')
        # Что делать с кликом в зависимости от текущего состояния
        self.click_funcs = {
            'default' : self.doNothing,
            'point_drawing' : self.pointDrawing,
            'line_drawing_1' : self.lineDrawing1,
            'line_drawing_2' : self.lineDrawing2,
            'dot_coinc_1' : self.dotCoinc1,
            'dot_coinc_2' : self.dotCoinc2
        }
        # Какое состояние следующей в зависимости от текущего состояния
        self.next_states = {
            'default' : 'default',
            'point_drawing' : 'point_drawing',
            'line_drawing_1' : 'line_drawing_2',
            'line_drawing_2' : 'line_drawing_1',
            'dot_coinc_1' : 'dot_coinc_2',
            'dot_coinc_2' : 'default'
        }
        print('StateClass constructor')

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def takeClick(self, x, y):
        func = self.click_funcs[self.state]
        func(x, y)
        self.state = self.next_states[self.state]

    ### Функции для клика
    def pointDrawing(self, x, y):
        self.gc.addPoint(x,y)

    def lineDrawing1(self, x, y):
        self.gc.ld_fp_x = x
        self.gc.ld_fp_y = y

    def lineDrawing2(self, x, y):
        self.gc.ld_sp_x = x
        self.gc.ld_sp_y = y
        self.gc.addLine(self.gc.ld_fp_x, self.gc.ld_fp_y,
                        self.gc.ld_sp_x, self.gc.ld_sp_y)

    def dotCoinc1(self, x, y):
        self.gc.dc_fp = self.gc.findClosePoint(x, y)
        self.gc.addPointToSelected(self.gc.dc_fp)


    def dotCoinc2(self, x, y):
        self.gc.dc_sp = self.gc.findClosePoint(x, y)
        self.gc.addDotCoinc(self.gc.dc_fp, self.gc.dc_sp)
        self.gc.dropSelected()

    def doNothing(self, x, y):
        pass
    ###
