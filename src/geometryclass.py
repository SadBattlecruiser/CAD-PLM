#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
#from scipy.optimize import newton_krylov
#from scipy.optimize import broyden1
from scipy.optimize import *

class GeometryClass():
    def __init__(self):
        self.points = np.empty([0, 2])                      # Каждая точка - x,y
        self.lines = np.empty([0, 2], dtype=int)            # Каждая линия - p1_idx, p2_idx
        self.constraints_idxs = np.empty([0, 3], dtype=int) # Таблица ограничений (тип-idx1-idx2)
        self.constraints_values = np.empty([0, 2])          # Тут храним значения ограничений (value1-value2)
        self.selected_points = np.empty([0, 2])             # Массив выбранных точек - нужно только для gui
        self.selected_lines = np.empty([0, 2], dtype=int)   # Массив выбранных линий - нужно только для gui
        print('GeometryClass constructor')

    ### Работа с точками и линиями
    # Добавить точку в существующие
    def addPoint(self, x, y):
        self.points = np.vstack([self.points, [x, y]])
    # Добавить линию в существующие
    def addLine(self, x1, y1, x2, y2):
        fp_idx = self.points.shape[0]
        sp_idx = fp_idx + 1
        # Добавляем обе точки линии ко всем точкам
        self.points = np.vstack([self.points, [x1, y1], [x2, y2]])
        # Добавляем линию как индексы двух точек
        self.lines = np.vstack([self.lines, [fp_idx, sp_idx]])

    def addPointToSelected(self, idx):
        self.selected_points = np.vstack([self.selected_points, self.points[idx]])

    def addLineToSelected(self, idx):
        self.selected_lines = np.vstack([self.selected_lines, self.lines[idx]])

    def dropSelected(self):
        self.selected_points = np.empty([0, 2])
        self.selected_lines = np.empty([0, 2], dtype=int)

    ### Вспомогательное
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

    ### Добавляем ограничения в таблицу
    def addDotPos(self, idx, x, y):
        self.constraints_idxs = np.vstack([self.constraints_idxs , [0, idx, 0]])
        self.constraints_values = np.vstack([self.constraints_values, [x, y]])

    def addDotCoinc(self, idx1, idx2):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [1, idx1, idx2]])
        self.constraints_values = np.vstack([self.constraints_values, [0., 0.]])

    def addDotDist(self, idx1, idx2, dist):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [2, idx1, idx2]])
        self.constraints_values = np.vstack([self.constraints_values, [dist, 0.]])

    def addLineParal(self, idx1, idx2):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [3, idx1, idx2]])
        self.constraints_values = np.vstack([self.constraints_values, [0., 0.]])

    def addLineOrth(self, idx1, idx2):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [4, idx1, idx2]])
        self.constraints_values = np.vstack([self.constraints_values, [0., 0.]])

    def addLineAngle(self, idx1, idx2, angle):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [5, idx1, idx2]])
        self.constraints_values = np.vstack([self.constraints_values, [angle, 0.]])

    def addLineHor(self, idx):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [6, idx, 0]])
        self.constraints_values = np.vstack([self.constraints_values, [0., 0.]])

    def addLineVer(self, idx):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [7, idx, 0]])
        self.constraints_values = np.vstack([self.constraints_values, [0., 0.]])

    def addPointToLine(self, idx_p, idx_l):
        self.constraints_idxs  = np.vstack([self.constraints_idxs , [8, idx_p, idx_l]])
        self.constraints_values = np.vstack([self.constraints_values, [0., 0.]])

    ### Для рассчета решения
    # Для каждой точки все ограничения, в которых она участвует
    # Причем отдельно для x и для y, т.к. на кажду т. будет по две производных
    # def points_constraints_form(self):
    #     pc_ll = []
    #     for i in range(2 * self.points.shape[0]):
    #         pc_ll.append([])
    #     for i, constr_i in enumerate(self.constraints_idxs):
    #         type, idx_k, idx_l = constraint_i
    #         #val1, val2 = self.constraints_values[i]
    #



    # Непосредственно система, корни которой ищем
    def equations_func(self, l_vec):
        # Кол-во уравнений = Ndx + Ndy + Nlambd = 2*Npoints + Nconstr
        n_points = self.points.shape[0]
        n_constr = self.constraints_idxs.shape[0]
        n_eqs = n_points * 2 + n_constr
        r_vec = np.zeros(n_eqs)
        # Первыми идут производные по изменению координат
        # Они равны изменениям координат + то, что приплюсуем дальше
        r_vec[: n_points*2] = l_vec[: n_points*2]
        # Дальше для каждого ограничения отдельные уравнения
        #r_vec_cnt = 0
        for i, constr_i in enumerate(self.constraints_idxs):
            type, idx_k, idx_l = constr_i
            val1, val2 = self.constraints_values[i]
            if (type == 0):                 # Положение точки
                pass
            elif (type == 1 or type == 2):  # Расстояние между точками
                # Производная по первому иксу
                r_vec[2*idx_k] += self.Dfi2Ddxk(l_vec, idx_k, idx_l, val1, i)
                # Производная по первому игреку
                r_vec[2*idx_k+1] += self.Dfi2Ddyk(l_vec, idx_k, idx_l, val1, i)
                # Производная по второму иксу
                r_vec[2*idx_l] += self.Dfi2Ddxl(l_vec, idx_k, idx_l, val1, i)
                # Производная по второму игреку
                r_vec[2*idx_l+1] += self.Dfi2Ddyl(l_vec, idx_k, idx_l, val1, i)
                # производная по лямбде
                r_vec[2*n_points+i] = self.fi2(l_vec, idx_k, idx_l, val1)
            elif (type == 3):               # Параллелность линий
                idx_kp, idx_lp = self.lines[idx_k]
                idx_pp, idx_qp = self.lines[idx_l]
                r_vec[2*idx_kp] += self.Dfi3Ddxk(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_kp+1] += self.Dfi3Ddyk(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_lp] += self.Dfi3Ddxl(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_lp+1] += self.Dfi3Ddyl(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_pp] += self.Dfi3Ddxp(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_pp+1] += self.Dfi3Ddyp(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_qp] += self.Dfi3Ddxq(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*idx_qp+1] += self.Dfi3Ddyq(l_vec, idx_kp, idx_lp, idx_pp, idx_qp, i)
                r_vec[2*n_points+i] = self.fi3(l_vec, idx_kp, idx_lp, idx_pp, idx_qp)

            elif (type == 4):               # Перпендикулярность линий
                pass
            elif (type == 5):               # Угол между линиями
                pass
            elif (type == 6):               # Горизонтальность линии
                pass
            elif (type == 7):               # Вертикальность линии
                pass
            elif (type == 8):               # Принадлежность точки линии
                pass
        return r_vec

    # Пересчитать положения с учетом ограничений
    def satisfy_constraints(self):
        n_points = self.points.shape[0]
        n_constr = self.constraints_idxs.shape[0]
        #r_vec0 = np.linspace(0., 10., n_points*2 + n_constr)
        r_vec0 = np.zeros(n_points*2 + n_constr)
        r_vec = fsolve(self.equations_func, r_vec0)
        delta = np.reshape(r_vec[:n_points*2], [n_points, 2])
        #print(r_vec)
        #print(self.equations_func(r_vec0))
        #print(delta)
        self.points += delta

    ### Сами функции ограничений и производные
    # Расстояние между точками
    def fi2(self, l_vec, idx_k, idx_l, dist):
        xk = self.points[idx_k, 0]
        yk = self.points[idx_k, 1]
        xl = self.points[idx_l, 0]
        yl = self.points[idx_l, 1]
        return (xk-xl+l_vec[2*idx_k]-l_vec[2*idx_l])**2 + (yk-yl+l_vec[2*idx_k+1]-l_vec[2*idx_l+1])**2 - dist**2

    def Dfi2Ddxk(self, l_vec, idx_k, idx_l, dist, idx_eq):
        xk = self.points[idx_k, 0]
        xl = self.points[idx_l, 0]
        return 2 * l_vec[idx_eq] * (xk-xl+l_vec[2*idx_k]-l_vec[2*idx_l])

    def Dfi2Ddyk(self, l_vec, idx_k, idx_l, dist, idx_eq):
        yk = self.points[idx_k, 1]
        yl = self.points[idx_l, 1]
        return 2 * l_vec[idx_eq] * (yk-yl+l_vec[2*idx_k+1]-l_vec[2*idx_l+1])

    def Dfi2Ddxl(self, l_vec, idx_k, idx_l, dist, idx_eq):
        xk = self.points[idx_k, 0]
        xl = self.points[idx_l, 0]
        return -2 * l_vec[idx_eq] * (xk-xl+l_vec[2*idx_k]-l_vec[2*idx_l])

    def Dfi2Ddyl(self, l_vec, idx_k, idx_l, dist, idx_eq):
        yk = self.points[idx_k, 1]
        yl = self.points[idx_l, 1]
        return -2 * l_vec[idx_eq] * (yk-yl+l_vec[2*idx_k+1]-l_vec[2*idx_l+1])

    # Параллельность двух прямых
    def fi3(self, l_vec, idx_k, idx_l, idx_p, idx_q):
        xk = self.points[idx_k, 0]
        yk = self.points[idx_k, 1]
        xl = self.points[idx_l, 0]
        yl = self.points[idx_l, 1]
        xp = self.points[idx_p, 0]
        yp = self.points[idx_p, 1]
        xq = self.points[idx_q, 0]
        yq = self.points[idx_q, 1]
        return ((xk+l_vec[2*idx_k]-xl-l_vec[2*idx_l]) * (yp+l_vec[2*idx_p+1]-yq-l_vec[2*idx_q+1]) -
                (xp+l_vec[2*idx_p]-xq-l_vec[2*idx_q]) * (yk+l_vec[2*idx_k+1]-yl-l_vec[2*idx_l+1]))

    def Dfi3Ddxk(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        yp = self.points[idx_p, 1]
        yq = self.points[idx_q, 1]
        L = l_vec[idx_eq]
        return L * (yp+l_vec[2*idx_p+1]-yq-l_vec[2*idx_q+1])

    def Dfi3Ddyk(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        xp = self.points[idx_p, 0]
        xq = self.points[idx_q, 0]
        L = l_vec[idx_eq]
        return -L * (xp+l_vec[2*idx_p]-xq-l_vec[2*idx_q])

    def Dfi3Ddxl(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        yp = self.points[idx_p, 1]
        yq = self.points[idx_q, 1]
        L = l_vec[idx_eq]
        return -L * (yp+l_vec[2*idx_p+1]-yq-l_vec[2*idx_q+1])

    def Dfi3Ddyl(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        xp = self.points[idx_p, 0]
        xq = self.points[idx_q, 0]
        L = l_vec[idx_eq]
        return L * (xp+l_vec[2*idx_p]-xq-l_vec[2*idx_q])

    def Dfi3Ddxp(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        yk = self.points[idx_k, 1]
        yl = self.points[idx_l, 1]
        L = l_vec[idx_eq]
        return -L * (yk+l_vec[2*idx_k+1]-yl-l_vec[2*idx_l+1])

    def Dfi3Ddyp(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        xk = self.points[idx_k, 0]
        xl = self.points[idx_l, 0]
        L = l_vec[idx_eq]
        return L * (xk+l_vec[2*idx_k]-xl-l_vec[2*idx_l])

    def Dfi3Ddxq(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        yk = self.points[idx_k, 1]
        yl = self.points[idx_l, 1]
        L = l_vec[idx_eq]
        return L * (yk+l_vec[2*idx_k+1]-yl-l_vec[2*idx_l+1])

    def Dfi3Ddyq(self, l_vec, idx_k, idx_l, idx_p, idx_q, idx_eq):
        xk = self.points[idx_k, 0]
        xl = self.points[idx_l, 0]
        L = l_vec[idx_eq]
        return -L * (xk+l_vec[2*idx_k]-xl-l_vec[2*idx_l])


if __name__ == '__main__':
    print('Не туда воюешь!')
    # gc = GeometryClass()
    # gc.addPoint(100., 50.)
    # gc.addPoint(150., 30.)
    # gc.addDotDist(0, 1, 0.)
    # gc.satisfy_constraints()
    # print(gc.points)
