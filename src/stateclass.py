#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geometryclass import *

class StateClass():
    def __init__(self, geometry):
        self.draw_points_ = True             # Отрисовывать ли точки
        self.draw_lines_ = True              # Отрисовывать ли линии
        self.gc = geometry
        # Что делать с кликом в зависимости от текущего состояния
        self.click_funcs = {
            'default' : self.doNothing,
            'point_drawing' : self.pointDrawing,
            'line_drawing_1' : self.lineDrawing1,
            'line_drawing_2' : self.lineDrawing2,
        }
        # Какое состояние следующей в зависимости от текущего состояния
        self.next_states = {
            'default' : 'default',
            'point_drawing' : 'point_drawing',
            'line_drawing_1' : 'line_drawing_2',
            'line_drawing_2' : 'line_drawing_1',
        }
        #self.setDefaultState()
        self.setState('default')
        print('StateClass constructor')

    def getState(self):
        return self.state_

    def setState(self, state):
        self.state_ = state

    def takeClick(self, x, y):
        func = self.click_funcs[self.state_]
        func(x, y)
        self.state_ = self.next_states[self.state_]

    ### Функции для клика
    def pointDrawing(self, x, y):
        self.gc.addPoint(x,y)


    def lineDrawing1(self, x, y):
        self.gc.ld_fp_x_ = x
        self.gc.ld_fp_y_ = y

    def lineDrawing2(self, x, y):
        self.gc.ld_sp_x_ = x
        self.gc.ld_sp_y_ = y
        self.gc.addLine(self.gc.ld_fp_x_, self.gc.ld_fp_y_,
                        self.gc.ld_sp_x_, self.gc.ld_sp_y_)

    def doNothing(self, x, y):
        pass
    ###

    ### Функции для кнопок
    def change_draw_points(self):
        if self.draw_points_:
            self.draw_points_ = False
        else:
            self.draw_points_ = True
        print('draw_points_ ', self.draw_points_)

    def change_draw_lines(self):
        if self.draw_lines_:
            self.draw_lines_ = False
        else:
            self.draw_lines_ = True
        print('draw_lines_ ', self.draw_lines_)
