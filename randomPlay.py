import random
from gameplay import valid


def nextMove(board, color, time):
    moves = []
    for i in range(8):
        for j in range(8):
            if valid(board, color, (i,j)):
                moves.append((i,j))
    if len(moves) == 0:
        return "pass"
    bestMove = moves[random.randint(0,len(moves) - 1)]
    return bestMove


def nextMoveR(board, color, time):
    return nextMove(board, color, time)
