import numpy.random

from generateData import *
from generateItemsCorelation import generateItems

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import csv

numpy.random.seed(10)
global N
N= 32
W_max = 60
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
                    el[1][i] = 1 ^ el[1][i]

            weight = calcWeight(el[1], items)
            while weight > W_max:
                el[1] = adjustRepValue(el[1], items)
                weight = calcWeight(el[1], items)

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
    bestNowForPlotting = []
    for _ in tqdm(range(numOfGen), desc="Evolution in progress..."):
        population = doTournament(population, tournamentSize)
        population = binaryMutation(population, p_bar, p_gen_type)
        population = adjustValues(population)
        best = findBest(population)
        bestNowForPlotting.append(best[0])
        if best[0] > theBest[0]:
            theBest = best.copy()
        bestForPlotting.append(theBest[0])

    plt.plot(bestNowForPlotting, 'o', color='blue')
    plt.xlabel('number of generations')
    plt.ylabel('max value at given generation')
    plt.title('Correlated items')
    plt.show()
            # print(theBest)
        # print(best)
    return theBest

if __name__ == "__main__":
    global items

    # items = generateItems(N, False)
    items = generateItems(N, True)
    print(items)
    items_df = pd.DataFrame(items, columns=['weight', 'values'])
    items_df.to_csv('cor_items.csv', index=False)

    bests = [[] for x in range(10)]
    generations = [100, 1000, 10000]
    for gen in generations:
        for i in range(10):
            population_reps = 150
            numOfGen = gen
            tournamentSize = 3
            p_bar = 0.7  # p-nstwo braku zdarzenia mutacji
            p_gen_type = 0.9  # p-nstwo mniej zroznicowanego genotypu

            # print(W_max)
            population = generatePopulation(items, population_reps, W_max)
            # population = adjustValues(population)
            # print('first population:')
            # print(population)

            best = []
            best = findOpt(population, numOfGen, tournamentSize, p_bar, p_gen_type)

            bests[i].append(best)


            plt.plot(bestForPlotting, 'o', color='red')
            plt.xlabel('number of generations')
            plt.ylabel('max value found')
            plt.title('Correlated items')
            plt.show()
            bestForPlotting = []
    # df = pd.DataFrame(bests)
    # df.to_excel('binMut.xlsx')
    file = open('mutBin.csv', 'w+', newline='')

    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(bests)

