class Cell:
    """
    Represents a cell in a maze or a move applied to a cell.
    """

    # Describing the states of the cells in a maze.
    state_descriptions = {
        'W': 'White',
        'B': 'Black',
        'X': 'Blocked',
        'O': 'Out-of-boundries Gap',
    }

    def __init__(self, state='B'):
        """
        Initilize a Cell Object
        """
        # Args:
        #     rowOrList: Either an integer representing the row index or a list containing the row and column indices.
        #     column: The column index.
        # """
        # if column is not None:
        #     # Accepting two separate values for row and column
        #     self.row = rowOrList
        #     self.column = column
        # else:
        #     # Accepting a list containing row and column
        #     self.row, self.column = rowOrList
        
        self.state = state
    
    def get_state(self):
        return self.state
    
    def get_detailed_state(self):
        return self.state_description[self.state]