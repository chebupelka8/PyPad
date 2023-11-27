from PySide6.QtWidgets import QTreeView, QFileSystemModel, QFileDialog
from PySide6.QtCore import Qt, QItemSelectionModel
from scripts.load import load_style


class FileManager(QTreeView):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/file_manager.css"))
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
        self.setRootIndex(self.model.index(""))
        self.setHeaderHidden(True)

        for i in range(1, 4): self.header().setSectionHidden(i, True)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            pass
    
    def _get_path(self, index):
        path = self.model.filePath(index)

        return path

    def _get_directory(self):
        path = self.model.rootPath()
        
        return path
    
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
