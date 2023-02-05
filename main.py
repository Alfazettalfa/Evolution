from copy import copy, deepcopy
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import json


R = np.random.rand
Rn = lambda: (R - .5) * 2
GLOBAL = {'Gene' : ['mutation rate', 'Offspring feeding', 'max speed', 'rand2'],
                    'WORLD SIZE' : 100, 'START POPULATION' : 30, 'START FOOD' : 30}
GLOBAL['Gen Index'] =  {v : i for i, v in enumerate(GLOBAL['Gene'])}

with open('GLOBALS.json', 'w') as outfile:
    json.dump(GLOBAL, outfile)
    outfile.close()
    from Subjektklassen import Subjekt, Food

def delete_the_dead():
    dead_specimen = []
    for An in Specimen:
        if An.state['health'] <= 0 or An.dead:
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

def encounter_handler(S1, S2):
    def Subjekt_to_Subjekt_handler():
        Paarungswahrscheinlichkeit = Subjekt.normalize(S1.taste_function(S2))
        if Paarungswahrscheinlichkeit >= 4:
            next_Specimen.append(S1 + S2)

    def Subjekt_to_Food_handler():
        if not S2.dead:
            S1.state['saturation'] += max([1, S2.nutrition])
            S2.nutrition -= max([1, S2.nutrition])
        if S2.nutrition <= 0:
            S2.dead = True

    if isinstance(S1, Subjekt) and isinstance(S2, Subjekt):
        return Subjekt_to_Subjekt_handler()
    elif isinstance(S2, Food) and isinstance(S1, Subjekt):
        return Subjekt_to_Food_handler()


t = 0
dt = 0.1
Specimen = [Subjekt() for _ in range(GLOBAL['START POPULATION'])]
next_Specimen, next_Plants = [], []
Plants = [Food() for _ in range(GLOBAL['START FOOD'])]
next_world_template = np.zeros(shape=(GLOBAL['WORLD SIZE'], GLOBAL['WORLD SIZE']), dtype="object")
for x in range(GLOBAL['WORLD SIZE']):
    for y in range(GLOBAL['WORLD SIZE']):
        next_world_template[x,y] = []
next_world = deepcopy(next_world_template)

while True:
    Specimen = deepcopy(Specimen) + deepcopy(next_Specimen)
    Plants = deepcopy(Plants) + deepcopy(next_Plants)
    world = deepcopy(next_world)
    next_Specimen, next_Plants = [], []
    next_world = deepcopy(next_world_template)
    Interaction_traker = {}
    for Ind in Specimen:
        Interaction_traker[Ind.ID] = []
    for P in Plants:
        Interaction_traker[P.ID] = []
    t += dt
    if R()<0:
        next_Plants.append(Food())
    for P in Plants:
        world[P.x][P.y].append(P)

    for An in Specimen: #move
        stepsize = An.stepsize_function()
        An.state['pos'] += np.array([np.cos(An.state['direction']),
                                     np.sin(An.state['direction'])])*stepsize
        An.state['saturation'] -= stepsize**2/10
        world[int(An.x)][int(An.y)].append(An)


    for Ind in Specimen:
        base = [Ind.x, Ind.y]
        for x in range(-2, 3):
            for y in range(-2, 3):
                for other in world[(base[0] + x)%GLOBAL['WORLD SIZE']][(base[1] + y)%GLOBAL['WORLD SIZE']]:
                    if not   ((other.ID in Interaction_traker[Ind.ID]) or (Ind.ID in Interaction_traker[other.ID])):

                        encounter_handler(Ind, other)
                        Interaction_traker[Ind.ID].append(other.ID)
        Ind.update()

    delete_the_dead()
    assert len(Specimen) != 0
    print(f'Plants: {len(Plants)}, Subjects: {len(Specimen)} , {len(next_Specimen)}, health: {Specimen[0].state["health"]}')
















