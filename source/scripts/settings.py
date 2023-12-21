from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QCheckBox, QComboBox,
    QLineEdit, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import json
from typing import Any
from scripts.load import load_style


class ScrollerWidget(QScrollArea):
    def __init__(self, parent = None, vertical_policy: bool = True, horizontal_policy: bool = False) -> None:
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("source/gui/icons/main_icon_1.png"))
        self.setMaximumSize(800, 600)
        self.setStyleSheet(load_style("source/gui/style/scrollbar.css"))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn) if vertical_policy else self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn) if horizontal_policy else self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

class SettingsMenu(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setObjectName("settings-menu")
        self.setStyleSheet(load_style("source/gui/style/settings_menu.css"))
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(50)
        self.setLayout(self.mainLayout)
        self.__settings = [] 

        self.init_ui()
    
    def init_ui(self) -> None:
        self.add_setting("Font Family", QLineEdit(self))
        self.add_setting("Hints", QCheckBox(self))
        self.add_setting("Color theme", QComboBox())
        self.add_setting("Color theme", QPushButton("world"))

    def add_setting(self, __title: str, widget) -> None:
        self.__settings.append([__title, widget])
        
        l = QHBoxLayout()
        
        l.addSpacing(20)
        l.addWidget(QLabel(__title))
        l.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.mainLayout.addLayout(l)
    
    def count(self) -> int:
        return len(self.__settings)

    def get_widget_by_title(self, __title: str) -> Any:
        for title, widget in self.__settings:
            if title == __title: return widget
    
    def get_index_by_title(self, __title: str) -> int:
        for index, seq in enumerate(self.__settings):
            if __title == seq[0]: return index
