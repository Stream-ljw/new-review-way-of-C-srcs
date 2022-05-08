import sys
import os
import threading

from nbformat import write

sys.path.append(r'E:/Github_repo/new-review-way-of-C-srcs/features')
# from pyqtgraph.flowchart import Flowchart

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog, \
                            QMessageBox, QAction,  QLineEdit, QTextEdit, QLayoutItem,QMenu,QSizePolicy
from PyQt5.QtCore import Qt, QObject, QDir, QFileInfo, QFile, QTextStream,QVariant,QUrl,pyqtSignal,pyqtSlot,QThread

from PyQt5.QtGui import QColor,QTextFormat, QTextCursor,QCursor
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import *
#from GraphicView_field import GraphicsView_field as Gf
from WebEngineView import *
from LineNumer_field import LineNumber_field as Lf
from FuncDefTree_field import create_Tree_field as Tf
from CodeText_Field import *
from InputDialog import *
from parser_csource import *


# 记录每个函数是否有前置条件和后置条件
# 该列表格式为： [{funcname: [pre-condition,post-condition]}, {funcname2:[pre,post]},{...},...]
# 该列表初次由生成FuncDef列表时生成，后续在inputDialog更新
g_funcVerify_info = {}

class Window(QMainWindow):

    def __init__(self):
        super(Window,self).__init__()

        # 在当前目录创建一个临时的隐藏文件，用于实时保存文本区内容
        # 从而实现动态生成函数调用关系图
        self.tmp_file_path = os.getcwd()+'/_tmp.c'
        if os.path.exists(self.tmp_file_path):
            os.remove(self.tmp_file_path)
        # if not os.path.exists(tmp_file_path):
        # open操作可快捷的创建一个文件，如果该文件不存在的话
        self.tmp_inVisible_file = open(self.tmp_file_path, 'w').close()
        # 设置为隐藏文件
        os.system('attrib +h ' + self.tmp_file_path)
        print(self.tmp_file_path)
        
        self.filename = ""
        self.create_Actions()
        self.create_MenuBar()

        #self.callgraph_field = create_WebEngineView_field()
        #self.callgraph_field.selectionChanged.connect(self.jump_to_line)
        self.editor = create_TextArea() 
        # self.editor.setMinimumSize(600,600)
        # sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # self.editor.setSizePolicy(sizePolicy)
        # 在文本区域调用右键菜单
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.create_rightmenu)
        self.editor.blockCountChanged.connect(self.create_callgraph) 
        # 设置行号跳转
        # self.signal = test_signal()
        # print('line42 :', self.signal.JumpToLine_signal)
        #self.signal = self.Js.JumpToLine_signal
        g_signal.JumpToLine_signal.connect(self.editor.jump_to_line)
        g_signal.inputDialog_signal.connect(self.create_inputDialog)
        self.lineNumberBar = Lf(self.editor)
        
        #1. layout control
        self.layoutH = QHBoxLayout()
        self.layoutH.addWidget(self.lineNumberBar)
        self.layoutH.addWidget(self.editor, 3)
        #self.layoutH.addWidget(self.callgraph_field)

        #fc_item = self.fc.widget()
        #layoutH.addWidget(fc_item)

        self.layoutV = QVBoxLayout()
        self.layoutV.addWidget(self.menubar_field)
        self.layoutV.addLayout(self.layoutH)

        #2.  add layout into QWidget module to show
        self.mainQWiget = QWidget(self)
        self.mainQWiget.setLayout(self.layoutV)

        #3. QMainWindow.setCentralWidget takes ownership of the widget pointer
        #and deletes it at the approparite time. 
        self.setCentralWidget(self.mainQWiget)

        # 这里有一个令我困惑的地方，感觉对python的函数生命周期理解还不到位的原因
        # 如果signal在create_inputDialog里创建，那么每次点击ok之后就会重复调用create_verify_field从而添加好几次该窗口
        # 待解决
        signal.finished.connect(self.create_verify_field)

    # 主窗口关闭
    def closeEvent(self,e):
        print("window closed")

        #前提条件是该文件是closed
        os.remove(str(self.tmp_file_path))


    
    # create submenu and add action like open file
    def create_MenuBar(self):
        
        # first level menu : file
        self.menubar_field = self.menuBar()
        self.fileMenu = self.menubar_field.addMenu('&file')
        self.fileMenu.addAction(self.newAcion)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = self.menubar_field.addMenu('&edit')
        self.editMenu = self.menubar_field.addMenu('&view')
        self.editMenu = self.menubar_field.addMenu('&help')

    def create_rightmenu(self):
        # 右键菜单显示
        self.rightClick = QMenu(self)
        self.rightClick.addAction(self.verifyAction)
        self.rightClick.popup(QCursor.pos())
        

    def create_Actions(self):

        #sencond level menu operation : open exit
        self.newAcion = QAction('&new', self)
        self.openAction = QAction('&open', self)
        self.exitAction = QAction('&exit', self)
        self.saveAction = QAction('&save', self)
        #define open file operation to openAction
        self.newAcion.triggered.connect(self.New_file_event)
        self.openAction.triggered.connect(self.Open_file_event)
        self.saveAction.triggered.connect(self.Save_file_event)
        self.exitAction.triggered.connect(self.close)

        # 右键菜单部分的Actions
        self.verifyAction = QAction('程序验证',self)
        self.verifyAction.triggered.connect(self.create_inputDialog)
    

    def create_callgraph(self):
        # 文本区发生变化时：实时保存到tmp_inVisible_file
        content = self.editor.toPlainText()
        # new操作时程序崩溃，所以提前进行检查
        if content == '':
            pass
        else:
            os.system('attrib -h ' + self.tmp_file_path)
            with open(self.tmp_file_path, 'w') as tmp_inVisible_file:
                tmp_inVisible_file.write(str(content))
            os.system('attrib +h ' + self.tmp_file_path)

            # 如果代码出现错误，则程序崩溃
            # 解决方法： try except
            # 如果文本区存在错误，则放弃生成调用关系图，或者更新调用关系图
            try:
                # 获取 内容里面 relation_list
                relation_list, funcDef_list = new_relationList(self.tmp_file_path)

                # 生成FuncVerify_list
                for funcDef_info in funcDef_list:
                    for (key,val) in funcDef_info.items():
                        g_funcVerify_info[key] = []

                # 使用GraphicsView作为callgraph
                #self.callgraph_field = Gf()
                # 使用 WebEngineView制作CallGraph
                print(funcDef_list)
                print(relation_list)
                self.callgraph_field = create_WebEngineView_field(relation_list)
                #self.callgraph_field.create_call_graph(relation_list)
                # self.callgraph_field.selectionChanged.connect()
                self.funcTree = Tf(funcDef_list)

                # =================================================
                # 为了解决 添加内容后 重复添加treewidget从而界面崩坏的问题
                if self.layoutH.count() == 4:
                    self.layoutH.removeItem(self.layoutH.itemAt(0))
                # ==================================================

                self.layoutH.insertWidget(0,self.funcTree, 0)
                # 删除原来的layout
                # print(self.layoutH.count())
                if self.layoutH.count() > 3:
                    self.layoutH.removeItem(self.layoutH.itemAt(3))

                # 实现动态的更新 call graph
                self.layoutH.insertWidget(3,self.callgraph_field, 2)
                # self.create_Flowchart_field()
            except Exception as e:
                # print('error occured,pass')
                # 错误跟踪， 保留功能
                errorMes = e.args 
                line = str(errorMes).split(':')
                print(line)


    def create_verify_field(self, res_list):
            print('inputDialog finished , create_verify_field')
            # 更新FuncVerify
            g_funcVerify_info[self.current_verifyContent] = res_list
            print('g_funcVerify_info:', g_funcVerify_info)

            self.verify_field = QPlainTextEdit()
            textToBeShowed = "这里是程序验证入口 \n验证结果将这里显示 \n" + \
                            'Pre-condition: '+ str(res_list[0]) +'\n' + \
                            'Post-condition: '+ str(res_list[1]) 
            self.verify_field.setPlainText(textToBeShowed)
            # =====================================================
            # 动态添加可视化验证结果窗口
            print('layoutV items count:', self.layoutV.count())
            if self.layoutV.count() == 3:
                self.layoutV.removeItem(self.layoutV.itemAt(2))

            self.layoutV.addWidget(self.verify_field)


    # 右键菜单 点击程序验证后，创建程序验证显示结果
    # 因为该接口尚没有对应函数，所以暂时 留白
    # 参数说明： verify_content 可以是函数名，也可以是一段代码，分别对应双击验证和选择验证
    def create_inputDialog(self, verify_content):
        print("create_inputDialog")
        # 记录当前的验证的内容, 以便后续更新对应的条件列表
        self.current_verifyContent = verify_content
        if verify_content not in g_funcVerify_info.keys():
            g_funcVerify_info[verify_content] = []

        # 如果不定义为类成员的话,窗口会一闪然后退出,因为 方法执行完之后就被destory了
        self.inputDialog = inputDialog(g_funcVerify_info[verify_content])
        # python 自带的thread方法
        # dialog_thread = threading.Thread(target=self.createInputDialog,args=(g_funcVerify_info[verify_content],))
        # dialog_thread.start()
        # 如何用pyqt QThread方法
        # self.dialog_thread = QThread()
        # self.create_inputDialog = inputDialog(g_funcVerify_info[verify_content])
        # self.create_inputDialog.moveToThread(self.dialog_thread)
        # self.dialog_thread.start()
        # self.dialog_thread.wait()
       
        # print('create_inputDialog:' ,g_funcVerify_info)
        # 不能定义在这里！我一时想不清楚
        # signal.finished.connect(self.create_verify_field)
   

    #Implement create new plain text file to newAcion
    def New_file_event(self):
        
        self.filename = ''
        self.editor.clear()
        self.editor.setPlainText('')
        
        # reserved operation 
        #self.editor.moveCursor(self.cursor.End)        

    #Implement open file operation to openAction
    def Open_file_event(self):

        # path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath() + '../dependencies/pycparser-master/examples/c_files/' ,\
        #         'Text Files (*.txt *.c *.py);; All Files (*.*)')
        path, _ = QFileDialog.getOpenFileName(self, "Open File", 
        'E:/Github_repo/new-review-way-of-C-srcs/dependencies/pycparser-master/examples/c_files/' ,
        'Text Files (*.txt *.c *.py);; All Files (*.*)')
        
        # path, _ = QFileDialog.getOpenFileName(self, "Open File",'',
        #         'Text Files (*.txt *.c *.py);; All Files (*.*)', None, QFileDialog.DontUseNativeDialog)
        
        if path:
            inFile = QFile(path)
            
            if inFile.open(QFile.ReadWrite | QFile.Text):
                text = inFile.readAll()

                os.system('attrib -h ' + self.tmp_file_path)
                with open(self.tmp_file_path, 'w') as tmp_inVisible_file:
                    tmp_inVisible_file.write(str(text))
                os.system('attrib +h ' + self.tmp_file_path)

                try:
                    text = str(text, encoding = 'utf-8')
                except TypeError:
                    text = str(text)
                
                self.editor.setPlainText(text)
                self.filename = path
                self.fname = QFileInfo(path).fileName()
                
                # sync fname to WindowTitile
                self.setWindowTitle(self.fname + '[*]')
                #self.create_callgraph()
    
    #Implement save file operation to saveAction
    def Save_file_event(self):
        # print('stream is saving file !!')

        #if filename isn't null, save action write modified content to origin path
        if self.filename != "":
            outfile = QFile(self.filename)

            #open file 
            if not outfile.open( QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self, "Error", "Cannot write file")
                return 

            # write file
            # QTextStream construct a QTextStream, must assign a device or a string before use it
            outContent = QTextStream(outfile)

            # set a wait period until write file successfully
            QApplication.setOverrideCursor(Qt.WaitCursor)
            outContent << self.editor.toPlainText()
            QApplication.restoreOverrideCursor()
            
            #update window title
            self.setWindowTitle(self.fname + '[*]')
        else:

            #save file that newly created
            self.Save_new_file()
    
    def Save_new_file(self):
        
        # new file means that need to choose a path to save 
        # QFileDialog.getSaveFileName method satisfy this need
        
        new_file_path, _ = QFileDialog.getSaveFileName(self, 'Save as..', self.filename, 'Python files (*.py)')

        if not new_file_path :
            QMessageBox.warning(self, 'Error', 'save file failed')
            return

        self.filename = new_file_path
        self.fname = QFileInfo(new_file_path).fileName()
        print('new_file_path is : %s' %(self.filename))

        return self.Save_file_event()
    
    # 代码高亮， 当文本被创建时以及需要更新时就调用 paintEvent函数
    def paintEvent(self, event):
        highlighted_line = QTextEdit.ExtraSelection()

        highlighted_line.format.setBackground(QColor("#E8F6F3"))
        highlighted_line.format.setProperty(QTextFormat.FullWidthSelection,QVariant(True))
        highlighted_line.cursor = self.editor.textCursor()
        highlighted_line.cursor.clearSelection()
        self.editor.setExtraSelections([highlighted_line])




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    ex.show()

    sys.exit(app.exec_())