from board import Board


class NaivePlayer:
    """
    常に同一のポリシーで同じ手を打つプレーヤー
    盤面の左上を起点に、右に一つずつ移していき、
    最初に到達した打てる箇所に打つ
    """

    def __init__(self, color):
        self.color = color
        self.name = 'naive'

    def next_move(self, board_data, color):
        board = Board(board_data)
        positions = board.valid_positions(self)

        if len(positions) == 0:
            return "pass"

        for row_i in range(0, 4):
            for col_i in range(0, 4):
                if (row_i, col_i) in positions:
                    return (row_i, col_i)


    def nextMoveR(self, board, color, time):
        return self.next_move(board, color)


    def getGameResult(self, board_data, game_ended=False, opponent_player=None):
        pass
