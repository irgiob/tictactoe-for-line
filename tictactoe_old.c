#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define BOARD_SIZE 3
#define GAME_ON 1
#define GAME_END 0
#define PLAYER_1 -1

typedef int board_t[BOARD_SIZE][BOARD_SIZE];

void start_game(int opponent);
void print_board(board_t board);
int is_full(board_t board);
int is_invalid_move(board_t board, int row, int col);
void play_round(board_t board, int player);
int check_win(board_t board, int player);
void AI_choose(board_t board, int *row, int *col);

int main(int argc, char *argv[]) {
    int opponent;
    srand(time(NULL));
    printf("\nIt's time for some Tic-Tac-Toe!\n");
    printf("Type 1 to verse Human & 2 to verse AI: ");
    scanf("%d", &opponent);
    start_game(opponent);
}

void start_game(int opponent) {
    board_t board = {{0,0,0},{0,0,0},{0,0,0}};
    print_board(board);
    while (GAME_ON) {
        play_round(board, PLAYER_1);
        play_round(board, opponent);
    }
}

void play_round(board_t board, int player) {
    int row = 0, col = 0;
    if (player == PLAYER_1 || player == 1) {
        printf("Player %d, choose board location (row col): ", (int)(0.5*player+1.5));
        while (is_invalid_move(board, row, col)) {
            scanf("%d %d",&row,&col);
            if (is_invalid_move(board, row, col) == 1) {
                printf("Out of bounds, try again: ");
            } else if (is_invalid_move(board, row, col) == 2) {
                printf("Space already filled, try again: ");
            }
        }
    } else if (player == 2) {
        AI_choose(board, &row, &col);
    }
    board[row-1][col-1] = player;
    print_board(board);
    if (check_win(board,player) || is_full(board)) {
        if (check_win(board,player)) {
            printf("  Player %d wins!\n\n", (int)(0.5*player+1.5));
        } else if (is_full(board)) {
            printf("   It's a tie!\n\n");
        }
        printf("Thank you for playing\n\n");
        exit(GAME_END);
    }
}

void print_board(board_t board) {
    int i,j, count = 1;
    printf("\n    1   2   3  \n  -------------\n");
    for (i=0;i<BOARD_SIZE;i++) {
        printf("%d ", count++);
        for (j=0;j<BOARD_SIZE;j++) {
            printf("| ");
            if (board[i][j] == 0) {
                printf("  ");
            } else if (board[i][j] < 0) {
                printf("X ");
            } else if (board[i][j] > 0) {
                printf("O ");
            }
        }
        printf("|\n  -------------\n");
    }
    printf("\n");
}

int is_full(board_t board) {
    int i,j;
    for (i=0;i<BOARD_SIZE;i++) {
        for (j=0;j<BOARD_SIZE;j++) {
            if (board[i][j] == 0) {
                return 0;
            }
        }
    }
    return 1;
}

int check_win(board_t board, int player) {
    int i;
    for (i=0;i<BOARD_SIZE;i++) {
        if (board[i][0]+board[i][1]+board[i][2] == 3*player ||
            board[0][i]+board[1][i]+board[2][i] == 3*player) {
            return 1;
        }
    }
    if (board[0][0]+board[1][1]+board[2][2] == 3*player || 
        board[0][2]+board[1][1]+board[2][0] == 3*player) {
        return 1;
    }
    return 0;
}

int is_invalid_move(board_t board, int row, int col) {
    if (row < 1 || col < 1 || row > BOARD_SIZE || col > BOARD_SIZE) {
        return 1;
    } else if (board[row-1][col-1] != 0) {
        return 2;
    }
    return 0;
}

void AI_choose(board_t board, int *row, int *col) {
    while (is_invalid_move(board,*row,*col)) {
        *row = rand()%3+1;
        *col = rand()%3+1;
    }
    printf("The AI has picked spot (%d,%d)\n",*row,*col);
}