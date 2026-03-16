import math
import random
import PyQt5.QtWidgets as Q
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtCore import QSize, Qt
import sys


class CustomButton(Q.QPushButton):
    def __init__(self, text="", parent=None, is_mine=False, button_width=100, button_height=50):
        super().__init__(text, parent)
        self.is_mine = is_mine
        self.clicked.connect(self.on_click)
        self.setStyleSheet("padding: 0px; margin: 0px;font-size: 20px;")
        self.reset()
        self.setFixedSize(button_width, button_height)

    def reset(self):
        self.is_mine = False
        self.neighbor_mines = 0
        self.is_revealed = False
        self.is_flagged = False
        self.setStyleSheet(self.styleSheet() +
                           "background-color: lightgrey;")
        self.setDisabled(False)

    def on_click(self):
        if not self.is_revealed:
            if self.is_flagged:
                return
            self.is_revealed = True
            self.setDisabled(True)

    @property
    def is_mine(self) -> bool:
        return self._is_mine

    @is_mine.setter
    def is_mine(self, is_mine: bool):
        self._is_mine = is_mine

    @property
    def is_revealed(self) -> bool:
        return self._is_revealed

    @is_revealed.setter
    def is_revealed(self, is_revealed: bool):
        self._is_revealed = is_revealed
        if self._is_revealed:
            self.reveal()
        else:
            self.setText("")
            self.setStyleSheet(self.styleSheet() +
                               "background-color: lightgrey;")

    @property
    def is_flagged(self):
        return self._is_flagged

    @is_flagged.setter
    def is_flagged(self, is_flagged):
        self._is_flagged = is_flagged
        if self._is_flagged:
            self.setText("🚩")
        else:
            self.setText("")

    def reveal(self, end_game: bool = False):
        if self.is_mine:
            self.setText("💣")
            self.setStyleSheet(self.styleSheet() + "background-color: red;")
        else:
            self.setText(str(self.neighbor_mines))
            self.setStyleSheet(self.styleSheet() +
                               "background-color: lightgreen;")
        if end_game:
            self.setDisabled(True)
            if self.is_flagged:
                self.setText("🚩")

    # This is overriding the parent class

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_flagged = not self.is_flagged

        elif event.button() == Qt.LeftButton:
            # Call the base class's method to maintain normal left-click behavior
            super().mousePressEvent(event)


class EndScreen(Q.QDialog):
    def __init__(self, parent=None, title="Game over", message="You win!", won=True):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.label = Q.QLabel(message, self)
        # added - change label font size:
        self.label.setFont(QFont("Arial", 40))
        layout = Q.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(
            Q.QLabel("Would you like to play again?", self), alignment=Qt.AlignCenter)
        button_row = Q.QHBoxLayout()
        yes_button = Q.QPushButton("Yes", self)
        no_button = Q.QPushButton("No", self)
        button_row.addWidget(yes_button)
        button_row.addWidget(no_button)
        layout.addLayout(button_row)
        no_button.clicked.connect(self.reject)
        yes_button.clicked.connect(self.accept)


