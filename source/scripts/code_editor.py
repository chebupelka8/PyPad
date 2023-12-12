from PySide6.QtWidgets import (
    QPlainTextEdit, QTextEdit
)
from PySide6.QtGui import (
    QFontMetrics, QFont, QColor, 
    QTextFormat, QTextCursor, QKeyEvent, QCursor
)
from PySide6.QtCore import Qt
from scripts.highlighter import Highlighter
from scripts.constants import data, theme
from scripts.window_hint import WindowHint


class CodeEditorArea(QPlainTextEdit):
    def __init__(self, parent):
        super(CodeEditorArea, self).__init__(parent)
        
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        self._highlightCurrentLine()
        self._updateCursorWidth()
        if data["workbench.settingsCustomization"]["editor.cursorStyle"] == "block":
            self.cursorPositionChanged.connect(self._highlightCurrentLine)
            self.cursorPositionChanged.connect(self._updateCursorWidth)
        else:
            self.setCursorWidth(1)
        self.cursorPositionChanged.connect(self._updateCurrentLine)
        self.verticalScrollBar().valueChanged.connect(self._show_hints)
        
        Highlighter(self) # set syntax highlitning

        self.setStyleSheet(
            f"""
            font-size: {data["workbench.settingsCustomization"]["editor.fontSize"]}px;
            color: {theme["workbench.colorCustomization"]["editor.syntaxHighlighterCustomization"]["-default"]["color"]};
            background-color: {theme["workbench.colorCustomization"]["editor"]["background-color"]};
            font-family: '{data["workbench.settingsCustomization"]["editor.fontFamily"]}';
            """
        )
        self.setTabStopDistance(
            QFontMetrics(QFont(data["workbench.settingsCustomization"]["editor.fontFamily"], int(data["workbench.settingsCustomization"]["editor.fontSize"]))).horizontalAdvance('    ') - 15
        )

        self.windowHint = WindowHint(self)
        self.windowHint.show()
        self.windowHint.setVisible(False)
        self.textChanged.connect(self._show_hints)

        # variables 
        self.currentLine = None
        self.currentPath = None
    
    def setCurrentPath(self, __path: str) -> None:
        self.currentPath = __path
    
    def getCurrentPath(self) -> str:
        return self.currentPath
    
    def _append_hint(self, index):
        word = self.windowHint.listWidget.itemFromIndex(index).text()

        cursor_position = self.textCursor().position() # save cursor position before insert
        last_word = self._find_last_word()
        
        text = self.toPlainText().split("\n")
        text_line = text[self.currentLine]
        before_last = text_line[:self.textCursor().positionInBlock()].rfind(last_word)
        text[self.currentLine] = text_line[:before_last] + word + text_line[self.textCursor().positionInBlock() + len(last_word):]
        
        self.setPlainText("\n".join(text))

        # keep cursor position
        cursor = self.textCursor()
        cursor.setPosition(cursor_position + len(word) - len(last_word))
        self.setTextCursor(cursor)

        self.windowHint.setVisible(False)
        self.setFocus()
    
    def _show_hints(self):
        try: self.windowHint.listWidget._set_hints(self.windowHint._find_matches(self._find_last_word()))
        except TypeError: return
        
        if self.windowHint.listWidget._get_count_hints() == 0: 
            self.windowHint.setVisible(False)
            self.setFocus()
        else: 
            self.windowHint.setVisible(True)
            self.windowHint.move(self.cursorRect().x(), self.cursorRect().y() + self.font().pixelSize())
    
    def _find_last_word(self) -> str:
        cursor = self.textCursor()
        try: 
            dt = self.toPlainText().split("\n")[self.currentLine][:cursor.positionInBlock()].split(" ")[-1].split(".")[-1]
            for char in "()[]{}": dt = dt.strip(char)
            return dt
        
        except IndexError: pass 
    
    def _highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly() and self.hasFocus():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(theme["workbench.colorCustomization"]["editor"]["current-line-color"])

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
            try: return 1 if string.rstrip()[-1] == ":" else 0
            except: return 0

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
            if not self.windowHint.isVisible() and not self.windowHint.hasFocus():
                previous = self.toPlainText().split("\n")[cursor.blockNumber()]
                
                if previous == "": prev = "//none" # it's need for remove exception - list has no index -1
                elif not previous.isspace() and previous.replace(" ", "") != "": 
                    try: 
                        prev = previous[:cursor.positionInBlock()].rstrip()
                        prev[-1]
                    except IndexError: prev = "//none"
                else: prev = previous
                
                if prev[-1] == ":" or self.toPlainText().split("\n")[cursor.blockNumber()][:4] == "    ":
                    tab_count = _find_tabs(previous) + _find_colons(prev)
                    cursor.insertText("\n" + ("    " * tab_count))
                else:
                    super().keyPressEvent(event)
            else:
                try:
                    self._append_hint(*self.windowHint.listWidget.selectedIndexes())
                except TypeError:
                    return
        
        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            if self.windowHint.isVisible():
                self.windowHint.listWidget.setFocus()
                self.windowHint.listWidget.selectFirstItem()
            else:
                super().keyPressEvent(event)
        
        elif event.key() == Qt.Key.Key_Escape and self.windowHint.isVisible():
            self.windowHint.setVisible(False)
            self.setFocus()
        
        else:
            super().keyPressEvent(event)