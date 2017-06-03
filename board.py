from gameplay import valid


class Board:
    def __init__(self, board_data):
        self.board_data = board_data

    def print(self, q=None):
        """ Print a board, with letters and numbers as guides """
        print("   " + "  ".join(map(chr, range(ord('A'), ord('D') + 1))))
        for (x, y) in zip(range(1,9), self.board_data):
            row = y
            if q is not None:
                row = []
                for i, piece in enumerate(y):
                    if piece == '.':
                        piece = q.get(tuple(self.flattend_data()), (x,i))
                    row.append(str(piece))

            y_str = self.to_circle("  ".join(row))

            print(str(x) + '  ' + y_str)
        print("Black = %d, White = %d" % self.score())

        # For fun, here is a one-line board printer, without the
        # row and column labels
        # print "\n".join(["".join(x) for x in board])

    def to_circle(self, str):
        return str.replace('W', '◯').replace('B', '●')


    def score(self):
        """ returns the current score for the board as a tuple
            containing # of black pieces, # of white pieces """
        black = white = 0
        for row in self.board_data:
            for square in row:
                if (square == "B"):
                    black = black + 1
                elif (square == "W"):
                    white = white + 1
        return (black, white)


    def valid_positions(self, player):
        moves = []
        for i in range(4):
            for j in range(4):
                if valid(self.board_data, player.color, (i, j)):
                    moves.append((i, j))
        return moves


    def flattend_data(self):
        return [flatten for inner in self.board_data for flatten in inner]


    def color_of_more(self):
        res = self.score()

        if res[0] > res[1]:
            return 'B'
        elif res[0] < res[1]:
            return 'W'
        else:
            return ''


    def is_game_over(self):
        """ return true if the game is over, that is, no valid moves """
        return valid(self.board_data, "B", 'pass') and valid(self.board_data, "W", 'pass')

