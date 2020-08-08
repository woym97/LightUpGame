# importing the required libraries

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import random

b_dim = 7
blk_sqs_max = 9
blk_sqs_min = 5
win_dim = 300
tile_dim = 30


class Tile(QPushButton):
    def __init__(self, row, col, color):
        super().__init__()
        self.row = row      # row loc
        self.col = col      # col loc
        self.color = color  # txt color
        self.val = None     # if black, num that displays
        self.setFixedSize(QSize(tile_dim, tile_dim))    # size of object
        self.clicked.connect(self.on_click)     # action binder
        self.bl_adj = 0     # if color=black this represents the number of adjacent black tiles
        self.lit_adj = 0    # num of tile neighbors that are lit (used for black cells)
        self.max_adj = 0    # max num of tile neighbors that could be lit

        if self.color == "black":
            self.setStyleSheet("background-color: black; color: white")
        else:
            self.setStyleSheet("background-color: white")

    def on_click(self):
        if self.color == "white" or self.color == "yellow":
            self.setStyleSheet("background-color: orange")
            self.color = "orange"
            game.update_board(self)
        elif self.color == "black":
            return
        elif self.color == "orange" or self.color == "red" or self.color == 'gray':
            self.setStyleSheet("background-color: white")
            self.color = "white"
            game.update_board(self)

    def set_value(self, val):
        self.val = val
        self.setText(str(val))

    def set_yellow(self):
        self.setStyleSheet("background-color: yellow")
        self.color = "yellow"

    def set_red(self):
        self.setStyleSheet("background-color: red")
        self.color = "red"

    def set_orange(self):
        self.setStyleSheet("background-color: orange")
        self.color = "orange"

    def set_white(self):
        self.setStyleSheet("background-color: white")
        self.color = "white"

    def set_gray(self):
        self.setStyleSheet("background-color: darkgray")
        self.color = "gray"

    def reset_adj(self):
        self.bl_adj = 0
        self.lit_adj = 0

    def inc_bl_adj(self):
        self.bl_adj += 1

    def inc_lit_adj(self):
        self.lit_adj += 1


