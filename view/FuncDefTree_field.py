import sys
sys.path.append(r'E:/Github_repo/new-review-way-of-C-srcs/features')
from parser_csource import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QTreeWidget,QWidget,QTreeWidgetItem,\
                            QPlainTextEdit,QHBoxLayout,QVBoxLayout,QSizePolicy
from PyQt5.QtCore import QObject,pyqtSignal
from CodeText_Field import *

class TreeWidgetSignal(QObject):
    jump_signal = pyqtSignal(int)
    verify_signal = pyqtSignal(str)

jumpSignal = TreeWidgetSignal()

class create_Tree_field(QTreeWidget):

    def __init__(self, FuncDef_list : list):
        super().__init__()
        #self.funcDef_list = FuncDef_list
        self.funcDef_list = {}
        # 列表转换为字典形式
        for funcInfo in FuncDef_list:
            (key, val), = funcInfo.items()
            self.funcDef_list[key] = val

        self.setColumnCount(1)
        # 设置属性控件的头部标题
        self.setHeaderLabel('符号列表')
        for funcInfo in FuncDef_list:
            (funcname, coord), = funcInfo.items()
            node = QTreeWidgetItem()
            node.setText(0,funcname)
            self.addTopLevelItem(node)

        #self.setMinimumSize(130,600)
        self.setFixedWidth(150)

        self.clicked.connect(self.send_jump_signal)
        self.doubleClicked.connect(self.send_verify_signal)
        # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        # self.setSizePolicy(sizePolicy)
        # tree_field = QTreeWidget(self)
        # #设置列
        # tree_field.setColumnCount(1)
        # # 设置属性控件的头部标题
        # tree_field.setHeaderLabel('函数列表')

        # # 设置根节点
        # for funcInfo in self.funcDef_list:
        #     (funcname, coord), = funcInfo.items()
        #     node = QTreeWidgetItem()
        #     node.setText(0,funcname)
        #     tree_field.addTopLevelItem(node)
        
        # layoutV = QVBoxLayout()
        # layoutV.addWidget(tree)

    # 点击每个函数声明 可以跳转到行号
    def send_jump_signal(self):
        # print('reserve function ! ')
        # print('To be continue ! ')
        curItem = self.currentItem()
        treeName = curItem.text(0)
        #print(treeName)
        symbol_coord = int(self.funcDef_list[treeName])
        # for funcInfo in self.funcDef_list:
        jumpSignal.jump_signal.emit(symbol_coord)
    
    # 双击验证事件
    def send_verify_signal(self):
        curItem = self.currentItem()
        treeName = curItem.text(0)
        jumpSignal.verify_signal.emit(treeName)
        


# if __name__ == '__main__':
#     filename = 'E:/Github_repo/new-review-way-of-C-srcs/dependencies/pycparser-master/examples/c_files/year.c'
#     visitor = FuncDefVisitor(filename)
#     funcdef = visitor.return_FuncDefInfoList()

#     app = QApplication(sys.argv)

#     window = QMainWindow()
#     qw = QWidget()
#     text = QPlainTextEdit()
#     tree = create_Tree_field(funcdef)
#     layout = QHBoxLayout()
#     layout.addWidget(tree)
#     layout.addWidget(text)
#     qw.setLayout(layout)
#     window.setCentralWidget(qw)
#     window.show()

#     sys.exit(app.exec_())

        

