import pygame
from config import *
from copy import deepcopy


class Board:
    width = BOARD_WIDTH
    height = BOARD_HEIGHT

    points = []  # -1 outside the board, >=0 in board
    border = []  # 1 border , -1 not border
    legal_moves = []
    ball_pos = ()

    def __init__(self):
        self.border = starting_board(is_border=True)
        self.points = starting_board(is_border=False)
        self.set_default_moves()
        self.legal_moves = deepcopy(self.points)
        self.ball_pos = (BOARD_HEIGHT//2, BOARD_WIDTH//2)

    def set_default_moves(self):
        for i_idx, i in enumerate(self.points):
            for j_idx, j in enumerate(i):
                if j < 0:
                    continue
                neighbours = return_neighbours(self.points, i_idx, j_idx, self.border)
                self.points[i_idx][j_idx] = self.points[i_idx][j_idx] ^ self.points[i_idx][j_idx]
                direction = 0b1
                for neighbour in neighbours:
                    if neighbour is not None and neighbour >= 0:
                        self.points[i_idx][j_idx] = self.points[i_idx][j_idx] | direction
                    direction = direction << 1

        # delete illegal moves
        # left upper
        self.points[0][BOARD_WIDTH//2 - 1] &= 0b110111111
        self.points[1][BOARD_WIDTH//2 - 2] &= 0b111111011

        # right upper
        self.points[0][BOARD_WIDTH//2 + 1] &= 0b011111111
        self.points[1][BOARD_WIDTH//2 + 2] &= 0b111111110

        # left lower
        self.points[-1][BOARD_WIDTH//2 - 1] &= 0b111111110
        self.points[-2][BOARD_WIDTH//2 - 2] &= 0b011111111

        # right lower
        self.points[-1][BOARD_WIDTH//2 + 1] &= 0b111111011
        self.points[-2][BOARD_WIDTH//2 + 2] &= 0b110111111

    def draw_points(self, win):
        width_space = WIN_WIDTH // 20
        height_space = WIN_HEIGHT // 20

        current_pos = ((WIN_WIDTH - (BOARD_WIDTH - 1) * width_space) / 2,
                       (WIN_HEIGHT - BOARD_HEIGHT * height_space) / 2)
        for row_idx, i in enumerate(self.points):
            tmp_pos = current_pos
            for col_idx, j in enumerate(i):
                if j >= 0:
                    pygame.draw.circle(win, (255, 255, 255), current_pos, 5, 0)
                if row_idx == self.ball_pos[0] and col_idx == self.ball_pos[1]:
                    pygame.draw.circle(win, (0, 0, 0), current_pos, 2, 0)
                current_pos = (current_pos[0] + width_space, current_pos[1])
            current_pos = (tmp_pos[0], tmp_pos[1] + height_space)

    def draw_border(self, win):
        width_space = WIN_WIDTH // 20
        height_space = WIN_HEIGHT // 20

        current_pos = ((WIN_WIDTH - (BOARD_WIDTH - 1) * width_space) / 2,
                       (WIN_HEIGHT - BOARD_HEIGHT * height_space) / 2)

        for row_idx, row in enumerate(self.border):
            tmp_pos = current_pos
            for col_idx in range(len(row)):
                if row[col_idx] == 1:
                    if col_idx < BOARD_WIDTH - 1 and row[col_idx + 1] == 1:
                        pygame.draw.line(win, (0, 0, 0), current_pos, (current_pos[0] + width_space, current_pos[1]))
                    if row_idx < BOARD_HEIGHT - 1 and self.border[row_idx + 1][col_idx] == 1:
                        pygame.draw.line(win, (0, 0, 0), current_pos, (current_pos[0], current_pos[1] + height_space))
                current_pos = (current_pos[0] + width_space, current_pos[1])
            current_pos = (tmp_pos[0], tmp_pos[1] + height_space)

    def draw_lines(self, win):
        width_space = WIN_WIDTH // 20
        height_space = WIN_HEIGHT // 20

        current_pos = ((WIN_WIDTH - (BOARD_WIDTH - 1) * width_space) / 2,
                       (WIN_HEIGHT - BOARD_HEIGHT * height_space) / 2)

        for row_idx, row in enumerate(self.legal_moves):
            tmp_pos = current_pos
            for col_idx, cell in enumerate(row):
                if cell < 0:
                    current_pos = (current_pos[0] + width_space, current_pos[1])
                    continue
                tmp_cell_legal = cell
                tmp_cell_available = self.points[row_idx][col_idx]
                for x in range(-height_space, 2 * height_space, height_space):
                    for y in range(-width_space, 2 * width_space, width_space):
                        is_legal = tmp_cell_legal & 0b0000000001
                        is_available = tmp_cell_available & 0b0000000001
                        tmp_cell_legal = tmp_cell_legal >> 1
                        tmp_cell_available = tmp_cell_available >> 1
                        if is_legal and not is_available:
                            pygame.draw.line(win, (255, 0, 0), current_pos, (current_pos[0] + y, current_pos[1] + x))
                current_pos = (current_pos[0] + width_space, current_pos[1])
            current_pos = (tmp_pos[0], tmp_pos[1] + height_space)

    def make_move(self, direction):
        next_move = False
        self.points[self.ball_pos[0]][self.ball_pos[1]] &= direction
        if direction == 0b011111111:
            self.ball_pos = (self.ball_pos[0] + 1, self.ball_pos[1] + 1)
        elif direction == 0b101111111:
            self.ball_pos = (self.ball_pos[0] + 1, self.ball_pos[1])
        elif direction == 0b110111111:
            self.ball_pos = (self.ball_pos[0] + 1, self.ball_pos[1] - 1)
        elif direction == 0b111011111:
            self.ball_pos = (self.ball_pos[0], self.ball_pos[1] + 1)
        elif direction == 0b111110111:
            self.ball_pos = (self.ball_pos[0], self.ball_pos[1] - 1)
        elif direction == 0b111111011:
            self.ball_pos = (self.ball_pos[0] - 1, self.ball_pos[1] + 1)
        elif direction == 0b111111101:
            self.ball_pos = (self.ball_pos[0] - 1, self.ball_pos[1])
        elif direction == 0b111111110:
            self.ball_pos = (self.ball_pos[0] - 1, self.ball_pos[1] - 1)
        direction = int('{:09b}'.format(direction)[::-1], 2)
        if self.points[self.ball_pos[0]][self.ball_pos[1]] != self.legal_moves[self.ball_pos[0]][self.ball_pos[1]]:
            next_move = True
        if self.border[self.ball_pos[0]][self.ball_pos[1]] == 1:
            next_move = True
        self.points[self.ball_pos[0]][self.ball_pos[1]] &= direction
        return next_move

    def check_winner(self, turn):
        if self.ball_pos[0] == 0:
            return "Player 2"
        elif self.ball_pos[0] == BOARD_HEIGHT - 1:
            return "Player 1"
        elif self.points[self.ball_pos[0]][self.ball_pos[1]] == 0:
            if not turn:
                return "Player 1"
            else:
                return "Player 2"
        return None

    def draw(self, win):
        self.draw_points(win)
        self.draw_border(win)
        self.draw_lines(win)


def starting_board(is_border):
    array = []

    # first row
    row = []
    for i in range(0, BOARD_WIDTH // 2 - 1):
        row.append(-1)
    for i in range(3):
        row.append(1)
    for i in range(0, BOARD_WIDTH // 2 - 1):
        row.append(-1)
    array.append(row)

    # middle rows
    for i in range(1, BOARD_HEIGHT - 1):
        row = []
        for j in range(0, BOARD_WIDTH):
            # in border set only first and last cell ( excluding first and last row)
            if is_border and i != 1 and i != BOARD_HEIGHT - 2:
                if j == 0 or j == BOARD_WIDTH - 1:
                    row.append(1)
                else:
                    row.append(-1)
                continue
            row.append(1)
        array.append(row)

    # adjust border
    if is_border:
        array[1][BOARD_WIDTH // 2] = -1
        array[BOARD_HEIGHT - 2][BOARD_WIDTH // 2] = -1

    # last row
    row = []
    for i in range(0, BOARD_WIDTH // 2 - 1):
        row.append(-1)
    for i in range(3):
        row.append(1)
    for i in range(0, BOARD_WIDTH // 2 - 1):
        row.append(-1)
    array.append(row)

    return array


def return_neighbours(array, x, y, border):
    neighbours = []
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i == x and j == y) or i < 0 or i >= BOARD_HEIGHT or j < 0 or j >= BOARD_WIDTH:
                neighbours.append(None)
            elif array[i][j] < 0:
                neighbours.append(None)
            elif border[i][j] == 1 and border[x][y] == 1 and (x == i or y == j):
                neighbours.append(None)
            else:
                neighbours.append(array[i][j])
    return neighbours
