import random

from gameplay import valid


class QLearning:
    def nextMove(self, board, color, time):
        moves = []
        for i in range(4):
            for j in range(4):
                if valid(board, color, (i,j)):
                    moves.append((i,j))
        if len(moves) == 0:
            return "pass"
        bestMove = moves[random.randint(0,len(moves) - 1)]
        return bestMove


    def nextMoveR(self, board, color, time):
        return self.nextMove(board, color, time)
