import random
from deap import base, creator, tools, algorithms

# Parametreler
NUM_VARIABLES = 8  # Örnek olarak 10 temel olay var sayalım
POPULATION_SIZE = 100
GENERATION_COUNT = 15
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.2

# Genetik algoritma için uygunluk fonksiyonu
def fitness(individual):
    fitness_value = calculate_fitness_value(individual)
    return (fitness_value,)

# Genetik algoritma için birey oluşturma fonksiyonu
def create_individual():
    return random.sample(range(NUM_VARIABLES), NUM_VARIABLES)

# Genetik algoritma tanımı
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def calculate_fitness_value(individual):
    # Bu örnekte, temel olayları içeren bir liste varsayıyoruz
    basic_events = [f"Event_{i}" for i in range(len(individual))]

    # Temel olayları individual listesinde belirtilen sıraya göre sırala
    ordered_events = [basic_events[i] for i in individual]

    # Fitness değerini hesapla - Örnek olarak, sıralama düzeltme maliyetini kullanalım
    fitness_value = calculate_sorting_cost(ordered_events)

    return fitness_value

def calculate_sorting_cost(ordered_events):
    # Örnek bir sıralama düzeltme maliyeti hesaplama fonksiyonu
    # Daha küçük bir maliyet, daha iyi bir uygunluk anlamına gelir
    sorting_cost = sum([abs(i - int(event.split('_')[1])) for i, event in enumerate(ordered_events)])
    return sorting_cost

def main():
    # Popülasyon oluşturma
    population = toolbox.population(n=POPULATION_SIZE)

    # Genetik algoritma ana döngüsü
    for gen in range(GENERATION_COUNT):
        offspring = algorithms.varAnd(population, toolbox, cxpb=CROSSOVER_PROBABILITY, mutpb=MUTATION_PROBABILITY)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=len(population))

        # En iyi bireyi seçme
        best_individual = tools.selBest(population, k=1)[0]
        print(f"Generation {gen + 1}, Best Individual: {best_individual}, Fitness: {best_individual.fitness.values}")

if __name__ == "__main__":
    main()
