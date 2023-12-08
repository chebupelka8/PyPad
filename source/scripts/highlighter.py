from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
import re
from scripts.constants import theme


def set_text_char_format(form: str):
    data = theme["workbench.colorCustomization"]["editor.syntaxHighlighterCustomization"][form]

    format_ = QTextCharFormat()
    format_.setForeground(QColor(data["color"]))
    format_.setFontItalic(data["font"]["italic"])
    format_.setFontUnderline(data["font"]["underline"])
    if data["font"]["bold"]: format_.setFontWeight(QFont.Bold)
    
    return format_


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent.document())
        
        self.parent = parent

        self.keyword_format = set_text_char_format("-keywords")
        self.function_format = set_text_char_format("-functions")
        self.logical_format = set_text_char_format("-logical")
        self.string_format = set_text_char_format("-string")
        self.special_format = set_text_char_format("@self")
        self.decorator_format = set_text_char_format("-decorator")
        self.data_types_format = set_text_char_format("-types")
        self.brackets_format = set_text_char_format("-brackets")
        self.comments_format = set_text_char_format("-comment")
        self.symbols_format = set_text_char_format("-symbols")
        self.numbers_format = set_text_char_format("-numbers")
        self.classes_format = set_text_char_format("-classes")
        self.defindfunc_format = set_text_char_format("-defindfunc")

        self.syntax_words = []

    def highlightBlock(self, text):

        self.plainText = self.parent.toPlainText()
        # print("************\n" + self.plainText + "\n************")
        self._highlight_match(r"^\s*class .*", self.classes_format, text)
        self._highlight_match(r"^\s*def \w*\(.*\).*:", self.defindfunc_format, text)
        self._highlight_match(r"\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|case)\b", self.keyword_format, text)
        self._highlight_match(r"\b(divmod|map|filter|zip|super|open|help|hex|abs|eval|exec|ord|chr|sorted|reversed|enumerate|range|sum|repr|round|type|all|any)\b", self.function_format, text)
        self._highlight_match(r"\b(True|False|None)\b", self.logical_format, text)
        self._highlight_match(r"\b(int|float|str|dict|set|tuple|list|bool)\b", self.data_types_format, text)
        self._highlight_match(r"\(|\)|\[|\]|\{|\}", self.brackets_format, text)
        self._highlight_match(r"\b(self)\b", self.special_format, text)
        self._highlight_match(r"1|2|3|4|5|6|7|8|9|0", self.numbers_format, text)
        self._highlight_match(r"\=|\+|\-|\>|\&|\<|\%|\/|\*", self.symbols_format, text)
        self._highlight_match(r'@.*$', self.decorator_format, text)
        self._highlight_match(r'#.*$', self.comments_format, text)
        self._highlight_match(r'".*?\n*?"|".*?', self.string_format, text)
        self._highlight_match(r"'.*?'|'.*?", self.string_format, text)
        self._highlight_match(r'""".*?"""|""".*?', self.string_format, text)

        if self.syntax_words != []: self.window_hint._update_list(self.syntax_words)
    
    def _highlight_match(self, pattern, _format, text):
        for match in re.finditer(pattern, text):
            # if "def" in match.group() and "(" in match.group() and 1 == 0:
            #     txt = match.group()
            #     start, end = match.start(), len(txt[:txt.find("(")]) - match.start()
            #     self.setFormat(start, end, format)
                
            #     txt = txt.split()[1]
            #     if [txt[:txt.find("(")] + "()", "func"] not in self.syntax_words:
            #         self.syntax_words.append([txt[:txt.find("(")] + "()", "func"])
        
            
            txt = match.group()

            if "def" in txt and "(" in txt:
                start = match.start() + 4
                count = len(txt[4:txt.find("(")])
                # print(count)
            
            elif "class" in txt and ":" in txt:
                start = match.start() + 6
                if txt.find("(") != -1: count = len(txt[6:txt.find("(")])
                else: count = len(txt[6:txt.find(":")])

            # elif "0" in txt or "1" in txt or "2" in txt or "3" in txt or "4" in txt or "5" in txt or "6" in txt or "7" in txt or "8" in txt or "9" in txt:
            #     # print(txt[match.start() - 1])
            #     try:
            #         # print(self.plainText)
            #         # pass
            #         lines = self.plainText.split("\n")
            #         for i in range(len(lines)):
            #             if lines[i][match.start() - 1].isalpha():
            #                 return
                
            #         # if txt[match.start() - 1].isalpha():
            #         #     continue
            #     except:
            #         pass
                
            #     # lines = self.plainText.split("\n")
            #     # for i in len(lines):
            #     #     if lines[i][match.start() - 1].isalpha():
            #     #         return

            #     # print(list(re.finditer(r"0|1|2|3|4|5|6|7|8|9", txt)))
            #     start = match.start()
            #     count = match.end() - match.start()
                # print(txt.find("9"))
                
                # if txt.find("(")    count = len(txt[6:txt.find]) 

                # print(start, count, match.end())
            
            
            
            else:
                start = match.start()
                count = match.end() - match.start()
            
            # print(list(re.finditer(r"^\w*(.*)$", txt)))
            self.setFormat(start, count, _format)
        
        # if self.syntax_words != []: print(self.syntax_words) # get info
        # self.syntax_words.clear()