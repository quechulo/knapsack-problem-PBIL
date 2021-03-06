import matplotlib.pyplot as plt

from generateData import *
from generateItemsCorelation import generateItems
from random import uniform, seed
from tqdm import tqdm

global N
N= 5

def generate_population_based_on_probability(probability_vector, population_size):
    
    population_list = []
    for i in range(0, population_size):
        population_list.append(np.random.binomial(1, probability_vector))
    
    return population_list

def select_function(population_list, number_of_best_solutions, items, population_size, max_weight):
    value_list = []
    n_indexes_list = []
    for i in range(0, population_size):
        value_list.append(calcValue(population_list[i], items, max_weight))
    for i in range (0, number_of_best_solutions):
        n_indexes_list.append(np.argmax(value_list))
        value_list.pop(n_indexes_list[i])
    return n_indexes_list

def update_probability_vector(a, probability_vector, best_solutions_list, population_list, items_size):
    update_vector = np.full(items_size, 0)

    for i in best_solutions_list:
        update_vector = population_list[i] + update_vector
    updated_probability_vector = (1 - a) * probability_vector + a * (1/len(best_solutions_list)) * update_vector
    return updated_probability_vector

def mutate_population(mutation_probability, mutation_sigma, items_size, probability_vector):
    

    try_mutation = uniform(0,1)
    if(mutation_probability > try_mutation):
        probability_vector = np.random.normal(0, mutation_sigma, items_size) + probability_vector
    return probability_vector



def find_optimal(numOfGen, number_of_solutions_to_select, items, population_size, max_weight, a_parameter, probability_vector, items_size):
    absolute_best = 0
    best_population = np.zeros(population_size)
    bestForPlotting = []
    bestNowForPlotting = []

    for _ in tqdm(range(numOfGen), desc="Evolution in progress..."):
        population = generate_population_based_on_probability(probability_vector, population_size)
        best_N_solutions = select_function(population, number_of_solutions_to_select, items, population_size, max_weight)
        prob_vector = update_probability_vector(a_parameter, probability_vector, best_N_solutions, population, items_size)
        mutate_population(mutation_parameter, mutation_deviation, items_size, prob_vector)
        current_best_index = select_function(population, 1, items, population_size, max_weight)[0]
        current_best_value = calcValue(population[current_best_index], items, max_weight)

        bestNowForPlotting.append(current_best_value)

        if(current_best_value > absolute_best):
            absolute_best = current_best_value
            best_population = population[current_best_index]
        bestForPlotting.append(absolute_best)
    plt.plot(bestNowForPlotting, 'o', color='blue')
    plt.xlabel('number of generations')
    plt.ylabel('max value at given generation')
    plt.title('Correlated items')
    plt.show()
            
    return best_population, absolute_best, bestForPlotting

if __name__ == "__main__":
    N = 32
    seed(10)
    np.random.seed(10)
    items_size = N

    # items = generateItems(N, False)
    items = generateItems(N, True)
    
    items_df = pd.DataFrame(items, columns=['weight', 'values'])
    items_df.to_csv('cor_items_PBIL.csv', index=False)
    print(items)
    population_size = 150
    W_max = 60
    a_parameter = 0.2
    mutation_parameter = 0.05
    mutation_deviation = 0.15
    number_of_solutions_to_select = 2
    numOfGen = 1000

    init_probability = np.full(N, 0.5)
    print(init_probability.shape)
    bests = [[] for x in range(10)]
    generations = [10000]
    for gen in generations:
        for i in range(2):
            best_population_found_by_pbil, best_solution_found_by_pbil, bestForPlotting = find_optimal(gen, number_of_solutions_to_select, items, population_size, W_max, a_parameter, init_probability, items_size)
            bests[i].append([best_solution_found_by_pbil])
            plt.plot(bestForPlotting, 'o', color='red')
            plt.xlabel('number of generations')
            plt.ylabel('max value found')
            plt.title('Correlated items')
            plt.show()
    df = pd.DataFrame(bests)
    df.to_excel('PBIL.xlsx')