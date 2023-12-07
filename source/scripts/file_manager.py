from PySide6.QtWidgets import QTreeView, QFileSystemModel, QFileDialog, QMenu
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QAction, QCursor
from scripts.load import load_style
from scripts.input_filename import AskInputFileName
import os, pyperclip
from scripts.constants import theme


class FileManagerMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setStyleSheet(load_style("source/gui/style/menubar.css"))
        self.current_path = None

        self.setup_ui()

    def setup_ui(self):
        
        self.create_file_action = QAction("Create New File", self)
        self.addAction(self.create_file_action)

        self.create_folder_action = QAction("Create New Folder", self)
        self.addAction(self.create_folder_action)

        self.rename_file_action = QAction("Rename File", self)
        self.delete_file_action = QAction("Delete", self)
        self.copy_path_action = QAction("Copy Path", self)
        self.copy_relative_path_action = QAction("Copy Relative Path", self)

        if self.current_path != "" and self.current_path != None:

            self.addSeparator()

            self.addAction(self.rename_file_action)
            self.addAction(self.delete_file_action)

            self.addSeparator()
            
            self.addAction(self.copy_path_action)
            self.addAction(self.copy_relative_path_action)
    
    def _get_current_path(self, check: bool = False) -> str:
        if check: return self.current_path if not os.path.isfile(self.current_path) else "/".join(self.current_path.split("/")[:-1])
        else: return self.current_path

    def _set_current_path(self, __new_path: str) -> None:
        self.current_path = __new_path


class FileManager(QTreeView):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/file_manager.css") + "QTreeView {" + f"background-color: {theme["workbench.colorCustomization"]["file-manager"]["background-color"]}" + "}")
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        self.setRootIndex(self.model.index(""))
        self.setHeaderHidden(True)
        
        self.fileMenu = FileManagerMenu(self)
        # self.trigger_file_menu()

        for i in range(1, 4): self.header().setSectionHidden(i, True)

        # variables
        self.opened_file = None
        self.update_function = lambda: None
    
    def setOpenedFile(self, __path: str) -> None:
        self.opened_file = __path
    
    def getOpenedFile(self) -> str:
        return self.opened_file

    def setUpdateFunction(self, func: object) -> None:
        self.update_function = func
    
    def trigger_file_menu(self, index):
        self.fileMenu.rename_file_action.triggered.connect(lambda: self._rename_file(self.fileMenu._get_current_path()))
        self.fileMenu.delete_file_action.triggered.connect(lambda: self.model.remove(index))
        self.fileMenu.copy_path_action.triggered.connect(lambda: self._copy_path(self.fileMenu._get_current_path()))
        self.fileMenu.copy_relative_path_action.triggered.connect(lambda: self._copy_path(self.fileMenu._get_current_path(), relative=True))
        self.fileMenu.create_file_action.triggered.connect(self._ask_create_file)
        self.fileMenu.create_folder_action.triggered.connect(self._ask_create_folder)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            # self.openPersistentEditor(self.indexAt(event.pos()))
            self.fileMenu.clear()
            
            self.fileMenu._set_current_path(self._get_path(self.indexAt(event.pos())))
            self.fileMenu.setup_ui()
            self.trigger_file_menu(self.indexAt(event.pos()))
            if len(self._get_path(self.indexAt(event.pos()))) == 0: self.fileMenu._set_current_path(self._get_directory())
            
            self.fileMenu.move(QCursor.pos())
            self.fileMenu.show()
    
    def _get_path(self, index) -> str:
        path = self.model.filePath(index)

        return path

    def _get_directory(self) -> str:
        path = self.model.rootPath()
        
        return path

    def _rename_file(self, __path: str, new_filename: str = None) -> None:
        if __path == "" or __path == None: return
        
        if new_filename != "" and new_filename != None: os.rename(__path, new_filename)
        else:
            self.inputName = AskInputFileName(self, "Enter path for rename the file", __path.split("/")[-1])
            self.inputName.show()

            self.inputName.buttons.accepted.connect(lambda: os.rename(__path, f"{"/".join(__path.split("/")[:-1])}/{self.inputName.getFileName()}"))
            self.inputName.buttons.accepted.connect(lambda: self.setOpenedFile(f"{"/".join(__path.split("/")[:-1])}/{self.inputName.getFileName()}")) # see up
            self.inputName.buttons.accepted.connect(self.update_function)

        self.update_function()
    
    def _delete_file(self, __path: str) -> None:
        if __path == "" or __path == None: return

        os.remove(__path)

        self.update_function()
    
    def _copy_path(self, __path: str, relative: bool = False) -> None:
        if __path == "" or __path == None: return

        if not relative: pyperclip.copy(__path)
        else: pyperclip.copy(__path[__path.find(self._get_directory()) + len(self._get_directory()) + 1:])
    
    def _open_folder(self, __path: str = None) -> None | str:
        if __path == None or not isinstance(__path, str): __path = QFileDialog.getExistingDirectory()
        if __path == "": return

        self.model.setRootPath(__path)
        self.setRootIndex(self.model.index(__path))

        return __path if __path != "" else None
    
    def _open_file(self, __path_to_file: str) -> None | str:
        if __path_to_file == None or not isinstance(__path_to_file, str): __path_to_file = QFileDialog.getOpenFileName()[0]
        if __path_to_file == "": return

        __path = "/".join(__path_to_file.split("/")[:-1])
        self._open_folder(__path)

        self.selectionModel().clearSelection()
        self.selectionModel().select(self.model.index(__path_to_file), QItemSelectionModel.Select) # select opened file

        return __path_to_file if __path_to_file != "" else None
    
    def _create_file(self, __filename: str = None) -> None:
        if __filename == None or __filename == "": return

        with open(__filename, "w", encoding="utf-8") as file:
            file.write("")
        
    def _create_folder(self, __foldername: str = None) -> None:
        if __foldername == "" or __foldername == None: return

        os.mkdir(__foldername)
    
    def _open_dialog(self, title: str, placed_text: str, *accept_commands):
        self.inputFileName = AskInputFileName(self, title, placed_text)
        self.inputFileName.show()

        for com in accept_commands: self.inputFileName.buttons.accepted.connect(com)
    
    def _ask_create_file(self):
        self.inputFileName = AskInputFileName(self, "Enter path for the new file")
        self.inputFileName.show()

        self.inputFileName.buttons.accepted.connect(lambda: self._create_file(f"{self.fileMenu._get_current_path(True)}/{self.inputFileName.getFileName()}"))
    
    def _ask_create_folder(self):
        self.inputFileName = AskInputFileName(self, "Enter path for the new folder")
        self.inputFileName.show()

        self.inputFileName.buttons.accepted.connect(lambda: self._create_folder(f"{self.fileMenu._get_current_path(True)}/{self.inputFileName.getFileName()}"))