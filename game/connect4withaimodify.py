#This is the implementaion of connect 4 game
#for 667 final project
#author Weiheng Chai
#email wchai01@syr.edu
############################################################

import numpy as np
import random
from random import choice
import copy
import math
import datetime
import torch
import sys
from torch.autograd import Variable




def hwc2chw(state):
    return np.transpose(state, (2, 0, 1))

def chw2hwc(encode):
    return np.transpose(encode, (1, 2, 0))

def update_chessboard(player_state):
    a = player_state[:,:,1].copy()
    a[a == 1] = 2
    return a + player_state[:,:,0]

def player12player2(temp_state):
    transpose1 = np.transpose(temp_state, (2, 0, 1))
    temp_transpose = transpose1.copy()
    transpose1[1] = temp_transpose[0] 
    transpose1[0] = temp_transpose[1]
    result_state = np.transpose(transpose1, (1, 2, 0))
    result_board = update_chessboard(result_state)
    return result_state, result_board

def CNNchoice(net,state,turn):
    if turn == -1:
        state,board = player12player2(state)
    encode = hwc2chw(state)
    actionlist = []
    for i in range(state.shape[0]):
        actionlist.append(i)
    #print(encode)
    variable_state = Variable(torch.FloatTensor(encode))
    cuda_state = variable_state.cuda().unsqueeze(0)
    #print(cuda_state.shape)
    y = net(cuda_state).squeeze(0)
    #print(y)
    m = torch.nn.Softmax(dim = 0)
    
    probs = m(y).cpu().clone().detach().numpy()
    #print(probs)
    a = np.random.choice(actionlist,1,False, probs)[0]
    #print(a)
    return a


def player1play(col, chessboard, player_state):
    row = chessboard.shape[0] - 1
    player_state_copy = copy.deepcopy(player_state)
    while row >= 0:
        if chessboard[row,col] == 0:
            player_state_copy[:,:,0][row,col] = 1
            break
        row -= 1
    return player_state_copy, update_chessboard(player_state_copy)
    

def player2play(col, chessboard, player_state):
    row = chessboard.shape[0] - 1
    player_state_copy = copy.deepcopy(player_state)
    while row >= 0:
        if chessboard[row,col] == 0:
            player_state_copy[:,:,1][row,col] = 1
            break
        row -= 1
    return player_state_copy, update_chessboard(player_state_copy)

def tree_check_col_available(col,chessboard):

    if chessboard[0,col] != 0:
        return False
    return True
    
def tree_check_available_actions(chessboard):
    available_list = []
    for i in range(chessboard.shape[1]):
        if tree_check_col_available(i,chessboard):
            available_list.append(i)
    # print('available actions are:')
    # print(available_list)
    return available_list

def removepiece(col, chessboard, state):
    state_copy = copy.deepcopy(state)
    if chessboard[chessboard.shape[0] - 1, col] != 0:
        i = chessboard.shape[0] - 1
        while i > 0:
            state_copy[:,:,0][i, col] = state_copy[:,:,0][i - 1, col]
            state_copy[:,:,1][i, col] = state_copy[:,:,1][i - 1, col]
            i -= 1
        state_copy[:,:,0][0, col] = 0
        state_copy[:,:,1][0, col] = 0
    return state_copy, update_chessboard(state_copy)

def win_check(player, chessboard, player_state):
        board = np.zeros((chessboard.shape[0],chessboard.shape[1]), dtype = int)
        height = chessboard.shape[0]
        width = chessboard.shape[1]
        if player == 1:
            board = player_state[:,:,0]
        if player == 2:
            board = player_state[:,:,1]
        #horizontal
        for row in range(height):
            for col in range(width - 3):
                if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1 and board[row][col + 3] == 1:
                    return True, player
        #vertical
        for row in range(height - 3):
            for col in range(width):
                if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1 and board[row + 3][col] == 1:
                    return True, player
        #-pi/4 diagonal
        for row in range(height - 3):
            for col in range(width - 3):
                if board[row][col] == 1 and board[row + 1][col + 1] == 1 and board[row + 2][col + 2] == 1 and board[row + 3][col + 3] == 1:
                    return True, player
        #+pi/4 diagonal
        for row in range(3,height):
            for col in range(width - 3):
                if board[row][col] == 1 and board[row - 1][col + 1] == 1 and board[row - 2][col + 2] == 1 and board[row - 3][col + 3] == 1:
                    return True, player
        return False, player
    
def check_full(chessboard):
    zeros = np.sum(chessboard == 0)
    if zeros == 0:
        return True
    return False

