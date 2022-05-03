import sys
from PyQt5.QtWidgets import QGraphicsTextItem ,QGraphicsLinearLayout, \
                            QGraphicsScene , QGraphicsView, \
                            QApplication, QGraphicsWidget,  QGraphicsLayoutItem,\
                            QGraphicsRectItem,\
                            QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
                            
# 传入一个 形如 ：
# [
#   [{'fname':'coord'}, {'callfname':'coord'},{'callfname2':'coord'}],
#   [{'fname2':'coord'}],
#   [{'fname': 'coord'}] 
# ]
# 这样的数组， 要将fname放入 button 内容，然后排版
# 返回一个graphicsview 

class create_callgraph(QGraphicsView):

    def __init__(self, callgraph_group: list):
        super().__init__() 

        self.callgraph_group = callgraph_group
        
        # 如果传入的list 为空，结束
        if len(callgraph_group) == 0:
            print('stream echo : no data to be processed! exit...')
            return 
        
        self.final_layout = QVBoxLayout()
        self.create_layout()
        self.setLayout(self.final_layout)

#def Jump_to_line(self):
    #    print('this is jump')

    def create_buttons(self, button_text):
        # 创建button 
        # 设置 button的格式: 水平策略和 垂直策略，控制控件随着窗口拉伸的形变
        # 还要绑定button的槽 可以跳转到文本
        button = QPushButton(button_text)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layoutH = QHBoxLayout()
        layoutH.addWidget(button)
        layoutH.addStretch()
        #button.mouseDoubleClickEvent()
        return layoutH

    def create_layout(self):
        # fname_dict 形如： [{'fname': 'coord'}, {'callfname': 'coord'}]
        for call_graph_list in self.callgraph_group:
            #对于每组函数调用表 如果长度只有1 说明没有调用其他函数。可以直接放入final_layout
            # 如果长度大于2 那么需要排版
            if len(call_graph_list)  < 2:
                (funcname, coord), = call_graph_list[0].items()
                button = self.create_buttons(funcname)

                # tmp_layoutH = QHBoxLayout()
                # tmp_layoutH.addWidget(button, Qt.AlignLeft)
                # tmp_layoutH.addStretch()
                #tmp_layoutH.addLayout(layoutV_single)
                self.final_layout.addLayout(button)
                
            else:
                group_layout = QHBoxLayout()

                #存在调用。主调函数先单独一列
                (funcname, coord), = call_graph_list[0].items()
                button = self.create_buttons(funcname)
                # layoutH_single = QHBoxLayout()
                # layoutH_single.addWidget(button, Qt.AlignLeft)
                # layoutH_single.addStretch()
                tmp_layoutV = QVBoxLayout()
                #tmp_layoutV.addWidget(button)
                tmp_layoutV.addLayout(button)
                group_layout.addLayout(tmp_layoutV)

                # 剩下的被调函数 遍历获取 funcname：coord 给 fname_info,
                # 创建button，放入layoutV
                layoutV = QVBoxLayout()
                for i in range(1,len(call_graph_list)):
                    func_info = call_graph_list[i]
                    (funcname, coord), = func_info.items()
                    
                    button = self.create_buttons(funcname)
                    #layoutV.addWidget(button)
                    layoutV.addLayout(button)
                # 被调函数是否还调用了其他函数
                # 通过查询其 主调，被调表 ，主调：  ，被调 

                group_layout.addLayout(layoutV)
                self.final_layout.addLayout(group_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    sample_list = [
                [{'fname':'coord'}, {'callfname':'coord'},{'callfname2':'coord'}],
                [{'fname2':'coord'}],
                [{'fname': 'coord'}] 
                ]
                
    demo = create_callgraph(sample_list)
    demo.show()
    
    sys.exit(app.exec_())            

# class LayoutItem(QGraphicsLayoutItem):

#     def __init__(self , TextItem: QGraphicsTextItem):
#         super().__init__()
#         self.textItem = self.setGraphicsItem(TextItem)

#     def setGeometry(self, rect: QRectF) -> None:
#         return super().setGeometry(rect)
    
#     def sizeHint(self, which: Qt.SizeHint, constraint: QSizeF = ...) -> QSizeF:
#         if which == Qt.MinimumSize:
#             pass
#         elif which == Qt.PreferredSize:
#             return self.textItem.