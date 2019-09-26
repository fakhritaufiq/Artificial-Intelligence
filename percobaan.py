# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 20:46:04 2019

@author: fakhri
"""

import random

kromosom_count = 14
gen_count = 150


def PopulasiGen(count):
    Population = []
    for i in range(count):
        krom = {
            "x1": random.uniform(-3, 3),
            "x2": random.uniform(-2, 2)
        }
        Population.append(krom)

    return Population


def Rumus(x1, x2):
    return round(((4-2.1*(x1**2)) + (x1**4//3))*(x1**2) + (x1 * x2) + (-4 + 4*(x2**2))*x2**2, 2)


def fitness(Population):
    result = []
    a = 0.1
    for i in range(kromosom_count):
        c = Population[i]
        h = Rumus(c['x1'], c['x2'])
        fit = 1 / (h + a)
        result.append({
            'x': i,
            'h': h,
            'fit': fit
        })
    return result


def Maksimalfitness(Population):
    resultmax = []
    for i in range(kromosom_count):
        h = Rumus(['x1'], ['x2'])
        fit = 1 / (h+0.1)
        resultmax.append({
            'h': h,
            'fit': fit
        })
    return resultmax


def MencariOrangtua(Population, fit_res):
    sorted_fit = sorted(fit_res, key=lambda x: x['fit'], reverse=True)
    parent1 = Population[sorted_fit[0]['x']]
    parent2 = Population[sorted_fit[1]['x']]
    return parent1, parent2


def crossover(parrent):
    p1, p2 = parrent
    i = random.randint(0, 1)
    if i != 0:
        return {
            'x1': p2['x1'],
            'x2': p1['x2']
        }
    else:
        return {
            'x1': p1['x1'],
            'x2': p2['x2']
        }


def mutasi(child):
    i = random.randint(0, 1)
    if i == 0:
        return {
            'x1': random.uniform(-3, 3),
            'x2': child['x2']
        }
    else:
        return {
            'x1': child['x1'],
            'x2': random.uniform(-2, 2)
        }


def BerhasilBerjuang(populasi, fit_res, child):

    sorted_fit = sorted(fit_res, key=lambda x: x['fit'], reverse=True)
    meninggal = sorted_fit[len(sorted_fit)-1]['x']
    populasi[meninggal] = child
    return populasi


def MencariKromosomTerbaik(populasi, fit_res):
    sorted_fit = sorted(fit_res, key=lambda x: x['h'])
    terbaik1 = Population[sorted_fit[0]['x']]
    return terbaik1


Population = PopulasiGen(kromosom_count)
for i in range(gen_count):
    fit_res = fitness(Population)
    parent = MencariOrangtua(Population, fit_res)
    child = crossover(parent)
    child = mutasi(child)
    Population = BerhasilBerjuang(Population, fit_res, child)
    Terbaik = MencariKromosomTerbaik(Population, fit_res)

print(Population)
print(" ")
print(fitness(Population))
print(" ")
print(Terbaik)
