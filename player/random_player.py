import random

from board import Board
from gameplay import valid

class RandomPlayer:

    def __init__(self, color):
        self.color = color
        self.name = 'random'

    def next_move(self, board_data, color):
        board = Board(board_data)
        positions = board.valid_positions(self)

        if len(positions) == 0:
            return "pass"
        bestMove = positions[random.randint(0,len(positions) - 1)]
        return bestMove


    def nextMoveR(self, board, color, time):
        return self.next_move(board, color)


    def getGameResult(self, board_data, game_ended=False, opponent_player=None):
        pass
