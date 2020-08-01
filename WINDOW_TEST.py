# importing the required libraries

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import random

b_dim = 15
blk_sqs_max = 25
blk_sqs_min = 15


class Tile(QPushButton):
    def __init__(self, row, col, color):
        super().__init__()
        self.row = row
        self.col = col
        self.color = color
        self.setFixedSize(QSize(25, 25))
        self.clicked.connect(self.on_click)

        if self.color == "black":
            self.setStyleSheet("background-color: black; color: white")
            if self.is_corner():
                self.setText(str(random.randint(0, 2)))
            else:
                self.setText(str(random.randint(0, 4)))
        elif self.color == "yellow":
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: white")

    def is_corner(self):
        corners = [[0, 0], [0, b_dim - 1], [b_dim - 1, 0], [b_dim - 1, b_dim - 1]]
        for corner in corners:
            if self.col == corner[0] and self.row == corner[1]:
                return True

    def on_click(self):
        if self.color == "white" or self.color == "yellow":
            self.setStyleSheet("background-color: orange")
            self.color = "orange"
            game.update_board(self, True)
        elif self.color == "black":
            return
        elif self.color == "orange":
            self.setStyleSheet("background-color: white")
            self.color = "white"
            game.update_board(self, False)

    def set_yellow(self):
        print("asldk;fjas;ldkfj")
        #self.setStyleSheet("background-color: yellow")
        #self.color = "yellow"


class Board(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        #grid = QGridLayout()
        self.grid.setSpacing(0)
        self.setLayout(self.grid)
        self.blk_sqs = []
        self.get_bl_squares()

        # set the title
        self.setWindowTitle("LIGHT UP")
        width = 500
        height = 500
        # setting  the fixed width & height of window
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        for x in range(b_dim):
            for y in range(b_dim):
                if [x, y] in self.blk_sqs:
                    button = Tile(x, y, "black")
                    # button.clicked.connect(say_hello)
                    self.grid.addWidget(button, x, y)
                else:
                    button = Tile(x, y, "white")
                    self.grid.addWidget(button, x, y)

        # show all the widgets
        self.show()

    def get_bl_squares(self):
        # get the number of black squares on the board
        num_bl = random.randint(blk_sqs_min, blk_sqs_max)
        bl_sq_li = []
        for num in range(num_bl):
            bl_sq_li.append([random.randint(0, b_dim), random.randint(0, b_dim)])
        self.blk_sqs = bl_sq_li

    def update_board(self, tile, co_bool):
        if co_bool is True:
            color = "yellow"
        else:
            color = "white"
        print(type(self.grid.itemAtPosition(tile.row, tile.col)))
        for x in range(b_dim):
            for y in range(b_dim):
                if x == tile.row and y == tile.col:
                    pass
                elif [x, y] in self.blk_sqs:
                    pass
                elif x == tile.row:
                    self.grid.addWidget(Tile(x, y, color), x, y)
                elif y == tile.col:
                    self.grid.addWidget(Tile(x, y, color), x, y)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Board()
    game.show()
    sys.exit(app.exec_())
