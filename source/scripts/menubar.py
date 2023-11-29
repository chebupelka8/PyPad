from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction
from scripts.load import load_style


class MenuBar(QMenuBar):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setStyleSheet(load_style("source/gui/style/menubar.css"))

        # create "File" menu
        self.file_menu = QMenu("File", self)
        self.file_menu.setObjectName("file-menu")
        self.addMenu(self.file_menu)

        # create "New File" action
        self.new_file_action = QAction("New File", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.file_menu.addAction(self.new_file_action)

        # create  "New Folder" action
        self.new_folder_action = QAction("New Folder", self)
        # self.new_folder_action.setShortcut("Ctrl+Shift+N")
        self.file_menu.addAction(self.new_folder_action)
        self.file_menu.addSeparator()
        
        # create "Open File" action
        self.open_file_action = QAction("Open File", self)
        self.open_file_action.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.open_file_action)

        # create "Open Folder" action
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.setShortcut("Ctrl+K")
        self.file_menu.addAction(self.open_folder_action)
        self.file_menu.addSeparator()

        # create "Save File" action
        self.save_file_action = QAction("Save File", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.file_menu.addAction(self.save_file_action)


        # create "Edit" menu
        self.edit_menu = QMenu("Edit", self)
        self.addMenu(self.edit_menu)

        # create "Undo" action
        self.undo_edit_action = QAction("Undo", self)
        self.undo_edit_action.setShortcut("Ctrl+Z")
        self.edit_menu.addAction(self.undo_edit_action)

        # create "Redo" action
        self.redo_edit_action = QAction("Redo", self)
        self.redo_edit_action.setShortcut("Ctrl+Y")
        self.edit_menu.addAction(self.redo_edit_action)
        self.edit_menu.addSeparator()

        # create "Copy", "Paste", "Cut" and "Delete" action
        self.cut_edit_action = QAction("Cut", self)
        self.cut_edit_action.setShortcut("Ctrl+X")
        self.copy_edit_action = QAction("Copy", self)
        self.copy_edit_action.setShortcut("Ctrl+C")
        self.paste_edit_action = QAction("Paste", self)
        self.paste_edit_action.setShortcut("Ctrl+V")
        self.delete_edit_action = QAction("Delete", self)
        self.edit_menu.addActions([
            self.cut_edit_action, self.copy_edit_action, 
            self.paste_edit_action, self.delete_edit_action
        ])
        self.edit_menu.addSeparator()

        # create "Select All" action
        self.select_all_edit_action = QAction("Select All", self)
        self.select_all_edit_action.setShortcut("Ctrl+A")
        self.edit_menu.addAction(self.select_all_edit_action)
        

        # create "View" menu
        self.view_menu = QMenu("View", self)
        self.addMenu(self.view_menu)

        # create "Palette" action
        self.palette_view_action = QAction("Palette", self)
        self.view_menu.addAction(self.palette_view_action)


        # create "Settings" menu
        self.settings_menu = QMenu("Settings", self)
        self.addMenu(self.settings_menu)

        # create "Open Settings" action
        self.open_settings_menu_action = QAction("Open Settings", self)
        self.settings_menu.addAction(self.open_settings_menu_action)

        # create "Console" menu
        self.console_menu = QMenu("Console", self)
        self.addMenu(self.console_menu)

        # create "Launch Console" action
        self.launch_console = QAction("Launch Console", self)
        self.console_menu.addAction(self.launch_console)
        
        # create "Run" menu
        self.run_menu = QMenu("Run", self)
        self.addMenu(self.run_menu)

        # create "Run File" action
        self.run_file_action = QAction("Run File", self)
        self.run_menu.addAction(self.run_file_action)

        # create "Run In Console" action
        self.run_in_console_action = QAction("Run In Console", self)
        self.run_menu.addAction(self.run_in_console_action)