#script for play the game
#for 667 final proj
#Author Weiheng Chai
#email wchai01@syr.edu
###############################################

from game.connect4withai import *

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
    while True:        
        count += 1
        win, player = game.random_player(1)
        if win:
            if player == 3:
                print('all win')
                print(game.chessboard)
                return player,count

            print('player' + str(player) +' win!')
            print(game.chessboard)
            return player,count
            break
        boardfullcheck = game.check_full()
        if boardfullcheck:
            print('board is full, no one win!')
            return 3,count
            break
        win, player,tempcount = game.MCTS_player()
        count += tempcount
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
            return 3,count
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
 

print('please input which ai you want to play with, 1 for random ai, 2 for monte carlo tree search ai:')
x = input()
if x == '1':
    playconnect4withrandomai()
elif x == '2':
    playconnect4withmctsai()
else:
    print('invalid ai')
# count2 = 0
# count1 = 0
# count3 = 0
# countlist = []
# for i in range(0,100):
#     #try:
#     a,count = playconnect4aimctwithrandom(15,15)
#     if a == 2:
#         count2 += 1
#     elif a == 1:
#         count1 += 1
#     elif a == 3:
#         count3 += 1 
#     countlist.append(count)
#     # except:
#     #     print('error')
#     #     continue

# print(count2)
# print(count1)
# print(count3)
# print(countlist)
# fileObject = open('sampleList.txt', 'w')
# for ip in countlist:
#     fileObject.write(str(ip))
#     fileObject.write('\n')
# fileObject.close()
