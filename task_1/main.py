import random
import heapq
import time

class PuzzleSolver:
    def __init__(self):
        pass  # No need for initialization of goal state anymore.

    def generateRandomState(self):
        """
        Function:
        - Randomly generates a 3x3 matrix which serves as initial state for 8-puzzle.
        - Makes sure that it is solvable through use of checkSolveability(self).
        Input: None.
        Output: A randomly generated, solvable 3x3 matrix.
        """
        state = list(range(9))
        while True:
            random.shuffle(state)
            matrix = [state[:3], state[3:6], state[6:]]
            if self.checkSolveability(matrix):
                return matrix

    def goalState(self):
        """
        Function:
        - Defines goal state of the 8-puzzle.
        Input: None.
        Output: A 3x3 matrix which serves as the goal state.
        """
        return [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # 0 represents the empty tile.

    def checkSolveability(self, state):
        """
        Function:
        - Checks whether randomly generated initial state is solvable.
        Input: randomly generated initial state.
        Output: A boolean response of yes or no.
        """
        flattened = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flattened)):
            for j in range(i + 1, len(flattened)):
                if flattened[i] > flattened[j]:
                    inversions += 1
        return inversions % 2 == 0

    def calculateHammingDistance(self, state):
        """
        Function:
        - Calculates Hamming distance between puzzle & goal state.
        Input: current state & goal state.
        Output: Hamming distance in the form of an integer.
        """
        goal = self.goalState()
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != goal[i][j]:
                    distance += 1
        return distance

    def calculateManhattanDistance(self, state):
        """
        Function:
        - Calculates Manhattan distance between puzzle & goal state.
        Input: current state & goal state.
        Output: Manhattan distance in the form of an integer.
        """
        goal = self.goalState()
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    value = state[i][j]
                    goal_x, goal_y = divmod(value - 1, 3)
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance

    def generateSuccessors(self, state):
        """
        Function:
        - Generates all possible successor states.
        Input: current state.
        Output: List of successor states.
        """
        successors = []
        zero_x, zero_y = [(x, y) for x in range(3) for y in range(3) if state[x][y] == 0][0]
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in moves:
            new_x, new_y = zero_x + dx, zero_y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = [row[:] for row in state]
                new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
                successors.append(new_state)

        return successors

    def solve(self, initial_state):
        """
        Function:
        - Runs A* algorithm solving the puzzle.
        Input: initial state, goal state.
        Output: List of states representing the solution path and statistics.
        """
        start_time = time.time()
        queue = []
        heapq.heappush(queue, (0, initial_state, []))  # (f(n), state, path)
        visited = set()
        nodes_expanded = 0
        goal = self.goalState()

        while queue:
            cost, current_state, path = heapq.heappop(queue)

            # Convert state to a hashable tuple for visited set
            state_tuple = tuple(tuple(row) for row in current_state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            nodes_expanded += 1
            path = path + [current_state]

            # Calculate g(n), h(n), and f(n)
            g_n = len(path) - 1  # g(n) is the number of moves from the start (cost so far)
            h_n = self.calculateManhattanDistance(current_state)  # h(n) is the Manhattan distance to goal
            f_n = g_n + h_n  # f(n) = g(n) + h(n)

            # If we have found the goal state, print the solution path and stats
            if current_state == goal:
                end_time = time.time()
                print(f"Nodes expanded: {nodes_expanded}")
                print(f"Time taken: {end_time - start_time:.4f} seconds")
                print(f"Solution Path:")

                # Now, print g(n), h(n), and f(n) for each step in the solution path
                for step, state in enumerate(path):
                    g_n = step  # g(n) = step number in the path
                    h_n = self.calculateManhattanDistance(state)  # h(n) is Manhattan distance to goal
                    f_n = g_n + h_n  # f(n) = g(n) + h(n)

                    print(f"Step {step}:")
                    for row in state:
                        print(row)
                    print(f"g(n) = {g_n}, h(n) = {h_n}, f(n) = {f_n}\n")

                return path

            # Generate successors and add to queue
            for successor in self.generateSuccessors(current_state):
                if tuple(tuple(row) for row in successor) not in visited:
                    h_cost = self.calculateManhattanDistance(successor)
                    g_cost = len(path)  # Path cost so far
                    f_cost = g_cost + h_cost
                    heapq.heappush(queue, (f_cost, successor, path))

        return None  # No solution found


# Example usage
solver = PuzzleSolver()
initial = solver.generateRandomState()
print("Initial State:")
for row in initial:
    print(row)
solution = solver.solve(initial)
