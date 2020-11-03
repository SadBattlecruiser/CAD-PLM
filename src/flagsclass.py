#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Просто хранилище флагов состояний
class FlagsClass():
    def __init__(self):
        self.draw_points = True             # Отрисовывать ли точки
        self.draw_lines = True              # Отрисовывать ли линии
        self.in_line_draw = False           # Рисуем ли линию прямо сейчас?
        self.line_first_point = False       # Если рисуем, первая ли это точка?
        print('FlagsClass constructor')

    def change_draw_points(self):
        if self.draw_points:
            self.draw_points = False
        else:
            self.draw_points = True
        print('draw_points ', self.draw_points)

    def change_draw_lines(self):
        if self.draw_lines:
            self.draw_lines = False
        else:
            self.draw_lines = True
        print('draw_lines ', self.draw_lines)

    def change_in_line_draw(self):
        if self.in_line_draw:
            self.in_line_draw = False
            self.line_first_point = False
        else:
            self.in_line_draw = True
            self.line_first_point = True
        print('in_line_draw ', self.in_line_draw)
