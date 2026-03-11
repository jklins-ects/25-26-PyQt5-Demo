# buttons are a way for users to trigger events in your application.

# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

import PyQt5.QtWidgets as Q
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import sys


class MainWindow(Q.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Push Button Example")
        self.setGeometry(500, 500, 600, 400)
        self.initUI()

    def initUI(self):
        self.count = 0
        self.label = Q.QLabel("Hello", self)
        self.label.setGeometry(150, 100, 200, 100)
        self.label.setStyleSheet("font-size: 50px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.updateCountLabel(self.count)
        # Create our first button!
        self.button = Q.QPushButton("", self)
        self.button.setGeometry(150, 0, 200, 100)
        self.button.setStyleSheet("font-size: 30px")

        self.pixmap = QIcon("images/Greg.png")
        # put the image (pixmap) into the label
        self.button.setIcon(self.pixmap)
        # set size, give width, height
        self.button.setIconSize(
            QSize(self.button.width(), self.button.height()))
        # associate code to an event (clicked)
        self.button.clicked.connect(self.on_click)

    # we want this to run when our button is clicked:
    def on_click(self):
        self.count += 1
        self.updateCountLabel(self.count)

    def updateCountLabel(self, count: int):
        self.label.setText(str(count))


def main():
    app = Q.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
