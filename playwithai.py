#script for play the game
#for 667 final proj
#Author Weiheng Chai
#email wchai01@syr.edu
###############################################

from game.connect4withaimodify import *
from game.CNN import CNNpolicy

def get_cnn_model(boardsize):
    if boardsize == 7:
        net = CNNpolicy(98,7).cuda()
        net.load_state_dict(torch.load('./game/pretrained/7x7.pth'))
        return net.eval()
    elif boardsize == 8:
        net = CNNpolicy(128,8).cuda()
        net.load_state_dict(torch.load('./game/pretrained/8x8.pth'))
        return net.eval()
    elif boardsize == 9:
        net = CNNpolicy(162,9).cuda()
        net.load_state_dict(torch.load('./game/pretrained/9x9.pth'))
        return net.eval()
    elif boardsize == 10:
        net = CNNpolicy(200,10).cuda()
        net.load_state_dict(torch.load('./game/pretrained/10x10.pth'))
        return net.eval()
    elif boardsize == 11:
        net = CNNpolicy(242,11).cuda()
        net.load_state_dict(torch.load('./game/pretrained/11x11.pth'))
        return net.eval()

def playconnect4():
    validsize = [7,8,9,10,11]
    print('please input board size 7,8,9,10,11 for 7x7,8x8,9x9,10x10,11x11:')
    x = input()
    while not x.isdigit() or int(x) == 0 or int(x) not in validsize:
        print('because of the CNN policy is pretrained on some board size, please in put from the listed size')
        print('please input board size 7,8,9,10,11 for 7x7,8x8,9x9,10x10,11x11:')
        x = input()
    net = get_cnn_model(int(x))
    print('please input the first player: 1 for human player, 2 for random player, 3 for MCTS player, 4 for MCTS+NN player')
    player1 = input()
    print('please input the second player: 1 for human player, 2 for random player, 3 for MCTS player, 4 for MCTS+NN player')
    player2 = input()
    game = Connect4(int(x),int(x),net)
    while True:    
        if int(player1) == 1:
            win, player = game.player1()
        elif int(player1) == 2:
            win, player = game.random_player(1)
        elif int(player1) == 3:
            win, player,tempcount,action,reward = game.MCTS_player(1,0)
        elif int(player1) == 4:
            win, player,tempcount,action,reward = game.MCTS_player(1,1)

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
        if int(player2) == 1:
            win, player = game.player2()
        elif int(player2) == 2:
            win, player = game.random_player(2)
        elif int(player2) == 3:
            win, player,tempcount,action,reward = game.MCTS_player(2,0)
        elif int(player2) == 4:
            win, player,tempcount,action,reward = game.MCTS_player(2,1)
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

def playconnectexp(size,iters):
    wincount = 0
    net = get_cnn_model(size)
    rewardlist = [] 
    for i in range(iters):
        game = Connect4(size,size,net)
        reward1total = 0
        reward2total = 0
        while True:    

            win, player,tempcount,action,reward1 = game.MCTS_player(1,0)
            reward1total += reward1


            if win:
                if player == 3:
                    print('all win')
                    print(game.chessboard)
                    break
                elif player == 2:
                    wincount += 1
                print('player' + str(player) +' win!')
                print(game.chessboard)
                break
            boardfullcheck = game.check_full()
            if boardfullcheck:
                print('board is full, no one win!')
                break


            win, player,tempcount,action,reward2 = game.MCTS_player(2,1)
            reward2total += reward2
            if win:
                if player == 3:
                    print('all win')
                    print(game.chessboard)
                    break
                elif player == 2:
                    wincount += 1
                print('player' + str(player) +' win!')
                print(game.chessboard)
                break
            boardfullcheck = game.check_full()
            if boardfullcheck:
                print('board is full, no one win!')
                break
        rewarddif = reward1total - reward2total
        rewardlist.append(rewarddif)
    return wincount,rewardlist

# def playconnect4withrandomai():
#     print('please input widht:')
#     x = input()
#     print('please input height')
#     y = input()
#     while not x.isdigit() or not y.isdigit() or int(x) == 0 or int(y) == 0:
#         print('h or w can not be 0')
#         print('please input widht:')
#         x = input()
#         print('please input height')
#         y = input()

#     game = Connect4(int(x),int(y))
#     while True:        
#         win, player = game.player1()
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             break
#         win, player = game.random_player(2)
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             break

# def playconnect4withmctsai():
#     print('please input widht:')
#     x = input()
#     print('please input height')
#     y = input()
#     while not x.isdigit() or not y.isdigit() or int(x) == 0 or int(y) == 0:
#         print('h or w can not be 0')
#         print('please input widht:')
#         x = input()
#         print('please input height')
#         y = input()

#     game = Connect4(int(x),int(y))
#     countnode = 0
#     while True:        
#         win, player = game.player1()
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             break
#         win, player,count = game.MCTS_player()
#         countnode += count
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             break

# def playconnect4aimctwithrandom(x,y):
#     game = Connect4(x,y)
#     count= 0
#     while True:        
#         count += 1
#         win, player = game.random_player(1)
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 return player,count

#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             return player,count
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             return 3,count
#             break
#         win, player,tempcount = game.MCTS_player()
#         count += tempcount
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 return player,count
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             return player,count
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             return 3,count
#             break

# def playconnect4aimcwithrandom(x,y):
#     game = Connect4(x,y)
#     count= 0
#     while True:        
#         count += 1
#         win, player = game.random_player(1)
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 return player,count
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             return player,count
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             break
#         win, player = game.monte_carlo_player()
#         if win:
#             if player == 3:
#                 print('all win')
#                 print(game.chessboard)
#                 return player,count
#                 break
#             print('player' + str(player) +' win!')
#             print(game.chessboard)
#             return player,count
#             break
#         boardfullcheck = game.check_full()
#         if boardfullcheck:
#             print('board is full, no one win!')
#             break
 

# print('please input which ai you want to play with, 1 for random ai, 2 for monte carlo tree search ai:')
# x = input()
# if x == '1':
#     playconnect4withrandomai()
# elif x == '2':
#     playconnect4withmctsai()
# else:
#     print('invalid ai')
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
# a = playconnectexp(8,100)
# print(a)
# player2win,reward = playconnectexp(11,100)
# print(player2win)
# print(reward)
playconnect4()
