from generateData import generateItems, generatePopulation, calcValue
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

N = 32
bestForPlotting = []


def adjustValues(population):
    for el in population:
        el[0] = calcValue(el[1], items)
    return population


def doTournament(population, s):
    # idxs = []
    population = adjustValues(population)
    new_population = []
    population.sort(reverse=True)

    for i in range(0, len(population)):
        idxs = []
        while(len(idxs) != s):
            idx = np.random.randint(0, len(population))
            # if idx not in idxs:
            idxs.append(idx)

        bestValue = 0
        winner = 0
        for id in idxs:
            if population[id][0] >= bestValue:
                bestValue = population[id][0]
                winner = id
        # for id in idxs:
        #     population[id] = population[winner].copy()
        new_population.append(population[winner])
    # print(population)
    return new_population

def binaryMutation(pop, p_bar, p_gen_type=.6):
    numOfItems = len(pop[0][1])
    pop.sort(reverse=True)
    # print(numOfItems)
    for el in pop[20:]:
        p = np.random.rand()
        if p >= p_bar:
            # rep = np.zeros(numOfItems, dtype=int).tolist()
            for i in range(0, numOfItems):
                pp = np.random.rand()
                if pp >= p_gen_type:
                    # rep[i] = 1
                    el[1][i] = 1 ^ el[1][i]
            # idx = np.random.randint(0, numOfItems)
            # el[1][idx] = 1 ^ el[1][idx]
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
    for _ in tqdm(range(numOfGen), desc="Loading..."):
        population = doTournament(population, tournamentSize) #  for tournament
        population = binaryMutation(population, p_bar, p_gen_type) #  for tournament
        # population = doElitarySelect(population, tournamentSize, p_bar, p_gen_type) # for elitary select
        population = adjustValues(population)
        best = findBest(population)
        bestForPlotting.append(best[0])
        if best[0] > theBest[0]:
            theBest = best.copy()
            # bestForPlotting.append(theBest[0])
            # print(theBest)
    return theBest

if __name__ == "__main__":
    global items
    items = generateItems(N)
    print(items)

    population_reps = 120
    numOfGen = 10500
    # tournamentSize = 30  # for elitary select
    tournamentSize = 2  # for tournament select
    p_bar = 0.7  # p-nstwo braku zdarzenia mutacji
    p_gen_type = 0.8  # p-nstwo mniej zroznicowanego genotypu

    W_max = np.round(np.sum(items, axis=0)[0] * 0.3, 1)  # max weight of knapsack
    print(W_max)
    population = generatePopulation(items, population_reps, W_max)
    population = adjustValues(population)
    print('first population:')
    print(population)

    #
    best = []
    best = findOpt(population, numOfGen, tournamentSize, p_bar, p_gen_type)

    print("best value:", best[0])
    for i in range(0, len(items)):
        if best[1][i] == 1:
            print(items[i])
    print("best knapsack:", best[1])


    plt.plot(bestForPlotting, 'o', color='black')
    plt.show()
