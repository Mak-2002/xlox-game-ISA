from collections import deque
import heapq
import copy
from State import State
from Node import Node
from initial_mazes import initial_mazes
from TerminalStyling import *

# Playing modes
USER_MODE = 1
COMPUTER_MODE = 2

# Algorithms
DFS = 1
BFS = 2
A_STAR = 3


class Game:
    def __init__(self, starting_maze_data=initial_mazes[0]) -> None:
        self.initial_node = Node(State(starting_maze_data))

    def main(self):
        welcome_str = \
            yellow_color + 'An assignment for the Intelligent Search Algorithms course at university, applying concepts to the XLOX game.\n' + \
            'You can check the rules and play the game at: ' + cyan_color + "https://www.puzzleplayground.com/xlox" + \
            yellow_color + '\n-------------------------------------------' + reset_color

        print(welcome_str)

        while True:
            try:
                input_value = input(
                    grey_color + 'Choose a level from 1 to 7, or q to quit\n')
                if input_value == 'q':
                    return
                level = int(input_value) - 1
                if level < 0 or level > 6:
                    raise Exception
                print()
                game = Game(starting_maze_data=initial_mazes[level])
                choice = input('u : User mode  ||  c : Computer mode\n')
                if choice == 'u':
                    mode = USER_MODE
                    mode_str = 'user'
                elif choice == 'c':
                    mode = COMPUTER_MODE
                    mode_str = 'computer'
                else:
                    raise Exception
                print(yellow_color +
                      f"New game started in {mode_str} mode..." + reset_color)
                game.play(mode)
            except Exception:
                print(red_color + "Invalid Input!" + reset_color)

    def find_path(self, node: 'Node') -> list['Node']:
        node = copy.deepcopy(node)
        path = []
        while True:
            path.append(node)
            if not node.parent:
                break
            node = node.parent
        path.reverse()
        return path

    def solution_stats(self, node: 'Node', iters: int, print_solution: bool = False):
        stats_str = green_color + 'Solution found!\n' + blue_color + \
            f"Visited nodes: {iters} nodes\n" + \
            f"Solution depth: {node.depth} moves\n"
        if print_solution:
            solution = self.find_path(node)
            stats_str += 'Solution:\n'
            for node in solution:
                stats_str += cyan_color + '#' + \
                    str(node.depth + 1) + '\n' + reset_color
                stats_str += str(node.state)
                stats_str += '\n-------------------------------------------\n'
        return stats_str

    def dfs(self, print_solution: bool = False):  # Deapth first search algorithm
        current_node = copy.deepcopy(self.initial_node)
        iters = 0
        stack = [current_node]
        visited = set()
        while stack:
            iters += 1
            current_node = stack.pop()
            if current_node.state.is_final():
                print(blue_color + 'DFS: ' +
                      self.solution_stats(current_node, iters, print_solution))
                break
            visited.add(str(current_node.state))
            for node in current_node.get_possible_next_nodes():
                if str(node.state) not in visited:
                    stack.append(node)

    def bfs(self, print_solution: bool = False):  # Breadth first search algorithm
        current_node = copy.deepcopy(self.initial_node)
        iters = 0
        queue = deque([current_node])
        visited = set()
        while queue:
            iters += 1
            current_node = queue.popleft()
            if current_node.state.is_final():
                print(blue_color + 'BFS: ' +
                      self.solution_stats(current_node, iters, print_solution))
                break
            visited.add(str(current_node.state))
            for node in current_node.get_possible_next_nodes():
                if str(node.state) not in visited:
                    queue.append(node)

    def ucs(self, print_solution: bool = False):  # Uniform cost search algorithm
        current_node = copy.deepcopy(self.initial_node)
        iters = 0
        opened_nodes_pq = [current_node]
        visited = set()
        while opened_nodes_pq:
            iters += 1
            current_node = heapq.heappop(opened_nodes_pq)
            if current_node.state.is_final():
                print(blue_color + 'UCS: ' +
                      self.solution_stats(current_node, iters, print_solution))
                break

            visited.add(str(current_node.state))
            for node in current_node.get_possible_next_nodes():
                if str(node.state) not in visited:
                    heapq.heappush(opened_nodes_pq, node)

        # !Important:
        # UCS is a greedy algorithm, meaning that whenever a node is reached,
        # it is guaranteed to have been reached with the least cost. Therefore, there is
        # no need to check whether it is reachable with a lower cost when we try to
        # reach it again.

    def play_in_computer_mode(self, print_solution: bool = False):
        print()
        self.dfs(print_solution)
        print('\n')
        self.bfs(print_solution)
        print('\n')
        self.ucs(print_solution)

    def play_in_user_mode(self):
        current_node = copy.deepcopy(self.initial_node)
        while not current_node.state.is_final():
            moves_count = current_node.cost
            current_state = current_node.state
            print(current_state)

            print(cyan_color + f"Moves: {moves_count}")
            print(
                grey_color + '(row) (column) : Make a move  ||  q : terminate\n' + reset_color)

            # Take input from user
            inputs = input('').split()
            # print(f"{row}, {column}") # DEBUG:wrote
            if inputs[0] == 'q':
                # End the game
                print(
                    red_color + f"Game terminated with {current_state.get_white_cells_count()} remaining white cells and {moves_count} moves." + reset_color)
                return
            else:
                # Make a move
                try:
                    row = int(inputs[0])
                    column = int(inputs[1])
                    # print(type(row)) # DEBUG:wrote
                    newState = current_state.apply_move(row, column)
                    if newState:
                        current_node = Node(newState,
                                            current_node,
                                            current_node.cost + 1,
                                            current_node.depth + 1)
                    else:
                        print(red_color +
                              'You can only change white cells!' + reset_color)
                except Exception:
                    print(
                        red_color + 'Invalid input! Please enter indices as integers inside of boundries separated by a space.' + reset_color)
                print()

        # ? Puzzle solved
        print(current_node.state)
        print(green_color +
              f"Congrats! You solved the puzzle with {current_node.depth} moves." + reset_color)

    def play(self, mode: int = USER_MODE, starting_maze_data=None):
        if starting_maze_data:
            self.initial_node = Node(State(starting_maze_data))

        if mode == USER_MODE:
            self.play_in_user_mode()
        else:
            print_solution = input('Do you want to print the solution (y/n): ')
            if print_solution == 'y':
                print_solution = True
            elif print_solution == 'n':
                print_solution = False
            else:
                raise Exception
            self.play_in_computer_mode(print_solution)


if __name__ == '__main__':
    obj = Game()
    obj.main()
