import gameplay
from copy import deepcopy
INF = float('inf')

### Default depth is 5

def nextMove(board, color, time):
    if gameplay.valid(board, color, 'pass'):
        return "pass"
    depth = 6
    if time <= 170 and time > 100:
        depth = 5
    if time <= 100 and time > 50:
        depth = 4
    if time <= 50 and time > 20:
        depth = 3
    if time <= 20 and time > 5:
        depth = 2
    if time <= 5:
        depth = 1

    (move, value) = max_val(board, -INF, INF, depth, color)
    return move


def nextMoveR(board, color, time):
    if gameplay.valid(board, color, 'pass'):
        return "pass"
    depth = 6
    if time <= 170 and time > 100:
        depth = 5
    if time <= 100 and time > 50:
        depth = 4
    if time <= 50 and time > 20:
        depth = 3
    if time <= 20 and time > 5:
        depth = 2
    if time <= 5:
        depth = 1

    (move, value) = min_val(board, -INF, INF, depth, color, True)
    return move
    #return nextMove(board, gameplay.opponent(color), time)

### state in this program is always a "board"
### Check if the state is the end
def endState(state):
    return gameplay.gameOver(state)


def max_val(state, alpha, beta, depth, color, reversed=False):
    if endState(state):
        return None, utility(state, color)
    elif depth == 0:
        return None, evaluation(state, color)
    best = None
    v = -INF
    if not reversed:
        moves = successors(state, color)
    else:
        moves = successors(state, gameplay.opponent(color))
    for (move, state) in moves:
        value = min_val(state, alpha, beta, depth - 1, color, reversed)[1]
        if best is None or value > v:
            best = move
            v = value
        if v >= beta:
            return best, v
        alpha = max(alpha, v)
    return best, v



def min_val(state, alpha, beta, depth, color, reversed=False):
    if endState(state):
        return None, utility(state, color)
    elif depth == 0:
        return None, evaluation(state, color)
    best = None
    v = INF
    if not reversed:
        moves = successors(state, gameplay.opponent(color))
    else:
        moves = successors(state, color)
    for (move, state) in moves:
        value = max_val(state, alpha, beta, depth - 1, color, reversed)[1]
        if best is None or value < v:
            best = move
            v = value
        if alpha >= v:
            return best, v
        beta = min(beta, v)
    return best, v


### Generate all the possible moves and 
### the new state related with the move
def successors(state, color):
    successors_list = []
    moves = []
    for i in range(8):
        for j in range(8):
            if gameplay.valid(state, color, (i, j)):
                moves.append((i, j))
    for moves in moves:
        newBoard = deepcopy(state)
        gameplay.doMove(newBoard, color, moves)
        successors_list.append((moves, newBoard))
    return successors_list



def utility(state, color):
    answer = 0
    if gameplay.score(state)[0] == gameplay.score(state)[1]:
        answer = 0
    elif gameplay.score(state)[0] < gameplay.score(state)[1] and color == "W":
        answer = INF
    elif gameplay.score(state)[0] > gameplay.score(state)[1] and color == "B":
        answer = INF
    else:
        answer = -INF
    return answer


### Implementation of Positional Strategy
def evaluation(state, color):
    result = 0
    weight = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],
    [8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],
    [6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],
    [-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]

    for i in range(8):
        for j in range(8):
            if state[i][j] == color:
                result += weight[i][j]
            if state[i][j] == gameplay.opponent(color):
                result -= weight[i][j]

    #if reversed:
    #    result = -result

    return result



