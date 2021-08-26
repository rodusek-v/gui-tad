from PyQt6.QtWidgets import QFrame, QWidget

class Grid(QFrame):

    def __init__(self) -> None:
        super().__init__()
        self.a = QWidget(self)
        self.a.setGeometry(400,0, self.width() + 400, 200)
        self.a.setStyleSheet("background-color: red")
        self.b = QWidget(self)
        self.b.setGeometry(0,0, 100, 100)
        self.b.setStyleSheet("background-color: rgba(255, 255, 255, 0)")