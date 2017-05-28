
from copy import deepcopy

import gameplay
from board import Board


class MinmaxPlayer:
    INF = float('inf')

    def __init__(self, color):
        self.color = color
        self.name = 'minmax'


    def nextMove(self, board, color, time):
        if gameplay.valid(board, color, 'pass'):
            return "pass"
        depth = 3
        # if time <= 170 and time > 100:
        #     depth = 5
        # if time <= 100 and time > 50:
        #     depth = 4
        # if time <= 50 and time > 20:
        #     depth = 3
        # if time <= 20 and time > 5:
        #     depth = 2
        # if time <= 5:
        #     depth = 1

        (move, value) = self.max_val(board, -self.INF, self.INF, depth, color)
        return move



    def get_valid_positions(self):
        moves = []
        for i in range(4):
            for j in range(4):
                if gameplay.valid(self._board, self._color, (i, j)):
                    moves.append((i, j))
        return moves


    def get_successors_list(self, positions):
        if self._color == 'B':
            idx = 0
        elif self._color == 'W':
            idx = 1

        successors_list = []
        before_score = gameplay.score(self._board)

        for position in positions:
            newBoard = deepcopy(self._board)
            gameplay.doMove(newBoard, self._color, position)
            after_score = gameplay.score(newBoard)
            gain = after_score[idx] - before_score[idx] - 1
            successors_list.append((position, newBoard, gain))

            # Board().print(newBoard)
        return successors_list


    def get_best_positions(self, successors_list):
        max_gain = 0
        best_positions = []

        for (move, state, gain) in successors_list:
            if max_gain < gain:
                max_gain = gain

        for (move, state, gain) in successors_list:
            if gain == max_gain:
                best_positions.append(move)

        return best_positions


    ### state in this program is always a "board"
    ### Check if the state is the end
    def endState(self, state):
        # TODO DRYにしたい
        return gameplay.valid(state, "B", 'pass') and gameplay.valid(state, "W", 'pass')


    def max_val(self, state, alpha, beta, depth, color, reversed=False):
        if self.endState(state):
            return None, self.utility(state, color)
        elif depth == 0:
            return None, self.evaluation(state, color)
        best = None
        v = -self.INF
        if not reversed:
            moves = self.successors(state, color)
        else:
            moves = self.successors(state, gameplay.opponent(color))
        for (move, state) in moves:
            value = self.min_val(state, alpha, beta, depth - 1, color, reversed)[1]
            if best is None or value > v:
                best = move
                v = value
            if v >= beta:
                return best, v
            alpha = max(alpha, v)
        return best, v



    def min_val(self, state, alpha, beta, depth, color, reversed=False):
        if self.endState(state):
            return None, self.utility(state, color)
        elif depth == 0:
            return None, self.evaluation(state, color)
        best = None
        v = self.INF
        if not reversed:
            moves = self.successors(state, gameplay.opponent(color))
        else:
            moves = self.successors(state, color)
        for (move, state) in moves:
            value = self.max_val(state, alpha, beta, depth - 1, color, reversed)[1]
            if best is None or value < v:
                best = move
                v = value
            if alpha >= v:
                return best, v
            beta = min(beta, v)
        return best, v


    ### Generate all the possible moves and
    ### the new state related with the move
    def successors(self, state, color):
        successors_list = []
        moves = []
        for i in range(4):
            for j in range(4):
                if gameplay.valid(state, color, (i, j)):
                    moves.append((i, j))
        for moves in moves:
            newBoard = deepcopy(state)
            gameplay.doMove(newBoard, color, moves)
            successors_list.append((moves, newBoard))
        return successors_list



    def utility(self, state, color):
        board = Board(state)
        answer = 0
        if board.score()[0] == board.score()[1]:
            answer = 0
        elif board.score()[0] < board.score()[1] and color == "W":
            answer = self.INF
        elif board.score()[0] > board.score()[1] and color == "B":
            answer = self.INF
        else:
            answer = -self.INF
        return answer


    ### Implementation of Positional Strategy
    def evaluation(self, state, color):
        result = 0
        # 8x8
        # weight = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],
        # [8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],
        # [6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],
        # [-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]

        # 4x4
        weight = [
            [2, 1, 1, 2],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [2, 1, 1, 2],
        ]

        for i in range(4):
            for j in range(4):
                if state[i][j] == color:
                    result += weight[i][j]
                if state[i][j] == gameplay.opponent(color):
                    result -= weight[i][j]

        #if reversed:
        #    result = -result

        return result


    def getGameResult(self, board_data, game_ended=False):
        pass
