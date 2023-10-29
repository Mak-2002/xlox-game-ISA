from Maze import Maze
from initial_mazes import initial_mazes
class Game:
    def __init__(self, initial_maze_data = initial_mazes[0]) -> None:
        self.current_maze = Maze(initial_maze_data)
        # print(type(self.current_maze)) # DEBUG:wrote

    def main(self):
        game = Game(initial_maze_data=initial_mazes[1])
        game.play()

    def play(self):
        print('XLOX game started...')
        print('You can check the rules and play the game at: https://www.puzzleplayground.com/xlox')
        while not self.current_maze.is_final_state():
            print(self.current_maze)
            print('Enter row and column to make a move...\nor q to terminate.')
            # Take input from user
            inputs = input('').split()
            # print(f"{row}, {column}") # DEBUG:wrote
            if inputs[0] == 'q':
                # End the game
                print(f"Game ended with {self.current_maze.get_white_cells_count()} white cells.")
                return
            else:
                # Make a move
                try:
                    row = int(inputs[0])
                    column = int(inputs[1])
                    # print(type(row)) # DEBUG:wrote
                    newMaze = self.current_maze.apply_move(row, column)
                    if newMaze is None:
                        print('You can only change white cells!')
                    else:
                        self.current_maze = newMaze
                except Exception:
                     print('Invalid input! Please enter row and column as integers inside of boundries.')
                print()
        print('Game Ended.. Allah ya3teek el3afi')

if __name__ == '__main__':
    obj = Game()
    obj.main()                