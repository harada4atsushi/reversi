import time
from copy import deepcopy
from gameplay import newBoard, gameOver, valid, doMove, score


class Organizer:
    def play_game(self, p1, p2, verbose=False, t=128):
        """ Takes as input two functions p1 and p2 (each of which
            calculates a next move given a board and player color),
            and returns either a tuple containing the score for black,
            score for white, and final board (for a normal game ending)
            or a tuple containing the final score for black, final score
            for white, and the  invalid move (for a game that ends with
            and invalid move """
        board = newBoard()
        (currColor, nextColor) = ("B", "W")
        p1time = t
        p2time = t
        p1realTime = t * 2  # gives a little extra time to each player
        p2realTime = t * 2
        if verbose:
            printBoard(board)
            print("START: Clock remaining: %s=%f, %s=%f" % (currColor, p1time, nextColor, p2time))
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
            if verbose:
                printBoard(board)
                print("Clock remaining: %s=%f, %s=%f" % (currColor, p1time, nextColor, p2time))

        return score(board) + (board,)