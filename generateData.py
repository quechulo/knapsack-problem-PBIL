import numpy as np
import random
from generateItemsCorelation import generateItems

INDEX = 305862
np.random.seed(INDEX)  # lowest index
MAX_WEIGHT_PERC = 0.3  # % of sum of generated items allowed in single knapsack


def calcWeight(rep, items):
    weight = 0
    for i in range(0, len(items)):
        weight += rep[i] * items[i][0]
    return weight

def calcValue(rep, items):
    W_max = np.round(np.sum(items, axis=0)[0] * MAX_WEIGHT_PERC, 1)  # max weight of knapsack
    value = 0
    for i in range(0, len(items)):
        value += rep[i] * items[i][1]
    weight = calcWeight(rep, items)
    while weight > W_max:
        rep = adjustRepValue(rep, items)
        weight = calcWeight(rep, items)
    return value

def adjustRepValue(rep, items):
    idxs = []
    for i in range(0, len(rep)):
        if rep[i] == 1:
            idxs.append(i)
    idx = np.random.randint(0, len(idxs))
    rep[idx] = 0

    return rep

def generatePopulation(items, pop_size, W_max):
    population = []

    for i in range(0, pop_size):
        rep = np.zeros(32, dtype=int).tolist()
        while calcWeight(rep, items) < 0.8 * W_max:  # first representants not the best, only around 80% good
            rep[np.random.randint(len(items))] = 1
        population.append([calcValue(rep, items), rep])

    return population


if __name__ == "__main__":

    items = generateItems(32, False)
    W_max = np.round(np.sum(items, axis=0)[0] * 0.3, 1)  # max weight of knapsack
    print(W_max)
    print(items)
    population = generatePopulation(items, 5, W_max)
    print(population)

