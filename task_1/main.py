import random
import heapq
import time


class PuzzleSolver:
    def __init__(self):
        pass  # No need for initialisation of goal state anymore.

    def generateRandomState(self):
        """
        Function:   Randomly generates a 3x3 matrix for 8-puzzle & ensures solvability.
        Input:      None.
        Output:     Solvable 3x3 matrix representing initial state of puzzle.
        """
        state = list(range(9)) # List from 0 to 8
        while True:
            random.shuffle(state) # Randomly shuffle
            matrix = [state[:3], state[3:6], state[6:]] # Convert to 3x3 matrix
            if self.checkSolvability(matrix): # Check solvability
                return matrix

    def goalState(self):
        """
        Function:   Defines goal state of 8-puzzle.
        Input:      None.
        Output:     3x3 matrix representing goal state where 0 is empty tile.
        """
        return [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]  # 0 represents empty tile

    def checkSolvability(self, state):
        """
        Function:   Checks if given state is solvable based on inversions
                    (inversion = tile pair where larger-numbered tile is before smaller-numbered in flattened list).
        Input:      3x3 matrix representing current state.
        Output:     Boolean value (True if solvable, False if not).
        """
        flattened = [num for row in state for num in row if num != 0] # Flatten matrix, excluding 0
        inversions = 0
        for i in range(len(flattened)):
            for j in range(i + 1, len(flattened)):
                if flattened[i] > flattened[j]:
                    inversions += 1
        return inversions % 2 == 0 # Solvable if even inversion number

    def calculateHammingDistance(self, state):
        """
        Function:   Calculates Hamming distance between current state & goal state.
        Input:      3x3 matrix representing current state.
        Output:     Integer value representing number of misplaced tiles.
        """
        goal = self.goalState() # Retrieve goal state
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != goal[i][j]: # Compare non-zero tiles
                    distance += 1
        return distance

    def calculateManhattanDistance(self, state):
        """
        Function:   Calculates Manhattan distance between current state & goal state.
        Input:      3x3 matrix representing current state.
        Output:     Integer value representing sum of Manhattan distances of each tile from its goal position
        """
        goal = self.goalState() # Retrieve goal state
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0: # Skip empty tile (0)
                    value = state[i][j]
                    goal_x, goal_y = divmod(value - 1, 3) # Tile's goal position
                    distance += abs(i - goal_x) + abs(j - goal_y) # Sum of Manhattan distances
        return distance

    def generateSuccessors(self, state):
        """
        Function:   Generates all possible successor states from current state by moving empty tile.
        Input:      3x3 matrix representing current state.
        Output:     List of 3x3 matrices representing successor states.
        """
        successors = []
        zero_x, zero_y = [(x, y) for x in range(3) for y in range(3) if state[x][y] == 0][0] # Find position of 0
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible moves (Up, Down, Left, Right)

        # Generate new states by swapping empty tile with neighbouring tiles
        for dx, dy in moves:
            new_x, new_y = zero_x + dx, zero_y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3: # Ensure within bounds
                new_state = [row[:] for row in state] # Make copy of state
                new_state[zero_x][zero_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[zero_x][zero_y]
                successors.append(new_state)

        return successors

    is_printed = bool

    def solve(self, initial_state, heuristic, is_printed):
        """
        Function:   Solves 8-puzzle using A* algorithm with specified heuristic.

        Input:      > initial_state: 3x3 matrix representing initial state.
                    > heuristic: Function (either Hamming or Manhattan).
                    > is_printed: Boolean flag indicating whether to print solution path/stats.

        Output:     > path: List of 3x3 matrices representing solution path.
                    > nodes_expanded: Number of nodes expanded.
                    > execution_time: Time taken to solve puzzle.
        """
        start_time = time.time()
        queue = []
        heapq.heappush(queue, (0, initial_state, []))  # (f(n), state, path)
        visited = set()
        nodes_expanded = 0
        goal = self.goalState() # Retrieve goal state

        while queue:
            cost, current_state, path = heapq.heappop(queue) # Pop state with lowest f(n)

            # Convert state to hashable tuple for visited set
            state_tuple = tuple(tuple(row) for row in current_state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            nodes_expanded += 1 # Increment nodes expanded
            path = path + [current_state] # Add current state to path

            # Calculate g(n), h(n), and f(n)
            g_n = len(path) - 1  # Cost / number of moves so far
            h_n = heuristic(current_state)  # Heuristic value
            f_n = g_n + h_n

            # If goal state reached, return solution path/stats
            if current_state == goal:
                end_time = time.time()
                self.execution_time = end_time - start_time  # Save execution time
                if is_printed: # Print solution path/stats if True
                    print(f"Nodes expanded: {nodes_expanded}")
                    print(f"Time taken: {self.execution_time:.4f} seconds")
                    print(f"Solution Path:")

                    # Print g(n), h(n) & f(n) for each step in solution path
                    for step, state in enumerate(path):
                        g_n = step
                        h_n = heuristic(state)
                        f_n = g_n + h_n

                        print(f"Step {step}:")
                        for row in state:
                            print(row)
                        print(f"g(n) = {g_n}, h(n) = {h_n}, f(n) = {f_n}\n")

                return path, nodes_expanded, self.execution_time  # Return all 3 values

            # Generate successors & add to queue
            for successor in self.generateSuccessors(current_state):
                if tuple(tuple(row) for row in successor) not in visited:
                    h_cost = heuristic(successor) # Calculate heuristic for successor
                    g_cost = len(path)  # Path cost so far
                    f_cost = g_cost + h_cost
                    heapq.heappush(queue, (f_cost, successor, path)) # Add to queue with priority

        return None, nodes_expanded, self.execution_time  # No solution found, return other values