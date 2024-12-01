from main import PuzzleSolver


def simulate_puzzle():
    solver = PuzzleSolver()
    initial = solver.generateRandomState()

    print("Initial State:")
    for row in initial:
        print(row)

    # Solve with Manhattan Distance
    print("\nSolving with Manhattan Distance heuristic...")
    solver.solve(initial, solver.calculateManhattanDistance, True)

    # Solve with Hamming Distance
    print("\nSolving with Hamming Distance heuristic...")
    solver.solve(initial, solver.calculateHammingDistance, True)


if __name__ == "__main__":
    simulate_puzzle()