from PySide6.QtCore import QSize


class Vec2:
    """
    class: Vec2
        x: float
        y: float
    """

    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = float(x), float(y)
    
    @property
    def array(self) -> list:
        return [self.x, self.y]
    
    @property
    def qsize(self) -> QSize:
        return QSize(self.x, self.y)