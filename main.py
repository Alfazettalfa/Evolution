import numpy as np
import matplotlib.pyplot as plt

R = np.random.rand

gene_index = {}
class Subjekt:
    global gene_index
    def __init__(self, gene = np.array([]), paras = {"taste": np.array([0]*10), "saturation" : R(), "health" : R()} ):
        self.gene = gene
        self.paras = paras
    def __radd__(self, other):
        return self.__add__(other)


    def taste_function(self, other):
        return np.sum(np.abs(self.paras["taste"] - other.gene)) * np.sum(np.abs(other.paras["taste"] - self.gene))

    def __add__(self, other):
        new_gene = ((.5 - R(self.gene.size)) * 2 * self.gene[self.gene_index["mutation rate"]] + self.gene)/2
        + ((.5 - R(other.gene.size)) * 2 * other.gene[other.gene_index["mutation rate"]] + other.gene) / 2

        return Subjekt(gene = new_gene, paras = self.newborn_paras(other))

    def newborn_paras(self, other):
        






