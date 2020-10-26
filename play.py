from game.connect4 import Connect4

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
        win, player = game.player2()
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



playconnect4()