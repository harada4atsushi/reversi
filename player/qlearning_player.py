import random
from copy import deepcopy

import gameplay
from board import Board
from player.quantity import Quantity
from player.random_player import RandomPlayer


class QlearningPlayer:
    INF = float('inf')
    DEFAULT_E = 0.2
    INITIAL_Q = 1  # default 1

    def __init__(self, color, e=DEFAULT_E, alpha=0.3):
        self.color = color
        self.name = 'ql'
        self.q = Quantity(alpha, 0.9)
        self._e = e
        self._total_game_count = 0
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

        # for debug
        # if self._total_game_count > 1000 and self._total_game_count % 100 == 0:
        #     print(self._total_game_count)

        # ゲーム回数が少ない間は、ある程度の確率で打ち手をランダムにする
        if random.random() < (self._e / (self._total_game_count // 10000 + 1)):
            move = random.choice(positions)
        else:
            qs = []
            for position in positions:
                qs.append(self.q.get(tuple(self._last_board.flattend_data()), position))

            # for debug
            # if self._total_game_count > 9000 and self._total_game_count % 300 == 0:
            #     # print(positions)
            #     print(qs)

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


    def getGameResult(self, board_data):
        board = Board(board_data[:])
        is_game_over = board.is_game_over()

        # 相手のターン行動後のQ値を取得するための処理
        # tmp_player = RandomPlayer(gameplay.opponent(self.color))
        # vp = board.valid_positions(tmp_player)
        # if len(vp) != 0:
        #     gameplay.doMove(board.board_data, gameplay.opponent(self.color), random.choice(vp))

        reward = 0
        if is_game_over:
            color = board.color_of_more()

            if color == self.color:
                reward = 1
            elif color == '':
                reward = 0
            elif color != self.color:
                reward = -1

        # for debug
        # if self._total_game_count > 1000:
        #     aaa = 'aaa'

        self.learn(self._last_board, self._last_move, reward, board, is_game_over)

        if not is_game_over:
            self._total_game_count += 1
            self._last_move = None
            self._last_board = None

    def learn(self, s, a, r, fs, game_ended):

        flattend_data = s.flattend_data()
        # pQ = self.q.get(tuple(flattend_data), a)

        list = []
        for position in fs.valid_positions(self):
            list.append(self.q.get(tuple(fs.flattend_data()), position))

        # print(list)

        if game_ended or len(list) == 0:
            max_q_new = 0
        else:
            # 相手のターン行動後のQ値を取得するための処理
            # tmp_player = RandomPlayer(gameplay.opponent(self.color))
            # vp = fs.valid_positions(tmp_player)
            # if len(vp) != 0:
            #     gameplay.doMove(fs.board_data, gameplay.opponent(self.color), random.choice(vp))
            # if len(list) == 0:
            #     max_q_new = 0
            # else:
            #     max_q_new = max(list)
            max_q_new = max(list)

        self.q.update(tuple(flattend_data), a, r, max_q_new)


    def change_to_battle_mode(self):
        self._e = 0




