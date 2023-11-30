from PySide6.QtGui import QKeyEvent, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PySide6.QtCore import QRunnable, Qt
from scripts.load import load_style
import subprocess, os
from typing import Any


class CommandLineEditor(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.command = None
    
    def enterConnect(self, __command):
        self.command = __command
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.command()
        else:
            super().keyPressEvent(event)


class ConsoleEmulator(QWidget, QRunnable):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/console_emulator.css"))
        self.setObjectName("console-widget")
        self.setWindowTitle("Console")
        self.setWindowIcon(QIcon("source/gui/icons/main_icon_1.png"))

        self.mainLayout = QVBoxLayout()

        self.outputArea = QTextEdit(self)
        self.outputArea.setLineWrapMode(QTextEdit.NoWrap)
        self.outputArea.setReadOnly(True)
        
        self.inputArea = CommandLineEditor(self)
        self.inputArea.enterConnect(lambda: self._run_command(self.inputArea.text()))

        self.mainLayout.addWidget(self.outputArea)
        self.mainLayout.addWidget(self.inputArea)

        self.setLayout(self.mainLayout)
    
    def _run_command(self, __command: Any | list):
        try:
            # launch command using subprocess
            result = subprocess.run(__command, shell=True, capture_output=True, encoding=os.device_encoding(0))

            if __command == "cls": self.outputArea.clear()
            if __command == "exit": self.hide()

            # create output
            self.outputArea.append(result.stdout + result.stderr)

        except Exception as error:
            # print error
            self.outputArea.append(f"Error: {str(error)}")
        
        self.inputArea.clear()