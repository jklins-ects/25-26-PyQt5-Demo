import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# qpixmap loads and manages the image file before it is placed in a label
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

"""
sys: This is a built-in Python module that provides access to variables and functions that interact with the Python interpreter.
PyQt5.QtWidgets: This module contains all the main GUI “widgets” such as buttons, labels, and windows.
QApplication: This class manages the GUI application itself.
QMainWindow: This class provides a main application window that you can customize.
"""

# Create a custom window:


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMP 25-26 Year 1")
        self.setGeometry(00, 00, 500, 500)  # (x,y,width, height)
        # x: distance from the left edge of your screen
        # y: distance from the top of your screen
        self.setWindowIcon(QIcon("images/Greg.png"))

        self.label = QLabel("Hello", self)

        self.label.setFont(QFont("Arial", 40))

        self.label.setGeometry(0, 0, 500, 100)
        self.label.setStyleSheet(
            # This IS CSS!
            "color: rgb(0,0,255);"  # Supports HEX, RGB and ColorNames
            "background-color: #87CEFA;"  # Supports HEX, RGB and ColorNames
            "border: 10px solid black;"
            "font-weight: bold;"
            "font-style: italic;"
            "text-decoration: underline;"
        )
        self.label.setAlignment(Qt.AlignCenter)

        self.piclabel = QLabel(self)
        self.piclabel.setGeometry(0, 100, 300, 250)

        self.pixmap = QPixmap("images/Greg.png")
        # put the image (pixmap) into the label
        self.piclabel.setPixmap(self.pixmap)
        # if image is too big or too small, we can make it fit our container.
        self.piclabel.setScaledContents(True)
        # let's try putting greg in the bottom right corner - we'll use MATH!
        self.piclabel.setGeometry(self.width(
        ) - self.piclabel.width(), self.height() - self.piclabel.height(), 300, 250)

        # % is mod, // is integer division
        # let's try putting greg in the middle - we'll use MATH!
        self.piclabel.setGeometry((self.width(
        ) - self.piclabel.width())//2, (self.height() - self.piclabel.height()) // 2, 300, 250)


def main():
    # Creates the main application and passes in an y command line arguments
    app = QApplication(sys.argv)
    window = MainWindow()  # Instatiate our main window
    window.show()  # Make the window visible

    # Starts the application loop. The program will keep running until you close the Window
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
