# 667proj
Required package: 

1.python 3.6.8

2.numpy 1.18.4

3.torch==1.2.0

4.torchfile==0.1.0

5.torchsummary==1.5.1

6.torchvision==0.4.0

7.matplotlib==3.1.1

Download python:

https://www.python.org/downloads/


Install numpy:

pip install numpy==1.18.4

For MileStone 1:
Run the code in the command line: 

python play.py 

to play the game.

The play.py is a script to run the game code. The game code is in game folder.

The connect4.py:
This is the implentation part of the connect 4 game.

The player_state is the states of player1 and player2, structure is (H,W,2), 0 means not occupied, 1 means occupied.

Chessboard is combined the player1 and player2's states together, 0 means not occupied, 1 means player1 occupied, 2 means player2 occupied

Functions:
1. update_chessboard(): get the up-to-date state of the chessboard.
2. check_col_available(col): check if one col is full filled, have to do this when the player try to put to this col.
3. player1play(col), player2play(col), the player put the chess in that col, player1play will modify player_state[:,:,0], player2play will modify player_state[:,:,1]
4. win_check(player): check if the player is winner.
5. check_full: check if the chessboard is fully filled.
6. check_available_actions(): check the available actions for the player
7. random_remove(): as the professor's requirement, 1/4 chance one piece is removed, this is the implementation of it. remove the bottom one if not 0, and then shif down.
6. player1(), player2(): integration of all actions the player and the game should take.

For Milestone 2:

Three AI are added, please look at the game/connect4withai.py file:

1. Random player AI

2. Monte Carlo algorithm AI

3. Monte Carlo tree search based AI



Learning the implementation of Monte Carlo tree search from: https://github.com/Alfo5123/Connect4, and using the structure of their code, but most of the code is written by me(maybe only the name of the function is the same) , because of the different structure of the game designed and game rule.

Play the game: 

python playwithai.py, and following the instruction on the command line to select the AI. Did not offer the interface of the Monte Carlo algorithm based AI, because the performance of the MCTs based AI is better.
