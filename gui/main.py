from PyQt6.QtGui import QFont
from view.windows.main_window import MainWindow
import sys

from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Futura", 10)
    QApplication.setFont(font)
    
    main_window = MainWindow()
    main_window.show()
    app.exec()