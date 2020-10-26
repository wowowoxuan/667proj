# 667proj
Required package: 
1.python 3.6.8
2.numpy 1.18.4

Run the code: 
python play.py to play the game.

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
6. player1(), player2(): integration of all actions the player and the game should take.
