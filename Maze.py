import copy

class Maze:
    """
    Represents a maze (state).
    """
    def __init__(self, maze_data) -> None:

        #? Before we create the maze, we should validate that maze_data is a two-dimensional array
        if not isinstance(maze_data, list):
            raise ValueError("Maze data should be a two-dimensional array!")
        for row in maze_data:
            if not isinstance(row, list):
                raise ValueError("Maze data should be a two-dimensional array!")
        
        # Initial Assignment
        self.white_cells = set()
        self.grid = maze_data
        for row, rowList in enumerate(maze_data):
            for column, cell in enumerate(rowList):
                if cell == 'W':
                    self.white_cells.add((row, column))

    def __hash__(self) -> int:
        return hash(tuple(map(tuple, self.grid)))
    
    def __eq__(self, other: 'Maze') -> bool:
        return isinstance(other, Maze) and hash(self) == hash(other)

    def __str__(self) -> str:
        maze_str = " "
        for column_index, _ in enumerate(self.grid[0]):
            maze_str += str(column_index) + ' '
        maze_str += '\n'

        for row_index, row in enumerate(self.grid):
            maze_str += str(row_index)
            for cell in row:
                if cell == 'W':
                    maze_str += '\033[47m' + '  ' + '\033[0m'  # White square
                elif cell == 'X':
                    maze_str += '\033[44m' + '  ' + '\033[0m'  # Blue square
                elif cell == 'B':
                    maze_str += '\033[40m' + '  ' + '\033[0m'  # Black square
                else:
                    maze_str += '  '  # Empty cell
            maze_str += '\n'

        return maze_str
        
    def __copy__(self):
        new_obj = Maze(self.grid)
        return new_obj


    def check_move_validity(self, row, column) -> bool:
        """
        Checks whether a move is applied on a white cell or not, Returns true if so.
        """
        try:
            return self.grid[row][column] == 'W'
        except IndexError:
            return False
    
    def apply_move(self, row, column) -> 'Maze':
        if not self.check_move_validity(row, column):
            return None
        
        newMaze = copy.copy(self)
        newMaze.inverse_cell_color(row, column)
        indices_changes = {
            (-1, 0),
            (+1, 0),
            (0, -1),
            (0, +1),
        }
        for change in indices_changes:
            newMaze.inverse_cell_color(row+change[0], column+change[1])

        return newMaze    
    
    def inverse_cell_color(self, row, column) -> None:
        try:
            cell = self.grid[row][column]
            if cell == 'W':
                self.grid[row][column] = 'B'
                self.white_cells.discard((row, column))
            elif cell == 'B':
                self.grid[row][column] = 'W'
                self.white_cells.add((row, column))
        except IndexError:
            pass
    
    def get_white_cells_count(self):
        return len(self.white_cells)

    def get_cell_state_description(self, row, column):
        cell_state_descriptions = {
            'W': 'White',
            'B': 'Black',
            'X': 'Blocked',
            'O': 'Out-of-boundries Gap',
        }
        return cell_state_descriptions[self.grid[row][column]]

    def possible_next_states(self) -> set['Maze']:
        return {self.apply_move(move[0], move[1]) for move in self.white_cells}
    
    def is_final_state(self) -> bool:
        return len(self.white_cells) == 0

