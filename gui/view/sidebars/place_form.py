
from PyQt6.QtWidgets import QHBoxLayout, QTabWidget, QWidget

from view.sidebars.form import Form

style = """
    QTabWidget::pane {
        background: transparent;
        border: none;
    }

    QTabBar::tab {
        border: none;
        width: 132px;
        color: #bfbfbf;
    }

    QTabBar::tab:selected {
        background: #545454;
    }

    QTabBar::tab:!selected {
        background: #3d3d3d;
    }

    QTabBar::tab:!selected:hover {
        background: #999;
    }

    QTabBar::tab:top:!selected {
        margin-top: 3px;
    }

    QTabBar::tab:bottom:!selected {
        margin-bottom: 3px;
    }

    QTabBar::tab:top, QTabBar::tab:bottom {
        min-width: 8ex;
        margin-right: -1px;
        padding: 5px 0px 5px 0px;
    }

    QTabBar::tab:top:selected {
        border-bottom-color: none;
    }

    QTabBar::tab:bottom:selected {
        border-top-color: none;
    }

    QTabBar::tab:top:last, QTabBar::tab:bottom:last,
    QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
        margin-right: 0;
    }

    QTabBar::tab:left:!selected {
        margin-right: 3px;
    }

    QTabBar::tab:right:!selected {
        margin-left: 3px;
    }

    QTabBar::tab:left, QTabBar::tab:right {
        min-height: 8ex;
        margin-bottom: -1px;
        padding: 10px 5px 10px 5px;
    }

    QTabBar::tab:left:selected {
        border-left-color: none;
    }

    QTabBar::tab:right:selected {
        border-right-color: none;
    }

    QTabBar::tab:left:last, QTabBar::tab:right:last,
    QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
        margin-bottom: 0;
    }
"""

class PlaceForm(Form):
    
    def __init__(self, model, parent=None) -> None:
        super().__init__(model, parent=parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(style)
        layout.addWidget(self.tab_widget)
        self.contains_widget = QWidget()
        self.props_widget = QWidget()
        self.tab_widget.addTab(self.props_widget, "Properties")
        self.tab_widget.addTab(self.contains_widget, "Place objects")