class Node():
# Data structure to keep track of our search
    def __init__(self, player_state, chessboard, parent = None):
        self.visits = 1 
        self.reward = 0
        self.state = player_state
        self.chessboard = chessboard
        self.children = []
        self.children_move = []
        self.parent = parent 
        self.move = None

    def addChild( self , child_state, child_chessboard , move ):
        child = Node(child_state,child_chessboard, self)
        child.move = move
        self.children.append(child)
        self.children_move.append(move)

    def update( self,reward ):
        self.reward += reward 
        self.visits += 1

    def fully_explored(self):
        if len(self.children) == len(tree_check_available_actions(self.chessboard)):
            return True
        return False

def checkwin_nextstep(board,state):
    vaild = tree_check_available_actions(board)
    for item in vaild:
        new_state,new_chessboard = player2play(item, board, state)
        win,player = win_check(2, new_chessboard, new_state)
        newnode = Node(new_state,new_chessboard)
        newnode.move = item
        if win:
            return win,newnode
    return False,None


def monte_carlo(root,maxIter):
    win,node = checkwin_nextstep(root.chessboard,root.state)
    if win:
        return node.move
    valid = tree_check_available_actions(root.chessboard)
    scorelist = [0 for n in range(len(valid))]
    numbervisited = [0 for n in range(len(valid))]
    for idex,item in enumerate(valid):
        temp_state,temp_board = player2play(item, root.chessboard, root.state)
        for i in range(maxIter):
            random_remove = random.randint(0,3)
            if random_remove == 0:
                random_piece = random.randint(0,root.chessboard.shape[1]-1)
                new_player_state,new_chessboard = removepiece(random_piece, temp_board,temp_state)
                temp_state = new_player_state
                temp_board = new_chessboard
            win1,_ = win_check(1,temp_board,temp_state)
            win2,_ = win_check(2,temp_board,temp_state)
            if win1 and win2:
                scorelist[idex] += 0
                numbervisited[idex] += 1
                continue
            if win1:
                scorelist[idex] -= 1
                numbervisited[idex] += 1
                continue
            if win2:
                scorelist[idex] += 1
                numbervisited[idex] += 1
                continue
            score, tempcount = search(temp_board,temp_state, -1)
            scorelist[idex] += score
            numbervisited[idex] += tempcount
    maxindex = scorelist.index(max(scorelist))
    return valid[maxindex]

            
                

def search(chessboard,state, turn):
    win1,_ = win_check(1,chessboard,state)
    win2,_ = win_check(2,chessboard,state)
    count = 0
    while check_full(chessboard) == False and not win1 and not win2:
        count += 1
        available_moves = tree_check_available_actions(chessboard)
        new_state = state
        if len(available_moves) > 0:
            randompick = choice(available_moves)
            if turn == -1:
                state,chessboard = player1play(randompick,chessboard,state)
            elif turn == 1:
                state,chessboard = player2play(randompick,chessboard,state)
            win1,_ = win_check(1,chessboard,state)
            win2,_ = win_check(2,chessboard,state) 
            if win1 and win2:
            #print('equal')
                return 0,count
            if win1:
                #print('1win')
                return -1,count
            if win2:
                #print('2win')
                return 1,count
            random_remove = random.randint(0,3)
            if random_remove == 0:
                random_piece = random.randint(0,chessboard.shape[1]-1)
                new_player_state,new_chessboard = removepiece(random_piece, chessboard, state)
                state = new_player_state
                chessboard = new_chessboard
            win1,_ = win_check(1,chessboard,state)
            win2,_ = win_check(2,chessboard,state)   
            
        turn *= -1
        if win1 and win2:
            #print('equal')
            return 0,count
        if win1:
            #print('1win')
            return -1,count
        if win2:
            #print('2win')
            return 1,count
        
    return  0,count

def UCTserach( maxIter , root , factor, policy, net ):
    count = 0
    start = datetime.datetime.now()
    win,node = checkwin_nextstep(root.chessboard,root.state)
    if win:
        return node,count,node.reward
    #print('debug')
    for inter in range(maxIter):
        #print('debug')
        front, turn = treePolicy(root, 1 , factor )
        if policy == 0:
            reward,tempcount = defaultPolicy(front.chessboard,front.state, turn)
        if policy == 1:
            reward,tempcount = CNNPolicy(front.chessboard,front.state, turn,net)
        count += tempcount
        backup(front,reward,turn)

    ans = bestChild(root,0,1)
    print([(c.reward/c.visits) for c in ans.parent.children ])
    end = datetime.datetime.now()
    print(end - start)
    return ans,count,ans.reward


def treePolicy( node, turn , factor ):
    win1,_ = win_check(1,node.chessboard,node.state)
    win2,_ = win_check(2,node.chessboard,node.state)
    while check_full(node.chessboard) == False and not win1 and not win2:
        if ( node.fully_explored() == False ):
            return expand(node, turn), -turn
        else:
            node = bestChild ( node , factor,turn )
            random_remove = random.randint(0,3)
            if random_remove == 0:
                random_piece = random.randint(0,node.chessboard.shape[1]-1)
                new_player_state,new_chessboard = removepiece(random_piece, node.chessboard,node.state)
                node.state = new_player_state
                node.chessboard = new_chessboard
            win1,_ = win_check(1,node.chessboard,node.state)
            win2,_ = win_check(2,node.chessboard,node.state)
            turn *= -1
    return node, turn

