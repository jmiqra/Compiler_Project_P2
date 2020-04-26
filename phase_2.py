"""
@author: iqrah
"""

import sys
import tokens
import phase_1

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
    printDebug("------decl " + str(t))
    if(t.value in tokens.type_list or t.value == tokens.T_Void):
        next_token()
        if(t.type == tokens.T_Identifier):
            next_token()
            if(t.value == tokens.T_LP):
                return functionDecl()
            else:
                return variableDecl() and next_token()
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
    if t.value == tokens.T_RP:
        return True
    while True:
        if t.value in tokens.type_list:
            next_token()
            if(t.type == tokens.T_Identifier):
                next_token()
                if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
                    continue
                elif t.value == tokens.T_RP:
                    return True
            else:
                handleError(t)
                return False

def stmtBlock():
    printDebug("------stmtBlock" + str(t))
    if t.value == tokens.T_LC:
        next_token()
        if t.value == tokens.T_RC:
            return True
        else:
            stmtBlockParam = variableDecl_2() and t.value == tokens.T_RC
            printDebug("~~~~~~ " + str(t))
            next_token()
            return stmtBlockParam

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
    
    elif expr() and t.value == tokens.T_SemiColon: #need to work:  prev work expr() semi nexttok stmt
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
    if t.value == tokens.T_SemiColon:
        printDebug("return done without expr" + str(t))
        return True
    elif expr() and t.value == tokens.T_SemiColon and next_token(): # next_token should be removed?
        printDebug("return done with expr" + str(t))
        return True
    else:
        handleError(t)
        return False
        
def printStmt():
    printDebug("------printStmt")
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
                continue
            elif t.value == tokens.T_RP:
                printDebug("RightParen found in printStmt")
                next_token()
                if t != None and t.value == tokens.T_SemiColon:
                    printDebug("semicolon after printDebug")
                    return True
                else:
                    handleError(t)
                    return False
    else:
        handleError(t)
        return False


def expr():
    printDebug("------expr " + str(t))

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
        next_token()
        if t.value == tokens.T_LP:
            next_token()
            return actuals()
        elif (t.value == tokens.T_Equal) or (t.value in tokens.op_list): 
            return next_token() and expr()
        else:
            printDebug("ture from expr Identifier" + str(t.value))
            return True
    
    elif t.type in tokens.const_list:
        next_token()
        if (t.value in tokens.op_list): 
            return next_token() and expr()
        elif t.value == ".":
            next_token()
            handleError(t)
            return False
        else:
            printDebug("ture from expr Constant" + str(t.value))
            return True
    
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

if __name__ == "__main__":
    main()