import random
from copy import deepcopy

import gameplay
from board import Board


class QlearningPlayer:
    INF = float('inf')

    def __init__(self, color, e=0.2, alpha=0.3):
        self.color = color
        self.name = 'ql'
        self._e = e
        self._alpha = alpha
        self._total_game_count = 0


    def nextMove(self, board, color, _):
        return self.policy(board, color)

        # if gameplay.valid(board, color, 'pass'):
        #     return "pass"
        # depth = 3
        #
        # (move, value) = self.max_val(board, -self.INF, self.INF, depth, color)
        # return move


    def policy(self, board, color):
        # ゲーム回数が少ない間は、ある程度の確率で打ち手をランダムにする
        # if random.random() < (self._e / (self._total_game_count // 10000 + 1)):
        #     print('do random action')


        board_c = Board()
        moves = board_c.valid_positions(board, self)

        if len(moves) == 0:
            return "pass"

        bestMove = moves[random.randint(0, len(moves) - 1)]
        return bestMove


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
        return gameplay.gameOver(state)


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
        board = Board()
        answer = 0
        if board.score(state)[0] == board.score(state)[1]:
            answer = 0
        elif board.score(state)[0] < board.score(state)[1] and color == "W":
            answer = self.INF
        elif board.score(state)[0] > board.score(state)[1] and color == "B":
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

