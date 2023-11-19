from PySide6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, 
    QPushButton, QMenu, QMenuBar, QInputDialog
)
from PySide6.QtGui import (
    QAction, QCloseEvent, QFontMetrics, QFont, QIcon
)
from PySide6.QtCore import Qt
from scripts.load import load_style
from scripts.constants import *
from scripts.code_editor import CodeEditorArea
from scripts.file_manager import FileManager
from scripts.input_newfile import InputCreateNewFile
from scripts.menubar import MenuBar
import sys, os


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.resize(WINDOW_SIZE.qsize)
        self.setWindowTitle("PyPad")
        self.setWindowIcon(QIcon("source/gui/icons/main_icon_1.png"))
        self.setObjectName("main-widget")
        self.setStyleSheet(load_style("source/gui/style/style.css"))

        self.call_layouts()
        self.setup_ui()

        self.setLayout(self.mainLayout) # set main layout
        self.create_menu_bar()

        # variables 
        self.opened_file = None # current file (opened in editor)
    
    def call_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.codeLayout = QHBoxLayout()
        
        self.mainLayout.addLayout(self.codeLayout)

    def create_menu_bar(self):
        self.menu_bar = MenuBar(self)

        self.menu_bar.new_file_action.triggered.connect(self._open_input_newfile_dialog)
        self.menu_bar.open_file_action.triggered.connect(lambda: self.fileManager._open_file())
        self.menu_bar.open_folder_action.triggered.connect(lambda: self.fileManager._open_folder())
        self.menu_bar.save_file_action.triggered.connect(self._save_file)
        self.menu_bar.undo_edit_action.triggered.connect(self.codeArea.undo)
        self.menu_bar.redo_edit_action.triggered.connect(self.codeArea.redo)
        self.menu_bar.cut_edit_action.triggered.connect(self.codeArea.cut)
        self.menu_bar.copy_edit_action.triggered.connect(self.codeArea.copy)
        self.menu_bar.paste_edit_action.triggered.connect(self.codeArea.paste)
        self.menu_bar.select_all_edit_action.triggered.connect(self.codeArea.selectAll)
        self.menu_bar.run_file_action.triggered.connect(self._run_python_file)
        
        self.mainLayout.setMenuBar(self.menu_bar)
    
    def setup_ui(self):

        # editor.settingsCustomization & editor.theme.colorCustomization
        self.codeArea = CodeEditorArea()
        self.codeArea.setStyleSheet(
            f"""
            font-size: {data["workbench.settingsCustomization"]["editor.fontSize"]}px;
            color: {theme["workbench.theme.colorCustomization"]["editor.syntaxHighlighterCustomization"]["-default"]["color"]};
            background-color: {theme["workbench.theme.colorCustomization"]["editor.background"]};
            font-family: '{data["workbench.settingsCustomization"]["editor.fontFamily"]}';
            """
        )
        if data["workbench.settingsCustomization"]["editor.cursorStyle"] == "block":
            self.codeArea.setCursorWidth(
                QFontMetrics(QFont(data["workbench.settingsCustomization"]["editor.fontFamily"], int(data["workbench.settingsCustomization"]["editor.fontSize"]))).horizontalAdvance("e") - 3
            )
        elif data["workbench.settingsCustomization"]["editor.cursorStyle"] == "column":
            self.codeArea.setCursorWidth(1)
        else:
            self.codeArea.setCursorWidth(1)
        self.codeArea.setTabStopDistance(
            QFontMetrics(QFont(data["workbench.settingsCustomization"]["editor.fontFamily"], int(data["workbench.settingsCustomization"]["editor.fontSize"]))).horizontalAdvance('    ') - 15
        )

        self.fileManager = FileManager()
        self.fileManager.clicked.connect(lambda index: self._open_file_editor(self.fileManager._get_path(index)))

        # add Widgets to layouts
        self.codeLayout.addWidget(self.fileManager, stretch=4)
        self.codeLayout.addWidget(self.codeArea, stretch=9)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            self.inputFileName.destroy()
        except:
            pass
        super().closeEvent(event)
    
    def _open_file_editor(self, __path: str):

        if os.path.isfile(__path):
            try:
                with open(__path, "r") as file:
                    code = file.read()
                    file.close()
                
                self.codeArea.clear()
                self.codeArea.insertPlainText(code)
                self.opened_file = __path
            except:
                print("Unknown file.")
    
    def _save_file(self):
        if self.opened_file == None: return

        with open(self.opened_file, "w") as file:
            file.write(self.codeArea.toPlainText())
            file.close()
    
    def _open_input_newfile_dialog(self):
        self.inputFileName = InputCreateNewFile(self)
        self.inputFileName.show()

        self.inputFileName.buttons.accepted.connect(lambda: self._create_new_file(self.inputFileName.getFileName()))
    
    def _create_new_file(self, __filename: str) -> None:
        print(f"{self.fileManager._get_directory()}/{__filename}")
        
        filename = f"{self.fileManager._get_directory()}/{__filename}"
        if filename == "" or filename[:filename.find(".")] == "": return 

        with open(f"{self.fileManager._get_directory()}/{__filename}", "w") as file:
            file.write("")
            file.close()
    
    def _run_python_file(self):
        self._save_file()

        if self.opened_file != None and self.opened_file.split(".")[-1] == "py":
            dir_ = self.fileManager._get_directory()
            os.system(f"cd {dir_} && python {self.opened_file[self.opened_file.find(dir_) + len(dir_) + 1:]}")
            
            # print(f"cd {dir_} && python {self.opened_file[self.opened_file.find(dir_) + len(dir_) + 1:]}")
        
        self._save_file()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wid = MainWidget()
    wid.show()

    sys.exit(app.exec())