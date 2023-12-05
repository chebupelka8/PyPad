from scripts.vector import Vec2
from scripts.load import load_settings


WINDOW_SIZE = Vec2(1200, 820)

data = load_settings("source/gui/settings/settings.json")
theme = load_settings("source/gui/themes/pyPad_theme.json")

keywords = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 
    'while', 'with', 'yield',
]