"""
Parameter-tuning experiments for the Genetic Algorithm.

Each experiment sweeps one GA parameter (population size, mutation rate, or
crossover rate) across several values, runs the algorithm multiple times per
value, and reports the average generations to convergence and the success rate.
Results are written to CSV files and plotted under the `results/` directory.
"""

import csv

import matplotlib.pyplot as plt

from genetic_password_cracker import GeneticAlgorithmPasswordCracker


def experiment_population_size():
    """Study the effect of population size on convergence speed."""
    population_sizes = [50, 100, 200, 500]
    results = []

    for size in population_sizes:
        print(f"\n{'=' * 60}")
        print(f"Testing Population Size: {size}")
        print('=' * 60)

        generation_counts = []
        success_rates = []

        for run in range(5):  # 5 runs per setting
            print(f"\nRun {run + 1}/5 for population size {size}")

            ga = GeneticAlgorithmPasswordCracker(
                population_size=size,
                crossover_rate=0.8,
                mutation_rate=0.01,
                elitism_count=2,
                max_generations=1000
            )

            result = ga.run()

            if result['success']:
                generation_counts.append(result['generations'])
                success_rates.append(1)
            else:
                generation_counts.append(1000)  # generation cap
                success_rates.append(0)

            # Save convergence data for this run.
            ga.save_convergence_data(f'results/pop_size_{size}_run_{run}.csv')

        avg_generations = sum(generation_counts) / len(generation_counts)
        success_rate = sum(success_rates) / len(success_rates)

        results.append({
            'population_size': size,
            'avg_generations': avg_generations,
            'success_rate': success_rate
        })

        print(f"\nResults for population size {size}:")
        print(f"  Average generations: {avg_generations:.1f}")
        print(f"  Success rate: {success_rate:.2%}")

    # Plot the results.
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    sizes = [r['population_size'] for r in results]
    avg_gens = [r['avg_generations'] for r in results]
    plt.plot(sizes, avg_gens, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Population Size')
    plt.ylabel('Average Generations to Convergence')
    plt.title('Effect of Population Size on Convergence Speed')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    success_rates = [r['success_rate'] for r in results]
    plt.bar(sizes, success_rates, color='green', alpha=0.7)
    plt.xlabel('Population Size')
    plt.ylabel('Success Rate')
    plt.title('Effect of Population Size on Success Rate')
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('results/population_size_experiment.png', dpi=300)
    plt.show()

    # Save the results to a CSV file.
    with open('results/population_size_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Population_Size', 'Avg_Generations', 'Success_Rate'])
        for r in results:
            writer.writerow([r['population_size'], r['avg_generations'], r['success_rate']])

    return results


def experiment_mutation_rate():
    """Study the effect of mutation rate on convergence speed."""
    mutation_rates = [0.001, 0.01, 0.05, 0.1, 0.2]
    results = []

    for rate in mutation_rates:
        print(f"\n{'=' * 60}")
        print(f"Testing Mutation Rate: {rate}")
        print('=' * 60)

        generation_counts = []
        success_rates = []

        for run in range(5):
            print(f"\nRun {run + 1}/5 for mutation rate {rate}")

            ga = GeneticAlgorithmPasswordCracker(
                population_size=100,
                crossover_rate=0.8,
                mutation_rate=rate,
                elitism_count=2,
                max_generations=1000
            )

            result = ga.run()

            if result['success']:
                generation_counts.append(result['generations'])
                success_rates.append(1)
            else:
                generation_counts.append(1000)
                success_rates.append(0)

        avg_generations = sum(generation_counts) / len(generation_counts)
        success_rate = sum(success_rates) / len(success_rates)

        results.append({
            'mutation_rate': rate,
            'avg_generations': avg_generations,
            'success_rate': success_rate
        })

        print(f"\nResults for mutation rate {rate}:")
        print(f"  Average generations: {avg_generations:.1f}")
        print(f"  Success rate: {success_rate:.2%}")

    # Plot the results.
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    rates = [r['mutation_rate'] for r in results]
    avg_gens = [r['avg_generations'] for r in results]
    plt.semilogx(rates, avg_gens, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('Mutation Rate (log scale)')
    plt.ylabel('Average Generations to Convergence')
    plt.title('Effect of Mutation Rate on Convergence Speed')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    success_rates = [r['success_rate'] for r in results]
    plt.semilogx(rates, success_rates, 'go-', linewidth=2, markersize=8)
    plt.xlabel('Mutation Rate (log scale)')
    plt.ylabel('Success Rate')
    plt.title('Effect of Mutation Rate on Success Rate')
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/mutation_rate_experiment.png', dpi=300)
    plt.show()

    # Save the results.
    with open('results/mutation_rate_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Mutation_Rate', 'Avg_Generations', 'Success_Rate'])
        for r in results:
            writer.writerow([r['mutation_rate'], r['avg_generations'], r['success_rate']])

    return results


