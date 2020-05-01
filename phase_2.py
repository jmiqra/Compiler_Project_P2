"""
@author: iqrah
"""

import sys
import tokens
import phase_1
from treelib.treelib import Node, Tree

astree = Tree()
astree.create_node("   .Program", "Program") # abstract syntax tree root
parent = "Program"

errorFound = False

def printDebug(str):
    #print(str)
    return True

def printFunction(str):
    global errorFound 
    if not errorFound:
        print(str)
    return True

t = phase_1.get_next_token()
printDebug(t)

def next_token():
    global t
    t = phase_1.get_next_token()
    printDebug(t)
    if t != None:
        return True
    else:
        return False

def find_line(t):
    return phase_1.lines[t.lineno-1]

def find_col(t):
    #str(find_column(input_str, t)) + "-" + 
    #str(find_column(input_str, t)+len(str(t.value))-1)
    return phase_1.find_column(phase_1.input_str, t) - 1

def find_node_id(t, id):
    node_id = id + "_" + str(t.lineno) + "_" + str(find_col(t))
    return node_id

def update_parent(par):
    global parent
    parent = par
    return True


def handleError(t):
    global errorFound
    if not errorFound:
        print()
        printFunction("*** Error Line " + str(t.lineno) + ".")
        printFunction(find_line(t))
        #printDebug(find_col(t))
        err_str = ""
        for i in range(find_col(t)):
            err_str += " "
        for j in range(len(t.value)):
            err_str += "^"
        printFunction(err_str)
        printFunction("*** syntax error")
        print()
        errorFound = True
        return True
    else:
        return False

def program_start():
    printDebug("------program")
    if t == None:
        printFunction("Empty program is syntactically incorrect.")
        #handleError(t)
        return False
    return decl() and program()

def program():
    #next_token()
    if t == None:
        printDebug("Program ended successfully!")
        return True
    else:
        return program_start()


def decl():
    global parent
    prevPar = parent
    printDebug("------decl " + str(t))
    if(t.value in tokens.type_list or t.value == tokens.T_Void):
        dataType = t.value
        next_token()
        if(t.type == tokens.T_Identifier):
            ident = t.value
            next_token()
            if(t.value == tokens.T_LP):
                node_id = find_node_id(t, "FnDecl")
                node_label = "  " + str(t.lineno) + "." + "FnDecl:"
                astree.create_node( node_label, node_id, parent=parent)
                
                parent = node_id
                
                node_label = "   " + "." + "(return type) Type: " + dataType
                astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                node_label = "  " + str(t.lineno) + "." + "Identifier: " + ident
                astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)

                return functionDecl() and update_parent(prevPar)
            else:
                node_id = find_node_id(t, "VarDecl")
                node_label = "  " + str(t.lineno) + "." + "VarDecl:"
                astree.create_node( node_label, node_id, parent=parent)
                
                parent = node_id

                node_label = "   " + "." + "Type: " + dataType
                astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                node_label = "  " + str(t.lineno) + "." + "Identifier: " + ident
                astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)

                return variableDecl() and next_token() and update_parent(prevPar)
        else:
            printDebug("Syntax Error 1 " + str(t))
            handleError(t)
            return False
    else:
        printDebug("Syntax Error 2 " + str(t))
        handleError(t)
        return False

def functionDecl():
    printDebug("------funtionDecl")
    next_token()
    params = formals()
    next_token()
    return params and stmtBlock()

def formals():
    printDebug("------formals")
    global parent
    prevPar = parent
    if t.value == tokens.T_RP:
        return True
    while True:
        if t.value in tokens.type_list:
            dataType = t.value
            next_token()
            if(t.type == tokens.T_Identifier):
                ident = t.value
                next_token()
                if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
                    node_id = find_node_id(t, "VarDecl")
                    node_label = "  " + str(t.lineno) + "." + "(formals) VarDecl:"
                    astree.create_node( node_label, node_id, parent=parent)
                    
                    parent = node_id

                    node_label = "   " + "." + "Type: " + dataType
                    astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                    node_label = "  " + str(t.lineno) + "." + "Identifier: " + ident
                    astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)
                    update_parent(prevPar)
                    continue
                elif t.value == tokens.T_RP:

                    node_id = find_node_id(t, "VarDecl")
                    node_label = "  " + str(t.lineno) + "." + "(formals) VarDecl:"
                    astree.create_node( node_label, node_id, parent=parent)
                    
                    parent = node_id

                    node_label = "   " + "." + "Type: " + dataType
                    astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                    node_label = "  " + str(t.lineno) + "." + "Identifier: " + ident
                    astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)

                    return True and update_parent(prevPar)
            else:
                handleError(t)
                return False

