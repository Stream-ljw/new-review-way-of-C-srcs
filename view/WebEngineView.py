import json
import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget,QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel

class create_WebEngineView_field(QWidget):
    
    # def __init__(self, relation_list):
    #     super().__init__()
    #     self.setMinimumSize(500, 500)
    #     self.relation_list = relation_list
    #     self.obj=JsObj(self.relation_list)
    #     browser = QWebEngineView(self)
    #     channel=QWebChannel(browser.page())
    #     channel.registerObject("obj", self.obj)
    #     browser.load(QUrl.fromLocalFile(os.getcwd() + "/html/index.html"))
    #     browser.page().setWebChannel(channel)
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400,600)
        # sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # self.setSizePolicy(sizePolicy)
        self.relation_list = []
    
    def create_call_graph(self, relation_list):
        self.relation_list = relation_list
        self.obj=JsObj()
        self.obj.set_relation_list(relation_list)
        browser = QWebEngineView(self)
        channel=QWebChannel(browser.page())
        channel.registerObject("obj", self.obj)
        browser.load(QUrl.fromLocalFile(os.getcwd() + "/html/index.html"))
        browser.page().setWebChannel(channel)

    def resizeEvent(self, evt):
        browser=self.findChild(QWebEngineView)
        if browser is not None:
            browser.resize(self.width(), self.height())

class global_signal(QObject):
    JumpToLine_signal = pyqtSignal(int)

    inputDialog_signal = pyqtSignal(str)
    #print('test_signal:', JumpToLine_signal)

g_signal = global_signal()

class JsObj(QObject):

    #JumpToLine_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.relation_list = []
        # JumpToLine_signal = pyqtSignal(int)

    # 从这里入口将 函数调用关系表传入 webEngineView
    @pyqtSlot(result=str)
    def getBtnJson(self):
        # sample_list = [
        #     [{'fname':'coord'}, {'callfname':'coord'},{'callfname2':'coord'}],
        #     [{'fname2':'coord'}],
        #     [{'fname': 'coord'}]]
        return json.dumps(self.relation_list)

    @pyqtSlot(str,result=str)
    def getBtnCoord(self, coord ):
        self.btn_coord = int(coord)
        # jump_to_line(self.btn_coord)
        
        #print("emit()")
        g_signal.JumpToLine_signal.emit(self.btn_coord)
        #print('getbtn:',self.signal.JumpToLine_signal)

        print("getBtnCoord", self.btn_coord)
        #return coord
    
    @pyqtSlot(str, result=str)
    def getBtnName(self,nodeName):
        print('btn double click',nodeName)
        #print(nodeName)
        g_signal.inputDialog_signal.emit(nodeName)
    
    def set_relation_list(self, relationList):
        self.relation_list = relationList

    def return_btn_coord(self):
        return self.btn_coord


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    demo = create_WebEngineView_field()
    demo.show()
    
    sys.exit(app.exec_())