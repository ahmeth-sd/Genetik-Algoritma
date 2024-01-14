import random

# Örnek bir Fault Tree sınıfı
class FaultTree:
    def __init__(self, events):
        self.events = events

    # Örnek bir fitness fonksiyonu (değiştirilebilir)
    def fitness(self, ordering):
        fitness = sum(ordering)
        return fitness

# Genetik Algoritma Sınıfı
class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    # Başlangıç popülasyonunu oluştur
    def initialize_population(self):
        # Her birey bir olay sıralamasını temsil eder
        return [list(range(len(events))) for _ in range(self.population_size)]

    # Fitness değerlerini hesapla
    # Fitness fonksiyonunu hesapla
    def calculate_fitness(self, fault_tree, population):
        fitness_values = []

        for individual in population:
            # Fitness fonksiyonunu burada güncelle
            fitness = self.fitness_function(fault_tree, individual)

            # Fitness değeri None ise hata mesajı yazdır ve None ekleyerek diziye ekleme
            if fitness is None:
                print("Hata: Fitness fonksiyonu None değeri döndürdü.")
                return None
            else:
                fitness_values.append(fitness)

        return fitness_values

    # Fitness fonksiyonu
    def fitness_function(self, fault_tree, individual):
        # Burada, individual'ı kullanarak fault_tree'nin bir tür fitness değeri üret
        # Bu değer bir sayı veya karşılaştırılabilir bir değer olmalı
        # Eğer fitness hesaplanamazsa, None döndür
        try:
            # Örnek bir fitness hesaplama, her bir bileşenin ağırlığını toplamak
            fitness = sum(individual)
            return fitness
        except Exception as e:
            print("Hata: Fitness hesaplanırken bir hata oluştu:", str(e))
            return None

    # Turnuva seçimi
    def tournament_selection(self, population, fitness_values):
        # Rastgele iki birey seç ve fitness değerleri karşılaştır
        idx1, idx2 = random.sample(range(len(population)), 2)
        return population[idx1] if fitness_values[idx1] > fitness_values[idx2] else population[idx2]

    # Çaprazlama (sıralama tabanlı çaprazlama)
    def crossover(self, parent1, parent2):
        # Rastgele bir nokta seç ve çocukları oluştur
        crossover_point = random.randint(0, len(parent1))
        child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
        child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
        return child1, child2

    # Mutasyon (sıralama tabanlı mutasyon)
    def mutate(self, individual):
        # Rastgele iki nokta seç ve yer değiştir
        mutation_points = random.sample(range(len(individual)), 2)
        individual[mutation_points[0]], individual[mutation_points[1]] = (
            individual[mutation_points[1]],
            individual[mutation_points[0]],
        )
        return individual

    # Genetik algoritmayı çalıştır
    def run_genetic_algorithm(self, fault_tree):
        population = self.initialize_population()

        for generation in range(self.generations):
            # Fitness değerlerini hesapla
            fitness_values = self.calculate_fitness(fault_tree, population)

            # Fitness değerlerini kontrol et
            if any(value is None for value in fitness_values):
                print("Hata: Fitness fonksiyonu None değeri döndürdü.")
                return None

            # Elitizm: En iyi birey bir sonraki nesle taşınır
            best_index = fitness_values.index(max(fitness_values))
            next_generation = [population[best_index]]

            # Turnuva seçimi ve çaprazlama
            while len(next_generation) < self.population_size:
                parent1 = self.tournament_selection(population, fitness_values)
                parent2 = self.tournament_selection(population, fitness_values)
                child1, child2 = self.crossover(parent1, parent2)

                # Mutasyon uygula
                if random.random() < self.mutation_rate:
                    child1 = self.mutate(child1)
                if random.random() < self.mutation_rate:
                    child2 = self.mutate(child2)

                next_generation.extend([child1, child2])

            population = next_generation

        # En iyi bireyi bul ve döndür
        best_index = fitness_values.index(max(fitness_values))
        return population[best_index]

# Örnek kullanım
if __name__ == "__main__":
    # Fault Tree sınıfını oluştur
    events = ["Event1", "Event2", "Event3", "Event4"]
    fault_tree = FaultTree(events)

    # Genetik Algoritma sınıfını oluştur
    population_size = 10
    generations = 50
    mutation_rate = 0.2
    genetic_algorithm = GeneticAlgorithm(population_size, generations, mutation_rate)

    # Genetik algoritmayı çalıştır ve en iyi sıralamayı al
    best_ordering = genetic_algorithm.run_genetic_algorithm(fault_tree)

    if best_ordering is not None:
        print("En iyi sıralama:", best_ordering)