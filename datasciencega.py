# -*- coding: utf-8 -*-
"""DataScienceGA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TJ4yD5jh9JjLBxu3uvLFIsegwxf4ngoP
"""

import random
import pandas as pd

df = pd.read_csv("Data Latih.csv", sep=";")
print(df)

SUHU = ['Rendah', 'Normal', 'Tinggi']
WAKTU = ['Pagi', 'Siang', 'Sore', 'Malam']
KONDISI = ['Cerah', 'Berawan', 'Rintik', 'Hujan'] 
KELEMBAPAN = ['Rendah', 'Normal', 'Tinggi']
TERBANG = ['Ya']

bit_count = 15
data = df.values

def checkrule(kolom, rule, value):
  i = kolom.index(value)
  return rule[i] == 1

# Tes Check rule
# print(checkrule(SUHU, [1, 0, 0], 'Rendah'))

def gen_population(count):
  populations = []
  for i in range(count):
    chromosome = []
    for b in range(bit_count):
      chromosome.append(random.randint(0, 1))
    populations.append(chromosome)
  
  return populations

# choromosome_count = 5
# populations = gen_population(choromosome_count)
# populations

def split_chromosome(l, n):
  return [l[i:i + n] for i in range(0, len(l), n)]

def predict(chromosome, data):
  rules = split_chromosome(chromosome, bit_count)
  for rule in rules:
    suhu_enc = rule[0:3]
    waktu_enc = rule[3:7]
    kond_enc = rule[7:11]
    kel_enc = rule[11:14]
    terbang_enc = rule[14]

    if checkrule(SUHU, suhu_enc, data[0]) and checkrule(WAKTU, waktu_enc, data[1]) and checkrule(KONDISI, kond_enc, data[2]) and checkrule(KELEMBAPAN, kel_enc, data[3]):
      if terbang_enc == 1:
        return 'Ya'
      else:
        return 'Tidak'
  return '-'

# chromosome = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
# print(predict(chromosome, ['Rendah', 'Siang', 'Cerah', 'Rendah']))

def fitness(populations):
  result = []
  for i in range(choromosome_count):
    chromosome = populations[i]
    true_predict = 0
    for d in data:
      hasil = predict(chromosome, d)
      if hasil == d[4]:
        true_predict += 1
    
    result.append({
        'index': i,
        'fit': true_predict / len(data)
    })
  return result

def get_parrent(populations, fit_res):
  sorted_fit = sorted(fit_res, key=lambda x: x['fit'], reverse=True) 
  parent1 = populations[sorted_fit[0]['index']]
  parent2 = populations[sorted_fit[1]['index']]
  return parent1, parent2

def roundup(n):
    # Smaller multiple 
    a = (n // bit_count) * bit_count; 
      
    # Larger multiple 
    b = a + bit_count; 

    return b

def rounddown(n):
    return (n // bit_count) * bit_count

def crossover(parrent, p = 0.8):
  p1, p2 = parrent
  
  prob = random.uniform(0, 1)
  if prob > p:
    return [p1[:], p2[:]]
  
  if len(p1) > len(p2):
    p1, p2 = p2, p1

  p1_s = [
          random.randint(0, len(p1)//2), 
          random.randint(len(p1)//2, len(p1))
        ]

  p2_arr = []

  p1_length = p1_s[1] - p1_s[0]
  p1_gap = p1_length % bit_count

  # Varian 1
  p2_1 = [p1_s[0], p1_s[0] + p1_length]
  if p2_1 not in p2_arr:
    p2_arr.append(p2_1)
  
  # Varian 2
  p2_2 = [p1_s[0], p1_s[0] + p1_gap]
  if p2_2 not in p2_arr:
    p2_arr.append(p2_2)
  
  # Varian 3
  p2_3 = [p1_s[1] - p1_length, p1_s[1]]
  if p2_3 not in p2_arr:
    p2_arr.append(p2_3)

  # Varian 4  
  p2_4 = [p1_s[1] - p1_gap, p1_s[1]]
  if p2_4 not in p2_arr:
    p2_arr.append(p2_4)

  selected_index = random.randint(0, len(p2_arr)-1)
  p2_s = p2_arr[selected_index]
  
  # Child 1
  kiri = p1[rounddown(p2_s[0]):p2_s[0]]
  tengah = p2[p2_s[0]:p2_s[1]]
  kanan = p1[p2_s[1]:roundup(p2_s[1])]
  child1 = kiri + tengah + kanan

  # Child 2
  kiri = p2[0:p2_s[0]]
  tengah = p1[p1_s[0]:p1_s[1]]
  kanan = p2[p2_s[1]:]

  child2 = kiri + tengah + kanan

  return [child1, child2]

def mutation(child, p = 0.2):
  for i in range(len(child[0])):
    prob = random.uniform(0, 1)
    if prob < p:
      if child[0][i] == 0:
        child[0][i] = 1
      else:
        child[0][i] = 0

  for i in range(len(child[1])):
    prob = random.uniform(0, 1)
    if prob < p:
      if child[1][i] == 0:
        child[1][i] = 1
      else:
        child[1][i] = 0
    
  return child

def survivor_selecton(populasi, fit_res, child):
  """
  Akan menghasilkan populasi baru dari parameter populasi, berdasarkan fit_res
  """
  sorted_fit = sorted(fit_res, key=lambda x: x['fit'], reverse=True)
  i1 = sorted_fit[len(sorted_fit)-1]['index']
  i2 = sorted_fit[len(sorted_fit)-2]['index']
  populasi[i1] = child[0]
  populasi[i2] = child[1]
  return populasi

# GENETIC ALGORITHM
choromosome_count = 10
gen_count = 1000
populations = gen_population(choromosome_count)
for i in range(gen_count):
  fit_res = fitness(populations)
  parent = get_parrent(populations, fit_res)
  child = crossover(parent, 0.8)
  child = mutation(child, 0.2)
  populations = survivor_selecton(populations, fit_res, child)

  if i % 100 == 0:
    fit = fitness(populations)
    sorted_fit = sorted(fit, key=lambda x: x['fit'], reverse=True)
    print("Akurasi: ", sorted_fit[0]['fit'])

fit = fitness(populations)
sorted_fit = sorted(fit, key=lambda x: x['fit'], reverse=True)
optimum = sorted_fit[0]
optimum_chromosome = populations[optimum['index']]

optimum

print(len(optimum_chromosome))

df_test = pd.read_csv("Data Uji.csv", sep=";")
data_test = df_test.values

for d in data_test:
  hasil = predict(optimum_chromosome, d)
  print(hasil)