def expand( node, turn ):
    tried_children_move = [m for m in node.children_move]
    possible_moves = tree_check_available_actions(node.chessboard)

    for move in possible_moves:
        if move not in tried_children_move:
            #row = node.state.tryMove(move)
            # new_player_state = copy.deepcopy(node.state)
            if turn == -1:
                new_player_state, new_chessboard = player1play(move,node.chessboard,node.state)
                

            elif turn == 1:
                new_player_state, new_chessboard = player2play(move,node.chessboard,node.state)

            break
    random_remove = random.randint(0,3)
    if random_remove == 0:
        random_piece = random.randint(0,new_chessboard.shape[1]-1)
        new_player_state,new_chessboard = removepiece(random_piece, new_chessboard,new_player_state)
    node.addChild(new_player_state,new_chessboard,move)
    return node.children[-1]

def bestChild(node,factor,turn):
    bestscore = -10000000.0
    bestChildren = []
    for c in node.children:
        exploit = c.reward / c.visits
        # if(turn == -1):
        #     exploit = 1-exploit
        explore = math.sqrt(math.log(node.visits)/float(c.visits))
        score = exploit + factor*explore
        if score == bestscore:
            bestChildren.append(c)
        if score > bestscore:
            bestChildren = [c]
            bestscore = score 
    return random.choice(bestChildren)

def defaultPolicy(chessboard,state, turn):
    win1,_ = win_check(1,chessboard,state)
    win2,_ = win_check(2,chessboard,state)
    count = 0
    while check_full(chessboard) == False and not win1 and not win2:
        count += 1
        available_moves = tree_check_available_actions(chessboard)
        new_state = state
        if len(available_moves) > 0:
            randompick = choice(available_moves)
            if turn == -1:
                state,chessboard = player1play(randompick,chessboard,state)
            elif turn == 1:
                state,chessboard = player2play(randompick,chessboard,state)
            win1,_ = win_check(1,chessboard,state)
            win2,_ = win_check(2,chessboard,state) 
            if win1 and win2:
            #print('equal')
                return 0,count
            if win1:
                #print('1win')
                return -1,count
            if win2:
                #print('2win')
                return 1,count
            random_remove = random.randint(0,3)
            if random_remove == 0:
                random_piece = random.randint(0,chessboard.shape[1]-1)
                new_player_state,new_chessboard = removepiece(random_piece, chessboard, state)
                state = new_player_state
                chessboard = new_chessboard
            win1,_ = win_check(1,chessboard,state)
            win2,_ = win_check(2,chessboard,state)   
            
        turn *= -1
        if win1 and win2:
            #print('equal')
            return 0,count
        if win1:
            #print('1win')
            return -1,count
        if win2:
            #print('2win')
            return 1,count
        
    return  0,count

def CNNPolicy(chessboard,state, turn,net):
    win1,_ = win_check(1,chessboard,state)
    win2,_ = win_check(2,chessboard,state)
    count = 0
    while check_full(chessboard) == False and not win1 and not win2:
        count += 1
        available_moves = tree_check_available_actions(chessboard)
        new_state = state
        if len(available_moves) > 0:
            randompick = CNNchoice(net,state,turn)
            while randompick not in available_moves:
                randompick = CNNchoice(net,state,turn)
            if turn == -1:
                state,chessboard = player1play(randompick,chessboard,state)
            elif turn == 1:
                state,chessboard = player2play(randompick,chessboard,state)
            win1,_ = win_check(1,chessboard,state)
            win2,_ = win_check(2,chessboard,state) 
            if win1 and win2:
            #print('equal')
                return 0,count
            if win1:
                #print('1win')
                return -1,count
            if win2:
                #print('2win')
                return 1,count
            random_remove = random.randint(0,3)
            if random_remove == 0:
                random_piece = random.randint(0,chessboard.shape[1]-1)
                new_player_state,new_chessboard = removepiece(random_piece, chessboard, state)
                state = new_player_state
                chessboard = new_chessboard
            win1,_ = win_check(1,chessboard,state)
            win2,_ = win_check(2,chessboard,state)   
            
        turn *= -1
        if win1 and win2:
            #print('equal')
            return 0,count
        if win1:
            #print('1win')
            return -1,count
        if win2:
            #print('2win')
            return 1,count
        
    return  0,count

def backup( node , reward, turn ):
    while node != None:
        node.visits += 1 
        node.reward -= turn*reward
        #node.reward += reward
        node = node.parent
        turn *= -1
    return


