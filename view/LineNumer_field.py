import sys
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QWidget,\
                            QVBoxLayout, QMainWindow,QHBoxLayout

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRect ,Qt
class LineNumber_field(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.LineNumberBarColor = QColor("#85929E")
        self.HighlightColor = QColor('#00FF04')

        # blockCountChanged 为行数变化时调用
        self.editor.blockCountChanged.connect(self.update_width)
        # 窗口滚动时调用，用来更新viewport
        self.editor.updateRequest.connect(self.update_on_scroll)

        # 编辑器刚被创建时，更新行号
        self.update_width('1')
    
    # 一旦窗口被 缩小，出现滚动条时，触发
    def update_on_scroll(self, rect, scroll_pixels):
        # 如果存在垂直滚动, scroll记录了每一次移动的pixels
        # scroll方法将移动 想上或下滚动的pixels
        # 向上滚动时 pixel是正数， 向下滚动时pixel时负数
        # 如果滚动停了，那么更新viewport的内容
        if scroll_pixels:
            self.scroll(0, scroll_pixels)
        else:
            self.update()
    
    # 根据字体长度动态的改变行号的宽度
    def update_width(self, string):
        # fontMetrics 获取字体的宽度
        width = self.fontMetrics().width(str(string)) + 10

        if self.width() != width:
            #self.editor.setViewportMargins(width,0,0,0)
            self.setFixedWidth(width)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # 填充 lineNumberBar 区域的颜色 ，看着更加醒目
        painter.fillRect(event.rect(), self.LineNumberBarColor)
        
        # 获取第一个 文本行
        block = self.editor.firstVisibleBlock()
        # 获取行号
        blockNum = block.blockNumber()
        
        # 获取 即将填充数字的 边界，
        # 这里通过block 的左上角的y坐标 决定数字的y坐标
        # top() 方法是QRectF 的方法，相当于 y() 
        block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        # 获取底部y坐标主要是为了下面做边界判断使用，确保填充的区域正确，合理
        block_bottom = block_top + self.editor.blockBoundingRect(block).height()
        # PaintRect_dy = block_top

        # 用于 当前行号 格式加粗
        font = painter.font()
        while block.isValid() and block_top <= event.rect().bottom():
            
            if block.isVisible() and block_bottom >= event.rect().top():

                # 通过TextCursor方法获取当前光标所在位置，和blockNum比较    
                if blockNum == self.editor.textCursor().block().blockNumber():
                    font.setBold(True)
                else:
                    font.setBold(False)
                
                painter.setFont(font)
                #用 painter.drawText方法画出 数字,数字要加1 
                Paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
                painter.drawText(Paint_rect, Qt.AlignRight, str(blockNum+1))
            
            # 下一行, 如果需要的话
            block = block.next()
            blockNum += 1

            # 下一行 需要重新找到边界
            block_top = block_bottom
            block_bottom = block_top + self.editor.blockBoundingRect(block).height()
            

# test ==========================================

# class Window(QMainWindow):

#     def __init__(self):
#         super().__init__()

#         self.editor = QPlainTextEdit()
#         self.NumberBar = LineNumber_field(self.editor)

#         layoutH = QHBoxLayout()
#         layoutH.addWidget(self.NumberBar)
#         layoutH.addWidget(self.editor)

#         mainQWiget = QWidget(self)
#         mainQWiget.setLayout(layoutH)

#         self.setCentralWidget(mainQWiget)

# if __name__ == '__main__':

#     app = QApplication(sys.argv)

#     win = Window()
#     win.show()

#     sys.exit(app.exec_())