def stmtBlock():
    printDebug("------stmtBlock" + str(t))
    
    global parent
    prevPar = parent
    node_label = "   " + "." + "(body) StmtBlock:"
    node_id = find_node_id(t, "StmtBlock")
    astree.create_node( node_label, node_id , parent= parent)
    parent = node_id
    
    if t.value == tokens.T_LC:
        next_token()
        if t.value == tokens.T_RC:
            return True and update_parent(prevPar)
        else:
            stmtBlockParam = variableDecl_2() and t.value == tokens.T_RC
            printDebug("~~~~~~ " + str(t))
            next_token()
            return stmtBlockParam and update_parent(prevPar)

def variableDecl():
    printDebug("------variableDecl")
    if(t.value == tokens.T_SemiColon):
        return True
    else:
        handleError(t)
        return False

def variableDecl_2():
    printDebug("------variableDecl_2")
    #if t.value == tokens.T_RC:
    #        return True
    if t.value in tokens.type_list and next_token() and t.type == tokens.T_Identifier:
        next_token()
        return variableDecl() and next_token() and variableDecl_2()
    else:
        while True:
            if stmt():
                if t.value == tokens.T_RC:
                    printDebug("true from varDecl_2")
                    return True
                if(t.value == tokens.T_Else):
                    printDebug("else found")
                    return True
                next_token()
                pass
            else:
                return True


def stmt():
    printDebug("------stmt")
    printDebug(t)
    if t.value == tokens.T_RC:
        printDebug("True Stmt for RightCurly")
        return True
    #next_token()
    if t.value == tokens.T_If:
        printDebug("If found from Stmt")
        if next_token() and ifStmt():
            if t.value == tokens.T_RC:
                printDebug("RightCurly found after ifStmt")
                return True
            else:
                printDebug("stmt from ifStmt")
                return stmt()
    
    elif t.value == tokens.T_While:
        printDebug("While found from Stmt")
        if next_token() and whileStmt():
            if t.value == tokens.T_RC:
                printDebug("RightCurly found after whileStmt")
                return True
            else:
                printDebug("stmt from whileStmt")
                return stmt()
    
    elif t.value == tokens.T_For:
        printDebug("For found from Stmt")
        if next_token() and forStmt():
            if t.value == tokens.T_RC:
                printDebug("RightCurly found after forStmt")
                return True
            else:
                printDebug("stmt from forStmt")
                return stmt()
    
    elif t.value == tokens.T_Break:
        printDebug("Break found from Stmt")
        return  next_token() and breakStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_Return:
        printDebug("Return found from Stmt")
        return  next_token() and returnStmt() # and next_token() and stmt()
    
    elif t.value == tokens.T_Print: # and next_token() and t.value == tokens.T_LP:
        printDebug("printDebug found from Stmt")
        return  next_token() and printStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_LC:
        return stmtBlock()
    
    elif t.value == tokens.T_SemiColon:
        printDebug("Semicolon found from stmt")
        return True
    
    elif initExprTree() and expr() and t.value == tokens.T_SemiColon: #need to work:  prev work expr() semi nexttok stmt
        printDebug("Expr and Semicolon found from stmt " + str(t.value))
        return True
        #printDebug("ret from stmt ")
        #var = expr() and t.value == tokens.T_SemiColon and next_token()     
        #work for single statement
    #elif t != None:
    #    printDebug("true from stmt last else")
    #    return stmt()

def ifStmt():
    printDebug("----XXXXXXXXXXXXXXXXXXXXXXXXXx--ifStmt")
    if t.value == tokens.T_LP:
        ifParam = next_token() and expr() and t.value == tokens.T_RP
        if not ifParam:
            printDebug("error from if ")
            handleError(t)
            return False
        
        printDebug("inside ifParam true" + t.value)
        
        if next_token() and not stmt():
            printDebug("false from ifStmt")
            handleError(t)
            return False

        #if(t!=None and t.value != tokens.T_Else):
        if t.value == tokens.T_SemiColon:
            next_token()
        
        if t != None and t.value == tokens.T_Else:
            printDebug("else found----------------------------------------------------------------------")
            next_token()
            if not stmt():
                printDebug("False from if.. else..")
                handleError(t)
                return False
            else:
                printDebug("true for if with else----------------------")
                return True
        else:
            printDebug("true for if----------------------")
            return True
    else:
        handleError(t)
        return False


