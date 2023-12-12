from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QListWidget
from PySide6.QtCore import Qt, QItemSelectionModel, QModelIndex
from scripts.constants import python_dictionary


class HintListWidget(QListWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.itemClicked.connect(self.on_item_clicked)
    
    def selectFirstItem(self) -> None:
        self.selectionModel().clearSelection()
        self.selectionModel().select(self.indexFromItem(self.item(0)), QItemSelectionModel.Select) # select opened file

    def _set_hints(self, hints: list) -> None:
        self.clear()
        self.addItems(hints)
    
    def _get_count_hints(self) -> int:
        return self.count()

    def getIndexByText(self, __text: str) -> QModelIndex | None:
        for item in range(self.count()):
            if self.item(item).text() == __text: return self.indexFromItem(self.item(item))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)

        # self.setPositionForIndex()
        if event.key() == Qt.Key.Key_Down:
            pass

    def on_item_clicked(self, item):
        index = self.row(item)
        
        if index > 0:
            previous_item = self.item(index - 1)
            self.setCurrentItem(previous_item)
        
        elif index < self.count() - 1:
            next_item = self.item(index + 1)
            self.setCurrentItem(next_item)


class WindowHint(QWidget):
    def __init__(self, parent) -> None:
        super(WindowHint, self).__init__(parent)

        self.resize(600, 200)
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.listWidget = HintListWidget()
        self.mainLayout.addWidget(self.listWidget)

    def _find_matches(self, text: str) -> list[str]:
        if text == "": return []
        
        result = []

        for match in python_dictionary:
            if match.find(text) != -1: result.append(match)
        
        return result
