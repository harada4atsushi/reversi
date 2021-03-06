import random
from copy import deepcopy, copy

import gameplay
from board import Board
from player.naive_player import NaivePlayer
from player.quantity import Quantity


class QlearningPlayer:
    DEFAULT_E = 0.2

    def __init__(self, color, e=DEFAULT_E, alpha=0.3):
        self.color = color
        self.name = 'ql'
        self.q = Quantity(alpha, 0.9)
        self.next_q_list = []
        self._e = e
        self._action_count = 0
        self._last_board = None
        self._last_move = None


    def next_move(self, board, color):
        return self.policy(board, color)


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
        if random.random() < (self._e / (self._action_count // 10000 + 1)):
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


    def getGameResult(self, board_data, opponent_player=None):
        board = Board(deepcopy(board_data))

        # 相手のターン行動後のQ値を取得するための処理
        act = opponent_player.next_move(board.board_data, opponent_player.color)
        gameplay.doMove(board.board_data, opponent_player.color, act)
        is_game_over = board.is_game_over()

        reward = 0
        if is_game_over:
            color = board.color_of_more()

            if color == self.color:
                reward = 1
            elif color == '':
                reward = 0
            elif color != self.color:
                reward = -1

        # passしていない場合のみ学習させる
        if self._last_move != None:
            self.learn(self._last_board, self._last_move, reward, board, is_game_over)

        if not is_game_over:
            self._action_count += 1
            self._last_move = None
            self._last_board = None


    def learn(self, s, a, r, fs, game_ended):
        flattend_data = s.flattend_data()
        # pQ = self.q.get(tuple(flattend_data), a)

        list = []
        for position in fs.valid_positions(self):
            list.append(self.q.get(tuple(fs.flattend_data()), position))

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

        # print('max_q_new: %s' % max_q_new)
        # self.next_q_list.append(max_q_new)
        self.q.update(tuple(flattend_data), a, r, max_q_new)


    def change_to_battle_mode(self):
        self._e = 0




