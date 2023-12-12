from PySide6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, 
    QLabel
)
from PySide6.QtGui import (
    QCloseEvent, QIcon
)
from PySide6.QtCore import Qt, QThreadPool, QItemSelectionModel
from scripts.load import load_style
from scripts.constants import *
from scripts.file_manager import FileManager
from scripts.input_filename import AskInputFileName
from scripts.menubar import MenuBar
from scripts.run_console import ConsoleRunWorker
from scripts.console import ConsoleEmulator
from scripts.welcome_page import WelcomePage
from scripts.status_bar import StatusBar
from scripts.tab_editor import TabEditorArea
import sys, os


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.resize(WINDOW_SIZE.qsize)
        self.setWindowTitle("PyPad")
        self.setWindowIcon(QIcon("source/gui/icons/main_icon_1.png"))
        self.setObjectName("main-widget")
        self.setStyleSheet(
            load_style("source/gui/style/style.css") + "QWidget#main-widget {" + f"background-color: {theme["workbench.colorCustomization"]["background-color"]}" + "}"
        )
    
        self.call_layouts()
        self.setup_ui()

        self.setLayout(self.mainLayout) # set main layout

        self._update()
    
    def call_layouts(self):
        self.mainLayout = QVBoxLayout()
        self.codeLayout = QHBoxLayout()
        self.sideBarLayout = QHBoxLayout()
        
        self.mainLayout.addLayout(self.codeLayout)
        self.mainLayout.addLayout(self.sideBarLayout)
    
    def _update(self):
        # retrigger menubar
        try: self.menu_bar.clear()
        except AttributeError: pass
        self.create_menu_bar()
        
        self.menu_bar.new_file_action.triggered.connect(self._open_input_newfile_dialog)
        self.menu_bar.new_folder_action.triggered.connect(self._open_input_newfolder_dialog)
        self.menu_bar.open_file_action.triggered.connect(self._open_file)
        self.menu_bar.open_folder_action.triggered.connect(lambda: self.fileManager._open_folder())
        self.menu_bar.save_file_action.triggered.connect(self._save_file)
        self.menu_bar.run_file_action.triggered.connect(self._run_python_file)
        self.menu_bar.run_in_console_action.triggered.connect(self._run_console)
        self.menu_bar.launch_console.triggered.connect(self.consoleEmulator.show)
        try:
            self.menu_bar.undo_edit_action.triggered.connect(self.tabEditor.currentWidget().undo)
            self.menu_bar.redo_edit_action.triggered.connect(self.tabEditor.currentWidget().redo)
            self.menu_bar.cut_edit_action.triggered.connect(self.tabEditor.currentWidget().cut)
            self.menu_bar.copy_edit_action.triggered.connect(self.tabEditor.currentWidget().copy)
            self.menu_bar.paste_edit_action.triggered.connect(self.tabEditor.currentWidget().paste)
            self.menu_bar.select_all_edit_action.triggered.connect(self.tabEditor.currentWidget().selectAll)
        except AttributeError: pass

        try: 
            self.statusBar._setCurrentPos([str(i) for i in self.tabEditor.currentWidget().getCursorPosition()])
            self.tabEditor.currentWidget().cursorPositionChanged.connect(lambda: self.statusBar._setCurrentPos([str(i) for i in self.tabEditor.currentWidget().getCursorPosition()]))
        except AttributeError: pass

        try: 
            self.fileManager.setOpenedFile(self.tabEditor.currentWidget().getCurrentPath())
        except AttributeError: pass

        try:
            self.fileManager.selectionModel().clearSelection()
            self.fileManager.selectionModel().setCurrentIndex(self.fileManager.model.index(self.tabEditor.currentWidget().getCurrentPath()), QItemSelectionModel.Select)
        except AttributeError: pass

        for widget, index in self.tabEditor._get_editor_widgets():
            if not os.path.exists(widget.getCurrentPath()): self.tabEditor.removeTab(index)
        
        if self.tabEditor.count() == 0: self.tabEditor.addTab(WelcomePage(self), "Welcome")

    def create_menu_bar(self):
        self.menu_bar = MenuBar(self)
        self.mainLayout.setMenuBar(self.menu_bar)
    
    def setup_ui(self):
        # tab widget setup
        self.tabEditor = TabEditorArea(self)
        self.tabEditor.currentChanged.connect(self._update)

        # console set up
        self.consoleEmulator = ConsoleEmulator()

        # file manager set up
        self.fileManager = FileManager()
        self.fileManager.clicked.connect(lambda index: self._open_file_editor(self.fileManager._get_path(index)))
        self.fileManager.setUpdateFunction(self._update)

        # side bar set up
        self.statusBar = StatusBar(self)

        # thread pool set up
        self.thread_pool = QThreadPool()

        # add Widgets to layouts
        self.codeLayout.addWidget(self.fileManager, stretch=4)
        self.codeLayout.addWidget(self.tabEditor, stretch=9)
        self.sideBarLayout.addWidget(self.statusBar)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.consoleEmulator.destroy()
        try: self.inputFileName.destroy()
        except AttributeError: pass
        
        super().closeEvent(event)
    
    def _open_file(self):
        if self.fileManager._open_file() != None: self._open_file_editor(self.fileManager._open_file())
    
    def _open_file_editor(self, __path: str):
        if os.path.isfile(__path):
            try:
                with open(__path, "r", encoding="utf-8") as file:
                    code = file.read()
                
                self.fileManager.setOpenedFile(__path)
                self.tabEditor._add_editor(__path.split("/")[-1], code, __path)
                self.tabEditor.setCurrentIndex(self.tabEditor._get_index_by_full_path(__path))
                
                self._update()
            
            except Exception as e:
                print(f"Unknown file. {e}")
    
    def _save_file(self):
        if self.fileManager.getOpenedFile() == None: return

        with open(self.fileManager.getOpenedFile(), "w", encoding="utf-8") as file:
            file.write(self.tabEditor.currentWidget().toPlainText())
    
    def _open_input_newfile_dialog(self):
        self.inputFileName = AskInputFileName(self, "Enter the path for the new file")
        self.inputFileName.show()

        self.inputFileName.buttons.accepted.connect(lambda: self._create_new_file(self.inputFileName.getFileName()))
    
    def _open_input_newfolder_dialog(self):
        self.inputFileName = AskInputFileName(self, "Enter the path for the new folder")
        self.inputFileName.show()

        self.inputFileName.buttons.accepted.connect(lambda: self.fileManager._create_folder(f"{self.fileManager._get_directory()}/{self.inputFileName.getFileName()}"))
    
    def _create_new_file(self, __filename: str) -> None:
        if __filename == "" or __filename[:__filename.find(".")] == "": return 
        
        filename = f"{self.fileManager._get_directory()}/{__filename}"
        
        self.fileManager._create_file(filename)
        self.fileManager._open_file(filename)
        self._open_file_editor(filename)
    
    def _run_python_file(self):
        self._save_file()

        if self.fileManager.getOpenedFile() != None and self.fileManager.getOpenedFile().split(".")[-1] == "py":
            dir_ = self.fileManager._get_directory()
            path_ = self.fileManager.getOpenedFile()[self.fileManager.getOpenedFile().find(dir_) + len(dir_) + 1:]
            
            console = ConsoleRunWorker(dir_, path_)
            self.thread_pool.start(console._run_python_file)
    
    def _run_console(self):
        self._save_file()

        if self.fileManager.getOpenedFile() != None and self.fileManager.getOpenedFile().split(".")[-1] == "py":
            dir_ = self.fileManager._get_directory()
            path_ = self.fileManager.getOpenedFile()[self.fileManager.getOpenedFile().find(dir_) + len(dir_) + 1:]

            self.thread_pool.start(lambda: self.consoleEmulator._run_command(f"cd {dir_} && python {path_}"))
            self.consoleEmulator.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wid = MainWidget()
    wid.show()

    sys.exit(app.exec())