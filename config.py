"""
Configuration parameters for the Genetic Algorithm
All parameters can be easily modified here
"""


class Config:
    # Target password settings
    PASSWORD_LENGTH = 32  # 32-bit password

    # Genetic Algorithm parameters
    POPULATION_SIZES = [50, 100, 200, 500]  # For experiments
    DEFAULT_POPULATION_SIZE = 100

    CROSSOVER_RATES = [0.3, 0.5, 0.7, 0.8, 0.9, 1.0]  # For experiments
    DEFAULT_CROSSOVER_RATE = 0.8

    MUTATION_RATES = [0.001, 0.01, 0.05, 0.1, 0.2]  # For experiments
    DEFAULT_MUTATION_RATE = 0.01

    ELITISM_COUNTS = [1, 2, 5, 10]  # For experiments
    DEFAULT_ELITISM_COUNT = 2

    MAX_GENERATIONS = 1000

    # Selection methods
    SELECTION_METHODS = ['roulette', 'tournament', 'rank']
    DEFAULT_SELECTION_METHOD = 'roulette'

    # Crossover methods
    CROSSOVER_METHODS = ['single_point', 'two_point', 'uniform']
    DEFAULT_CROSSOVER_METHOD = 'single_point'

    # Experiment settings
    NUM_RUNS_PER_EXPERIMENT = 5  # Number of runs for each parameter setting

    # File paths
    RESULTS_DIR = 'results'
    PLOTS_DIR = 'results/plots'
    DATA_DIR = 'results/data'

    # Plot settings
    PLOT_FIGSIZE = (12, 6)
    PLOT_DPI = 300
    PLOT_STYLE = 'ggplot'

    # Colors for plots
    COLORS = {
        'success': '#2ecc71',
        'failure': '#e74c3c',
        'best_fitness': '#3498db',
        'avg_fitness': '#e67e22',
        'population': '#9b59b6',
        'mutation': '#1abc9c',
        'crossover': '#f1c40f'
    }

    @classmethod
    def get_experiment_parameters(cls):
        """Return all parameter combinations for experiments"""
        experiments = []

        for pop_size in cls.POPULATION_SIZES:
            for crossover_rate in cls.CROSSOVER_RATES:
                for mutation_rate in cls.MUTATION_RATES:
                    for elitism in cls.ELITISM_COUNTS:
                        experiments.append({
                            'population_size': pop_size,
                            'crossover_rate': crossover_rate,
                            'mutation_rate': mutation_rate,
                            'elitism_count': elitism
                        })

        return experiments

    @classmethod
    def get_default_config(cls):
        """Get default configuration"""
        return {
            'population_size': cls.DEFAULT_POPULATION_SIZE,
            'chromosome_length': cls.PASSWORD_LENGTH,
            'crossover_rate': cls.DEFAULT_CROSSOVER_RATE,
            'mutation_rate': cls.DEFAULT_MUTATION_RATE,
            'elitism_count': cls.DEFAULT_ELITISM_COUNT,
            'max_generations': cls.MAX_GENERATIONS,
            'selection_method': cls.DEFAULT_SELECTION_METHOD,
            'crossover_method': cls.DEFAULT_CROSSOVER_METHOD
        }