from generateData import *
from generateItemsCorelation import generateItems

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

global N
N= 32
W_max = 5.5
bestForPlotting = []


def adjustValues(population):
    for el in population:
        # print('adjusting value')
        el[0] = calcValue(el[1], items, W_max)
    return population


def doTournament(population, s):
    new_population = []

    for i in range(0, len(population)):
        idxs = [i]
        while(len(idxs) != s):
            idx = np.random.randint(0, len(population))
            idxs.append(idx)

        bestValue = 0
        winner = 0
        for id in idxs:
            if population[id][0] >= bestValue:
                bestValue = population[id][0]
                winner = id
        new_population.append(population[winner])
    # print(population)
    return new_population


def binaryMutation(pop, p_bar, p_gen_type=.6):
    numOfItems = len(pop[0][1])
    pop.sort(reverse=True)
    # print(numOfItems)
    for el in pop:
        p = np.random.rand()
        if p >= p_bar:
            for i in range(0, numOfItems):
                pp = np.random.rand()
                if pp >= p_gen_type:
                    # rep[i] = 1
                    el[1][i] = 1 ^ el[1][i]

            weight = calcWeight(el[1], items)
            while weight > W_max:
                el[1] = adjustRepValue(el[1], items)
                weight = calcWeight(el[1], items)
    # print(pop)
    return pop


def findBest(population):
    bestOne = 0
    bestKnapsack = []
    for el in population:
        actual = el[0]
        if actual > bestOne:
            bestOne = actual
            bestKnapsack = el[1].copy()
    # print(bestOne, bestKnapsack)
    return [bestOne, bestKnapsack]

def findOpt(population, numOfGen, tournamentSize, p_bar, p_gen_type):
    theBest = [0, np.zeros(len(population[0][1]), dtype=int).tolist()]
    for _ in tqdm(range(numOfGen), desc="Evolution in progress..."):
        population = doTournament(population, tournamentSize)
        population = binaryMutation(population, p_bar, p_gen_type)
        population = adjustValues(population)
        best = findBest(population)
        # bestForPlotting.append(best[0])
        if best[0] > theBest[0]:
            theBest = best.copy()
            bestForPlotting.append(theBest[0])
            # print(theBest)
        # print(best)
    return theBest

if __name__ == "__main__":
    global items

    # items = generateItems(N, False)
    items = generateItems(N, True)
    print(items)

    population_reps = 250
    numOfGen = 25000
    tournamentSize = 3  # for tournament select
    p_bar = 0.7  # p-nstwo braku zdarzenia mutacji
    p_gen_type = 0.95  # p-nstwo mniej zroznicowanego genotypu

    print(W_max)
    population = generatePopulation(items, population_reps, W_max)
    # population = adjustValues(population)
    print('first population:')
    print(population)

    best = []
    best = findOpt(population, numOfGen, tournamentSize, p_bar, p_gen_type)

    print("best value:", best[0])
    for i in range(0, len(items)):
        if best[1][i] == 1:
            print(items[i])
    print("best knapsack:", best[1])


    plt.plot(bestForPlotting, 'o', color='green')
    plt.show()
