
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QHBoxLayout, QTabWidget, QWidget

from view.sidebars.form import Form

class PlaceForm(Form):
    
    def __init__(self, model, parent=None) -> None:
        super().__init__(parent=parent)
        self._model = model
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        self.contains_widget = QWidget()
        self.props_widget = QWidget()
        self.tab_widget.addTab(self.props_widget)
        self.tab_widget.addTab(self.contains_widget)

    def showEvent(self, event: QShowEvent) -> None:
        tabWidth = self.tab_widget.width() / self.tab_widget.count() - 24

        self.tab_widget.setStyleSheet(f"""
            QTabBar::tab {{
                width: {tabWidth}px; 
            }}
        """)
        super().showEvent(event)