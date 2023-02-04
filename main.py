import numpy as np
from numpy import random
import matplotlib.pyplot as plt

R = np.random.rand
Rn = lambda: (R - .5) * 2

Gene = ["mutation rate", "Offspring feeding", "max speed", "rand2"]
gene_index = {v : i for i, v in enumerate(Gene)}
world_diameter = 300
start_individuen = 30

class Subjekt:
    global gene_index, Gene
    @staticmethod
    def get_state():
        return {"taste": R(len(Gene)), "saturation" : R(), "health" : R(), "pos":R(2)*world_diameter, "direction" : R()*2*np.pi}

    def __init__(self, gene = R(len(Gene)), state = {} ):
        self.state = Subjekt.get_state()
        self.gene = gene
    def __radd__(self, other):
        return self.__add__(other)


    def taste_function(self, other):
        return np.sum(np.abs(self.state["taste"] - other.gene)) * np.sum(np.abs(other.state["taste"] - self.gene))

    def __add__(self, other):
        new_gene = ((.5 - R(self.gene.size)) * 2 * self.gene[self.gene_index["mutation rate"]] + self.gene)/2
        + ((.5 - R(other.gene.size)) * 2 * other.gene[other.gene_index["mutation rate"]] + other.gene) / 2

        return Subjekt(gene = new_gene, state = self.newborn_state(other))

    def newborn_state(self, other):
        random = np.random.randint(0, 2, size = (len(self.state["taste"])))
        new_state = {"taste" : np.array([self.state["taste"][i] if v != 0 else other.state["taste"][i] for i, v in enumerate(random)])}
        new_state["saturation"] = self.gene[gene_index["Offspring feeding"]]*self.state["saturation"] +  other.gene[other.gene_index["Offspring feeding"]]*other.state["saturation"]
        self.state["saturation"] -= self.gene[gene_index["Offspring feeding"]] * self.state["saturation"]
        other.state["saturation"] -= other.gene[gene_index["Offspring feeding"]] * other.state["saturation"]
        for para in ["health", "pos", "direction"]: new_state[para] = (other.state[para] + self.state[para])/2

    def direction_function(self):
        return self.state["pos"] + Rn()/5

    def stepsize_function(self):
        return self.gene[gene_index["max speed"]]


class Food:
    def __int__(self):
        self.nutrition = np.random.randint(1, 11)



t = 0
dt = 0.1
world = np.random.randint(low = 0, high = 2, size = (world_diameter, world_diameter))
x_world, y_world = np.zeros(shape=(world_diameter), dtype="int16"), np.zeros(shape=(world_diameter), dtype="int16")
Specimen = []
for _ in range(start_individuen): Specimen.append(Subjekt())

while True:
    t += dt
    for An in random.permutation(Specimen):
        stepsize = An.stepsize_function()
        An.state["pos"] += np.array([np.cos(An.state["direction"]), np.sin(An.state["direction"])])*stepsize
        An.state["saturation"] -= stepsize/10











