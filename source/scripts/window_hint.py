from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QListWidget
from PySide6.QtCore import Qt
from scripts.constants import keywords


class WindowHint1(QWidget):
    def __init__(self, hints: list):
        super(WindowHint, self).__init__()

        self.hints = hints

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        for i in self.hints: self.mainLayout.addWidget(QLabel(f"{i[0]}          {i[1]}"))
    
    def _update_list(self, hints: list):
        self.hints = hints
        self._clear_window()
        
        for i in self.hints: self.mainLayout.addWidget(QLabel(f"{i[0]}          {i[1]}"))
    
    def _clear_window(self):
        while self.mainLayout.count():
            item = self.mainLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()



class WindowHint(QWidget):
    def __init__(self, parent) -> None:
        super(WindowHint, self).__init__(parent, Qt.WindowType.FramelessWindowHint)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.listWidget = QListWidget()
        self.mainLayout.addWidget(self.listWidget)

    def _set_hints(self, hints: list):
        self.listWidget.clear()
        self.listWidget.addItems(hints)
    
    def _get_hints(self) -> list:
        return self.listWidget.count()

    def _find_matches(self, text: str) -> list[str]:
        if text.replace(" ", "") == "": return []
        
        result = []

        for match in keywords:
            if match.find(text) != -1: result.append(match)
        
        return result
