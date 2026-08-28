"""
Genetic Algorithm for Password-Cracking Simulation.

This module implements a Genetic Algorithm (GA) that "cracks" a randomly
generated 32-bit binary password. Each candidate solution (chromosome) is a
list of 32 bits, and the fitness of a candidate is the fraction of bits that
match the hidden target. The population is evolved with roulette-wheel
selection, single-point crossover, bit-flip mutation, and elitism until the
target is found or the maximum number of generations is reached.

Note: This is an educational simulation. The fitness function gives partial
credit for partially-correct guesses, which is what makes the search tractable;
it does not model attacking a real cryptographic hash.
"""

import random
import time
import csv
from typing import List, Tuple, Dict

import matplotlib.pyplot as plt


class GeneticAlgorithmPasswordCracker:
    """A Genetic Algorithm that evolves bit-strings to match a target password."""

    def __init__(self,
                 population_size: int = 100,
                 chromosome_length: int = 32,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.01,
                 elitism_count: int = 2,
                 max_generations: int = 1000):
        """
        Initialize the Genetic Algorithm.

        Parameters:
        - population_size: number of individuals in each generation.
        - chromosome_length: length of each chromosome (32 bits).
        - crossover_rate: probability of crossover between two parents (0-1).
        - mutation_rate: per-gene probability of a bit flip (0-1).
        - elitism_count: number of best individuals carried to the next generation.
        - max_generations: maximum number of generations before giving up.
        """
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        self.max_generations = max_generations

        # Generate the random target password (the value the GA tries to find).
        self.target_password = self.generate_random_chromosome()
        print(f"Target Password (Binary): {self.target_password}")
        print(f"Target Password (Decimal): {self.binary_to_decimal(self.target_password)}")

        # Statistics collected during the run.
        self.generation_history = []
        self.best_fitness_history = []
        self.avg_fitness_history = []

    def generate_random_chromosome(self) -> List[int]:
        """Generate a random chromosome (a sequence of 32 bits)."""
        return [random.randint(0, 1) for _ in range(self.chromosome_length)]

    def binary_to_decimal(self, chromosome: List[int]) -> int:
        """Convert a binary chromosome to its decimal value."""
        decimal = 0
        for bit in chromosome:
            decimal = (decimal << 1) | bit
        return decimal

    def initialize_population(self) -> List[List[int]]:
        """Create the initial random population."""
        return [self.generate_random_chromosome()
                for _ in range(self.population_size)]

    def fitness_function(self, chromosome: List[int]) -> float:
        """
        Fitness function: how similar a chromosome is to the target password.

        Defined as the number of matching bits divided by the total bit count,
        so the value is in [0, 1] where 1.0 means an exact match.
        """
        matches = sum(1 for i in range(self.chromosome_length)
                      if chromosome[i] == self.target_password[i])
        return matches / self.chromosome_length

    def calculate_population_fitness(self, population: List[List[int]]) -> Tuple[float, float, List[int]]:
        """Return the best fitness, average fitness, and best individual of a population."""
        fitness_scores = [self.fitness_function(individual) for individual in population]
        best_fitness = max(fitness_scores)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)
        best_individual = population[fitness_scores.index(best_fitness)]

        return best_fitness, avg_fitness, best_individual

    def selection(self, population: List[List[int]], fitness_scores: List[float]) -> List[List[int]]:
        """
        Roulette-wheel selection.

        Individuals are chosen with a probability proportional to their fitness.
        """
        total_fitness = sum(fitness_scores)

        # Guard against an all-zero-fitness population (fall back to uniform choice).
        if total_fitness == 0:
            return [random.choice(population).copy()
                    for _ in range(self.population_size - self.elitism_count)]

        probabilities = [score / total_fitness for score in fitness_scores]
        cumulative_probabilities = []
        cumulative_sum = 0

        for prob in probabilities:
            cumulative_sum += prob
            cumulative_probabilities.append(cumulative_sum)

        # Spin the wheel once per selected individual.
        selected = []
        for _ in range(self.population_size - self.elitism_count):
            r = random.random()
            for i, cum_prob in enumerate(cumulative_probabilities):
                if r <= cum_prob:
                    selected.append(population[i].copy())
                    break

        return selected

    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Single-point crossover.

        With probability `crossover_rate`, pick a random cut point and swap the
        tails of the two parents to produce two children. Otherwise the children
        are exact copies of the parents.
        """
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, self.chromosome_length - 2)

            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

            return child1, child2
        else:
            return parent1.copy(), parent2.copy()

    def mutation(self, chromosome: List[int]) -> List[int]:
        """
        Bit-flip mutation.

        Each gene is flipped (0 -> 1 or 1 -> 0) independently with
        probability `mutation_rate`.
        """
        mutated = chromosome.copy()
        for i in range(self.chromosome_length):
            if random.random() < self.mutation_rate:
                mutated[i] = 1 - mutated[i]
        return mutated

    def evolve_population(self, population: List[List[int]]) -> List[List[int]]:
        """Evolve the population by one generation."""
        fitness_scores = [self.fitness_function(ind) for ind in population]

        # Elitism: carry the best individuals over unchanged.
        elite_indices = sorted(range(len(fitness_scores)),
                               key=lambda i: fitness_scores[i],
                               reverse=True)[:self.elitism_count]
        new_population = [population[i].copy() for i in elite_indices]

        # Selection.
        selected = self.selection(population, fitness_scores)

        # Crossover and mutation.
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                parent1, parent2 = selected[i], selected[i + 1]
                child1, child2 = self.crossover(parent1, parent2)

                new_population.append(self.mutation(child1))
                new_population.append(self.mutation(child2))

        # Keep the population size constant.
        return new_population[:self.population_size]

    def run(self) -> Dict:
        """Run the Genetic Algorithm and return a result dictionary."""
        start_time = time.time()

        # Initialize the population.
        population = self.initialize_population()

        best_fitness, avg_fitness, best_individual = self.calculate_population_fitness(population)

        print(f"\nStarting Genetic Algorithm...")
        print(f"Initial Best Fitness: {best_fitness:.4f}")
        print(f"Initial Best Individual: {best_individual}")

        # Record generation 0.
        self.generation_history.append(0)
        self.best_fitness_history.append(best_fitness)
        self.avg_fitness_history.append(avg_fitness)

        # Evolution loop.
        for generation in range(1, self.max_generations + 1):
            population = self.evolve_population(population)

            best_fitness, avg_fitness, best_individual = self.calculate_population_fitness(population)

            self.generation_history.append(generation)
            self.best_fitness_history.append(best_fitness)
            self.avg_fitness_history.append(avg_fitness)

            # Print progress every 100 generations.
            if generation % 100 == 0:
                print(f"Generation {generation}: Best Fitness = {best_fitness:.4f}")

            # Check whether the password has been found.
            if best_fitness == 1.0:
                elapsed_time = time.time() - start_time
                print(f"\n[SUCCESS] Password found at generation {generation}")
                print(f"Found Password: {best_individual}")
                print(f"Time taken: {elapsed_time:.2f} seconds")

                return {
                    'success': True,
                    'generations': generation,
                    'time': elapsed_time,
                    'best_individual': best_individual,
                    'target_password': self.target_password
                }

        # Reached the generation limit without an exact match.
        elapsed_time = time.time() - start_time
        print(f"\n[FAILURE] Maximum generations reached without finding the password")
        print(f"Best fitness achieved: {best_fitness:.4f}")
        print(f"Best individual: {best_individual}")

        return {
            'success': False,
            'generations': self.max_generations,
            'time': elapsed_time,
            'best_fitness': best_fitness,
            'best_individual': best_individual,
            'target_password': self.target_password
        }

    def plot_convergence(self, save_path: str = None):
        """Plot fitness convergence and the number of correct bits over generations."""
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(self.generation_history, self.best_fitness_history,
                 'b-', linewidth=2, label='Best Fitness')
        plt.plot(self.generation_history, self.avg_fitness_history,
                 'r--', linewidth=1.5, label='Average Fitness')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Fitness Convergence')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.plot(self.generation_history,
                 [f * self.chromosome_length for f in self.best_fitness_history],
                 'g-', linewidth=2)
        plt.xlabel('Generation')
        plt.ylabel('Correct Bits')
        plt.title('Correct Bits Over Generations')
        plt.grid(True, alpha=0.3)
        plt.axhline(y=self.chromosome_length, color='r', linestyle='--', alpha=0.5,
                    label=f'Target ({self.chromosome_length} bits)')
        plt.legend()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
            plt.close()
        else:
            plt.show()

    def save_convergence_data(self, filename: str):
        """Save the convergence history to a CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Generation', 'Best_Fitness', 'Average_Fitness', 'Correct_Bits'])

            for gen, best, avg in zip(self.generation_history,
                                      self.best_fitness_history,
                                      self.avg_fitness_history):
                writer.writerow([gen, best, avg, int(best * self.chromosome_length)])


# Example usage
if __name__ == "__main__":
    # Default parameters.
    ga = GeneticAlgorithmPasswordCracker(
        population_size=100,
        chromosome_length=32,
        crossover_rate=0.8,
        mutation_rate=0.01,
        elitism_count=2,
        max_generations=1000
    )

    # Run the algorithm.
    result = ga.run()

    # Plot convergence.
    ga.plot_convergence()

    # Save the data.
    ga.save_convergence_data('convergence_data.csv')

    # Print a summary.
    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    print(f"Success: {result['success']}")
    print(f"Generations: {result.get('generations', 'N/A')}")
    print(f"Time: {result['time']:.2f} seconds")
    print(f"Target Password: {result['target_password']}")
    if result['success']:
        print(f"Found Password: {result['best_individual']}")
