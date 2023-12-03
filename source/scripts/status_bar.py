from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStatusBar, QFrame
from PySide6.QtCore import Qt
from scripts.load import load_style
from scripts.constants import theme


class StatusBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/status_bar.css") + "QFrame {" + f"background-color: {theme["workbench.colorCustomization"]["status-bar"]["background-color"]}" + "}")
        self.setObjectName("status-bar")
        self.setAutoFillBackground(True)
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setFixedHeight(40)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)

        self.setup_ui()

        self.setLayout(self.mainLayout)
    
    def setup_ui(self):
        self.nameLabel = QLabel("PyPad")
        self.curPosLabel = QLabel("{} Python")

        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addWidget(self.curPosLabel, alignment=Qt.AlignmentFlag.AlignRight)
    
    def _setCurrentPos(self, position: list):
        """
        args:
            position (list): [line, column] 
        """

        self.curPosLabel.setText("Position: " + "; ".join(position) + "    {} Python")


        