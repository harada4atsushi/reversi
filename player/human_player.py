import random

from board import Board
from gameplay import valid

class HumanPlayer:

    def __init__(self, color):
        self.color = color
        self.name = 'human'

    def next_move(self, board_data, color):
        board = Board(board_data)
        positions = board.valid_positions(self)

        if len(positions) == 0:
            return "pass"

        # bestMove = positions[random.randint(0,len(positions) - 1)]
        # return bestMove

        valid = False
        while not valid:
            try:
                row_i = int(input("Where would you like to place row index (0-3)? "))
                col_i = int(input("Where would you like to place col index (0-3)? "))

                if (row_i, col_i) in positions:
                    valid = True
                else:
                    print("That is not a valid move! Please try again.")
            except Exception as e:
                print("It is not a valid move! Please try again.")
        return (row_i, col_i)


    def nextMoveR(self, board, color, time):
        return self.next_move(board, color)


    def getGameResult(self, board_data, game_ended=False):
        pass

