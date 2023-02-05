from copy import copy, deepcopy
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import json
from Subjektklassen import Subjekt, Food

R = np.random.rand
Rn = lambda: (R - .5) * 2

Gene = ["mutation rate", "Offspring feeding", "max speed", "rand2"]
gene_index = {v : i for i, v in enumerate(Gene)}
WORLD_SIZE = 300
START_POPULATION = 30
START_FOOD = 0




def delete_the_dead():
    dead_specimen = []
    for An in Specimen:
        if An.state["health"] <= 0:
            dead_specimen.append(An)
    for An in dead_specimen:
        Specimen.remove(An)
        world[An.x][An.y].remove(An)
        del An
    dead_Plants = []
    for P in Plants:
        if P.dead:
            dead_Plants.append(P)
    for P in dead_Plants:
        Plants.remove(P)
        world[P.x][P.y].remove(P)
        del P


t = 0
dt = 0.1
Specimen = [Subjekt() for _ in range(START_POPULATION)]
next_Specimen, next_Plants = [], []
Plants = [Food() for _ in range(START_FOOD)]
next_world = [[[]] * WORLD_SIZE] * WORLD_SIZE
while True:
    world = deepcopy(next_world)
    next_world = [[[]] * WORLD_SIZE] * WORLD_SIZE
    t += dt
    if R()<.1:
        continue
        Plants.append(Food())
    for P in Plants:
        world[P.x][P.y].append(P)

    for An in random.permutation(Specimen): #move
        stepsize = An.stepsize_function()
        An.state["pos"] += np.array([np.cos(An.state["direction"]),
                                     np.sin(An.state["direction"])])*stepsize
        An.state["saturation"] -= stepsize**2/10
        world[An.x][An.y].append(An)

    for An in Specimen:
        base = [int(An.state["pos"][k]) for k in range(2)]
        for x in range(-3, 4):
            for y in range(-3, 4):
                for other in world[(base[0] + x)%WORLD_SIZE][(base[1] + y)%WORLD_SIZE]:
                    An.encounter(other)
        An.update()

    delete_the_dead()
    try:
        print(f'Plants: {len(Plants)}, Subjects: {len(Specimen)}, '
              f'{Specimen[0].state["saturation"], Specimen[0].state["health"]}')
    except Exception as e:
        print(e)















