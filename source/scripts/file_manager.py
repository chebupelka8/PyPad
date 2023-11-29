from PySide6.QtWidgets import QTreeView, QFileSystemModel, QFileDialog, QMenu
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QAction, QCursor
from scripts.load import load_style
from scripts.input_filename import AskInputFileName
import os, pyperclip


class FileManagerMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setStyleSheet(load_style("source/gui/style/menubar.css"))
        self.current_path = None

        self.setup_ui()

    def setup_ui(self, __path: str = ""):
        
        self.create_file_action = QAction("New File", self)
        self.addAction(self.create_file_action)

        self.create_folder_action = QAction("New Folder", self)
        self.addAction(self.create_folder_action)

        self.rename_file_action = QAction("Rename File", self)
        self.delete_file_action = QAction("Delete File", self)
        self.copy_path_action = QAction("Copy Path", self)
        self.copy_relative_path_action = QAction("Copy Relative Path", self)

        if __path != "":
            self.current_path = __path

            self.addSeparator()

            self.addAction(self.rename_file_action)
            self.addAction(self.delete_file_action)

            self.addSeparator()
            
            self.addAction(self.copy_path_action)
            self.addAction(self.copy_relative_path_action)
    
    def _get_current_path(self) -> str:
        return self.current_path


class FileManager(QTreeView):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/file_manager.css"))
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        self.setRootIndex(self.model.index(""))
        self.setHeaderHidden(True)

        self.fileMenu = FileManagerMenu(self)
        self.trigger_file_menu()

        for i in range(1, 4): self.header().setSectionHidden(i, True)
    
    def trigger_file_menu(self):
        self.fileMenu.rename_file_action.triggered.connect(lambda: self._rename_file(self.fileMenu._get_current_path()))
        self.fileMenu.delete_file_action.triggered.connect(lambda: self._delete_file(self.fileMenu._get_current_path()))
        self.fileMenu.copy_path_action.triggered.connect(lambda: self._copy_path(self.fileMenu._get_current_path()))
        self.fileMenu.copy_relative_path_action.triggered.connect(lambda: self._copy_path(self.fileMenu._get_current_path(), relative=True))
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            self.fileMenu.clear()
            
            self.fileMenu.setup_ui(self._get_path(self.indexAt(event.pos())))
            self.trigger_file_menu()
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
            self.inputName = AskInputFileName(self, "Enter path for rename the file")
            self.inputName.show()

            self.inputName.buttons.accepted.connect(lambda: os.rename(__path, f"{"/".join(__path.split("/")[:-1])}/{self.inputName.getFileName()}"))
    
    def _delete_file(self, __path: str) -> None:
        if __path == "" or __path == None: return

        os.remove(__path)
    
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
    
    def _open_file(self, __path_to_file: str = None) -> None | str:
        if __path_to_file == None or not isinstance(__path_to_file, str): __path_to_file = QFileDialog.getOpenFileName()[0]
        if __path_to_file == "": return

        __path = "/".join(__path_to_file.split("/")[:-1])
        self._open_folder(__path)

        self.selectionModel().clearSelection()
        self.selectionModel().select(self.model.index(__path_to_file), QItemSelectionModel.Select) # select opened file

        return __path_to_file if __path_to_file != "" else None