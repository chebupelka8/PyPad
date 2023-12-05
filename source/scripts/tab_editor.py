from PySide6.QtWidgets import QTabWidget
from scripts.load import load_style
from scripts.code_editor import CodeEditorArea
from scripts.welcome_page import WelcomePage


class TabEditorArea(QTabWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.addTab(WelcomePage(self), "Welcome")
        self.setStyleSheet(load_style("source/gui/style/tab_editor.css"))
    
    def _add_editor(self, __name: str, __text: str, full_path: str = None) -> None:
        self.codeArea = CodeEditorArea(self)
        self.codeArea.insertPlainText(__text)
        self.codeArea.setCurrentPath(full_path)

        if self._get_by_name(__name) == None: self.addTab(self.codeArea, __name)
    
    def _get_by_name(self, __name) -> int | None:
        res = 0

        for w in range(self.count()):
            if __name == self.tabText(w): res += 1
        
        return res if res != 0 else None