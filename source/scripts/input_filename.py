from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QDialogButtonBox
from scripts.load import load_style


class AskInputFileName(QDialog):
    def __init__(self, parent, title: str, placed_text: str = "") -> None:
        super().__init__(parent = parent, f = Qt.WindowType.FramelessWindowHint)

        self.setWindowTitle("")
        self.setMinimumWidth(500)
        self.setStyleSheet(load_style("source/gui/style/input_file_name.css"))

        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.mainLayout.addWidget(QLabel(title), alignment=Qt.AlignmentFlag.AlignCenter)
        self.inputName = QLineEdit()
        self.inputName.setText(placed_text)
        self.mainLayout.addWidget(self.inputName)
        self.mainLayout.addLayout(self.buttonLayout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.buttonLayout.addWidget(self.buttons, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.mainLayout) # set main layout (draw)
    
    def getFileName(self) -> str:
        return self.inputName.text()