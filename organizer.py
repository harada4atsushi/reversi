import random
import time
from copy import deepcopy

from board import Board
from gameplay import newBoard, gameOver, valid, doMove


class Organizer:
    def __init__(self, show_board=True, show_result=True, nplay=1, stat=100):
        self._show_board = show_board
        self._show_result = show_result
        self._nplay = nplay
        self._stat = stat


    def play_game(self, p1, p2, player1, player2, verbose=False, t=128):
        """ Takes as input two functions p1 and p2 (each of which
            calculates a next move given a board and player color),
            and returns either a tuple containing the score for black,
            score for white, and final board (for a normal game ending)
            or a tuple containing the final score for black, final score
            for white, and the  invalid move (for a game that ends with
            and invalid move """

        player1_win_count = 0
        player2_win_count = 0
        draw_count = 0
        (currColor, nextColor) = ("B", "W")

        for i in range(0, self._nplay):
            (p2, p1) = (p1, p2)
            (currColor, nextColor) = (nextColor, currColor)

            board = newBoard()
            p1time = t
            p2time = t
            p1realTime = t * 2  # gives a little extra time to each player
            p2realTime = t * 2

            while not gameOver(board):
                tmpBoard = deepcopy(board)
                t1 = time.time()
                nextMove = p1(tmpBoard, currColor, p1time)
                t2 = time.time()
                p1time = p1time - (t2 - t1)
                p1realTime = p1realTime - (t2 - t1)
                # if p1time < 0:
                if (p1realTime < 0):
                    if currColor == "B":
                        return (0, 16, board, "Timeout")
                    else:
                        return (16, 0, board, "Timeout")
                if valid(board, currColor, nextMove):
                    doMove(board, currColor, nextMove)
                else:
                    if currColor == "B":
                        return (0, 16, board, "Bad Move: %s" % str(nextMove))
                    else:
                        return (16, 0, board, "Bad Move: %s" % str(nextMove))

                (p1, p2) = (p2, p1)
                (p1time, p2time) = (p2time, p1time)
                (p1realTime, p2realTime) = (p2realTime, p1realTime)
                (currColor, nextColor) = (nextColor, currColor)

            # res = score(board) + (board,)

            board_c = Board()
            if self._show_board:

                board_c.print(board)

            res = board_c.score(board)

            if res[0] > res[1]:
                player1_win_count += 1
            elif res[0] < res[1]:
                player2_win_count += 1
            else:
                draw_count += 1

            if self._nplay > 1 and i % self._stat == 0:
                print("Win count, player1(%s): %d, player2(%s): %d, draw: %d" % (player1, player1_win_count, player2, player2_win_count, draw_count))

        if self._nplay > 1:
            print("Win count, player1(%s): %d, player2(%s): %d, draw: %d" % (
                player1, player1_win_count, player2, player2_win_count, draw_count))


        #     if (len(res) == 4):
        #         print(res[3])
        #         if (res[0] > res[1]):
        #             player1_win_count += 1
        #             self.print_winner(player1, player2, res[0], res[1])
        #         else:
        #             player2_win_count += 1
        #             self.print_winner(player2, player1, res[1], res[0])
        #     elif ((res[0] > res[1]) and reversed != "R") or ((res[0] < res[1]) and reversed == "R"):
        #         player1_win_count += 1
        #         self.print_winner(player1, player2, res[0], res[1])
        #     elif ((res[0] < res[1]) and reversed != "R") or ((res[0] > res[1]) and reversed == "R"):
        #         player2_win_count += 1
        #         self.print_winner(player2, player1, res[1], res[0])
        #     else:
        #         draw_count += 1
        #         self.print_winner(player2, player1, res[1], res[0])
        #
        #     if self._nplay > 1 and i % self._stat == 0:
        #         print("Win count, player1(%s): %d, player2(%s): %d, draw: %d" % (player1, player1_win_count, player2, player2_win_count, draw_count))
        #
        # if self._nplay > 1:
        #     print("Win count, player1(%s): %d, player2(%s): %d, draw: %d" % (player1, player1_win_count, player2, player2_win_count, draw_count))


    def print_winner(self, winner, loser, winner_count, loser_count):
        if self._show_result:
            if winner_count == loser_count:
                print("TIE %s, %s, (%d to %d)" % (winner, loser, winner_count, loser_count))
            else:
                print("%s Wins %s Loses (%d to %d)" % (winner, loser, winner_count, loser_count))

