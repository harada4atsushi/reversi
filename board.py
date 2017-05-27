from gameplay import score


class Board:
    def print(self, board):
        """ Print a board, with letters and numbers as guides """
        print("  " + " ".join(map(chr, range(ord('A'), ord('D') + 1))))
        for (x,y) in zip(range(1,9), board):
            print(str(x) + ' ' + self.to_circle(" ".join(y)))
        print("Black = %d, White = %d" % score(board))

        # For fun, here is a one-line board printer, without the
        # row and column labels
        # print "\n".join(["".join(x) for x in board])

    def to_circle(self, str):
        return str.replace('W', '◯').replace('B', '●')
