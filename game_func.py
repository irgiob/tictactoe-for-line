# tictactoe-for-line/game_func.py
from random import randint
BOARD_SIZE = 3

# initializes empty board
def start_game():
    game_board = [[0,0,0],[0,0,0],[0,0,0]]
    return game_board

# inserts move into board
def play_round(board, player, move):
    board[move[0]-1][move[1]-1] = player
    return board

# checks if board is full
def is_full(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                return False
    return True

# check if there is a winning condition for the player
def check_win(board, player):
    for i in range(BOARD_SIZE):
        if (board[i][0]+board[i][1]+board[i][2] == 3*player or
            board[0][i]+board[1][i]+board[2][i] == 3*player):
            return True
    if (board[0][0]+board[1][1]+board[2][2] == 3*player or 
        board[0][2]+board[1][1]+board[2][0] == 3*player):
        return True
    return False

# check if move made is invalid
def is_invalid_move(board, move):
    row = move[0]
    col = move[1]
    if (row < 1 or col < 1 or row > BOARD_SIZE or col > BOARD_SIZE):
        return 1
    elif board[row-1][col-1] != 0:
        return 2
    return 0

# convert board data to board string for export
def print_board(board):
    count = 1
    output = '    1   2   3  \n  ---------\n'
    for i in range(BOARD_SIZE):
        output += f'{count} '
        count += 1
        for j in range(BOARD_SIZE):
            output += '| '
            if board[i][j] == 0:
                output += '   '
            elif board[i][j] < 0:
                output += 'x '
            elif board[i][j] > 0:
                output += 'o '
        output += '|\n  ---------\n'
    return output

# AI chooses where to play randomly (will update with proper AI)
def AI_choose(board):
    move = [randint(1,3), randint(1,3)]
    while is_invalid_move(board, move) == True:
        move = [randint(1,3), randint(1,3)]
    return move