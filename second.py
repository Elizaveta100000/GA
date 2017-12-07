import requests
import math
import json
import random
from random import randint
from itertools import accumulate
new=[]
best_individual=[]
f = open('34.txt', 'r')
l = f.readline()
wordList = l.split()
w_lim = int(wordList[0])
v_lim = int(wordList[1])
read_data = []
i=0
for line in f:
    pieces = line.split()
    print(pieces)
    read_data.append({'name': i, 'weight': int(pieces[0]), 'volume': float(pieces[1]), 'value': int(pieces[2])})
    i = i+1
f.closed

def fitness(individual, data):
    values, weights, volumes = 0, 0, 0
    for selected, box in zip(individual, data):
        if selected:
            values += box.get('value')
            weights += box.get('weight')
            volumes += box.get('volume')
    if weights > w_lim or volumes > v_lim:
        values = 0
    return values

# 1.2
def generate_initial_population(read_data):
    initial_population = []
    sorted_items = sorted([(ind, val)for ind, val in enumerate(read_data)], key=lambda tup: tup[1][2], reverse=True)
    for size in range(200):
        individ = [0 for _ in range(len(read_data))]
        rand = randint(0, len(read_data) - 1)
        for i in range(0, len(read_data) - 1):
            modified = individ.copy()
            modified[sorted_items[(rand + i) % 30][0]] = 1
            if fitness(modified, read_data) == 0:
                break
            else:
                individ = modified
        initial_population.append(individ)
    return initial_population

#2.1
def roulette(population, read_data):
    parents = []
    sorted_population = sorted([[ind, fitness(val, read_data), val] for ind, val in enumerate(population)], key=lambda x: x[1], reverse=True)
    for pairs in range(int(len(population) / 2)):
        pair = []
        for p in range(2):
            wheel = list(accumulate([sorted_population[ind][1] for ind in range(len(sorted_population))]))
            ball = randint(1, sum(sorted_population[ind][1] for ind in range(len(sorted_population))))
            for i in range(len(wheel)):
                if ball <= wheel[i] and ball > wheel[i] - sorted_population[i][1]:
                    pair.append(sorted_population[i][2])
                    del sorted_population[i]
                    break
        parents.append(pair)
    return parents

#3.1
def select():
    parent1=roulette()
    parent2 = roulette()
    children = cross(parent1[0], parent2[0])
    for h in children:
        new.append(h, fitness(h))
def cross(parent1,parent2):
    child1=[]
    child2=[]
    cnt=len(parent2)
    one=random.randint(0, cnt//2)
    two=random.randint(one, cnt-1)
    three=random.randint(two, cnt-1)
    for i in range(0,one):
        child1.append(parent1[i])
        child2.append(parent2[i])
    for i in range(one,two):
        child1.append(parent2[i])
        child2.append(parent1[i])
    for i in range(two, three):
        child1.append(parent1[i])
        child2.append(parent2[i])
    for i in range(three,cnt):
        child1.append(parent2[i])
        child2.append(parent1[i])
    return [child1,child2]

#4.1
def mutation(make_children):
    for i in range(len(make_children)):
        make_children[i] = ~bool(make_children[i])
    return make_children

#5.1
def new_population(parents, make_children, items):
    old = sorted([[ind, fitness(val, read_data), val] for ind, val in enumerate(parents)], key=lambda x: x[1], reverse=True)
    new = sorted([[ind, fitness(val, read_data), val] for ind, val in enumerate(make_children)], key=lambda x: x[1], reverse=True)
    for i in range(int((len(old)*0.3))):
        if (old[len(old) - 1 - i][1]) < new[i][1]:
            old[len(old) - 1 - i] = new.pop(i)
        else:
            break
    return [old[_][2] for _ in range(len(old))]

#6
def run(read_data):
    population = generate_initial_population(read_data)
    for generations in range(100):
        pairs = roulette(population, read_data)
        children = mutation(cross(pairs, read_data), read_data)
        population = new_population(population, children, read_data)
    res = sorted([val for val in population], key=lambda x: x[1], reverse=True)
    return res[0]
best_individual = run(read_data)
items = []
i=1
for item in best_individual[1]:
    if item == 1:
        items.append(i)
    i= i+1

w,v= 0,0
v=int(sum(val*read_data[ind][1] for ind, val in enumerate(best_individual)))
w=sum(val*read_data[ind][0] for ind, val in enumerate(best_individual))
vv=sum(val*read_data[ind][2] for ind, val in enumerate(best_individual))

reg_a = 'https://cit-home1.herokuapp.com/api/ga_homework'
jsargs = {
    "user":34,
    "2": {
        "value" : 4325,
        "weight" : 12879,
        "volume" : 12,
        "items" :  [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
    }

}
head = {'content-type': 'application/json'}
print()

r = requests.post(reg_a, json=jsargs,headers=head)
print(r.json())