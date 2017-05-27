from gameplay import valid


class Board:
    def print(self, board):
        """ Print a board, with letters and numbers as guides """
        print("  " + " ".join(map(chr, range(ord('A'), ord('D') + 1))))
        for (x,y) in zip(range(1,9), board):
            print(str(x) + ' ' + self.to_circle(" ".join(y)))
        print("Black = %d, White = %d" % self.score(board))

        # For fun, here is a one-line board printer, without the
        # row and column labels
        # print "\n".join(["".join(x) for x in board])

    def to_circle(self, str):
        return str.replace('W', '◯').replace('B', '●')


    def score(self, board):
        """ returns the current score for the board as a tuple
            containing # of black pieces, # of white pieces """
        black = white = 0
        for row in board:
            for square in row:
                if (square == "B"):
                    black = black + 1
                elif (square == "W"):
                    white = white + 1
        return (black, white)


    def valid_positions(self, board, player):
        moves = []
        for i in range(4):
            for j in range(4):
                if valid(board, player.color, (i, j)):
                    moves.append((i, j))
        return moves
