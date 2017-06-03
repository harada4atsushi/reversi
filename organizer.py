import random
import time
from copy import deepcopy

from board import Board
from gameplay import newBoard, valid, doMove
from player.qlearning_player import QlearningPlayer


class Organizer:
    def __init__(self, show_board=True, show_result=True, nplay=1, stat=100, debug=False):
        self._show_board = show_board
        self._show_result = show_result
        self._nplay = nplay
        self._stat = stat
        self._debug = debug


    def play_game(self, player1, player2, verbose=False, t=128):
        """ Takes as input two functions p1 and p2 (each of which
            calculates a next move given a board and player color),
            and returns either a tuple containing the score for black,
            score for white, and final board (for a normal game ending)
            or a tuple containing the final score for black, final score
            for white, and the  invalid move (for a game that ends with
            and invalid move """

        # p1 = player1.nextMove
        # p2 = player2.nextMove

        p1 = player1
        p2 = player2

        player1_win_count = 0
        player2_win_count = 0
        draw_count = 0

        for i in range(0, self._nplay):
            # (p2, p1) = (p1, p2)

            board = Board(newBoard())
            p1time = t
            p2time = t
            p1realTime = t * 2  # gives a little extra time to each player
            p2realTime = t * 2

            while not board.is_game_over():
                tmpBoard = deepcopy(board.board_data)
                t1 = time.time()
                nextMove = p1.nextMove(tmpBoard, p1.color, p1time)
                t2 = time.time()
                p1time = p1time - (t2 - t1)
                p1realTime = p1realTime - (t2 - t1)
                # if p1time < 0:
                if (p1realTime < 0):
                    if p1.color == "B":
                        return (0, 16, board.board_data, "Timeout")
                    else:
                        return (16, 0, board.board_data, "Timeout")
                if valid(board.board_data, p1.color, nextMove):
                    doMove(board.board_data, p1.color, nextMove)
                else:
                    if p1.color == "B":
                        return (0, 16, board.board_data, "Bad Move: %s" % str(nextMove))
                    else:
                        return (16, 0, board.board_data, "Bad Move: %s" % str(nextMove))

                # p1.getGameResult(board.board_data, game_ended=self.game_over(board.board_data))
                p1.getGameResult(board.board_data)

                (p1, p2) = (p2, p1)
                (p1time, p2time) = (p2time, p1time)
                (p1realTime, p2realTime) = (p2realTime, p1realTime)

                if self._show_board:
                    if isinstance(p1, QlearningPlayer) and self._debug:
                        board.print(q=p1.q)
                    else:
                        board.print()

            # if self._show_board:
            #     board.print()

            res = board.score()

            if res[0] > res[1]:
                player1_win_count += 1
            elif res[0] < res[1]:
                player2_win_count += 1
            else:
                draw_count += 1

            if self._nplay > 1 and i % self._stat == 0:
                print("Win count, player1(%s): %d, player2(%s): %d, draw: %d" % (player1.name, player1_win_count, player2.name, player2_win_count, draw_count))

        if self._nplay > 1:
            print("Win count, player1(%s): %d, player2(%s): %d, draw: %d" % (
                player1.name, player1_win_count, player2.name, player2_win_count, draw_count))


    def print_winner(self, winner, loser, winner_count, loser_count):
        if self._show_result:
            if winner_count == loser_count:
                print("TIE %s, %s, (%d to %d)" % (winner, loser, winner_count, loser_count))
            else:
                print("%s Wins %s Loses (%d to %d)" % (winner, loser, winner_count, loser_count))


