#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Просто хранилище флагов состояний
class FlagsClass():
    def __init__(self):
        self.draw_points = True             # Отрисовывать ли точки
        self.draw_lines = True              # Отрисовывать ли линии
        self.reset_state()
        print('FlagsClass constructor')

    # Выставить флаги происходящих сейчас событий в дефолтные
    def reset_state(self):
        self.in_line_draw = False           # Рисуем ли линию прямо сейчас?
        self.line_first_point = False       # Если рисуем, первая ли это точка?
        self.in_point_pos = False           # Задаем ли ограничения на положения точки?
        self.in_select_point = False        # Выбираем ли сейчас точку?
        self.in_line_pos = False            # Задаем ли ограничения на положения точки?
        self.in_select_line = False         # Выбираем ли сейчас линию?

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
        temp = self.in_line_draw
        self.reset_state()
        if not temp:
            self.in_line_draw = True
            self.line_first_point = True
        print('in_line_draw ', self.in_line_draw)

    def change_in_point_pos(self):
        temp = self.in_point_pos
        self.reset_state()
        if not temp:
            self.in_point_pos = True
            self.in_select_point = True
        print('in_point_pos ', self.in_point_pos)

    def change_in_line_pos(self):
        temp = self.in_line_pos
        self.reset_state()
        if not temp:
            self.in_line_pos = True
            self.in_select_line = True
        print('in_line_pos ', self.in_line_pos)
