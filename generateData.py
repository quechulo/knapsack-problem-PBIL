import numpy as np

INDEX = 305858
np.random.seed(INDEX)  # lowest index


def generateItems(N):
    items = []
    pop_weights = np.random.uniform(0.1, 1, (N, 1))
    pop_p = np.random.uniform(1, 100, (N, 1))

    for i in range(0, N):
        pop_weights[i][0] = np.round(pop_weights[i][0], 1)
        pop_p[i][0] = np.round(pop_p[i][0])
        item = [pop_weights[i][0], pop_p[i][0]]
        items.append(item)
    # print(items)
    return items


def calcWeight(rep, items):
    weight = 0
    for i in range(0, len(items)):
        weight += rep[i] * items[i][0]
    return weight


def calcValue(rep, items):
    W_max = np.round(np.sum(items, axis=0)[0] * 0.3, 1)  # max weight of knapsack
    value = 0
    for i in range(0, len(items)):
        value += rep[i] * items[i][1]
    weight = calcWeight(rep, items)
    if weight > W_max:
        return 0
    return value


def generatePopulation(items, pop_size, W_max):
    population = []

    for i in range(0, pop_size):
        rep = np.zeros(32, dtype=int).tolist()
        while calcWeight(rep, items) < 0.7 * W_max:  # first representants not the best, only around 70% good
            rep[np.random.randint(len(items))] = 1
        population.append([0, rep])
        # print(calcValue(rep, items), W_max)
    return population



if __name__ == "__main__":

    items = generateItems(32)
    W_max = np.round(np.sum(items, axis=0)[0] * 0.3, 1)  # max weight of knapsack
    print(W_max)
    print(items)
    population = generatePopulation(items, 5, W_max)
    print(population)

