import sys
import time
import getopt
from copy import deepcopy

def opponent(x):
    """ Given a string representing a color (must be either "B" or "W"),
        return the opposing color """ 
    if x == "b" or x == "B":
        return "W"
    elif x == "w" or x == "W":
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
        for i in range(0,8):
            for j in range(0,8):
                if validMove(board, color, (i,j)):
                    return False
        return True
    else:
        return validMove(board, color, move)


def validPos(x,y):
    """ Return true of the (x,y) position is within the board """
    return x >= 0 and x < 8 and y >= 0 and y < 8

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
    for i in range(3):
        result = result + [["."]*8]
    result = result + [["."] * 3 + ["W","B"] + ["."] * 3]
    result = result + [["."] * 3 + ["B","W"] + ["."] * 3]
    for i in range(3):
        result = result + [["."]*8]
    return result


def printBoard(board):
    """ Print a board, with letters and numbers as guides """
    print " " + "".join(map(chr, range(ord('A'), ord('H') + 1)))
    for (x,y) in zip(range(1,9), board):
        print str(x) + "".join(y) 
    print("Black = %d, White = %d") % score(board)

    # For fun, here is a one-line board printer, without the
    # row and column labels
    # print "\n".join(["".join(x) for x in board])

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

def playGame(p1, p2, verbose = False, t = 128):
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
    p1realTime = t*2 # gives a little extra time to each player
    p2realTime = t*2
    if verbose:
        printBoard(board)
        print "START: Clock remaining: %s=%f, %s=%f" %(currColor, p1time, nextColor, p2time)
    while not gameOver(board):       
        tmpBoard = deepcopy(board)
        t1 = time.time()
        nextMove = p1(tmpBoard, currColor, p1time)
        t2 = time.time()
        p1time = p1time - (t2 - t1)
        p1realTime = p1realTime - (t2 - t1)
        #if p1time < 0:
        if (p1realTime < 0):
            if currColor == "B":
                return (0,64, board, "Timeout")
            else:
                return (64, 0, board, "Timeout")  
        if valid(board, currColor, nextMove):
            doMove(board, currColor, nextMove)
        else:
            if currColor == "B":
                return (0,64, board, "Bad Move: %s" %str(nextMove))
            else:
                return (64, 0, board, "Bad Move: %s" %str(nextMove))

        (p1, p2) = (p2, p1)
        (p1time, p2time) = (p2time, p1time)
        (p1realTime, p2realTime) = (p2realTime, p1realTime)
        (currColor, nextColor) = (nextColor, currColor)
        if verbose:
            printBoard(board)
            print "Clock remaining: %s=%f, %s=%f" %(currColor, p1time, nextColor, p2time)
        
    return score(board) + (board,)

##options: -r is reversed game; -v is verbose (print board & time after each move)
##  -t is a time to play (other than the default)
if __name__ == "__main__":
    try:
        optlist,args=getopt.getopt(sys.argv[1:],'vt:r')
    except getopt.error:
        print "Usage: python %s {-r} {-v} {-t time} player1 player2" % (sys.argv[0])
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
    print s1    
    s2 = "from " + args[1] + " import nextMove" + reversed;
    print s2   
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

    res = playGame(p1, p2, verbose, clockTime)
    printBoard(res[2])
    if (len(res) == 4):
        print res[3]
        if (res[0] > res[1]):
            print "%s Wins %s Loses (%d to %d)" %(args[0], args[1], res[0], res[1])
        else:
            print "%s Wins %s Loses (%d to %d)" %(args[1], args[0], res[1], res[0])
    elif ((res[0] > res[1]) and reversed != "R") or ((res[0] < res[1]) and reversed == "R"):
        print "%s Wins %s Loses (%d to %d)" %(args[0], args[1], res[0], res[1])
    elif ((res[0] < res[1]) and reversed != "R") or ((res[0] > res[1]) and reversed == "R"):
        print "%s Wins %s Loses (%d to %d)" %(args[1], args[0], res[1], res[0])
    else:
        print "TIE %s, %s, (%d to %d)" % (args[1], args[0], res[1], res[0])