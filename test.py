#import treelib.treelib.node
from treelib.treelib import Node, Tree

tree = Tree()
tree.create_node("   .Program", "Program")  # root node
tree.create_node("  1.FuncDecl", "FuncDecl", parent="Program")
tree.create_node("   .(return type) Type: void", "Type", parent="FuncDecl")
tree.create_node("  1.Identifier: main", "Identifier", parent="FuncDecl")
tree.create_node("   .(body) StmtBlock:", "StmtBlock", parent="FuncDecl")

#tree.create_node("(aody) StmtBlock:", "StmtBlock2", parent="FuncDecl")

tree.create_node("   .PrintStmt", "PrintStmt", parent="StmtBlock")
tree.create_node("  2.(args) StringConstant: \"hello world\"", "StringConstant", parent="PrintStmt")


#dicttree = tree.to_dict(sort = False)
#print(dicttree)
#tree.show(reverse = True)

child = tree.children("FuncDecl")


print(child)

tree.show(key = False, line_type = 'ascii-sp')