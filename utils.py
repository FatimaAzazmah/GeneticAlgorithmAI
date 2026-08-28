"""
Utility functions for the Genetic Algorithm project
"""

import math
import time
import random
from typing import List, Dict, Any
from datetime import datetime

import matplotlib.pyplot as plt


class Utils:

    @staticmethod
    def generate_random_bits(length: int) -> List[int]:
        """Generate random binary sequence of given length"""
        return [random.randint(0, 1) for _ in range(length)]

    @staticmethod
    def binary_to_decimal(binary_list: List[int]) -> int:
        """Convert binary list to decimal number"""
        decimal = 0
        for bit in binary_list:
            decimal = (decimal << 1) | bit
        return decimal

    @staticmethod
    def decimal_to_binary(decimal: int, length: int) -> List[int]:
        """Convert decimal number to binary list of specified length"""
        binary = []
        for _ in range(length):
            binary.append(decimal & 1)
            decimal >>= 1
        return binary[::-1]  # Reverse to get correct order

    @staticmethod
    def hamming_distance(seq1: List[int], seq2: List[int]) -> int:
        """Calculate Hamming distance between two binary sequences"""
        if len(seq1) != len(seq2):
            raise ValueError("Sequences must have same length")

        distance = 0
        for bit1, bit2 in zip(seq1, seq2):
            if bit1 != bit2:
                distance += 1
        return distance

    @staticmethod
    def calculate_similarity(seq1: List[int], seq2: List[int]) -> float:
        """Calculate similarity percentage between two sequences"""
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
        return (matches / len(seq1)) * 100

    @staticmethod
    def calculate_entropy(binary_list: List[int]) -> float:
        """Calculate Shannon entropy of binary sequence"""
        if not binary_list:
            return 0

        total = len(binary_list)
        count_0 = binary_list.count(0)
        count_1 = total - count_0

        p0 = count_0 / total
        p1 = count_1 / total

        entropy = 0
        if p0 > 0:
            entropy -= p0 * math.log2(p0)
        if p1 > 0:
            entropy -= p1 * math.log2(p1)

        return entropy

    @staticmethod
    def fitness_to_percentage(fitness: float) -> str:
        """Convert fitness value to percentage string"""
        return f"{fitness * 100:.2f}%"

    @staticmethod
    def format_time(seconds: float) -> str:
        """Format seconds to human readable time"""
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.2f} hours"

    @staticmethod
    def generate_timestamp() -> str:
        """Generate timestamp string for filenames"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def create_directories():
        """Create necessary directories for results"""
        import os

        directories = [
            'results',
            'results/plots',
            'results/data',
            'results/logs'
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def save_results_to_json(results: Dict[str, Any], filename: str):
        """Save results to JSON file"""
        import json

        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)

    @staticmethod
    def load_results_from_json(filename: str) -> Dict[str, Any]:
        """Load results from JSON file"""
        import json

        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def plot_comparison(data_dict: Dict[str, List[float]],
                        title: str,
                        xlabel: str,
                        ylabel: str,
                        save_path: str = None):
        """Create comparison plot for multiple datasets"""
        plt.figure(figsize=(10, 6))

        for label, data in data_dict.items():
            plt.plot(range(len(data)), data, label=label, linewidth=2)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    @staticmethod
    def create_box_plot(data_dict: Dict[str, List[float]],
                        title: str,
                        ylabel: str,
                        save_path: str = None):
        """Create box plot for comparing distributions"""
        plt.figure(figsize=(10, 6))

        labels = list(data_dict.keys())
        data = list(data_dict.values())

        plt.boxplot(data, labels=labels)
        plt.xlabel('Parameter Setting')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    @staticmethod
    def print_progress_bar(iteration: int,
                           total: int,
                           prefix: str = '',
                           suffix: str = '',
                           length: int = 50,
                           fill: str = '█'):
        """Print progress bar to console"""
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')

        if iteration == total:
            print()

    @staticmethod
    def timer_decorator(func):
        """Decorator to measure function execution time"""

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"\n{func.__name__} executed in {end_time - start_time:.4f} seconds")
            return result

        return wrapper

    @staticmethod
    def validate_chromosome(chromosome: List[int], length: int) -> bool:
        """Validate chromosome format"""
        if len(chromosome) != length:
            return False

        for gene in chromosome:
            if gene not in [0, 1]:
                return False

        return True

    @staticmethod
    def calculate_diversity(population: List[List[int]]) -> float:
        """Calculate genetic diversity of population"""
        if len(population) <= 1:
            return 0

        total_distance = 0
        count = 0

        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                total_distance += Utils.hamming_distance(population[i], population[j])
                count += 1

        return total_distance / count if count > 0 else 0


# Example usage
if __name__ == "__main__":
    # Test utility functions
    utils = Utils()

    # Test binary conversions
    test_bits = [1, 0, 1, 1, 0, 1]
    decimal = utils.binary_to_decimal(test_bits)
    print(f"Binary {test_bits} -> Decimal: {decimal}")

    # Test Hamming distance
    seq1 = [1, 0, 1, 0, 1]
    seq2 = [1, 1, 1, 0, 0]
    distance = utils.hamming_distance(seq1, seq2)
    print(f"Hamming distance: {distance}")

    # Test similarity
    similarity = utils.calculate_similarity(seq1, seq2)
    print(f"Similarity: {similarity:.2f}%")

    # Test entropy
    entropy = utils.calculate_entropy(test_bits)
    print(f"Entropy: {entropy:.4f}")