import random

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def distance_to(self, other_city):
        dx = self.x - other_city.x
        dy = self.y - other_city.y
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        return distance

    def __str__(self):
        return self.name
    
class World:
    def __init__(self, population_size):
        self.population_size = population_size
        self.cities = []
        self.tours = []

    def add_city(self, city):
        self.cities.append(city)

    def generate_initial_population(self):
        for _ in range(self.population_size):
            tour = self.random_tour()
            self.tours.append(tour)

    def random_tour(self):
        tour = self.cities.copy()
        random.shuffle(tour)
        return tour

    def calculate_tour_distance(self, tour):
        distance = 0
        num_cities = len(tour)
        for i in range(num_cities):
            distance += tour[i].distance_to(tour[(i + 1) % num_cities])
        return distance

    def get_best_tour(self):
        best_tour = min(self.tours, key=self.calculate_tour_distance)
        return best_tour
    
    def evolve_population(self):
        new_population = []
        # Elitism: Add the best tour from the previous generation to the new population
        best_tour = self.get_best_tour()
        new_population.append(best_tour)
        for _ in range(self.population_size):
            parent1, parent2 = self.tournament_selection(2)
            offspring = self.ordered_crossover(parent1, parent2)
            self.mutate(offspring)
            new_population.append(offspring)
        self.tours = new_population

    def tournament_selection(self, num_parents):
        selected_parents = []
        for _ in range(num_parents):
            tournament_population = random.sample(self.tours, 5)
            best_tour = min(tournament_population, key=self.calculate_tour_distance)
            selected_parents.append(best_tour)
        return selected_parents

    def ordered_crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end + 1] = parent1[start:end + 1]
        for i in range(size):
            if parent2[i] not in child:
                for j in range(size):
                    if child[j] == -1:
                        child[j] = parent2[i]
                        break
        return child

    def mutate(self, tour):
        size = len(tour)
        idx1, idx2 = random.sample(range(size), 2)
        tour[idx1], tour[idx2] = tour[idx2], tour[idx1]

    def best_tour_path(self):
        return ' -> '.join(str(city.name) for city in self.get_best_tour())

def main():
    num_cities = 15
    population_size = 100
    num_generations = 300

    world = World(population_size)

    # Create cities
    for i in range(num_cities):
        city = City(f"City {i+1}", random.randint(0, 1000), random.randint(0, 1000))
        world.add_city(city)

    # Generate initial population
    world.generate_initial_population()
    # Evolution loop
    for generation in range(num_generations):
        # Perform evolution
        world.evolve_population()

        # Print the best tour distance in each generation
        best_distance = world.calculate_tour_distance(world.get_best_tour())
        print(f"Generation {generation + 1}: Best Distance = {best_distance}")

    # Find the best tour in the final population
    best_tour = world.get_best_tour()
    best_distance = world.calculate_tour_distance(best_tour)
    best_tour_path = world.best_tour_path()
    print("\nOptimal Solution:")
    print(f"Best Tour: {best_tour_path}")
    print(f"Best Distance: {best_distance}")


if __name__ == "__main__":
    main()