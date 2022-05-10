#print('this file exits for future use')

import sys
import os

#sys.path.append(r'E:/Github_repo/new-review-way-of-C-srcs/dependencies/pycparser_master/pycparser')
#sys.path.append(r'E:/Github_repo/new-review-way-of-C-srcs/features')
sys.path.append(os.getcwd()+ '/..')
from dependencies.pycparser_master.pycparser import c_ast 
from dependencies.pycparser_master.pycparser import parse_file 
# from dependencies.pycparser_master.pycparser import c_parser
# c_ast, c_parser, parse_file

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
        self.FuncBody_dict = {}
        self.get_func_defs()
    
    def visit_FuncDef(self, node):
        # 获得函数体起始行号，和结束行号
        compoundVisitor = CompoundVisitor()
        compoundVisitor.get_Compound(node)
        coordList = compoundVisitor.return_CoordList()
        # print(coordList)
        decl_info = {node.decl.name: node.decl.coord.line}
        # 新增函数起始行号 ，结束行号的解析
        self.FuncBody_dict[node.decl.name] = coordList
        # print(decl_info)
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
        # cpp_args的路径是 相对当前执行的路径
        self.ast = parse_file(self.filepath, use_cpp=True,
                        cpp_args=r'-I../dependencies/pycparser_master/utils/fake_libc_include')
        # parser = c_parser.CParser()
        # self.ast = parser.parse(self.filepath)

        self.visit(self.ast)
    
    def return_FuncDefInfoList(self):
        return self.FuncDefInfo_list
    
    def return_relation_list(self):
        return self.relation_list
    
    def return_FuncBody_list(self):
        return self.FuncBody_dict

# get function call list
class FuncCallVisitor(c_ast.NodeVisitor):
    
    def __init__(self):
        super().__init__()
        # self.filename = filename
        #self.funcname = None
        self.FuncCall_list = []

    def visit_FuncCall(self, node):
        #self.callfunc_list.append(self.funcname)
        #print(node)
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

class CompoundVisitor(c_ast.NodeVisitor):
    
    def __init__(self):
        super().__init__()
        #self.filepath = filename
        self.FuncCoordList = []

    def visit_Compound(self, node):
        self.FuncCoordList.append(node.coord.line)
        self.FuncCoordList.append(node.end_coord.line)
        print('coord: ', node.coord.line,':', node.end_coord.line)
    
    def get_Compound(self,node):
        # self.ast = parse_file(self.filepath, use_cpp=True,
        #                 cpp_args=r'-I../dependencies/pycparser_master/utils/fake_libc_include')
        # self.visit(self.ast)
        self.visit(node)
    
    def return_CoordList(self):
        return self.FuncCoordList

# 清洗 relation_list ,因为包含了所有print ，scanf一些系统函数
# 与我们目标的函数调用的最终关系表不相干，所以需要去除
# 方法就是遍历，把FuncCall_list中不在 FuncDeflist声明列表里的函数去除
def generate_relationList(filename):

    visit = FuncDefVisitor(filename)
    FuncDefList = visit.return_FuncDefInfoList()
    FuncBodyList = visit.return_FuncBody_list()
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
    
    return relation_list,FuncDefList,FuncBodyList

# 判断funcInfo是否有调用其他函数
def haveCallFunc(funcname, relList):
    for funcinfo in relList:
        (key,val), = funcinfo[0].items()
        if key == funcname and len(funcinfo) >= 2:
            return True,funcinfo
    
    return False, []


# 我这里的递归绝了。
# 递归的判断后续的函数是否有调用其他函数
# 参数解释：
# tmpList ：每次要判断的函数列表
# relList ：relationList 函数调用关系表，用来查询其中的函数是否有调用，不发生改变
# tmp_relList： relationList复制版，每次符合’被调用且调用了其他函数‘会从中删除
# finalList ： 每次符合’被调用且调用了其他函数‘会添加到其中
# notshow ： 每次判断 “被调用但是没有调用其他函数” 会加入到其中，用来后续判断是否将tmp_relList中的
# 函数添加到final里面
def getFunc(tmpList, relList, tmp_relList,finalList, notshow):
    final = finalList
    tmp = tmp_relList
    notshow = notshow
    #print('final: ',final)
    #print('tmp: ',tmp)
    # 从main函数的第1个调用函数，也就是列表的第二位开始判断
    for IndexOfdictItem in range(1,len(tmpList)):
        (key,val), = tmpList[IndexOfdictItem].items()
        #print(key, ' : ', tmpList[IndexOfdictItem])
        res, funclist = haveCallFunc(key,relList)
        #print(res,' : ',funclist)
        if res == True :
            final.append(funclist)
            tmp.remove(funclist)
            getFunc(funclist, relList, tmp,final, notshow)
        else:
            # 这是被调用 但是没有调用其他函数
            notshow.append(tmpList[IndexOfdictItem])
    return final,tmp,notshow

