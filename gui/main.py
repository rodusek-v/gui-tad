from PyQt6.QtGui import QFont
from view.windows.main_window import MainWindow
import sys

from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Courier New", 10)
    font.setBold(True)
    font.setStyleHint(QFont.StyleHint.Monospace)
    QApplication.setFont(font)
    
    main_window = MainWindow()
    main_window.show()
    app.exec()