from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from scripts.load import load_style
from PySide6.QtGui import QPixmap
from scripts.vector import Vec2
from scripts.constants import theme


class WelcomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("welcome-page")
        self.setStyleSheet(
            load_style("source/gui/style/welcome_page.css")
        )

        self.mainLayout = QVBoxLayout()
        
        self.subWidget = QWidget(self)
        self.subWidget.setFixedSize(Vec2(1000, 1000).qsize)
        self.mainLayout.addWidget(self.subWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.horLayout = QHBoxLayout()
        self.horLayout.setSpacing(0)
        
        self.setLayout(self.mainLayout)

        self.setup_ui()
    
    def setup_ui(self):
        self.viewIcon = QLabel()
        pixmap = QPixmap("source/gui/icons/main_icon_1.png")
        self.viewIcon.setPixmap(pixmap)
        self.viewIcon.setContentsMargins(50, 0, 0, 0)

        self.labelName = QLabel("PyPad")
        self.labelName.setContentsMargins(0, 0, 280, 0)
        
        self.welcomeLabel = QLabel("Welcome to")
        self.welcomeLabel.setContentsMargins(240, 0, 0, 0)
        
        self.horLayout.addWidget(self.welcomeLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.horLayout.addWidget(self.viewIcon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.horLayout.addWidget(self.labelName, alignment=Qt.AlignmentFlag.AlignCenter)

        self.subWidget.setLayout(self.horLayout)

