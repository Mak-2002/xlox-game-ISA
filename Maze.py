from Cell import Cell
import copy

class Maze:
    """
    Represents a maze (state).
    """
    def __init__(self, maze_data) -> None:

        #? Before we create the maze, we should validate that maze_data is a two-dimensional array
        if not isinstance(maze_data, list):
            raise ValueError("The initial state data should be a two-dimensional array!")
        for row in maze_data:
            if not isinstance(row, list):
                raise ValueError("The initial state data should be a two-dimensional array!")
        
        # Initial Assignment
        self.white_cells = set()
        self.grid = maze_data
        for row, rowList in enumerate(maze_data):
            for column, cell in enumerate(rowList):
                if(cell == 'W'):
                    self.white_cells.add((row, column))


    def __hash__(self) -> int:
        return hash(frozenset(self.white_cells))
    
    def __eq__(self, other: 'Maze') -> bool:
        return isinstance(other, Maze) and hash(self) == hash(other)

    def __str__(self) -> str:
        if self.is_in_final_state():
            print('Finished!\n')
        else:
            print('Ongoing.\n')
        
        for row in self.grid:
            for cell in row:
                if cell.get_state() == 'O':
                    print(' ')
                else:
                    print(cell.get_state())
                print(' ')
            print('\n')

    def __copy__(self):
        new_obj = Maze(self.grid)
        return new_obj


    def check_move_validity(self, row, column) -> bool:
        """
        Checks whether a move is applied on a white cell or not, Returns true if so.
        """
        try:
            return self.grid[row][column].get_state() == 'W'
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
    
    def inverse_cell_color(self, row, column):
        try:
            cell = self.grid[row][column]
            if cell in ('B', 'W'):
                cell = 'B' if cell == 'W' else 'W'
                self.grid[row][column] = cell
        except IndexError:
            pass

    def possible_next_states(self) -> list['Maze']:
        return [self.apply_move(move[0], move[1]) for move in self.white_cells]
    
    def is_in_final_state(self) -> bool:
        return len(self.white_cells) == 0

