from PySide6.QtWidgets import QTabWidget
from scripts.load import load_style
from scripts.code_editor import CodeEditorArea
from scripts.welcome_page import WelcomePage


class TabEditorArea(QTabWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.addTab(WelcomePage(self), "Welcome")
        self.setStyleSheet(load_style("source/gui/style/tab_editor.css"))
        self.setTabsClosable(True)
    
    def _add_editor(self, __name: str, __text: str, full_path: str = None) -> None:
        self.codeArea = CodeEditorArea(self)
        self.codeArea.insertPlainText(__text)
        self.codeArea.setCurrentPath(full_path)

        if self._get_by_full_path(full_path) == None: self.addTab(self.codeArea, __name)
        # self.addTab(self.codeArea, __name)
    
    def _get_by_full_path(self, __path: str) -> int | None:
        res = 0
        
        for w in range(self.count()):
            try: 
                if self.widget(w).getCurrentPath() == __path: res += 1
            except: 
                pass
        
        return res if res != 0 else None
    
    def _get_count_by_name(self, __name) -> int | None:
        res = 0

        for w in range(self.count()):
            if __name == self.tabText(w): res += 1
        
        return res if res != 0 else None

    def _get_index_by_name(self, __name) -> int | None:
        index = None

        for w in range(self.count()):
            if __name == self.tabText(w): index = self.indexOf(self.widget(w))
        
        return index

    def _get_index_by_full_path(self, __path: str) -> int | None:
        index = None

        for w in range(self.count()):
            try:
                if __path == self.widget(w).getCurrentPath(): index = self.indexOf(self.widget(w))
            except:
                pass
        
        return index