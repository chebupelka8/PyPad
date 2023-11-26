from PySide6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, 
)
from PySide6.QtGui import (
    QCloseEvent, QIcon
)
from PySide6.QtCore import Qt, QThreadPool
from scripts.load import load_style
from scripts.constants import *
from scripts.code_editor import CodeEditorArea
from scripts.file_manager import FileManager
from scripts.input_newfile import InputCreateNewFile
from scripts.menubar import MenuBar
from scripts.run_console import ConsoleRunWorker
from scripts.console import ConsoleEmulator
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
        self.thread_pool = QThreadPool()
        self.opened_file = None # current file (opened in editor)
    
    def call_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.codeLayout = QHBoxLayout()
        
        self.mainLayout.addLayout(self.codeLayout)

    def create_menu_bar(self):
        self.menu_bar = MenuBar(self)

        self.menu_bar.new_file_action.triggered.connect(self._open_input_newfile_dialog)
        self.menu_bar.open_file_action.triggered.connect(self._open_file)
        self.menu_bar.open_folder_action.triggered.connect(lambda: self.fileManager._open_folder())
        self.menu_bar.save_file_action.triggered.connect(self._save_file)
        self.menu_bar.undo_edit_action.triggered.connect(self.codeArea.undo)
        self.menu_bar.redo_edit_action.triggered.connect(self.codeArea.redo)
        self.menu_bar.cut_edit_action.triggered.connect(self.codeArea.cut)
        self.menu_bar.copy_edit_action.triggered.connect(self.codeArea.copy)
        self.menu_bar.paste_edit_action.triggered.connect(self.codeArea.paste)
        self.menu_bar.select_all_edit_action.triggered.connect(self.codeArea.selectAll)
        self.menu_bar.run_file_action.triggered.connect(self._run_python_file)
        self.menu_bar.run_in_console_action.triggered.connect(self._run_console)
        self.menu_bar.launch_console.triggered.connect(self.consoleEmulator.show)
        
        self.mainLayout.setMenuBar(self.menu_bar)
    
    def setup_ui(self):
        # editor set up
        self.codeArea = CodeEditorArea(self)
        self.codeArea.setReadOnly(True)

        # console set up
        self.consoleEmulator = ConsoleEmulator()

        # file manager set up
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
    
    def _open_file(self):
        f = self.fileManager._open_file()

        if f != None: self._open_file_editor(f)
    
    def _open_file_editor(self, __path: str):
        self.codeArea.setReadOnly(False)

        if os.path.isfile(__path):
            try:
                with open(__path, "r", encoding="utf-8") as file:
                    code = file.read()
                
                self.codeArea.clear()
                self.codeArea.insertPlainText(code)
                self.opened_file = __path
            except:
                print("Unknown file.")
    
    def _save_file(self):
        if self.opened_file == None: return

        with open(self.opened_file, "w", encoding="utf-8") as file:
            file.write(self.codeArea.toPlainText())
    
    def _open_input_newfile_dialog(self):
        self.inputFileName = InputCreateNewFile(self)
        self.inputFileName.show()

        self.inputFileName.buttons.accepted.connect(lambda: self._create_new_file(self.inputFileName.getFileName()))
    
    def _create_new_file(self, __filename: str) -> None:
        
        filename = f"{self.fileManager._get_directory()}/{__filename}"
        if filename == "" or filename[:filename.find(".")] == "": return 

        with open(f"{self.fileManager._get_directory()}/{__filename}", "w") as file:
            file.write("")
        
        self._open_file_editor(filename)
    
    def _run_python_file(self):
        self._save_file()

        if self.opened_file != None and self.opened_file.split(".")[-1] == "py":
            dir_ = self.fileManager._get_directory()
            path_ = self.opened_file[self.opened_file.find(dir_) + len(dir_) + 1:]
            
            console = ConsoleRunWorker(dir_, path_)
            self.thread_pool.start(console._run_python_file)


            # os.system(f"cd {dir_} && python {self.opened_file[self.opened_file.find(dir_) + len(dir_) + 1:]}")
            
            # print(f"cd {dir_} && python {self.opened_file[self.opened_file.find(dir_) + len(dir_) + 1:]}")
        
        self._save_file()
    
    def _run_console(self):
        self._save_file()

        if self.opened_file != None and self.opened_file.split(".")[-1] == "py":
            dir_ = self.fileManager._get_directory()
            path_ = self.opened_file[self.opened_file.find(dir_) + len(dir_) + 1:]

            self.thread_pool.start(lambda: self.consoleEmulator._run_command(f"cd {dir_} && python {path_}"))
            self.consoleEmulator.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wid = MainWidget()
    wid.show()

    sys.exit(app.exec())