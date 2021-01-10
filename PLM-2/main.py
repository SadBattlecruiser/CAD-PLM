#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Считываем входные данные
data = pd.read_csv('input.csv', skipinitialspace=True)
data['prev'] = data['prev'].fillna(value='-')

# Листы, куда будем складывать входные и выходные точки
# Просто так, шобы було
inputs_list = []
outputs_list = []

# Формируем граф в виде матрицы смежности
# Где нет ребра, там -1
# Нулевая вершина - начало, последняя - конец
# Для i-й работы начало - 2i+1, конец 2i+2
adj_matr = np.full([data.shape[0]*2 + 2, data.shape[0]*2 + 2], -1)
for idx, [name, duration, prev_str] in data.iterrows():
    # Работа - ребро между своим началом и концом
    adj_matr[idx*2+1, idx*2+2] = duration
    # Если нет предыдущих, то это начало работы - вход
    if prev_str == '-':
        inputs_list.append(idx*2+1)
        adj_matr[0, idx*2+1] = 0;
    # Иначе связываем концы предыдущих работ с началом этой
    else:
        for i_str in prev_str.split():
            i = int(i_str)
            adj_matr[i*2+2, idx*2+1] = 0

# Проходимся по концам работ, если нет дуги - это выход
for idx in range(1, data.shape[0]):
    if np.all(adj_matr[idx*2+2] == -1):
        outputs_list.append(idx*2+2)
        adj_matr[idx*2+2, -1] = 0

# К этому моменту граф должен быть топологически отсортирован
# Т.е. все дуги выходят из вершин с меньшими индексами
# И входят в вершины с большими

# Проходим от начала до конца, находим максимальные пути
distances = np.full(data.shape[0]*2 + 2, -1)
distances[0] = 0;
# Смотрим по очереди все вершины
for i in range(data.shape[0]*2 + 2):
    # Путь до текущей берем как максимальную сумму
    # предыдущего пути + ребра
    for j in range(i):
        if (adj_matr[j, i] != -1) and (distances[j] + adj_matr[j, i] > distances[i]):
            distances[i] = distances[j] + adj_matr[j, i]

# Проходим из конца в начало
# Смотрим по очереди все вершины
distances_b = np.full(data.shape[0]*2 + 2, distances[-1])
for i in reversed(range(data.shape[0]*2 + 2)):
    # Путь до текущей берем как минимум
    # предыдущего пути и ребра
    for j in range(i, data.shape[0]*2 + 2):
        if (adj_matr[i, j] != -1) and (distances[j] - adj_matr[i, j] < distances_b[i]):
            distances_b[i] = distances_b[j] - adj_matr[i, j];

# Выходные данные
e_sf = distances[1: -1].reshape([data.shape[0], 2])
l_sf = distances_b[1: -1].reshape([data.shape[0], 2])
out = pd.DataFrame({'name' : data['name'],
                    'duration' : data['duration'],
                    'early start' : e_sf[:, 0],
                    'late start' : l_sf[:, 0],
                    'early finish' : e_sf[:, 1],
                    'late finish' : l_sf[:, 1],
                    'time margin' : l_sf[:, 0] - e_sf[:, 0]})
out.to_csv('out.csv', index=False)

# Критический путь
crit_path_full = out[out['early start'] == out['late start']]
crit_path = pd.DataFrame({'name' : crit_path_full['name'],
                          'duration' : crit_path_full['duration'],
                          'start' : crit_path_full['early start'],
                          'finish' : crit_path_full['early finish']})
crit_path.to_csv('crit_path.csv', index=False)

# Выводим
print('Работы, составляющие критический путь:')
print(crit_path)
print('\n\nРаботы, имеющие запас по времени:')
print(out[out['early start'] != out['late start']])
