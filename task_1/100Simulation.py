import time
import numpy as np
from main import PuzzleSolver  # Assuming PuzzleSolver is in your main.py


def run_tests():
    solver = PuzzleSolver()

    # Lists to store the results
    nodes_expanded_hamming = []
    nodes_expanded_manhattan = []
    execution_times_hamming = []
    execution_times_manhattan = []

    for _ in range(100):
        # Generate a random initial state for each test
        initial_state = solver.generateRandomState()

        # Test with Hamming Distance heuristic
        result_hamming, nodes_hamming, execution_time_hamming = solver.solve(initial_state, solver.calculateHammingDistance, False)

        # Append the correct values
        nodes_expanded_hamming.append(nodes_hamming)
        execution_times_hamming.append(execution_time_hamming)

        # Test with Manhattan Distance heuristic
        result_manhattan, nodes_manhattan, execution_time_manhattan = solver.solve(initial_state, solver.calculateManhattanDistance, False)

        # Append the correct values
        nodes_expanded_manhattan.append(nodes_manhattan)
        execution_times_manhattan.append(execution_time_manhattan)

    # Calculate statistics for both heuristics
    def calculate_statistics(nodes_expanded, execution_times):
        mean_nodes = np.mean(nodes_expanded)
        std_nodes = np.std(nodes_expanded)
        mean_time = np.mean(execution_times)
        std_time = np.std(execution_times)
        return mean_nodes, std_nodes, mean_time, std_time

    # Calculate statistics for Hamming and Manhattan heuristics
    mean_nodes_hamming, std_nodes_hamming, mean_time_hamming, std_time_hamming = calculate_statistics(
        nodes_expanded_hamming, execution_times_hamming)
    mean_nodes_manhattan, std_nodes_manhattan, mean_time_manhattan, std_time_manhattan = calculate_statistics(
        nodes_expanded_manhattan, execution_times_manhattan)

    # Print results with 3 decimal places
    print("Hamming Heuristic:")
    print(f"Total nodes expanded: {np.sum(nodes_expanded_hamming):.3f}")
    print(f"Mean of total nodes expanded: {mean_nodes_hamming:.3f}")
    print(f"Standard deviation of total nodes expanded: {std_nodes_hamming:.3f}")
    print(f"Total execution time: {np.sum(execution_times_hamming):.3f} seconds")
    print(f"Mean of execution time: {mean_time_hamming:.3f} seconds")
    print(f"Standard deviation of execution time: {std_time_hamming:.3f} seconds")

    print("\nManhattan Heuristic:")
    print(f"Total nodes expanded: {np.sum(nodes_expanded_manhattan):.3f}")
    print(f"Mean of total nodes expanded: {mean_nodes_manhattan:.3f}")
    print(f"Standard deviation of total nodes expanded: {std_nodes_manhattan:.3f}")
    print(f"Total execution time: {np.sum(execution_times_manhattan):.3f} seconds")
    print(f"Mean of execution time: {mean_time_manhattan:.3f} seconds")
    print(f"Standard deviation of execution time: {std_time_manhattan:.3f} seconds")


if __name__ == "__main__":
    run_tests()
