from PySide6.QtCore import QRunnable
import os


class ConsoleRunWorker(QRunnable):
    def __init__(self, __dir, __path) -> None:
        self.directory = __dir
        self.path = __path

    def _run_python_file(self):
        os.system(f"cd {self.directory} && python {self.path}")