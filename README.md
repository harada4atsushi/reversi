Creating three AI agents that play the game Reversi (also known by the trademark Othello).

Written by python

**gameplay.py**

This file will plays two AI agents against each other. From the command line, this function is invoked with:

	% python gameplay.py [-t ] [-v] [-r] player1 player2
	
Where player1.py and player2.py are python files that contain a nextMove and nextMoveR. The flags -v stands for verbose output (display the board after every turn, already implemented), and -r stands for "reversed" (use nextMoveR rather than nextMove).

**randomPlay.py**

AI agent that makes a random legal move

**simpleGreedy.py**

AI agent that uses a brain-dead evaluation function, with no search

**minMax.py**

AI agent that uses a minmax search, with alpha-beta pruning

For example, you could have two random players play against each other with:
	
	% python gameplay.py randomPlay randomPlay

If you wanted to play simpleGreedy against randomPlay (with simpleGreedy going first), seeing all the moves, with a clock of 150 seconds:
	
	% python gameplay.py -t150 -v simpleGreedy randomPlay 
