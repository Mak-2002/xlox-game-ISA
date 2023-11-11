import copy
from TerminalStyling import bg_white_color, bg_blue_color, bg_black_color, reset_color

# Constants for cell states
WHITE = 'W'
BLACK = 'B'
BLOCKED = 'X'
OUT_OF_BOUNDARIES = 'O'


class State:
    def __init__(self, maze_data):
        """
        Represents a maze (state).

        Args:
            maze_data (list of lists): A two-dimensional array representing the maze.
        """
        self.white_cells = set()
        self.grid = maze_data
        for row, row_list in enumerate(maze_data):
            for column, cell in enumerate(row_list):
                if cell == WHITE:
                    self.white_cells.add((row, column))

    def grid_tuple(self, grid):
        return tuple(map(tuple, grid))

    def __hash__(self):
        return hash(self.grid_tuple(self.grid))

    def __eq__(self, other):
        return isinstance(other, State) and hash(self) == hash(other)

    def __str__(self):
        maze_str = " "
        for column_index, _ in enumerate(self.grid[0]):
            maze_str += str(column_index) + ' '
        maze_str += '\n'

        for row_index, row in enumerate(self.grid):
            maze_str += str(row_index)
            for cell in row:
                if cell == WHITE:
                    bg_color = bg_white_color
                elif cell == BLOCKED:
                    bg_color = bg_blue_color
                elif cell == BLACK:
                    bg_color = bg_black_color
                else:
                    bg_color = reset_color
                maze_str += bg_color + '  ' + reset_color
            maze_str += '\n'
        return maze_str

    def __copy__(self):
        new_obj = State(self.grid)
        return new_obj

    def check_move_validity(self, row, column) -> bool:
        """
        Checks whether a move is applied on a white cell or not.

        Args:
            row (int): The row index of the cell.
            column (int): The column index of the cell.

        Returns:
            bool: True if the move is valid (applied to a white cell), False otherwise.
        """
        try:
            return self.grid[row][column] == WHITE
        except IndexError:
            return False

    def apply_move(self, row, column):
        """
        Applies a move to the maze and returns the resulting maze state.

        Args:
            row (int): The row index of the cell to move.
            column (int): The column index of the cell to move.

        Returns:
            State: The new maze state after the move, or None if the move is not valid.
        """
        if not self.check_move_validity(row, column):
            return None

        new_maze = State(copy.deepcopy(self.grid))
        new_maze.inverse_cell_color(row, column)
        indices_changes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for change in indices_changes:
            new_maze.inverse_cell_color(row + change[0], column + change[1])

        return new_maze

    def inverse_cell_color(self, row, column):
        """
        Inverses the color of a cell (white to black and vice versa).

        Args:
            row (int): The row index of the cell.
            column (int): The column index of the cell.
        """
        try:
            cell = self.grid[row][column]
            if cell == WHITE:
                self.grid[row][column] = BLACK
                self.white_cells.discard((row, column))
            elif cell == BLACK:
                self.grid[row][column] = WHITE
                self.white_cells.add((row, column))
        except IndexError:
            pass

    def get_white_cells_count(self) -> int:
        """
        Returns the count of white cells in the maze.

        Returns:
            int: The count of white cells.
        """
        return len(self.white_cells)

    def get_cell_state_description(self, row, column) -> str:
        """
        Returns a description of the cell's state.

        Args:
            row (int): The row index of the cell.
            column (int): The column index of the cell.

        Returns:
            str: A description of the cell's state (e.g., 'White', 'Black', 'Blocked', 'Out-of-boundaries Gap').
        """
        cell_state_descriptions = {
            WHITE: 'White',
            BLACK: 'Black',
            BLOCKED: 'Blocked',
            OUT_OF_BOUNDARIES: 'Out-of-boundaries Gap',
        }
        return cell_state_descriptions[self.grid[row][column]]

    def get_possible_next_states(self):
        """
        Returns a set of possible next maze states by making valid moves on white cells.

        Returns:
            set of State: A set of possible next maze states.
        """
        return [self.apply_move(move[0], move[1])
                for move in self.white_cells
                if self.apply_move(move[0], move[1]) is not None]

    def is_final(self) -> bool:
        """
        Checks if the maze is in a final state (no more white cells left).

        Returns:
            bool: True if it's a final state, False otherwise.
        """
        return len(self.white_cells) == 0