class MainWindow(Q.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper")
        self.EASY_MINE_COUNT = 20
        self.EASY_ROWS = 10
        self.EASY_COLS = 10
        self.MED_MINE_COUNT = 30
        self.MED_ROWS = 12
        self.MED_COLS = 14
        self.HARD_MINE_COUNT = 80
        self.HARD_ROWS = 15
        self.HARD_COLS = 15
        # self.setGeometry(500, 550, 600, 400)
        self.setMinimumHeight(550)
        self.click_count = 0
        self.total_mines = self.EASY_MINE_COUNT
        self.rows = self.EASY_ROWS
        self.cols = self.EASY_COLS
        self.initUI()

    def create_layout(self):
        self.create_menu()
        self.central_widget = Q.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_container = Q.QVBoxLayout()
        self.central_widget.setLayout(self.main_container)
        self.label_title = Q.QLabel("CMP Minesweeper!", self)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet(
            "font-size: 40px; font-weight: bold;")
        self.main_container.addWidget(self.label_title)
        self.grid = Q.QGridLayout()
        self.grid_widget = Q.QWidget()

        self.grid_widget.setFixedWidth(500)
        self.grid_widget.setFixedHeight(500)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.main_container.addWidget(
            self.grid_widget, alignment=Qt.AlignCenter)
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
                button.clicked.connect(
                    lambda checked, row=i, col=j: self.space_clicked(row, col))
                container.addWidget(button, i, j)
                self.mine_list[i].append(button)

    def create_menu(self):
        menu = self.menuBar()
        difficulty_menu = menu.addMenu("&Difficulty")
        self.add_menu_item(difficulty_menu, "Easy", "Ctrl+E",
                           self.EASY_MINE_COUNT, self.EASY_ROWS, self.EASY_COLS)
        self.add_menu_item(difficulty_menu, "Medium", "Ctrl+M",
                           self.MED_MINE_COUNT, self.MED_ROWS, self.MED_COLS)
        self.add_menu_item(difficulty_menu, "Hard", "Ctrl+H",
                           self.HARD_MINE_COUNT, self.HARD_ROWS, self.HARD_COLS)

    def add_menu_item(self, parent_menu, text, shortcut_text, mines, rows, cols):
        btn_action = Q.QAction(text, self)
        btn_action.setShortcut(QKeySequence(shortcut_text))
        parent_menu.addAction(btn_action)
        btn_action.triggered.connect(
            lambda clicked, mines=mines, rows=rows, cols=cols: self.update_difficulty(mines, rows, cols))

    def update_difficulty(self, mines, rows, cols):
        self.mine_count = mines
        self.rows = rows
        self.cols = cols
        self.restart_game()

    def space_clicked(self, row, col, testing=False):
        self.click_count += 1
        if self.click_count == 1:
            # await our first click
            self.place_mines(self.total_mines, row, col)
            self.create_neighbor_mine_counts()
            if testing:
                self.reveal_all(False)
        if self.mine_list[row][col].is_mine:
            self.do_ending("You lost!", "Boom! Too bad. You blew up!")
            return  # do some game over thing

        elif self.mine_list[row][col].neighbor_mines == 0:
            for i in range(-1, 2):  # -1, 0, 1
                # i represents the row above, same row, row below
                current_row = row + i
                for j in range(-1, 2):
                    current_col = col + j
                    if (self.is_valid_index_in_mine_list(current_row, current_col) and
                            not self.mine_list[current_row][current_col].is_flagged):

                        self.mine_list[current_row][current_col].click()
        if self.click_count == (self.rows * self.cols) - self.total_mines:
            self.do_ending("Congratulations, you won!",
                           "Way to go, you did it!")

    def do_ending(self, title, message):
        self.reveal_all(True)
        end_screen = EndScreen(
            title=title, message=message)
        again = end_screen.exec()
        if again == Q.QDialog.Accepted:
            print("Playing again")
            self.restart_game()
        else:
            print("not playing again")
            self.close()

    def restart_game(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        self.create_buttons(self.rows, self.cols, self.grid)
        self.click_count = 0

    def reveal_all(self, end_game=True):
        for row in self.mine_list:
            for cell in row:
                cell.reveal(end_game=end_game)

    def place_mines(self, num_of_mines, avoid_row=-100, avoid_col=-100):
        self.mine_count = num_of_mines
        mines_placed = 0
        while mines_placed < self.mine_count:
            # place a mine at a random space.
            choice_row = random.randint(0, len(self.mine_list)-1)
            choice_col = random.randint(0, len(self.mine_list[choice_row])-1)
            if choice_row in (avoid_row - 1, avoid_row, avoid_row + 1) and choice_col in (avoid_col-1, avoid_col, avoid_col+1):
                continue

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
        self.restart_game()


def main():
    app = Q.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
