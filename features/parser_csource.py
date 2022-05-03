#print('this file exits for future use')

import sys
import os
sys.path.append(r'E:/Github_repo/new-review-way-of-C-srcs/dependencies/pycparser-master')
sys.path.append(r'E:/Github_repo/new-review-way-of-C-srcs/features')

from pycparser import c_ast, c_parser, parse_file

''' 
A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
'''

'''
c_ast.py :

class NodeVisitor(object):
    def visit(self, node):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        #print('c_ast : ', node.__class__.__name__, method)
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c_name, c in node.children():
            self.visit(c)
'''

# get function declare list
class FuncDefVisitor(c_ast.NodeVisitor):

    def __init__(self, filename):
        super().__init__()
        self.filepath = filename 
        self.FuncDefInfo_list = []
        self.relation_list = []
        self.get_func_defs()
    
    def visit_FuncDef(self, node):
        #print('%s at %s' % (node.decl.name, node.decl.coord))
        #print(node.name.name)
        decl_info = {node.decl.name: node.decl.coord.line}
        FuncCall_list = [decl_info]
        #print(node)
        tmp_visitor = FuncCallVisitor()
        tmp_visitor.get_func_calls(node)
        
        FuncCall_list.append(tmp_visitor.return_callfunc_list())
        self.relation_list.append(FuncCall_list)

        self.FuncDefInfo_list.append(decl_info)
    
    def get_func_defs(self):
        # Note that cpp is used. Provide a path to your own cpp or
        # make sure one exists in PATH.
        self.ast = parse_file(self.filepath, use_cpp=True,
                        cpp_args=r'-Iutils/fake_libc_include')

        self.visit(self.ast)
    
    def return_FuncDefInfoList(self):
        return self.FuncDefInfo_list
    
    def return_relation_list(self):
        return self.relation_list

# get function call list
class FuncCallVisitor(c_ast.NodeVisitor):
    
    def __init__(self):
        super().__init__()
        # self.filename = filename
        #self.funcname = None
        self.FuncCall_list = []

    def visit_FuncCall(self, node):
        #self.callfunc_list.append(self.funcname)
        print(node)
        # print(node.name.coord)
        self.FuncCall_list.append({node.name.name: node.name.coord.line})
        # with open('out.txt','w') as of:
        #     of.write(str(node.name))
        # of.close()

        # if node.name.name == self.funcname:
        #     print('%s called at %s' % (self.funcname, node.name.coord))
    
    def get_func_calls(self, node):
        # self.ast = parse_file(self.filename, use_cpp=True,
        #                 cpp_args=r'-Iutils/fake_libc_include')
        
        # with open('out.txt') as of:
        #     of.write(self.ast)
        # of.close()

        # self.funcname = funcname
        # self.visit(self.ast)
        self.visit(node)    

    def return_callfunc_list(self):
        return self.FuncCall_list 

# 清洗 relation_list ,因为包含了所有print ，scanf一些系统函数
# 与我们目标的函数调用的最终关系表不相干，所以需要去除
# 方法就是遍历，把FuncCall_list中不在 FuncDeflist声明列表里的函数去除
def generate_relationList(filename):

    visit = FuncDefVisitor(filename)
    FuncDefList = visit.return_FuncDefInfoList()
    funcname_list = []
    for j in range(len(FuncDefList)):
        (funcname,coord),  = FuncDefList[j].items()
        funcname_list.append(funcname)

    relation_list = visit.return_relation_list()
    # print(FuncDefList)
    # print(funcname_list)
    # print(relation_list)
    for i in range(len(relation_list)):
        # FuncCall_list[0] 是 主调函数，后面跟着的是被调函数
        FuncCall_list = relation_list[i][1]
        
        relation_list[i].pop()
        # print(i , ':', FuncCall_list)
        # print(i , ':', relation_list[i])
        
        for item in FuncCall_list:
            (funcname,coord), = item.items()
            if funcname in funcname_list:
                relation_list[i].append(item)
    
    return relation_list,FuncDefList


# 生成 函数调用矩阵， 方法就是 横轴 数轴都为 函数名，如果其中有调用关系那么将位置坐标(index(func1) , index(func2))置为1
# 这是为了以后制作更复杂的调用关系图所用。
# 因为制作关系图的方法还未掌握，只能绘制简单的两层调用，所以暂时没有用 
# 尚未 完成
def generate_FuncCallMatrics():
    print('To be continued!')

if __name__ == '__main__':

    filename = 'E:/Github_repo/new-review-way-of-C-srcs/dependencies/pycparser-master/examples/c_files/year.c'

    # visit = FuncDefVisitor(filename)
    # infoList = visit.return_FuncDefInfoList()
    # # coord is class Coord class object ,which the format like : (file:line:column)
    # # and we can select the specified info to show
    # for item in infoList:
    #     (key,value), = item.items()
    #     print(key, ' : ',value.line)


    generate_relationList(filename)

    
    # visit = FuncCallVisitor(filename)
    # visit.get_func_calls(funcname)


