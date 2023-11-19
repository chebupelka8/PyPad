from PySide6.QtWidgets import (
    QPlainTextEdit
)
from scripts.highlighter import Highlighter
from scripts.load import load_style


class CodeEditorArea(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        Highlighter(self)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)