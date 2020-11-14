#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

class GeometryClass():
    def __init__(self):
        self.points = np.empty([0, 2])                             # Каждая точка - x,y
        self.lines = np.empty([0, 2], dtype=int)                   # Каждая линия - p1_idx, p2_idx
        self.selected_points = np.empty([0, 2])                    # Лист выбранных точек
        self.selected_lines = np.empty([0, 2], dtype=int)          # Лист выбранных линий
        print('GeometryClass constructor')


    # Добавить точку в существующие
    def addPoint(self, x, y):
        self.points = np.vstack([self.points, [x, y]])

    # Добавить линию в существующие
    def addLine(self, x1, y1, x2, y2):
        fp_idx = self.points.shape[0]
        sp_idx = fp_idx + 1
        # Добавляем обе точки линии ко всем точкам
        #self.points = np.vstack([self.points, np.vstack([self.first_point, self.second_point])])
        self.points = np.vstack([self.points, [x1, y1], [x2, y2]])
        # Добавляем линию как индексы двух точек
        self.lines = np.vstack([self.lines, [fp_idx, sp_idx]])

    # Ближайшая существующая точка
    def findClosePoint(self, x, y):
        if (self.points.size == 0):
            print('ERROR: self.points.size == 0 in findClosePoints')
            return -1
        dist = np.sqrt(np.power(self.points[:,0] - x, 2) + np.power(self.points[:,1] - y, 2))
        return np.argmin(dist)

    # Ближайшая существующая линия
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