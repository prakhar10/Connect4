#!/usr/bin/env python

import copy
import random
import sys

utility_value = {}
score_list = []
infinity = float('inf')


class MaxConnect4game:
    def __init__(self):
        self.gameboard = [[0 for i in range(7)] for j in range(6)]
        self.current_move = 0
        self.piece_count = 0
        self.player1Score = 0
        self.player2Score = 0
        self.gameFile = None
        self.computer_column = None
        self.depth = 1

    def checkPieceCount(self):
        self.piece_count = sum(1 for row in self.gameboard for piece in row if piece)

    def getPieceCount(self):
        return sum(1 for row in self.gameboard for piece in row if piece)

    def display_gameboard(self):
        print(' ------------------------')
        for i in range(6):
            print(' |'),
            for j in range(7):
                print('%d ' % int(self.gameboard[i][j])),
            print('| ')
        print(' ------------------------')

    def printGameBoardToFile(self):
        for row in self.gameboard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.current_move))

    def minimax(self, depth):
        current_state = copy.deepcopy(self.gameboard)
        for i in range(7):
            if self.playPiece(i) != None:
                if self.piece_count == 42 or self.depth == 0:
                    self.gameboard = copy.deepcopy(current_state)
                    return i
                else:
                    val = self.min_val(self.gameboard, -infinity, infinity, depth - 1)

                    utility_value[i] = val
                    self.gameboard = copy.deepcopy(current_state)

        max_utility_value = max([i for i in utility_value.values()])
        for i in range(7):
            if i in utility_value:
                if utility_value[i] == max_utility_value:
                    utility_value.clear()
                    return i

    def max_val(self, current_node, alpha, beta, depth):
        parent_node = copy.deepcopy(current_node)
        value = -infinity
        child_nodes = []
        for i in range(7):
            current_state = self.playPiece(i)
            if current_state != None:
                child_nodes.append(self.gameboard)
                self.gameboard = copy.deepcopy(parent_node)

        if child_nodes == [] or depth == 0:
            self.countScore1(self.gameboard)
            return self.evaluation_function(self.gameboard)
        else:
            for node in child_nodes:
                self.gameBoard = copy.deepcopy(node)
                value = max(value, self.min_val(node, alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

    def min_val(self, current_node, alpha, beta, depth):
        parent_node = copy.deepcopy(current_node)
        if self.current_move == 1:
            opponent = 2
        elif self.current_move == 2:
            opponent = 1
        value = infinity
        child_nodes = []
        for i in range(7):
            current_state = self.check_piece(i, opponent)
            if current_state != None:
                child_nodes.append(self.gameboard)
                self.gameboard = copy.deepcopy(parent_node)

        if child_nodes == [] or depth == 0:
            self.countScore1(self.gameboard)
            return self.evaluation_function(self.gameboard)
        else:
            for node in child_nodes:
                self.gameboard = copy.deepcopy(node)
                value = min(value, self.max_val(node, alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return value

    def evaluation_function(self, state):
        if self.current_move == 1:
            o_color = 2
        elif self.current_move == 2:
            o_color = 1
        my_fours = self.checkForStreak(state, self.current_move, 4)
        my_threes = self.checkForStreak(state, self.current_move, 3)
        my_twos = self.checkForStreak(state, self.current_move, 2)
        comp_fours = self.checkForStreak(state, o_color, 4)
        comp_threes = self.checkForStreak(state, o_color, 3)
        comp_twos = self.checkForStreak(state, o_color, 2)
        return (my_fours * 10 + my_threes * 5 + my_twos * 2) - (comp_fours * 10 + comp_threes * 5 + comp_twos * 2)

    def aiPlay(self):
        random_column = self.minimax(int(self.depth))
        result = self.playPiece(random_column)
        if not result:
            print('No Result')
        else:
            print('Player: %d, Column: %d\n' % (self.current_move, random_column + 1))
            self.change_move()

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameboard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameboard[i][column]:
                    self.gameboard[i][column] = self.current_move
                    self.piece_count += 1
                    return 1

    def change_move(self):
        if self.current_move == 1:
            self.current_move = 2
        elif self.current_move == 2:
            self.current_move = 1


    def checkForStreak(self, state, color, streak):
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j] == color:
                    count += self.verticalStreak(i, j, state, streak)
                    count += self.horizontalStreak(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

    def verticalStreak(self, row, column, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column] == state[row][column]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, row, column, state, streak):
        count = 0
        for j in range(column, 7):
            if state[row][j] == state[row][column]:
                count += 1
            else:
                break
        if count >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, column, state, streak):
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total

    def check_piece(self, column, opponent):
        if not self.gameboard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameboard[i][column]:
                    self.gameboard[i][column] = opponent
                    self.piece_count += 1
                    return 1

    def count_score(self):
        self.player1Score = 0;
        self.player2Score = 0;
        # Check horizontally
        for row in self.gameboard:
            # Check player 1
            if row[0:4] == [1] * 4:
                self.player1Score += 1
            if row[1:5] == [1] * 4:
                self.player1Score += 1
            if row[2:6] == [1] * 4:
                self.player1Score += 1
            if row[3:7] == [1] * 4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2] * 4:
                self.player2Score += 1
            if row[1:5] == [2] * 4:
                self.player2Score += 1
            if row[2:6] == [2] * 4:
                self.player2Score += 1
            if row[3:7] == [2] * 4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameboard[0][j] == 1 and self.gameboard[1][j] == 1 and
                    self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1):
                self.player1Score += 1
            if (self.gameboard[1][j] == 1 and self.gameboard[2][j] == 1 and
                    self.gameboard[3][j] == 1 and self.gameboard[4][j] == 1):
                self.player1Score += 1
            if (self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1 and
                    self.gameboard[4][j] == 1 and self.gameboard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameboard[0][j] == 2 and self.gameboard[1][j] == 2 and
                    self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2):
                self.player2Score += 1
            if (self.gameboard[1][j] == 2 and self.gameboard[2][j] == 2 and
                    self.gameboard[3][j] == 2 and self.gameboard[4][j] == 2):
                self.player2Score += 1
            if (self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2 and
                    self.gameboard[4][j] == 2 and self.gameboard[5][j] == 2):
                self.player2Score += 1
        # Check diagonally

        # Check player 1
        if (self.gameboard[2][0] == 1 and self.gameboard[3][1] == 1 and
                self.gameboard[4][2] == 1 and self.gameboard[5][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][0] == 1 and self.gameboard[2][1] == 1 and
                self.gameboard[3][2] == 1 and self.gameboard[4][3] == 1):
            self.player1Score += 1
        if (self.gameboard[2][1] == 1 and self.gameboard[3][2] == 1 and
                self.gameboard[4][3] == 1 and self.gameboard[5][4] == 1):
            self.player1Score += 1
        if (self.gameboard[0][0] == 1 and self.gameboard[1][1] == 1 and
                self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][1] == 1 and self.gameboard[2][2] == 1 and
                self.gameboard[3][3] == 1 and self.gameboard[4][4] == 1):
            self.player1Score += 1
        if (self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1 and
                self.gameboard[4][4] == 1 and self.gameboard[5][5] == 1):
            self.player1Score += 1
        if (self.gameboard[0][1] == 1 and self.gameboard[1][2] == 1 and
                self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1):
            self.player1Score += 1
        if (self.gameboard[1][2] == 1 and self.gameboard[2][3] == 1 and
                self.gameboard[3][4] == 1 and self.gameboard[4][5] == 1):
            self.player1Score += 1
        if (self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1 and
                self.gameboard[4][5] == 1 and self.gameboard[5][6] == 1):
            self.player1Score += 1
        if (self.gameboard[0][2] == 1 and self.gameboard[1][3] == 1 and
                self.gameboard[2][4] == 1 and self.gameboard[3][5] == 1):
            self.player1Score += 1
        if (self.gameboard[1][3] == 1 and self.gameboard[2][4] == 1 and
                self.gameboard[3][5] == 1 and self.gameboard[4][6] == 1):
            self.player1Score += 1
        if (self.gameboard[0][3] == 1 and self.gameboard[1][4] == 1 and
                self.gameboard[2][5] == 1 and self.gameboard[3][6] == 1):
            self.player1Score += 1

        if (self.gameboard[0][3] == 1 and self.gameboard[1][2] == 1 and
                self.gameboard[2][1] == 1 and self.gameboard[3][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][4] == 1 and self.gameboard[1][3] == 1 and
                self.gameboard[2][2] == 1 and self.gameboard[3][1] == 1):
            self.player1Score += 1
        if (self.gameboard[1][3] == 1 and self.gameboard[2][2] == 1 and
                self.gameboard[3][1] == 1 and self.gameboard[4][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][5] == 1 and self.gameboard[1][4] == 1 and
                self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1):
            self.player1Score += 1
        if (self.gameboard[1][4] == 1 and self.gameboard[2][3] == 1 and
                self.gameboard[3][2] == 1 and self.gameboard[4][1] == 1):
            self.player1Score += 1
        if (self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1 and
                self.gameboard[4][1] == 1 and self.gameboard[5][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][6] == 1 and self.gameboard[1][5] == 1 and
                self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][5] == 1 and self.gameboard[2][4] == 1 and
                self.gameboard[3][3] == 1 and self.gameboard[4][2] == 1):
            self.player1Score += 1
        if (self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1 and
                self.gameboard[4][2] == 1 and self.gameboard[5][1] == 1):
            self.player1Score += 1
        if (self.gameboard[1][6] == 1 and self.gameboard[2][5] == 1 and
                self.gameboard[3][4] == 1 and self.gameboard[4][3] == 1):
            self.player1Score += 1
        if (self.gameboard[2][5] == 1 and self.gameboard[3][4] == 1 and
                self.gameboard[4][3] == 1 and self.gameboard[5][2] == 1):
            self.player1Score += 1
        if (self.gameboard[2][6] == 1 and self.gameboard[3][5] == 1 and
                self.gameboard[4][4] == 1 and self.gameboard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameboard[2][0] == 2 and self.gameboard[3][1] == 2 and
                self.gameboard[4][2] == 2 and self.gameboard[5][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][0] == 2 and self.gameboard[2][1] == 2 and
                self.gameboard[3][2] == 2 and self.gameboard[4][3] == 2):
            self.player2Score += 1
        if (self.gameboard[2][1] == 2 and self.gameboard[3][2] == 2 and
                self.gameboard[4][3] == 2 and self.gameboard[5][4] == 2):
            self.player2Score += 1
        if (self.gameboard[0][0] == 2 and self.gameboard[1][1] == 2 and
                self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][1] == 2 and self.gameboard[2][2] == 2 and
                self.gameboard[3][3] == 2 and self.gameboard[4][4] == 2):
            self.player2Score += 1
        if (self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2 and
                self.gameboard[4][4] == 2 and self.gameboard[5][5] == 2):
            self.player2Score += 1
        if (self.gameboard[0][1] == 2 and self.gameboard[1][2] == 2 and
                self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2):
            self.player2Score += 1
        if (self.gameboard[1][2] == 2 and self.gameboard[2][3] == 2 and
                self.gameboard[3][4] == 2 and self.gameboard[4][5] == 2):
            self.player2Score += 1
        if (self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2 and
                self.gameboard[4][5] == 2 and self.gameboard[5][6] == 2):
            self.player2Score += 1
        if (self.gameboard[0][2] == 2 and self.gameboard[1][3] == 2 and
                self.gameboard[2][4] == 2 and self.gameboard[3][5] == 2):
            self.player2Score += 1
        if (self.gameboard[1][3] == 2 and self.gameboard[2][4] == 2 and
                self.gameboard[3][5] == 2 and self.gameboard[4][6] == 2):
            self.player2Score += 1
        if (self.gameboard[0][3] == 2 and self.gameboard[1][4] == 2 and
                self.gameboard[2][5] == 2 and self.gameboard[3][6] == 2):
            self.player2Score += 1

        if (self.gameboard[0][3] == 2 and self.gameboard[1][2] == 2 and
                self.gameboard[2][1] == 2 and self.gameboard[3][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][4] == 2 and self.gameboard[1][3] == 2 and
                self.gameboard[2][2] == 2 and self.gameboard[3][1] == 2):
            self.player2Score += 1
        if (self.gameboard[1][3] == 2 and self.gameboard[2][2] == 2 and
                self.gameboard[3][1] == 2 and self.gameboard[4][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][5] == 2 and self.gameboard[1][4] == 2 and
                self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2):
            self.player2Score += 1
        if (self.gameboard[1][4] == 2 and self.gameboard[2][3] == 2 and
                self.gameboard[3][2] == 2 and self.gameboard[4][1] == 2):
            self.player2Score += 1
        if (self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2 and
                self.gameboard[4][1] == 2 and self.gameboard[5][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][6] == 2 and self.gameboard[1][5] == 2 and
                self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][5] == 2 and self.gameboard[2][4] == 2 and
                self.gameboard[3][3] == 2 and self.gameboard[4][2] == 2):
            self.player2Score += 1
        if (self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2 and
                self.gameboard[4][2] == 2 and self.gameboard[5][1] == 2):
            self.player2Score += 1
        if (self.gameboard[1][6] == 2 and self.gameboard[2][5] == 2 and
                self.gameboard[3][4] == 2 and self.gameboard[4][3] == 2):
            self.player2Score += 1
        if (self.gameboard[2][5] == 2 and self.gameboard[3][4] == 2 and
                self.gameboard[4][3] == 2 and self.gameboard[5][2] == 2):
            self.player2Score += 1
        if (self.gameboard[2][6] == 2 and self.gameboard[3][5] == 2 and
                self.gameboard[4][4] == 2 and self.gameboard[5][3] == 2):
            self.player2Score += 1

    def countScore1(self, state):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in state:
            # Check player 1
            if row[0:4] == [1] * 4:
                self.player1Score += 1
            if row[1:5] == [1] * 4:
                self.player1Score += 1
            if row[2:6] == [1] * 4:
                self.player1Score += 1
            if row[3:7] == [1] * 4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2] * 4:
                self.player2Score += 1
            if row[1:5] == [2] * 4:
                self.player2Score += 1
            if row[2:6] == [2] * 4:
                self.player2Score += 1
            if row[3:7] == [2] * 4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameboard[0][j] == 1 and self.gameboard[1][j] == 1 and
                    self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1):
                self.player1Score += 1
            if (self.gameboard[1][j] == 1 and self.gameboard[2][j] == 1 and
                    self.gameboard[3][j] == 1 and self.gameboard[4][j] == 1):
                self.player1Score += 1
            if (self.gameboard[2][j] == 1 and self.gameboard[3][j] == 1 and
                    self.gameboard[4][j] == 1 and self.gameboard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameboard[0][j] == 2 and self.gameboard[1][j] == 2 and
                    self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2):
                self.player2Score += 1
            if (self.gameboard[1][j] == 2 and self.gameboard[2][j] == 2 and
                    self.gameboard[3][j] == 2 and self.gameboard[4][j] == 2):
                self.player2Score += 1
            if (self.gameboard[2][j] == 2 and self.gameboard[3][j] == 2 and
                    self.gameboard[4][j] == 2 and self.gameboard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameboard[2][0] == 1 and self.gameboard[3][1] == 1 and
                self.gameboard[4][2] == 1 and self.gameboard[5][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][0] == 1 and self.gameboard[2][1] == 1 and
                self.gameboard[3][2] == 1 and self.gameboard[4][3] == 1):
            self.player1Score += 1
        if (self.gameboard[2][1] == 1 and self.gameboard[3][2] == 1 and
                self.gameboard[4][3] == 1 and self.gameboard[5][4] == 1):
            self.player1Score += 1
        if (self.gameboard[0][0] == 1 and self.gameboard[1][1] == 1 and
                self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][1] == 1 and self.gameboard[2][2] == 1 and
                self.gameboard[3][3] == 1 and self.gameboard[4][4] == 1):
            self.player1Score += 1
        if (self.gameboard[2][2] == 1 and self.gameboard[3][3] == 1 and
                self.gameboard[4][4] == 1 and self.gameboard[5][5] == 1):
            self.player1Score += 1
        if (self.gameboard[0][1] == 1 and self.gameboard[1][2] == 1 and
                self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1):
            self.player1Score += 1
        if (self.gameboard[1][2] == 1 and self.gameboard[2][3] == 1 and
                self.gameboard[3][4] == 1 and self.gameboard[4][5] == 1):
            self.player1Score += 1
        if (self.gameboard[2][3] == 1 and self.gameboard[3][4] == 1 and
                self.gameboard[4][5] == 1 and self.gameboard[5][6] == 1):
            self.player1Score += 1
        if (self.gameboard[0][2] == 1 and self.gameboard[1][3] == 1 and
                self.gameboard[2][4] == 1 and self.gameboard[3][5] == 1):
            self.player1Score += 1
        if (self.gameboard[1][3] == 1 and self.gameboard[2][4] == 1 and
                self.gameboard[3][5] == 1 and self.gameboard[4][6] == 1):
            self.player1Score += 1
        if (self.gameboard[0][3] == 1 and self.gameboard[1][4] == 1 and
                self.gameboard[2][5] == 1 and self.gameboard[3][6] == 1):
            self.player1Score += 1

        if (self.gameboard[0][3] == 1 and self.gameboard[1][2] == 1 and
                self.gameboard[2][1] == 1 and self.gameboard[3][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][4] == 1 and self.gameboard[1][3] == 1 and
                self.gameboard[2][2] == 1 and self.gameboard[3][1] == 1):
            self.player1Score += 1
        if (self.gameboard[1][3] == 1 and self.gameboard[2][2] == 1 and
                self.gameboard[3][1] == 1 and self.gameboard[4][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][5] == 1 and self.gameboard[1][4] == 1 and
                self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1):
            self.player1Score += 1
        if (self.gameboard[1][4] == 1 and self.gameboard[2][3] == 1 and
                self.gameboard[3][2] == 1 and self.gameboard[4][1] == 1):
            self.player1Score += 1
        if (self.gameboard[2][3] == 1 and self.gameboard[3][2] == 1 and
                self.gameboard[4][1] == 1 and self.gameboard[5][0] == 1):
            self.player1Score += 1
        if (self.gameboard[0][6] == 1 and self.gameboard[1][5] == 1 and
                self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1):
            self.player1Score += 1
        if (self.gameboard[1][5] == 1 and self.gameboard[2][4] == 1 and
                self.gameboard[3][3] == 1 and self.gameboard[4][2] == 1):
            self.player1Score += 1
        if (self.gameboard[2][4] == 1 and self.gameboard[3][3] == 1 and
                self.gameboard[4][2] == 1 and self.gameboard[5][1] == 1):
            self.player1Score += 1
        if (self.gameboard[1][6] == 1 and self.gameboard[2][5] == 1 and
                self.gameboard[3][4] == 1 and self.gameboard[4][3] == 1):
            self.player1Score += 1
        if (self.gameboard[2][5] == 1 and self.gameboard[3][4] == 1 and
                self.gameboard[4][3] == 1 and self.gameboard[5][2] == 1):
            self.player1Score += 1
        if (self.gameboard[2][6] == 1 and self.gameboard[3][5] == 1 and
                self.gameboard[4][4] == 1 and self.gameboard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameboard[2][0] == 2 and self.gameboard[3][1] == 2 and
                self.gameboard[4][2] == 2 and self.gameboard[5][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][0] == 2 and self.gameboard[2][1] == 2 and
                self.gameboard[3][2] == 2 and self.gameboard[4][3] == 2):
            self.player2Score += 1
        if (self.gameboard[2][1] == 2 and self.gameboard[3][2] == 2 and
                self.gameboard[4][3] == 2 and self.gameboard[5][4] == 2):
            self.player2Score += 1
        if (self.gameboard[0][0] == 2 and self.gameboard[1][1] == 2 and
                self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][1] == 2 and self.gameboard[2][2] == 2 and
                self.gameboard[3][3] == 2 and self.gameboard[4][4] == 2):
            self.player2Score += 1
        if (self.gameboard[2][2] == 2 and self.gameboard[3][3] == 2 and
                self.gameboard[4][4] == 2 and self.gameboard[5][5] == 2):
            self.player2Score += 1
        if (self.gameboard[0][1] == 2 and self.gameboard[1][2] == 2 and
                self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2):
            self.player2Score += 1
        if (self.gameboard[1][2] == 2 and self.gameboard[2][3] == 2 and
                self.gameboard[3][4] == 2 and self.gameboard[4][5] == 2):
            self.player2Score += 1
        if (self.gameboard[2][3] == 2 and self.gameboard[3][4] == 2 and
                self.gameboard[4][5] == 2 and self.gameboard[5][6] == 2):
            self.player2Score += 1
        if (self.gameboard[0][2] == 2 and self.gameboard[1][3] == 2 and
                self.gameboard[2][4] == 2 and self.gameboard[3][5] == 2):
            self.player2Score += 1
        if (self.gameboard[1][3] == 2 and self.gameboard[2][4] == 2 and
                self.gameboard[3][5] == 2 and self.gameboard[4][6] == 2):
            self.player2Score += 1
        if (self.gameboard[0][3] == 2 and self.gameboard[1][4] == 2 and
                self.gameboard[2][5] == 2 and self.gameboard[3][6] == 2):
            self.player2Score += 1

        if (self.gameboard[0][3] == 2 and self.gameboard[1][2] == 2 and
                self.gameboard[2][1] == 2 and self.gameboard[3][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][4] == 2 and self.gameboard[1][3] == 2 and
                self.gameboard[2][2] == 2 and self.gameboard[3][1] == 2):
            self.player2Score += 1
        if (self.gameboard[1][3] == 2 and self.gameboard[2][2] == 2 and
                self.gameboard[3][1] == 2 and self.gameboard[4][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][5] == 2 and self.gameboard[1][4] == 2 and
                self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2):
            self.player2Score += 1
        if (self.gameboard[1][4] == 2 and self.gameboard[2][3] == 2 and
                self.gameboard[3][2] == 2 and self.gameboard[4][1] == 2):
            self.player2Score += 1
        if (self.gameboard[2][3] == 2 and self.gameboard[3][2] == 2 and
                self.gameboard[4][1] == 2 and self.gameboard[5][0] == 2):
            self.player2Score += 1
        if (self.gameboard[0][6] == 2 and self.gameboard[1][5] == 2 and
                self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2):
            self.player2Score += 1
        if (self.gameboard[1][5] == 2 and self.gameboard[2][4] == 2 and
                self.gameboard[3][3] == 2 and self.gameboard[4][2] == 2):
            self.player2Score += 1
        if (self.gameboard[2][4] == 2 and self.gameboard[3][3] == 2 and
                self.gameboard[4][2] == 2 and self.gameboard[5][1] == 2):
            self.player2Score += 1
        if (self.gameboard[1][6] == 2 and self.gameboard[2][5] == 2 and
                self.gameboard[3][4] == 2 and self.gameboard[4][3] == 2):
            self.player2Score += 1
        if (self.gameboard[2][5] == 2 and self.gameboard[3][4] == 2 and
                self.gameboard[4][3] == 2 and self.gameboard[5][2] == 2):
            self.player2Score += 1
        if (self.gameboard[2][6] == 2 and self.gameboard[3][5] == 2 and
                self.gameboard[4][4] == 2 and self.gameboard[5][3] == 2):
            self.player2Score += 1

