"""
*****************************************************************************************************
Author: Madison Woy
Last Modified: 8/9/2020

Implementation of the 'light-up' game which is an example of an np-complete
problem. This program will allow the user to play the game and then verify their solution.
*****************************************************************************************************
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import random

b_dim = 6          # board dimension
blk_sqs_max = 15    # max amount of black squares that can show up
blk_sqs_min = 7     # min amount of black squares that can show up
win_dim = 300       # window dimension
tile_dim = 30       # tile dimension


class Tile(QPushButton):
    """
    Push button representing all tiles on game board
    """

    def __init__(self, row, col, color):
        super().__init__()
        self.row = row  # row location
        self.col = col  # col location
        self.color = color  # color as a text argument
        self.val = None  # if tile is black, value that displays
        self.setFixedSize(QSize(tile_dim, tile_dim))  # size of tile
        self.clicked.connect(self.on_click)  # action binder
        self.bl_adj = 0  # if color=black this represents the number of adjacent black tiles
        self.light_adj = 0  # num of tile neighbors that are lit (used for black cells)
        self.max_adj = 0  # max num of tile neighbors that could be lit
        self.init_color()  # initiates teh color of each tile

    def init_color(self):
        """
        sets the color of the tile based on init passed argument
        """
        if self.color == "black":
            self.setStyleSheet("background-color: black; color: white")
        else:
            self.setStyleSheet("background-color: white")

    def on_click(self):
        """
        binds the object to an action when clicked, performs action based on passed color then sends object
        to 'update_board' method in game window
        """
        settable_colors = ['white', 'yellow']
        unsettable_colors = ['gray', 'orange', 'red']
        if self.color in settable_colors:
            self.set_orange()
            game.update_board(self)
        elif self.color in unsettable_colors:
            self.set_white()
            game.update_board(self)
        else:
            return

    def set_value(self, val):
        """
        sets the value of a black square
        :param val: value to be set
        """
        self.val = int(val)
        self.setText(str(val))

    def set_yellow(self):
        """
        sets color of tile; yellow = tile is lit by light beam
        """
        self.setStyleSheet("background-color: yellow")
        self.color = "yellow"

    def set_red(self):
        """
        sets color of tile; red = tile invalid, interferes with other light bulb
        """
        self.setStyleSheet("background-color: red")
        self.color = "red"

    def set_orange(self):
        """
        sets color of tile; orange = tile is light bulb
        """
        self.setStyleSheet("background-color: orange")
        self.color = "orange"

    def set_white(self):
        """
        sets color of tile; white = tile is unlit
        """
        self.setStyleSheet("background-color: white")
        self.color = "white"

    def set_gray(self):
        """
        sets color of tile; gray = tile overloads adjacent black square
        """
        self.setStyleSheet("background-color: darkgray")
        self.color = "gray"

    def reset_adj(self):
        """
        used when counting adjacent squares, resets those counts
        """
        self.bl_adj = 0
        self.light_adj = 0

    def inc_bl_adj(self):
        """
        used to increase the count of adjacent black squares
        """
        self.bl_adj += 1

    def inc_light_adj(self):
        """
        used to increase the count of adjacent light bulbs
        """
        self.light_adj += 1


class Board(QWidget):
    """
    represents a widget that displays a game board
    """

    def __init__(self):
        """
        initializations done in self.init_puzzle to allow for proper functioning of self.reset_puzzle
        """
        self.init_puzzle()

    def init_puzzle(self):
        """
        initiates the puzzle widget either on first call or after the reset button has been clicked
        """
        super().__init__()

        # initial widget set up
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.setLayout(self.grid)
        self.setWindowTitle("LIGHT UP")
        self.setFixedWidth(win_dim)
        self.setFixedHeight(win_dim)

        # variable set up
        self.blk_sqs = []  # holds the coordinates for each black square on the board
        self.get_bl_squares()  # fills self.blk_squares
        self.success_count = 0  # counts the correct squares on the board (lit/fulfilled black squares)
        self.solvability = True  # counts all invalid squares on board
        self.get_solvable_board()  # get a solvable board

        self.add_action_buttons()  # add buttons
        self.show()  # show window

    def reset_puzzle(self):
        """
        resets puzzle by closing current widget and re initializing a new one
        :return:
        """
        self.close()
        self.init_puzzle()

    def clear_puzzle(self):
        """
        action to clear board of all filled in tiles
        """
        self.iterate_board(self.clear_tile)

    def clear_tile(self, row, col):
        """
        clears the board by being called on all tiles by self.iterate_board
        """
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        if temp_tile.color != 'white' and temp_tile.color != 'black':
            temp_tile.set_white()

    def add_action_buttons(self):
        """
        adds action buttons to puzzle
        """
        reset_button = QPushButton("RESET PUZZLE")
        reset_button.clicked.connect(self.reset_puzzle)
        check_button = QPushButton("CHECK PUZZLE")
        check_button.clicked.connect(self.check_puzzle)
        clear_button = QPushButton("CLEAR PUZZLE")
        clear_button.clicked.connect(self.clear_puzzle)
        reset_button.setStyleSheet("background-color: darkred; color: white")
        check_button.setStyleSheet("background-color: darkgreen; color: white")
        clear_button.setStyleSheet("background-color: black; color: white")
        self.grid.addWidget(reset_button, b_dim + 1, 0, 1, b_dim)
        self.grid.addWidget(check_button, b_dim + 2, 0, 1, b_dim)
        self.grid.addWidget(clear_button, b_dim + 3, 0, 1, b_dim)

    def get_solvable_board(self):
        """
        checks if a board appears to be solvable by placing light bulbs on tiles where the black squares deem them
        necessary
            ex: a corner tile that is black with a value of 2 will have its adjacent tiles lit up because there
                are only two possible tiles to light up and both must be lit to win game
        calls a check on the board and looks for any red or gray tiles, if any are found the board is deemed
        'unsolvable' and the board is reset
        *** DOES NOT deem check that a board is actually solvable but looks at the simplest case where it is not ***
        """
        self.iterate_board(self.init_tile)  # initiates tiles
        self.iterate_board(self.look_at_adjacent)  # gets black adjacent squares
        self.iterate_board(self.set_bl_val)  # sets black square values
        self.iterate_board(self.solvability_check)  # checks for board validity by filling in 'mandatory' tiles
        self.iterate_board(self.check)  # checks if any invalid moves popped up in validity_check
        if self.solvability is False:
            print("Unsolvable board generated, regenerating board...")
            self.reset_puzzle()  # if board is unsolvable, reset board
        else:
            self.clear_puzzle()  # if board is solvable, clear the board to allow user to play

    def check_puzzle(self):
        """
        calls a check by resetting success count and using iterate board to call self check
        if the successful squares (deemed by self.success_count) equalds the total squares on the board then the game
        has been won and a success message is displayed
        if not the user is told the puzzle is incorrect
        """
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

    # noinspection PyMethodMayBeStatic
    def iterate_board(self, action):
        """
        iterate through each tile on the board and perform the given action
        :param action: method in current class to perform on the object
        """
        for row in range(b_dim):
            for col in range(b_dim):
                action(row, col)

    # noinspection PyMethodMayBeStatic
    def tile_action(self, tile, func):
        """
        calls a given method on all tiles affected by an action being performed
        on a given tile
        """
        col_ranges = [range(tile.col + 1, b_dim, 1), range(tile.col - 1, -1, -1)]
        # go left/right by looping through cells denoted by range options above
        for rng in col_ranges:
            for col in rng:
                if not func(tile.row, col):
                    break
                elif func(tile.row, col) == 'invalid_move':
                    tile.set_red()
        row_ranges = [range(tile.row + 1, b_dim, 1), range(tile.row - 1, -1, -1)]
        # go left/right by looping through cells denoted by range options above
        for rng in row_ranges:
            for row in rng:
                if not func(row, tile.col):
                    break
                elif func(row, tile.col) == 'invalid_move':
                    tile.set_red()
        return

    def solvability_check(self, row, col):
        """
        checks if a board is solvable by setting all 'mandatory' lights on a board
        """
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        if temp_tile.color == 'black' and temp_tile.val is not None:
            if temp_tile.val == temp_tile.max_adj:
                self.set_adj(row, col)

    def set_adj(self, row, col):
        adj_tile_li = self.get_adjacent_tiles(row, col)
        for ti in adj_tile_li:
            if ti.color == 'white' or ti.color == 'yellow':
                ti.set_orange()
                self.update_board(ti)

    def check(self, row, col):
        """
        calls a check on a tile at given row and col, adds successful tiles to the success count and
        if an invalid tile is found sets the solvability flag to false
        :return: solvability flag and success count modified
        """
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        success_li = ['orange', 'yellow']
        not_solvable_li = ['red', 'gray']
        if temp_tile.color in success_li:
            self.success_count += 1
        elif temp_tile.color == 'black' and temp_tile.val is not None:
            if temp_tile.light_adj == temp_tile.val:
                self.success_count += 1
        elif temp_tile.color == 'black':
            self.success_count += 1
        elif temp_tile.color in not_solvable_li:
            self.solvability = False
        return

    def init_tile(self, row, col):
        """
        initiates all tiles by being called on all tiles on bard by self.iterate_board
        :param row:
        :param col:
        :return:
        """
        if [row, col] in self.blk_sqs:
            button = Tile(row, col, "black")
            self.grid.addWidget(button, row, col)
        else:
            button = Tile(row, col, "white")
            self.grid.addWidget(button, row, col)

    def get_bl_squares(self):
        """
        randomly sets the number of black squares generated and sets the coordinates of those squares
        """
        num_bl = random.randint(blk_sqs_min, blk_sqs_max)
        bl_sq_li = []
        for num in range(num_bl):
            bl_sq_li.append([random.randint(0, b_dim), random.randint(0, b_dim)])
        self.blk_sqs = bl_sq_li

    def get_adjacent_tiles(self, row, col):
        """
        gets a list of all adjacent tiles to given tile at row and col
        :return: list of tile objects
        """
        rng = 1
        neighbors = [[row, col - rng], [row, col + rng], [row + rng, col], [row - rng, col]]
        adj_tile_li = []
        for ti in neighbors:
            try:
                adj_tile_li.append(self.grid.itemAtPosition(ti[0], ti[1]).widget())
            # catch tiles on edges
            except AttributeError:
                pass
        return adj_tile_li

    def look_at_adjacent(self, row, col):
        """
        looks at tiles adjacent to tile at given col and row and modifiers the following variables on that tile:
            .bl_adj, .light_adj
        also resets colors for cells adjacent to black tiles as needed
        """
        tile = self.grid.itemAtPosition(row, col).widget()
        tile.reset_adj()
        adj_tile_li = self.get_adjacent_tiles(row, col)
        for adj_tile in adj_tile_li:
            if adj_tile.color == 'black':
                tile.inc_bl_adj()
            elif adj_tile.color != 'white' and adj_tile.color != 'yellow':
                tile.inc_light_adj()
        if tile.val is None:
            return
        if tile.light_adj > tile.val:
            for adj in adj_tile_li:
                if adj.color == 'orange' or adj.color == 'red':
                    adj.set_gray()
        else:
            for adj in adj_tile_li:
                if adj.color == 'gray':
                    adj.set_orange()

    def set_bl_val(self, row, col):
        """
        called by iterate_board, if the tile passed is black then the tiles value is set
        NOTE: tiles have a 1 in 3 chance of being blank
        """
        tile = self.grid.itemAtPosition(row, col).widget()
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

    def validate_board(self, row, col):
        """
        called when a light is taken off the board, re establishes all remaining beams
        :return: ensures light beams are not broken by unset_tile()
        """
        temp_tile = self.grid.itemAtPosition(row, col).widget()
        if temp_tile.color == 'orange':
            self.tile_action(temp_tile, self.set_tile)
        elif temp_tile.color == 'red' or temp_tile.color == 'gray':
            temp_tile.set_orange()
            self.tile_action(temp_tile, self.set_tile)

    def update_board(self, tile):
        """
        gets passed a tile object on click and routes that click to the appropriate board action based on the
        color of the tile
        once the action is performed the board is re-validates to ensure no light beams were broken
        """
        tile = self.grid.itemAtPosition(tile.row, tile.col).widget()
        if tile.color == 'orange':
            self.tile_action(tile, self.set_tile)
        elif tile.color == 'white' or tile.color == 'red' or tile.color == 'gray':
            self.tile_action(tile, self.unset_tile)
        self.iterate_board(self.validate_board)
        self.iterate_board(self.look_at_adjacent)
        return

    def set_tile(self, row, col):
        """
        sets a tile given by row and col, if this tile is black then a false boolean is sent to
        self.tile_action which then stops for loop propagation in this direction if a red or orange or gray tile
        is found at this location the move is marked as invalid and the tile is set to red
        """
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
        """
        unsets a tile given by row and col, if this tile is red, gray or black then a false boolean is sent to
        self.tile_action which then stops for loop propagation in this direction
        """
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
