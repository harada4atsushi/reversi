import sys
import time
import getopt




def opponent(x):
    """ Given a string representing a color (must be either "B" or "W"),
        return the opposing color """ 
    if x == "b" or x == "B" or x == '●':
        return "W"
    elif x == "w" or x == "W" or x == '◯':
        return "B"
    else:
        return "."
    

def validMove(board, color, pos):
    """ Given a 2D array representing a board, a string
        representing a color, and a tuple representing a
        position, return true if the position is a valid
        move for the color """
    if board[pos[0]][pos[1]] != '.':
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if canFlip(board, color, pos, (i,j)):
                    return True
    return False

def valid(board, color, move):
    """ Given a 2D array representing a board, a string
        representing a color, and either a tuple representing a
        position or the string "pass", return true if the move
        is a valid for the color """
    if move == "pass":
        for i in range(0,4):
            for j in range(0,4):
                if validMove(board, color, (i,j)):
                    return False
        return True
    else:
        return validMove(board, color, move)


def validPos(x,y):
    """ Return true of the (x,y) position is within the board """
    return x >= 0 and x < 4 and y >= 0 and y < 4

def doFlip(board, color, pos, direction):
    """ Given a 2D array representing a board, a color, a position
        to move to, and a tuple representing a direction ( (-1,0)
        for up, (-1,1) for up and to the right, (0,1) for to the right,
        and so on), flip all the pieces in the direction until a
        piece of the same color is found """
    currX = pos[0] + direction[0]
    currY = pos[1] + direction[1]
    while board[currX][currY] == opponent(color):
        board[currX][currY] = color
        (currX, currY) = (currX + direction[0], currY + direction[1])        



def doMove(board, color, pos):
    """ Given a 2D array representing a board, a color, and a position,
        implement the move on the board.  Note that the move is assumed
        to be valid """
    if pos != "pass":
        if validMove(board, color, pos):
            board[pos[0]][pos[1]] = color
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 or j != 0:
                        if canFlip(board, color, pos, (i,j)):
                            doFlip(board, color, pos, (i,j))
        

def canFlip(board, color, pos, direction):
    """ Given a 2D array representing a board, a color, a position
        to move to, and a tuple representing a direction ( (-1,0)
        for up, (-1,1) for up and to the right, (0,1) for to the right,
        and so on), determine if there is a sequence of opponent pieces,
        followed by a color piece, that would allow a flip in this direction
        from this position, if a color piece is placed at pos """
    currX = pos[0] + direction[0]
    currY = pos[1] + direction[1]
    if not validPos(currX,currY):
        return False
    if board[currX][currY] != opponent(color):
        return False
    while True:
        (currX, currY) = (currX + direction[0], currY + direction[1])
        if not validPos(currX, currY):
            return False
        if board[currX][currY] == color:
            return True
        if board[currX][currY] == '.':
            return False


def newBoard():
    """ Create a new board:  2D array of strings:
        'B' for black, 'W' for white, and '.' for empty """
    result = []
    for i in range(1):
        result = result + [["."]*4]
    result = result + [["."] * 1 + ["W","B"] + ["."] * 1]
    result = result + [["."] * 1 + ["B","W"] + ["."] * 1]
    for i in range(1):
        result = result + [["."]*4]
    return result


def gameOver(board):
    """ return true if the game is over, that is, no valid moves """
    return valid(board, "B", 'pass') and valid(board, "W", 'pass') 

def score(board):
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


##options: -r is reversed game; -v is verbose (print board & time after each move)
##  -t is a time to play (other than the default)
if __name__ == "__main__":
    try:
        optlist,args=getopt.getopt(sys.argv[1:],'vt:r')
    except getopt.error:
        print("Usage: python %s {-r} {-v} {-t time} player1 player2" % (sys.argv[0]))
        exit()

    verbose = False
    clockTime = 320.0
    reversed = ""
    for (op,opVal) in optlist:
        if (op == "-v"):
            verbose = True
        if (op == "-t"):
            clockTime = float(opVal)
        if (op == "-r"):
            reversed = "R"
    s1 = "from " + args[0] + " import nextMove" + reversed;
    print(s1)
    s2 = "from " + args[1] + " import nextMove" + reversed;
    print(s2)
    exec("from " + args[0] + " import nextMove"+reversed)
    if (reversed != "R"):
        p1 = nextMove
    else:
        p1 = nextMoveR
    exec("from " + args[1] + " import nextMove"+reversed)
    if (reversed != "R"):
        p2 = nextMove
    else:
        p2 = nextMoveR

    from organizer import Organizer
    organizer = Organizer()
    res = organizer.play_game(p1, p2, verbose, clockTime)

    if (len(res) == 4):
        print(res[3])
        if (res[0] > res[1]):
            print("%s Wins %s Loses (%d to %d)" %(args[0], args[1], res[0], res[1]))
        else:
            print("%s Wins %s Loses (%d to %d)" %(args[1], args[0], res[1], res[0]))
    elif ((res[0] > res[1]) and reversed != "R") or ((res[0] < res[1]) and reversed == "R"):
        print("%s Wins %s Loses (%d to %d)" %(args[0], args[1], res[0], res[1]))
    elif ((res[0] < res[1]) and reversed != "R") or ((res[0] > res[1]) and reversed == "R"):
        print("%s Wins %s Loses (%d to %d)" %(args[1], args[0], res[1], res[0]))
    else:
        print("TIE %s, %s, (%d to %d)" % (args[1], args[0], res[1], res[0]))