import sys

from PyQt5.QtWidgets import QPlainTextEdit,QWidget

from PyQt5.QtGui import QColor,QTextFormat, QTextCursor,QCursor

class create_TextArea(QPlainTextEdit):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600,600)
    
    def jump_to_line(self, coord):
        print("stream echo : jump to line")
        doc = self.document()
        # 光标显示在文本区
        self.setFocus()
        cursor = QTextCursor(doc.findBlockByLineNumber(coord+1))
        self.setTextCursor(cursor)