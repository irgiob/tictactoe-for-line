# tictactoe-for-line/game_func.py

BOARD_SIZE = 3

def start_game():
    game_board = [[0,0,0],[0,0,0],[0,0,0]]

def print_board(board):
    count = 1
    output = '    1   2   3  \n  -------------\n'
    for i in range(BOARD_SIZE):
        output += f'{count} '
        count += 1
        for j in range(BOARD_SIZE):
            output += '| '
            if board[i][j] == 0:
                output += '  '
            elif board[i][j] < 0:
                output += 'X '
            elif board[i][j] > 0:
                output += 'O '
        output += '|\n  -------------\n'
    return output