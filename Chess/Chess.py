import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


WHITE = 1
BLACK = 2
A_ORD = 65


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


class Board:  # Доска
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        # возвращает фигуру и ее цвет
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if piece.can_move(self, row, col, row1, col1):
            self.field[row][col].m += 1
            self.field[row][col] = None
            self.field[row1][col1] = piece
            self.color = opponent(self.color)
            return True
        elif piece.can_attack(self, row, col, row1, col1):
            self.field[row][col].m += 1
            self.field[row][col] = None
            self.field[row1][col1] = piece
            self.color = opponent(self.color)
            return True

    def char(self, row, col):
        return self.cell(row, col)[1]

    def field_color(self, row, col):
        color = 1 if self.cell(row, col)[0] == 'w' else 2
        return color

    def number_of_moves(self, row, col):
        return self.field[row][col].m

    def is_under_attack(self, row, col):
        for r in range(7, -1, -1):
            for c in range(8):
                if not (self.field[r][c] is None) \
                        and self.field[r][c].color == opponent(self.color) \
                        and self.field[r][c].can_attack(self, r, c, row, col):
                    return True
        return False


class Rook:  # Ладья
    def __init__(self, color):
        self.color = color
        self.m = 0

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if row1 > row:
            stepr = 1
        elif row1 < row:
            stepr = -1
        else:
            stepr = 0

        if col1 > col:
            stepc = 1
        elif col1 < col:
            stepc = -1
        else:
            stepc = 0
        r = row
        c = col
        if stepr != 0 and stepc == 0:
            for i in range(row, row1, stepr):
                r += stepr
                c += stepc
                # Если на пути по вертикали есть фигура
                if not (board.get_piece(r - stepr, c) is None) and \
                        board.cell(r - stepr, c)[0] != board.cell(row, col)[0]:
                    return False
                if not (board.get_piece(r, c) is None) and \
                        board.cell(r, c)[0] == board.cell(row, col)[0]:
                    return False
        if stepr == 0 and stepc != 0:
            for i in range(col, col1, stepc):
                r += stepr
                c += stepc
                # Если на пути по горизонтали есть фигура
                if not (board.get_piece(r, c - stepc) is None) and \
                        board.cell(r, c - stepc)[0] != board.cell(row, col)[0]:
                    return False
                if not (board.get_piece(r, c) is None) and \
                        board.cell(r, c)[0] == board.cell(row, col)[0]:
                    return False
        if row == row1 or col == col1 and (0 <= row <= 7) and (0 <= col <= 7):
            if row == row1 and col == col1:
                return False
            else:
                return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:
    def __init__(self, color):
        self.color = color
        self.m = 0

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col - 1 != col1 and col + 1 != col1 and col != col1:
            return False
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if row + direction == row1 and col == col1:
            if not (board.get_piece(row1, col) is None) and board.cell(row1, col)[0] != board.cell(row, col)[0]:
                return True
            if board.get_piece(row1, col) is None:
                return True
        if row == start_row and row + 2 * direction == row1 and col == col1:
            if not (board.field[row + direction][col] is None):
                return False
            if not (board.field[row + 2 * direction][col] is None):
                if board.cell(row + 2 * direction, col)[0] != board.cell(row, col)[0]:
                    return True
            if board.field[row + 2 * direction][col] is None:
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if self.color == WHITE else -1
        if row + direction == row1 and (col + 1 == col1 or col - 1 == col1):
            if (not (board.get_piece(row1, col1) is None) and
                    board.cell(row1, col1)[0] != board.cell(row, col)[0]):
                return True
            if (board.get_piece(row1, col1) is None
                    and not (board.get_piece(row, col1) is None)
                    and board.char(row, col1) == 'P'
                    and board.cell(row, col1)[0] != board.cell(row, col)[0]):
                board.field[row][col1] = None
                return True


