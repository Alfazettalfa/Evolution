from numpy import random
from numpy.random import randint as RInt
import numpy as np
import json

R = random.rand
Rn = lambda: (R() - 1)*2

class Subjekt:
    global WORLD_SIZE

    @property
    def x(self):
        return int(self.state["pos"][0]) % WORLD_SIZE

    @property
    def y(self):
        return int(self.state["pos"][1]) % WORLD_SIZE

    @staticmethod
    def normalize(x):
        return x

    @staticmethod
    def get_random_state():
        return {"taste": R(len(Gene)), "saturation" : random.randint(10),
                "health" : R(), "pos":R(2)*WORLD_SIZE, "direction" : R()*2*np.pi}

    def __init__(self, gene = R(len(Gene)), state = {} ):
        self.state = Subjekt.get_random_state() if state == {} else state
        self.gene = gene
        self.dead = False

    def __radd__(self, other):
        return self.__add__(other)


    def taste_function(self, other):
        return np.sum(np.abs(self.state["taste"] - other.gene)) \
            * np.sum(np.abs(other.state["taste"] - self.gene))

    def __add__(self, other):
        new_gene = ((.5 - R(self.gene.size)) * 2 * self.gene[gene_index["mutation rate"]] + self.gene)/2
        + ((.5 - R(other.gene.size)) * 2 * other.gene[gene_index["mutation rate"]] + other.gene) / 2

        return Subjekt(gene = new_gene, state = self.newborn_state(other))

    def newborn_state(self, other):
        random = np.random.randint(0, 2, size = (len(self.state["taste"])))
        new_state = {"taste" : np.array([self.state["taste"][i] if v != 0 else other.state["taste"][i] for i, v in enumerate(random)])}
        new_state["saturation"] = self.gene[gene_index["Offspring feeding"]]*self.state["saturation"] +  other.gene[gene_index["Offspring feeding"]]*other.state["saturation"]
        self.state["saturation"] -= self.gene[gene_index["Offspring feeding"]] * self.state["saturation"]
        other.state["saturation"] -= other.gene[gene_index["Offspring feeding"]] * other.state["saturation"]
        for para in ["health", "pos", "direction"]: new_state[para] = (other.state[para] + self.state[para])/2

    def direction_function(self):
        return self.state["pos"] + Rn()/5

    def stepsize_function(self):
        return self.gene[gene_index["max speed"]]

    def encounter(self, other):
        if isinstance(other, Subjekt):
            self.encounter_equal(other)

        elif isinstance(other, Food):
            self.encounter_food(other)
        else: return

    def encounter_equal(self, other):
        return
        Paarungswahrscheinlichkeit = Subjekt.normalize(self.taste_function(other))
        if R() <= Paarungswahrscheinlichkeit:
            Specimen.append(self + other)
        return


    def encounter_food(self, food):
        if not food.dead:
            self.state["saturation"] += max([1, food.nutrition])
            food.nutrition -= max([1, food.nutrition])
        if food.nutrition <= 0:
            food.dead = True

    def update(self):
        self.state["saturation"] *= 0.9
        if self.state["saturation"] > 10:
            self.state["health"] += .1
            self.state["saturation"] -= .1
        if self.state["saturation"] < 1:
            self.state["health"] -= .03
        if self.state["health"] <= 0:
            self.dead = True

class Food:
    def __init__(self, x = random.randint(WORLD_SIZE), y = random.randint(WORLD_SIZE)):
        self.dead = False
        self.nutrition = RInt(1, 11)
        self.x, self.y = x, y