def experiment_crossover_rate():
    """Study the effect of crossover rate on convergence speed."""
    crossover_rates = [0.3, 0.5, 0.7, 0.8, 0.9, 1.0]
    results = []

    for rate in crossover_rates:
        print(f"\n{'=' * 60}")
        print(f"Testing Crossover Rate: {rate}")
        print('=' * 60)

        generation_counts = []
        success_rates = []

        for run in range(5):
            print(f"\nRun {run + 1}/5 for crossover rate {rate}")

            ga = GeneticAlgorithmPasswordCracker(
                population_size=100,
                crossover_rate=rate,
                mutation_rate=0.01,
                elitism_count=2,
                max_generations=1000
            )

            result = ga.run()

            if result['success']:
                generation_counts.append(result['generations'])
                success_rates.append(1)
            else:
                generation_counts.append(1000)
                success_rates.append(0)

        avg_generations = sum(generation_counts) / len(generation_counts)
        success_rate = sum(success_rates) / len(success_rates)

        results.append({
            'crossover_rate': rate,
            'avg_generations': avg_generations,
            'success_rate': success_rate
        })

        print(f"\nResults for crossover rate {rate}:")
        print(f"  Average generations: {avg_generations:.1f}")
        print(f"  Success rate: {success_rate:.2%}")

    # Plot the results.
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    rates = [r['crossover_rate'] for r in results]
    avg_gens = [r['avg_generations'] for r in results]
    plt.plot(rates, avg_gens, 'mo-', linewidth=2, markersize=8)
    plt.xlabel('Crossover Rate')
    plt.ylabel('Average Generations to Convergence')
    plt.title('Effect of Crossover Rate on Convergence Speed')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    success_rates = [r['success_rate'] for r in results]
    plt.plot(rates, success_rates, 'co-', linewidth=2, markersize=8)
    plt.xlabel('Crossover Rate')
    plt.ylabel('Success Rate')
    plt.title('Effect of Crossover Rate on Success Rate')
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/crossover_rate_experiment.png', dpi=300)
    plt.show()

    # Save the results.
    with open('results/crossover_rate_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Crossover_Rate', 'Avg_Generations', 'Success_Rate'])
        for r in results:
            writer.writerow([r['crossover_rate'], r['avg_generations'], r['success_rate']])

    return results


def main():
    """Run all parameter-tuning experiments."""
    print("Starting Parameter Tuning Experiments")
    print("=" * 60)

    # Create the results directory if it does not exist.
    import os
    if not os.path.exists('results'):
        os.makedirs('results')

    # Run all experiments.
    pop_results = experiment_population_size()
    mutation_results = experiment_mutation_rate()
    crossover_results = experiment_crossover_rate()

    print("\n" + "=" * 60)
    print("ALL EXPERIMENTS COMPLETED")
    print("=" * 60)

    # Find the best parameters.
    best_pop = min(pop_results, key=lambda x: x['avg_generations'])
    best_mutation = min(mutation_results, key=lambda x: x['avg_generations'])
    best_crossover = min(crossover_results, key=lambda x: x['avg_generations'])

    print("\nBest Parameters Found:")
    print(f"  Population Size: {best_pop['population_size']}")
    print(f"  Mutation Rate: {best_mutation['mutation_rate']}")
    print(f"  Crossover Rate: {best_crossover['crossover_rate']}")

    # Save the best parameters.
    with open('results/best_parameters.txt', 'w') as f:
        f.write("Best Parameters from Experiments:\n")
        f.write("=" * 40 + "\n")
        f.write(f"Population Size: {best_pop['population_size']}\n")
        f.write(f"Mutation Rate: {best_mutation['mutation_rate']}\n")
        f.write(f"Crossover Rate: {best_crossover['crossover_rate']}\n")
        f.write(f"Elitism Count: 2 (fixed)\n")


if __name__ == "__main__":
    main()