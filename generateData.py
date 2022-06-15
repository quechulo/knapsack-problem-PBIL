from ewolutionKnapsack import *
from generateItemsCorelation import generateItems



def calcWeight(rep, items):
    weight = 0.0
    for i in range(0, len(items)):
        weight += rep[i] * items[i][0]
    return weight

def calcValue(rep, items, max_weight):
    value = 0
    weight = calcWeight(rep, items)
    # if weight > W_max:
    #     return 0
    while weight > max_weight:
        rep = adjustRepValue(rep, items)
        weight = calcWeight(rep, items)
    for i in range(0, len(items)):
        value += rep[i] * items[i][1]
    return value


def adjustRepValue(rep, items):
    idx = np.random.randint(0, len(items))
    rep[idx] = 0

    return rep

def generatePopulation(items, pop_size, W_max):
    population = []

    for i in range(0, pop_size):
        rep = np.zeros(N, dtype=int).tolist()
        while calcWeight(rep, items) < 0.8 * W_max:  # first representants not the best, only around 80% good
            rep[np.random.randint(len(items))] = 1
        population.append([calcValue(rep, items, W_max), rep])

    return population


if __name__ == "__main__":

    items = generateItems(N, True)
    W_max = 5.5  # max weight of knapsack
    print(W_max)
    print(items)
    population = generatePopulation(items, 5, W_max)
    print(population)

