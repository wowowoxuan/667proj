#script for play the game
#for 667 final proj
#Author Weiheng Chai
#email wchai01@syr.edu
###############################################

from connect4withai import *
import numpy as np
def playconnect4():
    print('please input widht:')
    x = input()
    print('please input height')
    y = input()
    while not x.isdigit() or not y.isdigit() or int(x) == 0 or int(y) == 0:
        print('h or w can not be 0')
        print('please input widht:')
        x = input()
        print('please input height')
        y = input()

    game = Connect4(int(x),int(y))
    while True:        
        win, player = game.player1()
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break
        win, player = game.random_player(2)
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break

def playconnect4withrandomai():
    print('please input widht:')
    x = input()
    print('please input height')
    y = input()
    while not x.isdigit() or not y.isdigit() or int(x) == 0 or int(y) == 0:
        print('h or w can not be 0')
        print('please input widht:')
        x = input()
        print('please input height')
        y = input()

    game = Connect4(int(x),int(y))
    while True:        
        win, player = game.player1()
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break
        win, player = game.random_player(2)
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break

def playconnect4withmctsai():
    print('please input widht:')
    x = input()
    print('please input height')
    y = input()
    while not x.isdigit() or not y.isdigit() or int(x) == 0 or int(y) == 0:
        print('h or w can not be 0')
        print('please input widht:')
        x = input()
        print('please input height')
        y = input()

    game = Connect4(int(x),int(y))
    countnode = 0
    while True:        
        win, player = game.player1()
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break
        win, player,count = game.MCTS_player()
        countnode += count
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break

def playconnect4aimctwithrandom(x,y):
    game = Connect4(x,y)
    count= 0
    input_data = []
    output_data = []
    while True:        
        count += 1
        win, player = game.random_player(1)
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count,input_data,output_data

            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count,input_data,output_data
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            return 3,count,input_data,output_data
            break
        input_data.append(game.player_state)
        win, player,tempcount,action = game.MCTS_player()
        output_data.append(action)
        count += tempcount
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count,input_data,output_data
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count,input_data,output_data
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            return 3,count,input_data,output_data
            break

def playconnect4aimctwithmct(x,y):
    game = Connect4(x,y)
    count= 0
    input_data = []
    output_data = []
    while True:        
        count += 1
        tempstate = game.player_state.copy()
        tempstate,_ = player12player2(tempstate)
        input_data.append(tempstate)
        win, player,tempcount,action = game.MCTS_player2(1)
        output_data.append(action)
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count,input_data,output_data

            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count,input_data,output_data
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            return 3,count,input_data,output_data
            break
        input_data.append(game.player_state)
        win, player,tempcount,action = game.MCTS_player2(2)
        output_data.append(action)
        count += tempcount
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count,input_data,output_data
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count,input_data,output_data
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            return 3,count,input_data,output_data
            break

def playconnect4aimcwithrandom(x,y):
    game = Connect4(x,y)
    count= 0
    
    while True:        
        count += 1
        win, player = game.random_player(1)
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break
        win, player = game.monte_carlo_player()
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count
                break
            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            break
 

count2 = 0
count1 = 0
count3 = 0
countlist = []
input_data = []
output_data = []
for i in range(0,200):
    #try:
    a,count,input,output = playconnect4aimctwithmct(11,11)
    #print(input)
    input_temp = []
    for item in input:
        temp = np.transpose(item, (2, 0, 1))
        #print(temp)
        input_temp.append(temp)
        # test = np.transpose(temp, (1, 2, 0))

        # print(test - item)
    #print(input_temp)
    print(input_temp)
    print(output)
    input_data += input_temp
    output_data += output
    if a == 2:
        count2 += 1
    elif a == 1:
        count1 += 1
    elif a == 3:
        count3 += 1 
    countlist.append(count)
    # except:
    #     print('error')
    #     continue
input_data = np.array(input_data)
output_data = np.array(output_data)
print(input_data.shape)
print(output_data.shape)
np.save('./data1/state11x11.npy',input_data)
np.save('./data1/action11x11.npy',output_data)
print(input_data[0].shape)
#print(output_data)
# print(count2)
# print(count1)
# print(count3)
# print(countlist)
# fileObject = open('sampleList.txt', 'w')
# for ip in countlist:
#     fileObject.write(str(ip))
#     fileObject.write('\n')
# fileObject.close()
