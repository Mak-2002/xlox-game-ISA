from Maze import Maze
from initial_mazes import initial_mazes
from TerminalStyling import *

class Game:
    def __init__(self, initial_maze_data = initial_mazes[0]) -> None:
        self.current_maze = Maze(initial_maze_data)
        # print(type(self.current_maze)) # DEBUG:wrote

    def main(self):
        print(yellow_color, end='')
        print('An assignment for the Intelligent Search Algorithms course at university, applying concepts to the XLOX game.')
        print("You can check the rules and play the game at: " + cyan_color + "https://www.puzzleplayground.com/xlox" + yellow_color)
        print('-------------------------------------------'+ reset_color)
        while True:
            try:
                input_value = input(grey_color + 'choose a level from 1 to 4, or q to quit\n' + reset_color)
                if input_value == 'q':
                    return
                level = int(input_value) - 1
                if level < 0 or level > 3:
                    raise Exception
                print()
                game = Game(initial_maze_data=initial_mazes[level])
                print(yellow_color + 'New game started in user mode...' + reset_color)
                game.play()
            except Exception:
                print(red_color + 'Invalid input!' + reset_color)


    def play(self):
        move_count = 0
        while not self.current_maze.is_final_state():
            print(self.current_maze)
            print(grey_color, end='')
            print(f"Moves: {move_count}")
            print('(row) (column) : Make a move  ||  q : terminate')
            print(reset_color, end='')
            # Take input from user
            inputs = input('').split()
            print('\n')
            # print(f"{row}, {column}") # DEBUG:wrote
            if inputs[0] == 'q':
                # End the game
                print(red_color + f"Game terminated with {self.current_maze.get_white_cells_count()} remaining white cells and {move_count} moves." + reset_color)
                return
            else:
                # Make a move
                try:
                    row = int(inputs[0])
                    column = int(inputs[1])
                    # print(type(row)) # DEBUG:wrote
                    newMaze = self.current_maze.apply_move(row, column)
                    if newMaze is None:
                        print(red_color + 'You can only change white cells!' + reset_color)
                    else:
                        self.current_maze = newMaze
                except Exception:
                     print(red_color + 'Invalid input! Please enter indices as integers inside of boundries separated by a space.' + reset_color)
                print()
            move_count += 1
        print(self.current_maze)
        print( green_color + f"Congrats! You solved the puzzle with {move_count} moves." + reset_color)

if __name__ == '__main__':
    obj = Game()
    obj.main()                