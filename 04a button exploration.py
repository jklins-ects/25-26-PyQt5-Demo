import math
import random
import PyQt5.QtWidgets as Q
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import sys


class CustomButton(Q.QPushButton):
    def __init__(self, text="", parent=None, is_mine=False, button_width=100, button_height=50):
        super().__init__(text, parent)
        self.is_mine = is_mine
        self.neighbor_mines = 0
        self.clicked.connect(self.on_click)
        self.setStyleSheet("padding: 0px; margin: 0px;font-size: 20px;")
        self.setFixedSize(button_width, button_height)

    def on_click(self):
        self.reveal()
        self.setDisabled(True)

    @property
    def is_mine(self) -> bool:
        return self._is_mine

    @is_mine.setter
    def is_mine(self, is_mine: bool):
        self._is_mine = is_mine

    def reveal(self):
        print(self.styleSheet())
        if self.is_mine:
            self.setText("💣")
            self.setStyleSheet(self.styleSheet() + "background-color: red;")
        else:
            self.setText(str(self.neighbor_mines))
            self.setStyleSheet(self.styleSheet() +
                               "background-color: lightgreen;")


class MainWindow(Q.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Push Button Example")
        self.setGeometry(500, 550, 600, 400)
        self.setMinimumHeight(550)
        self.initUI()

    def create_layout(self):
        self.central_widget = Q.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_container = Q.QVBoxLayout()
        self.central_widget.setLayout(self.main_container)
        self.label_title = Q.QLabel("Many Buttons!", self.central_widget)
        self.grid = Q.QGridLayout()
        self.grid_widget = Q.QWidget()
        self.grid_widget.setFixedWidth(500)
        self.grid_widget.setFixedHeight(500)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.main_container.addWidget(self.grid_widget)
        self.grid_widget.setLayout(self.grid)

    def create_buttons(self, rows, cols, container):
        self.mine_list = []
        button_width = math.floor(self.grid_widget.width() / cols)
        button_height = math.floor(self.grid_widget.height() / rows)
        for i in range(rows):
            self.mine_list.append([])
            for j in range(cols):
                button = CustomButton(
                    f"{i}, {j}", self, button_height=button_height, button_width=button_width)
                container.addWidget(button, i, j)
                self.mine_list[i].append(button)

    def place_mines(self, num_of_mines):
        self.mine_count = num_of_mines
        mines_placed = 0
        while mines_placed < self.mine_count:
            # place a mine at a random space.
            choice_row = random.randint(0, len(self.mine_list)-1)
            choice_col = random.randint(0, len(self.mine_list[choice_row])-1)
            if not self.mine_list[choice_row][choice_col].is_mine:
                self.mine_list[choice_row][choice_col].is_mine = True
                mines_placed += 1

    def get_mine_counts(self, row, col):
        mine_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                target_row = row + i
                target_col = col + j
                if self.is_valid_index_in_mine_list(target_row, target_col) and self.mine_list[target_row][target_col].is_mine:
                    mine_count += 1
        return mine_count

    def is_valid_index_in_mine_list(self, row, col):
        # this short circuits
        # if row is invalid, it won't check col.
        return 0 <= row < len(self.mine_list) and 0 <= col < len(self.mine_list[row])

    def create_neighbor_mine_counts(self):
        # loop through each cell in our 2d list
        # check all cells around it
        # if they are a bomb, add one to the count
        # set the property of the button to the final count
        for i in range(len(self.mine_list)):
            for j in range(len(self.mine_list[i])):
                self.mine_list[i][j].neighbor_mines = self.get_mine_counts(
                    i, j)
                # self.mine_list[i][j].setText(
                #     str(self.mine_list[i][j].neighbor_mines))

    def initUI(self):
        self.create_layout()
        self.create_buttons(10, 10, self.grid)
        self.place_mines(20)
        self.create_neighbor_mine_counts()


def main():
    app = Q.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
