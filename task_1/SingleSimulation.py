from main import PuzzleSolver


def simulate_puzzle():
    """
    Function:   > Simulates solving 8-puzzle with both Manhattan & Hamming heuristics.
                > Generates random solvable initial state & prints state before solving.
                > Solves puzzle using both heuristics & prints solution path.
    Input:      None.
    Output:     Prints initial state, solution path, & stats (nodes expanded, execution time).
    """
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