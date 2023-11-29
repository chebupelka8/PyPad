from PySide6.QtWidgets import (
    QPlainTextEdit, QTextEdit
)
from PySide6.QtGui import (
    QFontMetrics, QFont, QColor, 
    QTextFormat, QTextCursor, QKeyEvent
)
from PySide6.QtCore import Qt
from scripts.highlighter import Highlighter
from scripts.constants import data, theme


class CodeEditorArea(QPlainTextEdit):
    def __init__(self, parent):
        super(CodeEditorArea, self).__init__(parent)
        
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        self._highlightCurrentLine()
        self._updateCursorWidth()
        if data["workbench.settingsCustomization"]["editor.cursorStyle"] == "block":
            self.cursorPositionChanged.connect(self._highlightCurrentLine)
            self.blockCountChanged.connect(self._updateCursorWidth)
        else:
            self.setCursorWidth(1)
        self.cursorPositionChanged.connect(self._updateCurrentLine)
        
        Highlighter(self) # set syntax highlitning

        self.setStyleSheet(
            f"""
            font-size: {data["workbench.settingsCustomization"]["editor.fontSize"]}px;
            color: {theme["workbench.theme.colorCustomization"]["editor.syntaxHighlighterCustomization"]["-default"]["color"]};
            background-color: {theme["workbench.theme.colorCustomization"]["editor.background"]};
            font-family: '{data["workbench.settingsCustomization"]["editor.fontFamily"]}';
            """
        )
        self.setTabStopDistance(
            QFontMetrics(QFont(data["workbench.settingsCustomization"]["editor.fontFamily"], int(data["workbench.settingsCustomization"]["editor.fontSize"]))).horizontalAdvance('    ') - 15
        )

        # variables 
        self.currentLine = None
    
    def _highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly() and self.hasFocus():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor("#1A1A1A").lighter(180)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)
    
    def _updateCursorWidth(self):
        cursor = self.textCursor()
        
        try:
            current_symbol = cursor.block().text()[cursor.positionInBlock()]
        except:
            current_symbol = " "

        self.setCursorWidth(
            QFontMetrics(QFont(data["workbench.settingsCustomization"]["editor.fontFamily"], 
            int(data["workbench.settingsCustomization"]["editor.fontSize"]))).horizontalAdvance(current_symbol) - 3
        )
    
    def _updateAutoSymbols(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
        selectedText = cursor.selectedText()
        # print(selectedText)

        def _insert(__symbols: list):
            if selectedText == __symbols[0]:
                cursor.insertText(f"{selectedText}".join(__symbols))
                cursor.setPosition(cursor.position() - 1)
                self.setTextCursor(cursor)
        
        _insert(["(", ")"])
        _insert(["[", "]"])
        _insert(["{", "}"])
        # _insert(["'", "'"])
        # _insert(['"', '"'])
    
    def _updateCurrentLine(self):
        cursor = self.textCursor()
        self.currentLine = cursor.blockNumber()
    
    def getCursorPosition(self) -> list:
        """returns list[line, column]"""
        
        cursor = self.textCursor()

        return [self.currentLine, cursor.positionInBlock()]

    def keyPressEvent(self, event):

        cursor = self.textCursor()
        selectedText = cursor.selectedText()

        def _insert(__symbols: list):
            cursor.insertText(f"{selectedText}".join(__symbols))
            cursor.setPosition(cursor.position() - 1)
            self.setTextCursor(cursor)
        
        def _double_symbol(__symbol: str):
            if len(self.toPlainText().split("\n")[self.currentLine][cursor.positionInBlock():]) != 0:
            
                if self.toPlainText().split("\n")[self.currentLine][cursor.positionInBlock()] == __symbol:
                    cursor.setPosition(cursor.position() + 1)
                    self.setTextCursor(cursor)
                
                else: raise Exception("//errror")
            
            else: raise Exception("//error")
        
        def _find_tabs(string: str) -> int:
            res = 0
            for letter in string:
                if letter == " ": res += 1
                else: break
            
            return res // 4
                
        def _find_colons(string: str) -> int:
            return 1 if string.rstrip()[-1] == ":" else 0

        if event.key() == Qt.Key.Key_ParenLeft:
            _insert(["(", ")"])
        
        elif event.key() == Qt.Key.Key_BraceLeft:
            _insert(["{", "}"])
        
        elif event.key() == Qt.Key.Key_BracketLeft:
            _insert(["[", "]"])
        
        elif event.key() == Qt.Key.Key_QuoteDbl:
            _insert(['"', '"'])
        
        elif event.key() == Qt.Key.Key_Apostrophe:
            _insert(["'", "'"])
        
        elif event.key() == Qt.Key.Key_ParenRight:
            try: _double_symbol(")")
            except: super().keyPressEvent(event)
        
        elif event.key() == Qt.Key.Key_BraceRight:
            try: _double_symbol("}")
            except: super().keyPressEvent(event)
        
        elif event.key() == Qt.Key.Key_BracketRight:
            try: _double_symbol("]")
            except: super().keyPressEvent(event)
        
        elif event.key() == Qt.Key.Key_Tab:
            cursor.insertText("    ")
        
        elif event.key() == Qt.Key.Key_Return:
        
            previous = self.toPlainText().split("\n")[cursor.blockNumber()]
            # if previous.replace(" ", "") == "": previous = "//none" # it's need for remove exception - list has no index -1
            
            if previous == "": prev = "//none" # it's need for remove exception - list has no index -1
            elif not previous.isspace(): prev = previous.rstrip()[-1]
            else: prev = previous
            
            if prev[-1] == ":" or self.toPlainText().split("\n")[cursor.blockNumber()][:4] == "    ":
                tab_count = _find_tabs(previous) + _find_colons(previous)
                cursor.insertText("\n" + ("    " * tab_count))
            else:
                super().keyPressEvent(event)
        
        else:
            super().keyPressEvent(event)