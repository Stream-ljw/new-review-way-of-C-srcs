import sys

from PyQt5.QtWidgets import QPlainTextEdit,QWidget

from PyQt5.QtGui import QColor,QTextFormat, QTextCursor,QCursor,QFont
from FuncDefTree_field import *

class create_TextArea(QPlainTextEdit):

    def __init__(self, funcBodyList):
        super().__init__()
        self.funcBody_list = funcBodyList
        self.setMinimumSize(600,600)
        self.setFont(QFont('Consolas', 10))

        # jumpSignal.jump_signal.connect(self.jump_to_line)
    
    def jump_to_line(self, coord):
        print("jump to ",coord-1)
        doc = self.document()
        # 光标显示在文本区
        self.setFocus()
        cursor = QTextCursor(doc.findBlockByLineNumber(coord-1))
        self.setTextCursor(cursor)
    
    def getSpecificContent(self, CoordList):
        content1 = ''
        # content2 = ''
        # content3 = ''
        doc = self.document()
        for lineNum in range(CoordList[0],CoordList[1]):
            content1 += doc.findBlockByLineNumber(lineNum).text()
            # content2 += doc.findBlock(lineNum).text()
            # content3 += doc.findBlockByNumber(lineNum).text()
        return content1
        #print('content',content1)

        #print('findBlockByLineNumber: ', doc.findBlockByNumber(1).text())