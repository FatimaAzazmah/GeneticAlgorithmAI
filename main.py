"""
Main script to run the Genetic Algorithm password cracker
"""

import os
import sys
from config import Config
from utils import Utils
from genetic_password_cracker import GeneticAlgorithmPasswordCracker
from run_experiments import main as run_experiments


def main():
    """Main function to run the program"""

    # Create necessary directories
    Utils.create_directories()

    print("=" * 60)
    print("GENETIC ALGORITHM PASSWORD CRACKER")
    print("32-bit Password Guessing Simulation")
    print("=" * 60)

    while True:
        print("\nPlease select an option:")
        print("1. Run single GA simulation with default parameters")
        print("2. Run parameter tuning experiments")
        print("3. Run multiple simulations for statistics")
        print("4. View documentation")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            run_single_simulation()
        elif choice == "2":
            run_parameter_experiments()
        elif choice == "3":
            run_multiple_simulations()
        elif choice == "4":
            show_documentation()
        elif choice == "5":
            print("\nThank you for using Genetic Algorithm Password Cracker!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


def run_single_simulation():
    """Run a single GA simulation with user-defined parameters"""

    print("\n" + "=" * 60)
    print("SINGLE SIMULATION WITH CUSTOM PARAMETERS")
    print("=" * 60)

    # Get parameters from user
    print("\nEnter GA parameters (press Enter for defaults):")

    pop_size = input(f"Population size (default {Config.DEFAULT_POPULATION_SIZE}): ")
    crossover_rate = input(f"Crossover rate (default {Config.DEFAULT_CROSSOVER_RATE}): ")
    mutation_rate = input(f"Mutation rate (default {Config.DEFAULT_MUTATION_RATE}): ")
    elitism = input(f"Elitism count (default {Config.DEFAULT_ELITISM_COUNT}): ")
    max_gens = input(f"Max generations (default {Config.MAX_GENERATIONS}): ")

    # Use defaults if input is empty
    params = Config.get_default_config()

    if pop_size:
        params['population_size'] = int(pop_size)
    if crossover_rate:
        params['crossover_rate'] = float(crossover_rate)
    if mutation_rate:
        params['mutation_rate'] = float(mutation_rate)
    if elitism:
        params['elitism_count'] = int(elitism)
    if max_gens:
        params['max_generations'] = int(max_gens)

    print("\n" + "-" * 60)
    print("Starting GA simulation with parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    print("-" * 60)

    # Create and run GA
    ga = GeneticAlgorithmPasswordCracker(
        population_size=params['population_size'],
        chromosome_length=params['chromosome_length'],
        crossover_rate=params['crossover_rate'],
        mutation_rate=params['mutation_rate'],
        elitism_count=params['elitism_count'],
        max_generations=params['max_generations']
    )

    result = ga.run()

    # Save results
    timestamp = Utils.generate_timestamp()
    ga.save_convergence_data(f'results/data/simulation_{timestamp}.csv')
    ga.plot_convergence(f'results/plots/convergence_{timestamp}.png')

    # Save summary
    summary_file = f'results/logs/summary_{timestamp}.txt'
    with open(summary_file, 'w') as f:
        f.write("GA SIMULATION SUMMARY\n")
        f.write("=" * 40 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Success: {result['success']}\n")
        f.write(f"Generations: {result.get('generations', 'N/A')}\n")
        f.write(f"Time: {result['time']:.2f} seconds\n")
        f.write(f"Target Password: {result['target_password']}\n")
        if result['success']:
            f.write(f"Found Password: {result['best_individual']}\n")
        else:
            f.write(f"Best Fitness: {result.get('best_fitness', 'N/A'):.4f}\n")

    print(f"\nResults saved to:")
    print(f"  - Data: results/data/simulation_{timestamp}.csv")
    print(f"  - Plot: results/plots/convergence_{timestamp}.png")
    print(f"  - Summary: results/logs/summary_{timestamp}.txt")


def run_parameter_experiments():
    """Run parameter tuning experiments"""

    print("\n" + "=" * 60)
    print("PARAMETER TUNING EXPERIMENTS")
    print("=" * 60)

    print("\nThis will run multiple experiments to find optimal parameters.")
    print(f"Number of runs per parameter setting: {Config.NUM_RUNS_PER_EXPERIMENT}")
    print("This may take several minutes...")

    confirm = input("\nDo you want to continue? (yes/no): ").strip().lower()

    if confirm == 'yes' or confirm == 'y':
        run_experiments()
    else:
        print("\nParameter experiments cancelled.")


def run_multiple_simulations():
    """Run multiple simulations for statistical analysis"""

    print("\n" + "=" * 60)
    print("MULTIPLE SIMULATIONS FOR STATISTICS")
    print("=" * 60)

    num_simulations = input("\nHow many simulations to run? (default: 10): ").strip()
    if not num_simulations:
        num_simulations = 10
    else:
        num_simulations = int(num_simulations)

    print(f"\nRunning {num_simulations} simulations with default parameters...")

    results = []
    success_count = 0

    for i in range(num_simulations):
        print(f"\nSimulation {i + 1}/{num_simulations}")

        ga = GeneticAlgorithmPasswordCracker(
            population_size=Config.DEFAULT_POPULATION_SIZE,
            chromosome_length=Config.PASSWORD_LENGTH,
            crossover_rate=Config.DEFAULT_CROSSOVER_RATE,
            mutation_rate=Config.DEFAULT_MUTATION_RATE,
            elitism_count=Config.DEFAULT_ELITISM_COUNT,
            max_generations=Config.MAX_GENERATIONS
        )

        result = ga.run()
        results.append(result)

        if result['success']:
            success_count += 1

    # Calculate statistics
    success_rate = (success_count / num_simulations) * 100

    if success_count > 0:
        successful_results = [r for r in results if r['success']]
        avg_generations = sum(r['generations'] for r in successful_results) / success_count
        avg_time = sum(r['time'] for r in successful_results) / success_count
    else:
        avg_generations = 0
        avg_time = 0

    # Print summary
    print("\n" + "=" * 60)
    print("STATISTICAL SUMMARY")
    print("=" * 60)
    print(f"Total simulations: {num_simulations}")
    print(f"Successful runs: {success_count}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average generations (successful): {avg_generations:.1f}")
    print(f"Average time (successful): {avg_time:.2f} seconds")

    # Save statistics
    timestamp = Utils.generate_timestamp()
    stats_file = f'results/logs/statistics_{timestamp}.txt'

    with open(stats_file, 'w') as f:
        f.write("MULTIPLE SIMULATIONS STATISTICS\n")
        f.write("=" * 40 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Number of simulations: {num_simulations}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n")
        f.write(f"Average generations: {avg_generations:.1f}\n")
        f.write(f"Average time: {avg_time:.2f} seconds\n\n")

        f.write("Individual Results:\n")
        f.write("-" * 40 + "\n")
        for i, result in enumerate(results):
            f.write(f"\nSimulation {i + 1}:\n")
            f.write(f"  Success: {result['success']}\n")
            if result['success']:
                f.write(f"  Generations: {result['generations']}\n")
                f.write(f"  Time: {result['time']:.2f} seconds\n")
            else:
                f.write(f"  Best fitness: {result.get('best_fitness', 'N/A'):.4f}\n")

    print(f"\nStatistics saved to: {stats_file}")


def show_documentation():
    """Show program documentation"""

    print("\n" + "=" * 60)
    print("DOCUMENTATION")
    print("=" * 60)

    print("""

GENETIC ALGORITHM PASSWORD CRACKER

This program simulates password cracking using Genetic Algorithms.

PROJECT STRUCTURE:
1. genetic_password_cracker.py - Main GA implementation
2. config.py - Configuration parameters
3. utils.py - Utility functions
4. run_experiments.py - Parameter tuning experiments
5. main.py - Main program interface

HOW IT WORKS:
1. Generates random 32-bit password (target)
2. Creates initial population of random guesses
3. Evolves population using selection, crossover, mutation
4. Continues until password is found or max generations reached

KEY CONCEPTS:
- Chromosome: 32-bit sequence representing a password guess
- Gene: Single bit (0 or 1) in the chromosome
- Fitness: Percentage of bits matching the target password
- Selection: Roulette wheel selection based on fitness
- Crossover: Single-point crossover between parents
- Mutation: Random bit flipping with small probability
- Elitism: Preserving best individuals for next generation

PARAMETERS TO TUNE:
1. Population size: Larger = more diversity but slower
2. Crossover rate: Higher = more exploration
3. Mutation rate: Higher = more random search
4. Elitism count: Preserves best solutions

RESULTS:
Results are saved in the 'results' directory:
- plots/: Convergence plots
- data/: CSV files with convergence data
- logs/: Text files with summaries and statistics

For more information, see the project report.
""")

    input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()