def whileStmt():
    printDebug("------whileStmt")
    if t.value == tokens.T_LP:
        whileParam = next_token() and expr() and t.value == tokens.T_RP
        if not whileParam:
            printDebug("error from whileStmt")
            handleError(t)
            return False
        if next_token() and not stmt():
            printDebug("returnning false from whileStmt")
            handleError(t)
            return False
        printDebug("true for while----------------------")
        return True
    else:
        handleError(t)
        return False 

def forStmt():
    printDebug("------forStmt")
    if t.value == tokens.T_LP:
        printDebug("LeftParen found forStmt")
        #1 for null init
        if next_token() and t.value == tokens.T_SemiColon:
            printDebug("First expr not present inside forStmt")
            pass
        #1 for init
        elif not expr() or t.value != tokens.T_SemiColon:
            printDebug("false for wrong first expr part inside forStmt")
            handleError(t)
            return False
        
        #2 for init and cond
        printDebug("inside forStmt token -> " + str(t))
        next_token()
        if not expr() or not t.value == tokens.T_SemiColon:
            printDebug("False for wrong second part inside forStmt")
            handleError(t)
            return False

        #3 for init cond update
        next_token()
        printDebug("start forStmt last part -> " + str(t))
        if t.value == tokens.T_RP:
            printDebug("No third part inside forStmt")
            return next_token() and stmt()
        elif expr() and t.value == tokens.T_RP:
            return next_token() and stmt()
    else:
        handleError(t)
        return False

def breakStmt():
    printDebug("------breakStmt")
    if t.value == tokens.T_SemiColon:
        printDebug("True from breakStmt" + str(t))
        return True

def returnStmt():
    printDebug("------returnStmt")
    global parent
    prevPar = parent
    node_id = find_node_id(t, "ReturnStmt")
    node_label = "  " + str(t.lineno) + "." + "ReturnStmt:"
    astree.create_node( node_label, node_id, parent= parent)
    parent = node_id

    if t.value == tokens.T_SemiColon:
        printDebug("return done without expr" + str(t))
        return True and update_parent(prevPar)
    elif initExprTree() and expr() and t.value == tokens.T_SemiColon and next_token(): # next_token should be removed?
        printDebug("return done with expr" + str(t))
        return True and update_parent(prevPar)
    else:
        handleError(t)
        return False
        
def printStmt():
    printDebug("------printStmt")
    global parent
    prevPar = parent
    node_id = find_node_id(t, "PrintStmt")
    node_label = "   " + "." + "PrintStmt:"
    astree.create_node( node_label, node_id, parent= parent)
    parent = node_id

    if t.value == tokens.T_LP:
        while True:
            printDebug("enter printDebug loop--")
            next_token()        
            if not expr():
                printDebug("false from printStmt")
                handleError(t)
                return False
            if t.value == tokens.T_Comma:
                printDebug("Comma inside printStmt")
                update_parent(prevPar)
                continue
            elif t.value == tokens.T_RP:
                printDebug("RightParen found in printStmt")
                next_token()
                if t != None and t.value == tokens.T_SemiColon:
                    printDebug("semicolon after printDebug")
                    return True and update_parent(prevPar)
                else:
                    handleError(t)
                    return False
    else:
        handleError(t)
        return False

exprTreeRoot = ""
lastTreeRoot = ""
currentTreeRoot = ""
prevOperator = ""
assignTreeRoot = ""
exprTree = Tree()

def initExprTree():
    global exprTree
    exprTree = Tree()
    global exprTreeRoot
    exprTreeRoot = ""
    global lastTreeRoot
    lastTreeRoot = ""
    global prevOperator
    prevOperator = ""
    global currentTreeRoot
    currentTreeRoot = ""
    global assignTreeRoot
    assignTreeRoot = ""
    return True