# 进一步调整函数调用关系图逻辑
# 优先显示 main，且接下来依次显示main中被调用函数的其他关系
# 如果函数只有被调用，没有调用其他函数，则不单独显示
# 如果函数既没有被调用，也没有调用其他函数，单独显示
# 参照
# [
#  [{'foo': 1}], 
#  [{'foo1': 6}], 
#  [{'hello': 11}], 
#  [{'foo2': 17}], 
#  [{'foo3': 22}], 
#  [{'maxout_in': 27}, {'foo': 29}, {'foo': 30}], 
#  [{'main': 34}, {'maxout_in': 40}]
# ]
def new_relationList(filename):
    final_relationList = []
    FuncNotToBeShowed = []
    relList, FuncDefList, FuncBodyList = generate_relationList(filename)
    tmp_relList = relList
    tmpList = []
    # 判断是否有main函数
    for funcInfo in tmp_relList:
        (key,val), = funcInfo[0].items()
        if key == 'main':
            final_relationList.append(funcInfo)
            tmpList = funcInfo
            tmp_relList.remove(funcInfo)
    
    if tmpList == []:
        # 不存在main 只需要过滤那些被调用且没有调用其他函数的函数
        for funcInfo in relList:
            if len(funcInfo) > 1:
                final_relationList, tmp_relList, FuncNotToBeShowed = getFunc(funcInfo,relList,tmp_relList,final_relationList,FuncNotToBeShowed)
        print('FuncNotToBeShowed: ',FuncNotToBeShowed)
    else:
        # 如果有main函数，则递归判断后续函数的情况
        final_relationList, tmp_relList, FuncNotToBeShowed = getFunc(tmpList,relList,tmp_relList,final_relationList,FuncNotToBeShowed)

    # print(tmp_relList)
    # print(FuncNotToBeShowed)
    FuncNotToBeShowed_name = []
    #过滤掉那些被调用但是没有调用其他函数的
    for item in FuncNotToBeShowed:
        (key,val), = item.items()
        FuncNotToBeShowed_name.append(key)

    # 剩下的都是既没有被调用，也没有调用其他的函数
    for listitem in tmp_relList:
        (key,val), = listitem[0].items()
        if key not in FuncNotToBeShowed_name:
            final_relationList.append(listitem)
    print('final_relationList', final_relationList)
    return final_relationList, FuncDefList, FuncBodyList
    
# 生成 函数调用矩阵， 方法就是 横轴 数轴都为 函数名，如果其中有调用关系那么将位置坐标(index(func1) , index(func2))置为1
# 这是为了以后制作更复杂的调用关系图所用。
# 因为如何更好显示关系图的方法还未找到，只能绘制简单的两层调用，所以暂时没有用 
# 尚未 完成
def generate_FuncCallMatrics():
    print('To be continued!')

if __name__ == '__main__':

    filename = 'E:/Github_repo/new-review-way-of-C-srcs/dependencies/pycparser_master/examples/c_files/year.c'

    visit = FuncDefVisitor(filename)

    body = visit.return_FuncBody_list()
    print(body)
    # infoList = visit.return_FuncDefInfoList()
    # # coord is class Coord class object ,which the format like : (file:line:column)
    # # and we can select the specified info to show
    # for item in infoList:
    #     (key,value), = item.items()
    #     print(key, ' : ',value.line)


    #generate_relationList(filename)
    #new_relationList(filename)

    # visit = CompoundVisitor(filename)
    # visit.get_Compound()


    
    # visit = FuncCallVisitor(filename)
    # visit.get_func_calls(funcname)