class Knight:
    def __init__(self, color):
        self.m = 0
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        stepr = row1 - row
        stepc = col1 - col
        if not (board.get_piece(row1, col1) is None) and \
                board.cell(row1, col1)[0] == board.cell(row, col)[0]:
            return False
        if ((((stepr == 1 or stepr == -1) and (stepc == 2 or stepc == -2)) or (
                (stepr == 2 or stepr == -2) and (stepc == 1 or stepc == -1)))
            or row == row1 or col == col1) and (
                0 <= row <= 7) and (0 <= col <= 7):
            if row == row1 or col == col1:
                return False
            else:
                return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        self.m = 0

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        stepr = row1 - row
        stepc = col1 - col
        if not (board.get_piece(row1, col1) is None) and \
                board.cell(row1, col1)[0] == board.cell(row, col)[0]:
            return False
        if ((stepr == 1 or stepr == -1 or stepr == 0) and
            (stepc == 1 or stepc == -1 or stepc == 0)) and (
                0 <= row <= 7) and (0 <= col <= 7):
            if row == row1 and col == col1:
                return False
            if board.is_under_attack(row1, col1):
                return False
            return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    def __init__(self, color):
        self.m = 0
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if row1 > row:
            stepr = 1
        elif row1 < row:
            stepr = -1
        else:
            stepr = 0
        if col1 > col:
            stepc = 1
        elif col1 < col:
            stepc = -1
        else:
            stepc = 0
        r = row
        c = col
        if stepr != 0 and stepc == 0:
            for i in range(row, row1, stepr):
                r += stepr
                c += stepc
                # Если на пути по вертикали есть фигура
                if not (board.get_piece(r - stepr, c) is None) and \
                        board.cell(r - stepr, c)[0] != board.cell(row, col)[0]:
                    return False
                if not (board.get_piece(r, c) is None) and \
                        board.cell(r, c)[0] == board.cell(row, col)[0]:
                    return False
        if stepr == 0 and stepc != 0:
            for i in range(col, col1, stepc):
                r += stepr
                c += stepc
                # Если на пути по горизонтали есть фигура
                if not (board.get_piece(r, c - stepc) is None) and \
                        board.cell(r, c - stepc)[0] != board.cell(row, col)[0]:
                    return False
                if not (board.get_piece(r, c) is None) and \
                        board.cell(r, c)[0] == board.cell(row, col)[0]:
                    return False
        if stepr != 0 and stepc != 0:
            for cr in range(row, row1, stepr):
                r += stepr
                c += stepc
                if not (board.get_piece(r - stepr, c - stepc) is None) and \
                        board.cell(r - stepr, c - stepc)[0] != \
                        board.cell(row, col)[0]:
                    return False
                if not (board.get_piece(r, c) is None) and \
                        board.cell(r, c)[0] == board.cell(row, col)[0]:
                    return False
        if ((row - row1 == col - col1) or (row - row1 == -(col - col1))
            or (row == row1) or (col == col1)) and (
                0 <= row <= 7) and (0 <= col <= 7):
            if row == row1 and col == col1:
                return False
            else:
                return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color
        self.m = 0

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        stepc = 1 if (col1 > col) else -1
        stepr = 1 if (row1 > row) else -1
        r = row
        c = col
        if stepr != 0 and stepc != 0:
            for cr in range(col, col1, stepc):
                r += stepr
                c += stepc
                if not (board.get_piece(r - stepr, c - stepc) is None) and \
                        board.cell(r - stepr, c - stepc)[0] != \
                        board.cell(row, col)[0]:
                    return False
                if not (board.get_piece(r, c) is None) and \
                        board.cell(r, c)[0] == board.cell(row, col)[0]:
                    return False

        if ((row - row1 == col - col1) or (row - row1 == -(col - col1))) \
                or (row == row1) or (col == col1) and (
                0 <= row <= 7) and (0 <= col <= 7):
            if row == row1 or col == col1:
                return False
            else:
                return True
        else:
            return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Chess(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board = Board()
        uic.loadUi('Chess.ui', self)
        self.setWindowIcon(QIcon('board/dilena/bK.png'))
        self.dict_of_cells = {}
        self.dict_of_btns = {}
        self.btns = [[self.pushButton_A_1, 'A1'], [self.pushButton_A_2, 'A2'],
                     [self.pushButton_A_3, 'A3'], [self.pushButton_A_4, 'A4'],
                     [self.pushButton_A_5, 'A5'], [self.pushButton_A_6, 'A6'],
                     [self.pushButton_A_7, 'A7'], [self.pushButton_A_8, 'A8'],
                     [self.pushButton_B_2, 'B2'], [self.pushButton_B_3, 'B3'],
                     [self.pushButton_B_4, 'B4'], [self.pushButton_B_5, 'B5'],
                     [self.pushButton_B_6, 'B6'], [self.pushButton_B_7, 'B7'],
                     [self.pushButton_B_8, 'B8'], [self.pushButton_B_1, 'B1'],
                     [self.pushButton_C_1, 'C1'], [self.pushButton_C_2, 'C2'],
                     [self.pushButton_C_3, 'C3'], [self.pushButton_C_4, 'C4'],
                     [self.pushButton_C_5, 'C5'], [self.pushButton_C_6, 'C6'],
                     [self.pushButton_C_7, 'C7'], [self.pushButton_C_8, 'C8'],
                     [self.pushButton_D_2, 'D2'], [self.pushButton_D_3, 'D3'],
                     [self.pushButton_D_4, 'D4'], [self.pushButton_D_5, 'D5'],
                     [self.pushButton_D_6, 'D6'], [self.pushButton_D_7, 'D7'],
                     [self.pushButton_D_8, 'D8'], [self.pushButton_D_1, 'D1'],
                     [self.pushButton_E_1, 'E1'], [self.pushButton_E_2, 'E2'],
                     [self.pushButton_E_3, 'E3'], [self.pushButton_E_4, 'E4'],
                     [self.pushButton_E_5, 'E5'], [self.pushButton_E_6, 'E6'],
                     [self.pushButton_E_7, 'E7'], [self.pushButton_E_8, 'E8'],
                     [self.pushButton_F_2, 'F2'], [self.pushButton_F_3, 'F3'],
                     [self.pushButton_F_4, 'F4'], [self.pushButton_F_5, 'F5'],
                     [self.pushButton_F_6, 'F6'], [self.pushButton_F_7, 'F7'],
                     [self.pushButton_F_8, 'F8'], [self.pushButton_F_1, 'F1'],
                     [self.pushButton_G_1, 'G1'], [self.pushButton_G_2, 'G2'],
                     [self.pushButton_G_3, 'G3'], [self.pushButton_G_4, 'G4'],
                     [self.pushButton_G_5, 'G5'], [self.pushButton_G_6, 'G6'],
                     [self.pushButton_G_7, 'G7'], [self.pushButton_G_8, 'G8'],
                     [self.pushButton_H_2, 'H2'], [self.pushButton_H_3, 'H3'],
                     [self.pushButton_H_4, 'H4'], [self.pushButton_H_5, 'H5'],
                     [self.pushButton_H_6, 'H6'], [self.pushButton_H_7, 'H7'],
                     [self.pushButton_H_8, 'H8'], [self.pushButton_H_1, 'H1']]
        for btn in self.btns:
            self.dict_of_cells[btn[0]] = btn[1]
            self.dict_of_btns[btn[1]] = btn[0]
            btn[0].clicked.connect(self.move_cell)
        self.pushButton_exit.clicked.connect(exit)
        self.pushButton_restart.clicked.connect(self.restart)
        self.first_phase = True  # первая фаза для кнопок

    def move_cell(self):
        # функция для перемещеняи по видимому полю
        if self.first_phase:
            self.command = 'move', str(int(self.dict_of_cells[self.sender()][1]) - 1), str(ord(
                self.dict_of_cells[self.sender()][0]) - A_ORD)
            self.chosen(int(self.dict_of_cells[self.sender()][1]) - 1, ord(
                self.dict_of_cells[self.sender()][0]) - A_ORD, self.dict_of_cells[self.sender()][0],
                        self.dict_of_cells[self.sender()][1])
            self.first_phase = False
        else:
            self.label_chosen.setText('')
            self.command += str(int(self.dict_of_cells[self.sender()][1]) - 1), str(ord(
                self.dict_of_cells[self.sender()][0]) - A_ORD)
            if len(self.command) == 6:
                move_type, row, col, row1, col1, char = self.command
                row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            elif len(self.command) == 1:
                move_type = self.command[0]
            elif len(self.command) == 5:
                move_type, row, col, row1, col1 = self.command
                self.row, self.col, self.row1, self.col1 = row, col, row1, col1
                row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            if move_type == 'move':
                if len(self.command) != 5:
                    self.label_status_move.setText('Координаты некорректы! Попробуйте другой ход!')
                elif self.board.move_piece(row, col, row1, col1):
                    if self.board.current_player_color() == BLACK:
                        self.label_status_move.setText('Белые:\nХод успешен')
                        if type(self.board.field[int(row1)][int(col1)]) == Pawn:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/wP.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Rook:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/wR.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Bishop:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/wB.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Queen:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/wQ.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == King:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/wK.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Knight:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/wN.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                    else:
                        self.label_status_move.setText('Черные:\nХод успешен')
                        if type(self.board.field[int(row1)][int(col1)]) == Pawn:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/bP.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Rook:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/bR.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Bishop:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/bB.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Queen:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/bQ.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == King:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/bK.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                        elif type(self.board.field[int(row1)][int(col1)]) == Knight:
                            self.dict_of_btns[chr(int(col1 + A_ORD)) + str(int(row1 + 1))].setIcon(
                                QIcon('board/alpha/bN.png'))
                            self.dict_of_btns[chr(int(col + A_ORD)) + str(int(row + 1))].setIcon(
                                QIcon(''))
                else:
                    if self.board.field[row][col] is not None:
                        if self.board.field[row][col].get_color() == WHITE:
                            self.label_status_move.setText(
                                'Белые:\nКоординаты некорректы! \nПопробуйте другой ход!')
                        else:
                            self.label_status_move.setText(
                                'Черные:\nКоординаты\n некорректы! \nПопробуйте другой ход!')
                    else:
                        self.label_status_move.setText('Неверный ход!\n Попробуйте другой ход!')
            self.first_phase = True
            self.check_win()
        if self.board.current_player_color() == WHITE:
            self.label_status.setText('Ход белых')
        else:
            self.label_status.setText('Ход чёрных')

    def check_win(self):
        banswer = False
        wanswer = False
        for row in self.board.field:
            for col in row:
                if type(King(BLACK)) is type(col):
                    if col.get_color() == WHITE:
                        wanswer = True
                    if col.get_color() == BLACK:
                        banswer = True
        if not banswer:
            self.win(WHITE)
        elif not wanswer:
            self.win(BLACK)

    def win(self, color):
        self.dialog = WinForm(color, self)
        self.dialog.show()
        self.hide()

    def restart(self):
        self.close()
        self.__init__()
        self.show()

    def chosen(self, row, col, rcol, rrow):
        if type(self.board.field[int(row)][int(col)]) == Pawn:
            self.label_chosen.setText('Выбрана пешка ' + rcol + rrow)
        elif type(self.board.field[int(row)][int(col)]) == Rook:
            self.label_chosen.setText('Выбрана ладья ' + rcol + rrow)
        elif type(self.board.field[int(row)][int(col)]) == Bishop:
            self.label_chosen.setText('Выбран слон ' + rcol + rrow)
        elif type(self.board.field[int(row)][int(col)]) == Queen:
            self.label_chosen.setText('Выбран ферзь ' + rcol + rrow)
        elif type(self.board.field[int(row)][int(col)]) == King:
            self.label_chosen.setText('Выбрана король ' + rcol + rrow)
        elif type(self.board.field[int(row)][int(col)]) == Knight:
            self.label_chosen.setText('Выбран конь ' + rcol + rrow)


class WinForm(QMainWindow):
    def __init__(self, color, chess):
        super().__init__()
        uic.loadUi('win.ui', self)
        self.setWindowIcon(QIcon('board/dilena/wK.png'))
        self.chess = chess
        if color == WHITE:
            self.label_winner.setText('Победили белые')
        elif color == BLACK:
            self.label_winner.setText('Победили черные')
        self.pushButton_retry.clicked.connect(self.restart)
        self.pushButton_exit.clicked.connect(exit)

    def restart(self):
        self.chess = Chess()
        self.hide()
        self.chess.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.exit(app.exec_())


# Баги: пешка сносит все перед собой(но может рубить как обычно)
# Идеи: подсвечивать выбранную клетку; запретить выбирать пустую клетку; изменить дизайн;
#       реализовать настройки: цвет фона, выбор моделей фигур; запретить выбирать чужую фигуру
# Требования: добавить на GitHub; Фиксация размера экрана;
