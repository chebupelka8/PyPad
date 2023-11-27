from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from scripts.load import load_style
from PySide6.QtGui import QPixmap


class WelcomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/welcome_page.css"))
        self.setObjectName("welcome-page")

        self.mainLayout = QVBoxLayout()
        self.horLayout = QHBoxLayout()
        self.horLayout.setSpacing(0)
        
        self.setLayout(self.mainLayout)

        self.setup_ui()
    
    def setup_ui(self):
        self.viewIcon = QLabel()
        pixmap = QPixmap("source/gui/icons/main_icon_1.png")
        self.viewIcon.setPixmap(pixmap)

        self.labelName = QLabel("PyPad")
        self.welcomeLabel = QLabel("Welcome to")
        self.welcomeLabel.resize(100, 40)
        
        # self.horLayout.addSpacing(250)
        self.horLayout.addWidget(self.welcomeLabel, alignment=Qt.AlignmentFlag.AlignRight)
        self.horLayout.addWidget(self.viewIcon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.horLayout.addSpacing(5)
        self.horLayout.addWidget(self.labelName, alignment=Qt.AlignmentFlag.AlignLeft)
        # self.horLayout.addSpacing(305)

        self.mainLayout.addLayout(self.horLayout)

