from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from view.worktop import GridScrollBar


class BasicList(QListWidget):

    def __init__(self) -> None:
        super().__init__()

        self.list_style = """
            QListWidget {{
                outline: 0;
                border: {};
            }}
            :enabled {{
                background: transparent;
                color: #bfbfbf;
            }}
            :focus {{
                border: {};
            }}
            :item {{
                margin: 0px;
                padding: 0px;
                border: none;
                border-bottom: 1px solid #545454;
            }}
            :item::selected {{
                background-color: rgba(61, 61, 61, 0.7);
            }}
        """
        self.setStyleSheet(self.list_style.format("2px solid #545454", "2px solid #ffffff"))
        self.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        self.setHorizontalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)


class BasicItem(QListWidgetItem):

    def __init__(self, item_data, parent=None) -> None:
        super().__init__(parent=parent)
        self._item_data = item_data
        self.setText(f"{self._item_data.flag.name} == {str(self._item_data.value).lower()}")

    @property
    def item_data(self):
        return self._item_data

