from scripts.vector import Vec2
from scripts.load import load_settings


WINDOW_SIZE = Vec2(1200, 820)

data = load_settings("source/gui/settings/settings.json")
theme = load_settings("source/gui/themes/pyPad_theme.json")

python_dictionary = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 
    'while', 'with', 'yield', 'map', 'print', 'filter', 'zip', 'enumerate',
    'range', 'slice', 'str', 'int', 'float', 'dict', 'set', 'list', 'tuple', 'iter', 'any',
    'all', 'reversed', 'repr', 'round', 'id', 'input', 'object', 'ord', 'chr', 'open', 'oct',
    'abs', 'sum', 'sorted', 'super', 'dir', 'divmod', 'format', 'help', 'hex', 'len', 'case'
]

