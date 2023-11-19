from scripts.vector import Vec2
from scripts.load import load_settings


WINDOW_SIZE = Vec2(1200, 820)

data = load_settings("source/gui/settings/settings.json")
theme = load_settings("source/gui/themes/pyPad_theme.json")