def expr():
    printDebug("------expr " + str(t))
    global exprTreeRoot
    global lastTreeRoot
    global assignTreeRoot
    global exprTree
    global prevOperator
    global currentTreeRoot
    prevPar = parent

    if t.value == tokens.T_Minus:
        return next_token() and expr()
    
    elif t.value == tokens.T_LP:
        printDebug("LeftParen found from expr")
        if next_token() and expr() and t.value == tokens.T_RP:
            next_token()
            if t.value in tokens.op_list:
                printDebug("op_list found inside LeftParen expr")
                return next_token() and expr()
            else:
                printDebug("true from expr LeftParen cond")
                return True

    elif t.value == tokens.T_Not:
        return next_token() and expr()

    elif t.type == tokens.T_Identifier:
        ident = t.value
        next_token()

        if(t.value == tokens.T_Equal):
            exprType = "AssignExpr"
            astree.create_node("  " + str(t.lineno) + "." + exprType + ":", find_node_id(t, exprType), parent=prevPar)
            assignTreeRoot = find_node_id(t, exprType)
            astree.create_node("  " + str(t.lineno) + "." + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=assignTreeRoot)
            astree.create_node("  " + str(t.lineno) + "." + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
            astree.create_node("  " + str(t.lineno) + "." + "Operator" + ": " + str(t.value), find_node_id(t, "Operator"), parent=assignTreeRoot)
        else: # todo: what happens when (
            exprType = "ArithmeticExpr"
        
        if assignTreeRoot == "":
            assignTreeRoot = prevPar

        if t.value == tokens.T_LP:
            next_token()
            return actuals()

        elif (t.value == tokens.T_Equal) or (t.value in tokens.op_list):

            if t.value in tokens.op_list:
                currOperator = str(t.value)
                if prevOperator == "":
                    exprTreeRoot = find_node_id(t, exprType)
                    exprTree.create_node("  " + str(t.lineno) + "." + exprType + ":", exprTreeRoot)
                    exprTree.create_node("  " + str(t.lineno) + "." + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=exprTreeRoot)
                    exprTree.create_node("  " + str(t.lineno) + "." + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                    exprTree.create_node("  " + str(t.lineno) + "." + "Operator" + ": " + currOperator, find_node_id(t, "Operator"), parent=exprTreeRoot)
                    prevOperator = currOperator
                    lastTreeRoot = exprTreeRoot

                elif tokens.precedence_list[prevOperator] >= tokens.precedence_list[currOperator]:

                    if currentTreeRoot != "":
                        exprTree.create_node("  " + str(t.lineno) + ".FieldAccess:", find_node_id(t, "FieldAccess"), parent=currentTreeRoot)
                        exprTree.create_node("  " + str(t.lineno) + ".Identifier: " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                        currentTreeRoot = ""
                    
                    else:
                        exprTree.create_node("  " + str(t.lineno) + ".FieldAccess:", find_node_id(t, "FieldAccess"), parent=exprTreeRoot)
                        exprTree.create_node("  " + str(t.lineno) + ".Identifier: " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                    
                    tempTree=Tree()
                    tempTreeRoot = find_node_id(t, exprType)
                    tempTree.create_node("  " + str(t.lineno) + "." + exprType + ":", tempTreeRoot)
                    tempTree.paste(tempTreeRoot, exprTree)
                    tempTree.create_node("  " + str(t.lineno) + ".Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                    exprTree = tempTree
                    exprTreeRoot = tempTreeRoot
                    prevOperator = currOperator
                    lastTreeRoot = tempTreeRoot

                elif tokens.precedence_list[prevOperator] < tokens.precedence_list[currOperator]:
                    tempTree=Tree()
                    tempTreeRoot = find_node_id(t, exprType)
                    tempTree.create_node("  " + str(t.lineno) + "." + exprType + ":", tempTreeRoot)
                    tempTree.create_node("  " + str(t.lineno) + ".FieldAccess:", find_node_id(t, "FieldAccess"), parent=tempTreeRoot)
                    tempTree.create_node("  " + str(t.lineno) + ".Identifier: " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                    tempTree.create_node("  " + str(t.lineno) + ".Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                    exprTree.paste(exprTreeRoot, tempTree)
                    prevOperator = currOperator
                    lastTreeRoot = tempTreeRoot
                    currentTreeRoot = tempTreeRoot
                
            next_token()
            return expr()
        else:
            printDebug("ture from expr Identifier" + str(t.value))
            if exprTree:
                exprTree.create_node("  " + str(t.lineno) + "." + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=lastTreeRoot)
                exprTree.create_node("  " + str(t.lineno) + "." + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                astree.paste(assignTreeRoot, exprTree)
                initExprTree()
            else:
                astree.create_node("  " + str(t.lineno) + "." + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=assignTreeRoot)
                astree.create_node("  " + str(t.lineno) + "." + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
            return True and update_parent(prevPar)
    
    elif t.type in tokens.const_list:
        
        constantVal = str(t.value)
        # done update for constant without args
        constant = str(t.type).split("_")[1]
        if t.type == tokens.T_StringConstant:
            constantType = "(args) " + constant
        else:
            constantType = constant

        """node_id = find_node_id(t, constant)
        node_label = "  " + str(t.lineno) + "." + "(args) " + constant + ": " + constantVal
        astree.create_node( node_label, node_id, parent=parent)"""
        
        next_token()
        
        exprType = "ArithmeticExpr"
        if assignTreeRoot == "":
            assignTreeRoot = prevPar

        if (t.value in tokens.op_list):
            currOperator = str(t.value)
            if prevOperator == "":
                exprTreeRoot = find_node_id(t, exprType)
                exprTree.create_node("  " + str(t.lineno) + "." + exprType + ":", exprTreeRoot)
                exprTree.create_node("  " + str(t.lineno) + "." + constantType + ": " +  constantVal, find_node_id(t, constantType), parent=exprTreeRoot)
                exprTree.create_node("  " + str(t.lineno) + "." + "Operator" + ": " + currOperator, find_node_id(t, "Operator"), parent=exprTreeRoot)
                prevOperator = currOperator
                lastTreeRoot = exprTreeRoot

            elif tokens.precedence_list[prevOperator] >= tokens.precedence_list[currOperator]:

                if currentTreeRoot != "":
                    exprTree.create_node("  " + str(t.lineno) + "." + constantType + ": " +  constantVal, find_node_id(t, constantType), parent=currentTreeRoot)
                    currentTreeRoot = ""
                
                else:
                    exprTree.create_node("  " + str(t.lineno) + "." + constantType + ": " +  constantVal, find_node_id(t, constantType), parent=exprTreeRoot)
                
                tempTree=Tree()
                tempTreeRoot = find_node_id(t, exprType)
                tempTree.create_node("  " + str(t.lineno) + "." + exprType + ":", tempTreeRoot)
                tempTree.paste(tempTreeRoot, exprTree)
                tempTree.create_node("  " + str(t.lineno) + ".Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                exprTree = tempTree
                exprTreeRoot = tempTreeRoot
                prevOperator = currOperator
                lastTreeRoot = tempTreeRoot

            elif tokens.precedence_list[prevOperator] < tokens.precedence_list[currOperator]:
                tempTree=Tree()
                tempTreeRoot = find_node_id(t, exprType)
                tempTree.create_node("  " + str(t.lineno) + "." + exprType + ":", tempTreeRoot)
                tempTree.create_node("  " + str(t.lineno) + "." + constantType + ": " +  constantVal, find_node_id(t, constantType), parent=tempTreeRoot)
                tempTree.create_node("  " + str(t.lineno) + ".Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                exprTree.paste(exprTreeRoot, tempTree)
                prevOperator = currOperator
                lastTreeRoot = tempTreeRoot
                currentTreeRoot = tempTreeRoot

            return next_token() and expr()
        elif t.value == ".":
            next_token()
            handleError(t)
            return False
        else:
            printDebug("ture from expr Constant" + str(t.value))

            if exprTree:
                exprTree.create_node("  " + str(t.lineno) + "." + constantType + ": " +  constantVal, find_node_id(t, constantType), parent=lastTreeRoot)
                astree.paste(assignTreeRoot, exprTree)
                initExprTree()
            else:
                astree.create_node("  " + str(t.lineno) + "." + constantType + ": " +  constantVal, find_node_id(t, constantType), parent=assignTreeRoot)

            return True and update_parent(prevPar)
    
    elif t.value == tokens.T_ReadInteger or t.value == tokens.T_ReadLine:
        printDebug("ReadInteger or ReadLine found")
        if (next_token() and t.value == tokens.T_LP) and (next_token() and t.value == tokens.T_RP):
            next_token()
            return True

    else:
        printDebug("exit expr false " + str(t.value))
        handleError(t)
        return False


def actuals():
    printDebug("------actuals")
    if t.value == tokens.T_RP:
        return True

    while True:
        printDebug("insilde actual loop " + str(t))    
        if not expr():
            handleError(t)
            return False
        
        if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
            continue
        if t.value == tokens.T_RP:
            next_token()
            return True
        else:
            handleError(t)
            return False



#start program
def main():
    printDebug(program_start())
    if errorFound == False:
        print()
        astree.show(key = False, line_type = 'ascii-sp')

if __name__ == "__main__":
    main()