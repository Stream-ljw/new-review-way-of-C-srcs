import sys

from PyQt5.QtWidgets import QWidget ,QLabel, QLineEdit,QPushButton,QVBoxLayout, QHBoxLayout,QSizePolicy,QApplication

from PyQt5.QtCore import QObject,pyqtSignal
# 前置条件和后置条件输入框 ，本质上是显示 FuncVerify_dict
# 点击 确定 按钮将改动写入 FuncVerify_dict， 并且调用程序验证, 并关闭窗口

class finished_signal(QObject):
    finished = pyqtSignal(list)

signal = finished_signal()

class inputDialog(QWidget):

    def __init__(self, condition):
        super().__init__()
        print('init...')
        if len(condition) == 0:
            self.condition = ['','']
        else:
            self.condition = condition

        self.initUI()
        self.show()
    
    def initUI(self):
        print('initUI...')
        self.setMinimumSize(350,100)
        
        self.setWindowTitle('输入条件')
        # 创建窗口中的控件
        self.Pre_label = QLabel('Pre-Condition:')
        self.Pre_inputLine = QLineEdit()
        self.Pre_inputLine.setText(self.condition[0])

        prelabel_layoutH = QHBoxLayout()
        prelabel_layoutH.addWidget(self.Pre_label)
        prelabel_layoutH.addWidget(self.Pre_inputLine)

        self.Post_label = QLabel('Post-Condition:')
        self.Post_inputLine = QLineEdit()
        self.Post_inputLine.setText(self.condition[1])

        postlabel_layoutH = QHBoxLayout()
        postlabel_layoutH.addWidget(self.Post_label)
        postlabel_layoutH.addWidget(self.Post_inputLine)

        self.confirmBtn = QPushButton('OK')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.confirmBtn.setSizePolicy(sizePolicy)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.confirmBtn)

        self.confirmBtn.clicked.connect(self.clickBtn)
        # 调整位置
       
        layoutV = QVBoxLayout()
        layoutV.addLayout(prelabel_layoutH)
        layoutV.addLayout(postlabel_layoutH)
        layoutV.addLayout(layoutH)

        self.setLayout(layoutV)
        print('endUI...')

    def clickBtn(self):

        # 将文本内容写入 self.conditon
        pre_text = self.Pre_inputLine.text()
        if pre_text != self.condition[0]:
            self.condition[0] = pre_text
        post_text = self.Post_inputLine.text()
        if post_text != self.condition[1]:
            self.condition[1] = post_text
        
        # 调用程序验证接口
        print(self.condition)

        # 关闭窗口
        self.close()

        signal.finished.emit(self.condition)

    def return_condition(self):
        return self.condition


        
# if __name__ == '__main__':

#     app = QApplication(sys.argv)

#     ex = inputDialog(['pre','post'])

#     ex.show()

#     sys.exit(app.exec_())

    



        


