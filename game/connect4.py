#This is the implementaion of connect 4 game
#for 667 final project
#author Weiheng Chai
#email wchai01@syr.edu
############################################################

import numpy as np
import random

class Connect4:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        # self.player_state[:,:,0] = np.zeros((self._height,self._width), dtype = int)
        # self.player_state[:,:,1] = np.zeros((self._height,self._width), dtype = int)
        #the chessboard is the combination of the player_state[:,:,0] and player_state[:,:,1], 1 for player1 occupied 2 for player2 occupied in the chessboard.
        self.chessboard = np.zeros((self._height,self._width), dtype = int)
        self.player_state = np.zeros((self._height,self._width,2), dtype = int)
    
    #
    def update_chessboard(self):
        a = self.player_state[:,:,1].copy()
        a[a == 1] = 2
        self.chessboard = a + self.player_state[:,:,0]

    def check_col_available(self,col):
        if col > self._width - 1 or col < 0:
            return False
        if self.chessboard[0,col] != 0:
            return False
        return True
    
    def player1play(self,col):
        row = self._height - 1
        while row >= 0:
            if self.chessboard[row,col] == 0:
                self.player_state[:,:,0][row,col] = 1
                break
            row -= 1
        self.update_chessboard()
        print(self.chessboard)

    def player2play(self,col):
        row = self._height - 1
        while row >= 0:
            if self.chessboard[row,col] == 0:
                self.player_state[:,:,1][row,col] = 1
                break
            row -= 1
        self.update_chessboard()
        print(self.chessboard)
    
    def win_check(self, player):
        board = np.zeros((self._height,self._width), dtype = int)
        if player == 1:
            board = self.player_state[:,:,0]
        if player == 2:
            board = self.player_state[:,:,1]
        #horizontal
        for row in range(self._height):
            for col in range(self._width - 3):
                if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1 and board[row][col + 3] == 1:
                    return True, player
        #vertical
        for row in range(self._height - 3):
            for col in range(self._width):
                if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1 and board[row + 3][col] == 1:
                    return True, player
        #-pi/4 diagonal
        for row in range(self._height - 3):
            for col in range(self._width - 3):
                if board[row][col] == 1 and board[row + 1][col + 1] == 1 and board[row + 2][col + 2] == 1 and board[row + 3][col + 3] == 1:
                    return True, player
        #+pi/4 diagonal
        for row in range(3,self._height):
            for col in range(self._width - 3):
                if board[row][col] == 1 and board[row - 1][col + 1] == 1 and board[row - 2][col + 2] == 1 and board[row - 3][col + 3] == 1:
                    return True, player
        return False, player
    
    def check_full(self):
        zeros = np.sum(self.chessboard == 0)
        if zeros == 0:
            return True
        return False

    def check_available_actions(self):
        available_list = []
        for i in range(self._width):
            if self.check_col_available(i):
                available_list.append(i)
        print('available actions are:')
        print(available_list)


    def random_remove(self):
        random_remove = random.randint(0,3)
        if random_remove == 0:
            random_col = random.randint(0,self._width - 1)
            if self.chessboard[self._height - 1, random_col] != 0:
                i = self._height - 1
                while i > 0:
                    self.player_state[:,:,0][i, random_col] = self.player_state[:,:,0][i - 1, random_col]
                    self.player_state[:,:,1][i, random_col] = self.player_state[:,:,1][i - 1, random_col]
                    i -= 1
                self.player_state[:,:,0][0, random_col] = 0
                self.player_state[:,:,1][0, random_col] = 0
        self.update_chessboard()
    def player1(self):
        print('player1 turn')
        self.random_remove()
        win1,player1 = self.win_check(1)
        win2,player2 = self.win_check(2)
        if win1 and win2:
            return win1,3
        if win1:
            return win1, player1        
        if win2:
            return win2, player2
        self.check_available_actions()
        # print('player1 state:')
        # print(self.player_state[:,:,0])
        print('chessboard:')
        #print(self.player_state)
        print(self.chessboard)
        print('please input the col player1 want to put between 0 and' + str(self._width - 1) + ':')
        player1input = input()
        while player1input == '' or not player1input.isdigit() or int(player1input) < 0 or int(player1input) > self._width - 1 or not self.check_col_available(int(player1input)):
            print('invalid input!')
            if player1input == '':
                print('input can not be none')
            elif not player1input.isdigit():
                print('please input int')
            elif not self.check_col_available(int(player1input)):
                print('the col is full')
            else:
                print('input not in range')  
            print('please input the col player1 want to put between 0 and' + str(self._width - 1) + ':')
            player1input = input()
        self.player1play(int(player1input))
        boardfullcheck = self.check_full()
        win,player = self.win_check(1)
        return win, player
    
    def player2(self):
        print('player2 turn')
        self.random_remove()
        win1,player1 = self.win_check(1)
        win2,player2 = self.win_check(2)
        if win1 and win2:
            return win1,3
        if win1:
            return win1, player1        
        if win2:
            return win2, player2
        self.check_available_actions()
        # print('player2 state:')
        #print(self.player_state)
        print('chessboard:')
        print(self.chessboard)
        print('please input the col player2 want to put between 0 and' + str(self._width - 1) + ':')
        player2input = input()
        while player2input == '' or not player2input.isdigit() or int(player2input) < 0 or int(player2input) > self._width - 1 or not self.check_col_available(int(player2input)):
            print('invalid input!')
            if player2input == '':
                print('input can not be none')
            elif not player2input.isdigit():
                print('please input int')
            elif not self.check_col_available(int(player2input)):
                print('the col is full')
            else:
                print('input not in range')  
            print('please input the col player2 want to put between 0 and' + str(self._width - 1) + ':')
            player2input = input()
        self.player2play(int(player2input))
        win,player = self.win_check(2)
        return win, player






