import random
from copy import deepcopy

import gameplay
from board import Board


class QlearningPlayer:
    INF = float('inf')
    DEFAULT_E = 0.2

    def __init__(self, color, e=DEFAULT_E, alpha=0.3):
        self.color = color
        self.name = 'ql'
        self._e = e
        self._alpha = alpha
        self._gamma = 0.9
        self._total_game_count = 0
        self._q = {}
        self._last_board = None
        self._last_move = None


    def nextMove(self, board, color, _):
        return self.policy(board, color)

        # if gameplay.valid(board, color, 'pass'):
        #     return "pass"
        # depth = 3
        #
        # (move, value) = self.max_val(board, -self.INF, self.INF, depth, color)
        # return move


    def policy(self, board_data, color):
        self._last_board = Board(board_data.copy())
        board = Board(board_data)
        positions = board.valid_positions(self)

        if len(positions) == 0:
            return "pass"

        # ゲーム回数が少ない間は、ある程度の確率で打ち手をランダムにする
        if random.random() < (self._e / (self._total_game_count // 10000 + 1)):
            move = random.choice(positions)
        else:
            qs = []
            for position in positions:
                qs.append(self.get_q(tuple(self._last_board.flattend_data()), position))

            # for debug
            if self._total_game_count > 9000 and self._total_game_count % 300 == 0:
                print(positions)
                print(qs)

            max_q = max(qs)

            if qs.count(max_q) > 1:
                # more than 1 best option; choose among them randomly
                best_options = [i for i in range(len(positions)) if qs[i] == max_q]
                i = random.choice(best_options)
            else:
                i = qs.index(max_q)
            move = positions[i]

        self._last_move = move
        return move


    def get_q(self, state, act):
        # encourage exploration; "optimistic" 1.0 initial values
        if self._q.get((state, act)) is None:
            self._q[(state, act)] = 1  # default 1
        return self._q.get((state, act))


    def getGameResult(self, board_data, game_ended=False):
        board = Board(board_data)
        color = board.color_of_more()

        reward = 0
        if game_ended:
            if color == self.color:
                reward = 1
            elif color == '':
                reward = 0
            elif color != self.color:
                reward = -1

        self.learn(self._last_board, self._last_move, reward, board)

        if not game_ended:
            self._total_game_count += 1
            self._last_move = None
            self._last_board = None


    def learn(self, s, a, r, fs):
        flattend_data = s.flattend_data()
        pQ = self.get_q(tuple(flattend_data), a)

        list = []
        for position in fs.valid_positions(self):
            list.append(self.get_q(tuple(fs.flattend_data()), position))

        if len(list) == 0:
            max_q_new = 0
        else:
            max_q_new = max(list)
        self._q[(tuple(flattend_data), a)] = pQ + self._alpha * ((r + self._gamma * max_q_new) - pQ)

        # pQ = self.getQ(tuple(s.board), a)
        # if fs.winner is not None:
        #     maxQnew = 0
        # else:
        #     maxQnew = max([self.getQ(tuple(fs.board), act) for act in fs.get_possible_pos()])
        # self.q[(tuple(s.board), a)] = pQ + self.alpha * ((r + self.gamma * maxQnew) - pQ)


    def change_to_battle_mode(self):
        self._e = 0