class Board(QWidget):
    def __init__(self):
        self.init_puzzle()

    def init_puzzle(self):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.setLayout(self.grid)
        self.blk_sqs = []
        self.get_bl_squares()
        self.success_count = 0
        self.solvable = 0

        # set the title
        self.setWindowTitle("LIGHT UP")
        # setting  the fixed width & height of window
        self.setFixedWidth(win_dim)
        self.setFixedHeight(win_dim)

        self.iterate_board(self.init_tile)
        self.iterate_board(self.get_bl_adj)
        self.iterate_board(self.set_bl_val)
        self.add_action_buttons()
        self.iterate_board(self.validity_check)
        self.iterate_board(self.check)
        if self.solvable > 0:
            print("Unsolvable board generated, regenerating board...")
            self.reset_puzzle()
        else:
            self.iterate_board(self.clear_board)

        # show all the widgets
        self.show()

    def validity_check(self, row, col):
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        if temp_tile.color == 'black' and temp_tile.val is not None:
            if int(temp_tile.val) == temp_tile.max_adj:
                self.set_adj(row, col)

    def set_adj(self, row, col):
        rng = 1
        neighbors = [[row, col - rng], [row, col + rng], [row + rng, col], [row - rng, col]]
        adj_tile_li = []
        for ti in neighbors:
            try:
                adj_tile_li.append(self.grid.itemAtPosition(ti[0], ti[1]).widget())
            # catch tiles on edges
            except AttributeError:
                pass
        for ti in adj_tile_li:
            if ti.color == 'white' or ti.color == 'yellow':
                ti.set_orange()
                self.update_board(ti)

    def add_action_buttons(self):
        reset_button = QPushButton("RESET PUZZLE")
        reset_button.clicked.connect(self.reset_puzzle)
        check_button = QPushButton("CHECK PUZZLE")
        check_button.clicked.connect(self.check_puzzle)
        self.grid.addWidget(reset_button, b_dim + 1, 0, 1, b_dim)
        self.grid.addWidget(check_button, b_dim + 2, 0, 1, b_dim)

    def reset_puzzle(self):
        self.close()
        self.init_puzzle()

    def check_puzzle(self):
        self.success_count = 0
        self.iterate_board(self.check)
        if self.success_count == b_dim * b_dim:
            alert = QMessageBox()
            alert.setText('Success!')
            alert.exec_()
        else:
            alert = QMessageBox()
            alert.setText('Incorrect')
            alert.exec_()
        return

    def check(self, row, col):
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        success_li = ['black', 'orange', 'yellow']
        not_solvable_li = ['red', 'gray']
        if temp_tile.color in success_li:
            self.success_count += 1
        elif temp_tile.color in not_solvable_li:
            self.solvable += 1
        return

    def clear_board(self, row, col):
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        if temp_tile.color != 'white' and temp_tile.color != 'black':
            temp_tile.set_white()


    """--- *** FUNCTIONS BELOW USE ITERATE_BOARD *** ---"""

    # noinspection PyMethodMayBeStatic
    def iterate_board(self, action):
        for row in range(b_dim):
            for col in range(b_dim):
                action(row, col)

    def init_tile(self, row, col):
        if [row, col] in self.blk_sqs:
            button = Tile(row, col, "black")
            self.grid.addWidget(button, row, col)
        else:
            button = Tile(row, col, "white")
            self.grid.addWidget(button, row, col)

    def get_bl_adj(self, row, col):
        tile = self.grid.itemAtPosition(row, col).widget()
        rng = 1
        neighbors = [[row, col - rng], [row, col + rng], [row + rng, col], [row - rng, col]]
        adj_tile_li = []
        for ti in neighbors:
            try:
                adj_tile_li.append(self.grid.itemAtPosition(ti[0], ti[1]).widget())
            # catch tiles on edges
            except AttributeError:
                pass
        tile.reset_adj()
        for adj_tile in adj_tile_li:
            if adj_tile.color == 'black':
                tile.inc_bl_adj()
            elif adj_tile.color != 'white' and adj_tile.color != 'yellow':
                tile.inc_lit_adj()
        if tile.val is None:
            return
        if tile.lit_adj > int(tile.val):
            for adj in adj_tile_li:
                if adj.color == 'orange' or adj.color == 'red':
                    adj.set_gray()
        else:
            for adj in adj_tile_li:
                if adj.color == 'gray':
                    adj.set_orange()

    def set_bl_val(self, row, col):
        tile = self.grid.itemAtPosition(row, col).widget()
        max_pos = 4 - tile.bl_adj
        if tile.color != 'black':
            return
        if random.randint(0, 3) == 3:
            return
        corners = [[0, 0], [0, b_dim - 1], [b_dim - 1, 0], [b_dim - 1, b_dim - 1]]
        for corner in corners:
            if col == corner[0] and row == corner[1]:
                max_pos = 2 - tile.bl_adj
                tile.max_adj = min(2, max_pos)
                tile.set_value(str(random.randint(0, tile.max_adj)))
                return
        if row == 0 or col == 0 or row == b_dim - 1 or col == b_dim - 1:
            max_pos = 3 - tile.bl_adj
            tile.max_adj = min(3, max_pos)
            tile.set_value(str(random.randint(0, tile.max_adj)))
        else:
            max_pos = 4 - tile.bl_adj
            tile.max_adj = min(4, max_pos)
            tile.set_value(str(random.randint(0, tile.max_adj)))

    def get_bl_squares(self):
        # get the number of black squares on the board
        num_bl = random.randint(blk_sqs_min, blk_sqs_max)
        bl_sq_li = []
        for num in range(num_bl):
            bl_sq_li.append([random.randint(0, b_dim), random.randint(0, b_dim)])
        self.blk_sqs = bl_sq_li

    def validate_board(self, row, col):
        """
        called when a light is taken off the board, re establishes all remaining beams
        :return: ensures light beams are not broken by unset_light()
        """
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        if temp_tile.color == 'orange':
            self.tile_action(temp_tile, self.set_tile)
        elif temp_tile.color == 'red' or temp_tile.color == 'gray':
            temp_tile.set_orange()
            self.tile_action(temp_tile, self.set_tile)

    """--- *** FUNCTIONS BELOW USE TILE_ACTION *** ---"""

    def update_board(self, tile):
        tile = self.grid.itemAtPosition(tile.row, tile.col).widget()
        if tile.color == 'orange':
            self.tile_action(tile, self.set_tile)
        elif tile.color == 'white' or tile.color == 'red' or tile.color == 'gray':
            self.tile_action(tile, self.unset_tile)
        self.iterate_board(self.validate_board)
        self.iterate_board(self.get_bl_adj)
        return

    # noinspection PyMethodMayBeStatic
    def tile_action(self, tile, func):
        """
        calls a given function on all tiles effected by an action being performed
        on a given tile
        :param tile:
        :param func:
        :return:
        """
        col_ranges = [range(tile.col + 1, b_dim, 1), range(tile.col - 1, -1, -1)]
        # go left/right by looping through cells denoted by range options above
        for opt in col_ranges:
            for col in opt:
                if not func(tile.row, col):
                    break
                elif func(tile.row, col) == 'invalid_move':
                    tile.set_red()
        row_ranges = [range(tile.row + 1, b_dim, 1), range(tile.row - 1, -1, -1)]
        # go left/right by looping through cells denoted by range options above
        for opt in row_ranges:
            for row in opt:
                if not func(row, tile.col):
                    break
                elif func(row, tile.col) == 'invalid_move':
                    tile.set_red()
        return

    def set_tile(self, row, col):
        tile = self.grid.itemAtPosition(row, col).widget()
        if tile.color == 'black':
            return False
        if tile.color == 'orange' or tile.color == 'red' or tile.color == 'gray':
            tile.set_red()
            return 'invalid_move'
        else:
            tile.set_yellow()
            return True

    def unset_tile(self, row, col):
        tile = self.grid.itemAtPosition(row, col).widget()
        if tile.color == 'black' or tile.color == 'red' or tile.color == 'gray':
            return False
        else:
            tile.set_white()
            return True


if __name__ == '__main__':
    QApplication.setStyle('Fusion')
    app = QApplication(sys.argv)
    game = Board()
    game.show()
    sys.exit(app.exec_())
