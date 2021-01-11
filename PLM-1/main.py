#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Считываем данные из текстового файла
data = pd.read_csv('input.csv', skipinitialspace=True)
data = data.fillna(value='-')
# Делим на позиции и переходы
places = data[data['type'] == 0].reset_index()[['name', 'n_tokens', 'out_edges']]
transitions = data[data['type'] == 1].reset_index()[['name', 'out_edges']]

# Поскольку граф двудольный, будем хранить два листа смежности
adj_list_t = {} # Для каждого перехода выходы из него
adj_list_p = {} # Для каждого перехода входы в него
state0 = np.zeros(places.shape[0]) # Начальная разметка
# Проходимся по позициям, смотрим и записываем выходы
for idx_curr, [name, out_edges_str] in transitions.iterrows():
    adj_list_t[idx_curr] = []
    adj_list_p[idx_curr] = []
    out_edges = out_edges_str.split()
    for name_i in out_edges:
        temp_df = places[places['name'] == name_i]
        if temp_df.size != 0:
            idx_to = temp_df.index[0]
            adj_list_t[idx_curr].append(idx_to)
    adj_list_t[idx_curr] = np.array(adj_list_t[idx_curr])
# Проходимся по позициям, смотрим выходы,
# Вписываем их как входы для соотв. перехода
for idx_curr, [name, n_tokens, out_edges_str] in places.iterrows():
    out_edges = out_edges_str.split()
    for name_i in out_edges:
        temp_df = transitions[transitions['name'] == name_i]
        if temp_df.size != 0:
            idx_to = temp_df.index[0]
            adj_list_p[idx_to].append(idx_curr)
    # Прописываем количество меток
    state0[idx_curr] = n_tokens
# Листы входов в массивы
for trns in adj_list_p:
    adj_list_p[trns] = np.array(adj_list_p[trns])

# Неплохо проверить, что у нас нет тупиковых переходов
for trns in adj_list_p:
    if adj_list_p[trns].size == 0:
        print('WARNING: Нет входа в переход', transitions['name'][trns])
for trns in adj_list_t:
    if adj_list_t[trns].size == 0:
        print('WARNING: Нет выхода из перехода', transitions['name'][trns])

# Массив интов (на деле бинарных) в число
def state_to_num(state):
    if state[state > 1].size > 0:
        print('WARNING: Больше одной метки в ячейке')
    state_bool = state == 1
    retval = 0
    for n, v in enumerate(np.flip(state_bool)):
        retval += np.power(2,n) * v
    return retval

# Теперь непосредственно строим граф достижимости
# Также в виде листа смежности
reach_list = {}
q = []
q.append(state0)
while(q):
    state_curr = q.pop()
    state_curr_num = state_to_num(state_curr)
    if state_curr_num not in reach_list:
        reach_list[state_curr_num] = []
    # Для текущего состояния определяем активные переходы
    active_trns = []
    for trns in adj_list_p:
        # Если во всех входах метки, переход активен
        inputs = state_curr[adj_list_p[trns]]
        if inputs.all():
            active_trns.append(trns)
    # Для каждого перехода получаем следующее состояние
    for trns in active_trns:
        state_next = state_curr.copy()
        state_next[adj_list_p[trns]] -= 1
        state_next[adj_list_t[trns]] += 1
        state_next_num = state_to_num(state_next)
        # Если еще не было такого перехода, создаем его и добавляем в очередь
        if state_next_num not in reach_list[state_curr_num]:
            reach_list[state_curr_num].append(state_next_num)
            q.append(state_next)

# Какой индекс какому состоянию соответсвует
states_list = []
for i in range(np.power(2, places.shape[0])):
    states_list.append("{0:b}".format(i).zfill(places.shape[0]))
states_list

state_descr = ''
for name in places['name']:
    state_descr += name + '|'

index_df = pd.DataFrame({
                        'num' : range(np.power(2, places.shape[0])),
                         state_descr : states_list,
                        'reachability' : False *np.power(2, places.shape[0]),
                        })
# Проходимся по графу и проставляем достижимость
for fr in reach_list:
    for to in reach_list[fr]:
        index_df.iloc[to, 2] = 1
# Отдельно проверяем начальную точку, ибо в нее может ничего не вести
index_df.iloc[state_to_num(state0), 2] = 1

# Пишем в файл индексы
index_df.sort_values(['reachability', 'num'], ascending=False).to_csv('out_index_reachability.csv', index=False)
# Пишем в файл граф
graph_df = pd.DataFrame(columns=['state', 'next'])
for idx, state in enumerate(reach_list):
    state_str = ("{0:b}".format(state).zfill(places.shape[0]))
    next_str = ''
    for next_i in reach_list[state]:
        next_str += ("{0:b}".format(next_i).zfill(places.shape[0]) + ' ')
    graph_df.loc[idx] = [state_str, next_str]
graph_df.sort_values(['state'], ascending=False).to_csv('out_graph.csv', index=False)

# Выводим в консольку
print('\n\n====================')
print('Позиции')
print(places)
print('\n\n====================')
print('Переходы')
print(transitions)
print('\n\n====================')
print('Достижимые состояния')
print(index_df[index_df['reachability'] == 1].sort_values(['num'], ascending=False))
print('\n\n====================')
print('Недостижимые состояния')
print(index_df[index_df['reachability'] == 0].sort_values(['num'], ascending=False))
print('\n\n====================')
print('Лист смежности')
print(graph_df.sort_values(['state'], ascending=False))
print('\n\n====================')
print('Тупиковые вершины')
print(graph_df[graph_df['next'] == '']['state'])
