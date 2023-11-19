from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt


class WindowHint(QWidget):
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


        
