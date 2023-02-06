import time

from numpy import random
from numpy.random import randint as RInt
import numpy as np
import json
from decimal import Decimal


R = random.rand
Rn = lambda: (R() - 0.5)*2

with open('GLOBALS.json', 'r') as file:
    GLOBAL = json.load(file)
    file.close()

class Subjekt:
    @property
    def x(self):
        return int(self.state['pos'][0]) % GLOBAL['WORLD SIZE']

    @property
    def y(self):
        return int(self.state['pos'][1]) % GLOBAL['WORLD SIZE']

    def posf(self):
        x, y = self.state['pos']
        return np.array((Decimal(str(x)) % Decimal(str(GLOBAL['WORLD SIZE'])),
                         Decimal(str(y)) % Decimal(str(GLOBAL['WORLD SIZE']))))

    @staticmethod
    def normalize(x):
        return x

    @staticmethod
    def get_random_state():
        return {'taste': R(len(GLOBAL['Gene'])), 'saturation' : random.randint(10),
                'health' : R(), 'pos': R(2)*GLOBAL['WORLD SIZE'], 'direction' : R()*2*np.pi}

    def __init__(self, gene = [], state = {} ):
        if gene == []:
            gene = R(len(GLOBAL["Gene"]))
        self.timestamp = time.time()
        self.ID = random.randint(0, 10**6)
        self.state = Subjekt.get_random_state() if state == {} else state
        self.gene = gene
        self.dead = False

    def __radd__(self, other):
        return self.__add__(other)


    def taste_function(self, other):
        return np.sum(np.abs(self.state['taste'] - other.gene)) * \
            np.sum(np.abs(other.state['taste'] - self.gene))

    def __add__(self, other):
        new_gene = ((.5 - R(self.gene.size)) * 2 * self.gene[GLOBAL['Gen Index']['mutation rate']] + self.gene)/2
        + ((.5 - R(other.gene.size)) * 2 * other.gene[GLOBAL['Gen Index']['mutation rate']] + other.gene) / 2

        return Subjekt(gene = new_gene, state = self.newborn_state(other))

    def newborn_state(self, other):
        random = np.random.randint(0, 2, size = (len(self.state['taste'])))
        new_state = {'taste' : np.array([self.state['taste'][i]
                                         if v != 0 else other.state['taste'][i] for i, v in enumerate(random)])}
        new_state['saturation'] = self.gene[GLOBAL['Gen Index']['Offspring feeding']] * self.state['saturation'] +  other.gene[GLOBAL['Gen Index']['Offspring feeding']]*other.state['saturation']
        self.state['saturation'] -= self.gene[GLOBAL['Gen Index']['Offspring feeding']] * self.state['saturation']
        other.state['saturation'] -= other.gene[GLOBAL['Gen Index']['Offspring feeding']] * other.state['saturation']
        for para in ['health', 'pos', 'direction']: new_state[para] = (other.state[para] + self.state[para])/2
        self.state['health'] *= 0.4
        other.state['health'] *= 0.4
        return new_state

    def direction_function(self):
        return self.state['direction'] + Rn()/5

    def stepsize_function(self):
        return self.gene[GLOBAL['Gen Index']['max speed']]

    def update(self):
        self.state['saturation'] *= 0.99999
        if self.state['saturation'] > 10:
            self.state['health'] += .1
            self.state['saturation'] -= .1
        if self.state['saturation'] < 1:
            self.state['health'] -= .005
        if self.state['health'] <= 0.1:
            self.dead = True

class Food:
    def __init__(self, x = False, y = False):
        self.timestamp = time.time()
        self.ID = -1 * random.randint(0, 10 ** 6)
        self.dead = False
        self.nutrition = RInt(1, 11)
        if not x:
            self.x, self.y = random.randint(GLOBAL['WORLD SIZE'], size=(2))