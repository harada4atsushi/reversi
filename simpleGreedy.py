import gameplay
from copy import deepcopy

def value(board):
    value = 0
    for row in board:
        for elem in row:
            if elem == "W":
                value = value + 1
            elif elem == "B":
                value = value - 1
    return value

def betterThan(val1, val2, color, reversed):
    if color == "W":
        retVal = val1 > val2
    else:
        retVal =  val2 > val1 #was typo here, val2<val1
    if reversed:
        return not retVal
    else:
        return retVal

def nextMoveR(board, color, time):
    return nextMove(board, color, time, True)
    
def nextMove(board, color, time, reversed = False):
    moves = []
    for i in range(8):
        for j in range(8):
            if gameplay.valid(board, color, (i,j)):
                moves.append((i,j))
    if len(moves) == 0:
        return "pass"
    best = None
    for move in moves:
        newBoard = deepcopy(board)
        gameplay.doMove(newBoard,color,move)
        moveVal = value(newBoard)
        if best == None or betterThan(moveVal, best, color, reversed):
            bestMove = move
            best = moveVal
    return bestMove