def printtree(root):
    print(root.chessboard)
    if len(root.children) == 0:
        return 
    for item in root.children:
        printtree(item)
def getnumofnodes(root):
    if len(root.children) == 0:
        return 1
    result = 1
    for item in root.children:
        result += getnumofnodes(item)
    return result






    



class Connect4:
    def __init__(self, width, height, net):
        self._width = width
        self._height = height
        # self.player_state[:,:,0] = np.zeros((self._height,self._width), dtype = int)
        # self.player_state[:,:,1] = np.zeros((self._height,self._width), dtype = int)
        #the chessboard is the combination of the player_state[:,:,0] and player_state[:,:,1], 1 for player1 occupied 2 for player2 occupied in the chessboard.
        self.chessboard = np.zeros((self._height,self._width), dtype = int)
        self.player_state = np.zeros((self._height,self._width,2), dtype = int)
        self.net = net
    
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
            print(row)
            print(col)
            print(self.chessboard)
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
        return available_list


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

    def random_player(self,i):
        print('player' + str(i) + ' turn')
        self.random_remove()
        win1,player1 = self.win_check(1)
        win2,player2 = self.win_check(2)
        if win1 and win2:
            return win1,3
        if win1:
            return win1, player1        
        if win2:
            return win2, player2
        available_action = self.check_available_actions()
        # print('player2 state:')
        #print(self.player_state)
        randomchoice = choice(available_action)
        print('chessboard:')
        print(self.chessboard)
        if i == 1:
            self.player1play(randomchoice)
        elif i == 2:
            self.player2play(randomchoice)
        win,player = self.win_check(i)
        return win, player
    
    def MCTS_player(self,i,policy):
        print('player' + str(i) + ' turn')
        self.random_remove()
        win1,player1 = self.win_check(1)
        win2,player2 = self.win_check(2)
        if win1 and win2:
            return win1,3,0,-1,0
        if win1:
            return win1, player1,0,-1,0       
        if win2:
            return win2, player2,0,-1,0
        temp_state = self.player_state.copy()
        temp_board = self.chessboard.copy()

        if i == 1:
            transpose1 = np.transpose(temp_state, (2, 0, 1))
            temp_transpose = transpose1.copy()
            transpose1[1] = temp_transpose[0] 
            transpose1[0] = temp_transpose[1]
            temp_state = np.transpose(transpose1, (1, 2, 0))
            temp_board = update_chessboard(temp_state)



        root = Node(temp_state,temp_board)
        iter = 100
        if self._width > 15 or self._height > 15:
            iter = 100
        if self._width > 20 or self._height > 20:
            iter = 50
        if self._width > 40 or self._height > 40:
            iter = 1
        if self._width > 80 or self._height > 80:
            print('=================================================================================')
            print("please select a smaller size board for using the mct ai!!!!!!!!!!!!!!!!!!!!!!!!")
            print('=================================================================================')
        #print('debug1')
        ans,count,reward = UCTserach( iter , root , 2,policy,self.net)
        print('chessboard:')
        print(self.chessboard)
        if i == 1:
            self.player1play(ans.move)
        if i == 2:
            self.player2play(ans.move)
        win,player = self.win_check(2)
        return win, player,count,ans.move,reward

    def monte_carlo_player(self):
        print('player2' + ' turn')
        self.random_remove()
        win1,player1 = self.win_check(1)
        win2,player2 = self.win_check(2)
        if win1 and win2:
            return win1,3
        if win1:
            return win1, player1        
        if win2:
            return win2, player2
        root = Node(self.player_state,self.chessboard)
        iter = 100
        if self._width > 10 or self._height > 10:
            iter = 1000
        if self._width > 20 or self._height > 20:
            iter = 100
        if self._width > 40 or self._height > 40:
            iter = 1
        if self._width > 80 or self._height > 80:
            print('=================================================================================')
            print("please select a smaller size board for using the mct ai!!!!!!!!!!!!!!!!!!!!!!!!")
            print('=================================================================================')
        ans = monte_carlo(root,iter)
        print('chessboard:')
        print(self.chessboard)

        self.player2play(ans)
        win,player = self.win_check(2)
        return win, player

    def tree_check_col_available(self,col,chessboard):
        if col > self._width - 1 or col < 0:
            return False
        if chessboard[0,col] != 0:
            return False
        return True
    
    def tree_check_available_actions(self,chessboard):
        available_list = []
        for i in range(self._width):
            if self.tree_check_col_available(i,chessboard):
                available_list.append(i)
        print('available actions are:')
        print(available_list)
        return available_list

    def tree_player(self,i):
        return 'not implent'

# c4 = Connect4(10,10)
# root = Node(c4.player_state,c4.chessboard)
# ans = UCTserach( 3000, root , 1 )
# print(getnumofnodes(root))
# #printtree(root)
# print(ans.move)






