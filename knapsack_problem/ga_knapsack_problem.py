"""
Solution to Knapsack problem using genetic algorithm
"""
import random
import copy

_MIN_ITERATIONS = 50
_POPULATION = 20
_MUTATION_SPEED = 2
_MUTATION_CHROMOSOMES = 2
_REMOVAL_PERCENTAGE = 30
_MINIMUM_FITNESS = 77
_PAIRS_FOR_CROSSBREED = 8

class Item:
    """
    Represents one item for the knapsack
    """

    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

    def __repr__(self):
        return '\n' + self.name + ': ' + str(self.weight) + ', ' + str(self.value)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
      return hash(self.name)

def init_loot():
    """
    Initialises the loot
    """
    loot = []
    loot.append(Item("map", 90, 150))
    loot.append(Item("compass", 130, 35))
    loot.append(Item("water", 1530, 200))
    loot.append(Item("sandwich", 500, 160))
    loot.append(Item("glucose", 150, 60))
    loot.append(Item("tin", 680, 45))
    loot.append(Item("banana", 270, 60))
    loot.append(Item("apple", 390, 40))
    loot.append(Item("cheese", 230, 30))
    loot.append(Item("beer", 520, 10))
    loot.append(Item("suntan cream", 110, 70))
    loot.append(Item("camera", 320, 30))
    loot.append(Item("T-shirt", 240, 15))
    loot.append(Item("trousers", 480, 10))
    loot.append(Item("umbrella", 730, 40))
    loot.append(Item("waterproof trousers", 420, 70))
    loot.append(Item("waterproof overclothes", 430, 75))
    loot.append(Item("note-case ", 220, 80))
    loot.append(Item("sunglasses", 70, 20))
    loot.append(Item("towel", 180, 12))
    loot.append(Item("socks", 40, 50))
    loot.append(Item("book", 300, 10))
    loot.append(Item("notebook", 900, 1))
    loot.append(Item("tent", 2000, 150))
    return loot


def fitness_function(taken_loot):
    """
    Returns the sum of the values of the chosen loot
    """
    value_sum = 0
    for item in taken_loot:
        value_sum += item.value
    return value_sum

def random_selection(loot, weight_so_far=0):
    """
    Selects up to 5 kilograms of items
    """
    items = []
    assignment_loot = list(loot)
    while True:
        random_item = random.randint(0, len(assignment_loot)-1)
        weight_to_add = assignment_loot[random_item].weight
        if weight_so_far + weight_to_add <= 5000:
            weight_so_far += weight_to_add
            items.append(assignment_loot[random_item])
        del assignment_loot[random_item]
        if not assignment_loot:
            break
    return items

def test_weight(loot):
    """
    Returns weight of whole loot
    """
    weight = 0
    for item in loot:
        weight += item.weight
    return weight

def generate_population():
    """
    Generates initial population
    """
    population = []
    loot = init_loot()
    for i in range(_POPULATION):
        population.append(random_selection(loot))
    return population

def kill_offspring(population):
    """
    Removes _REMOVAL_PERCENTAGE part of the population with lowest value sum
    """
    part = int(len(population)*_REMOVAL_PERCENTAGE/100)
    population.sort(key=fitness_function)
    for i in range(part):
        population.pop(0)

def get_percentage(number):
    """
    Returns percentage
    """
    return int(number*100)

def rand_crossbreed(selection_a, selection_b):
    """
    Crossbreeds two selections
    """
    bucket = selection_a + selection_b
    bucket = list(set(bucket))
    return random_selection(bucket)

def mutate(selection):
    """
    Mutates a selection by removing two items and filling the remaining space
    """
    filtered_loot = filter_loot(selection)
    for i in range(_MUTATION_CHROMOSOMES):
        random_item = random.randint(0, len(selection)-1)
        del selection[random_item]
    items_to_add = random_selection(filtered_loot, test_weight(selection))
    selection.extend(items_to_add)

def calculate_fitness_percentage(selection):
    """
    Calculates the fitness percentage against max value
    """
    return get_percentage(fitness_function(selection)/fitness_function(init_loot()))

def terminate_criteria(population):
    """
    Checks if population has individual that satisfies minimum value
    """
    fitness_values = list(map(calculate_fitness_percentage, population))
    larger_than_minium = list(filter(lambda x: x >= _MINIMUM_FITNESS, fitness_values))
    if larger_than_minium:
        return larger_than_minium
    return False

def mutate_population(population):
    for i in range(_MUTATION_SPEED):
        mutatable = select(population)
        mutate(mutatable)

def genetic_algorithm(initial_population):
    """
    The algorithm
    """
    iterations = 0
    for i in range(_MIN_ITERATIONS):
        terminate_criteria(initial_population)
        crossbreed(initial_population)
        kill_offspring(initial_population)
        mutate_population(population)
        iterations+=1


def crossbreed(population):
    """
    Crossbreeds some members of the population
    """
    tmp = copy.deepcopy(population)
    for i in range(_PAIRS_FOR_CROSSBREED):
        first = select(tmp, True)
        second = select(tmp, True)
        child = rand_crossbreed(first, second)
        population.append(child)

def select(population, with_delete = False):
    index = random.randint(0, len(population)-1)
    selection = population[index]
    if with_delete:
        del population[index]
    return selection

def filter_loot(selection):
    """
    Filters loot that is not in selection
    """
    loot = set(init_loot())
    loot = loot - set(selection)
    return list(loot)

loot = init_loot()
population = generate_population()
print("Mean fitness value of beginning population: ")
mean = 0
for item in population:
    mean += fitness_function(item)
print(mean/len(population))
genetic_algorithm(population)
print("Started solution: ")
mean = 0
for item in population:
    a = fitness_function(item)
    print(a)
    mean += a
print("Mean fitness value of final population: ")
print(mean/len(population))