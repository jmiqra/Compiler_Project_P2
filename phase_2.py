"""
@author: iqrah
"""

import sys
import tokens
import phase_1


t = phase_1.get_next_token()
print(t)

def next_token():
    global t
    t = phase_1.get_next_token()
    print(t)
    if t != None:
        return True
    else:
        return False

def handleError(t):
    print("*** Error Line ", t.lineno, ".")
    print(phase_1.lines[t.lineno-1])
    print("*** syntax error")
    pass

def program_start():
    print("------program")
    if t == None:
        print("Empty program is syntactically incorrect.")
        return False
    return decl() and program()

def program():
    next_token()
    if t == None:
        print("Program ended successfully!")
        return True
    else:
        return program_start()


def decl():
    print("------decl")
    if(t.value in tokens.type_list or t.value == tokens.T_Void):
        next_token()
        if(t.type == tokens.T_Identifier):
            next_token()
            if(t.value == tokens.T_LP):
                return functionDecl()
            else:
                return variableDecl()
        else:
            print("Syntax Error 1 ", t)
    else:
         print("Syntax Error 2 ", t)

def functionDecl():
    print("------funtionDecl")
    next_token()
    params = formals()
    next_token()
    return params and stmtBlock()

def formals():
    print("------formals")
    if t.value == tokens.T_RP:
        return True
    elif t.value in tokens.type_list:
        next_token()
        if(t.type == tokens.T_Identifier):
            next_token()
            if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
                return next_token() and formals()
            elif t.value == tokens.T_RP:
                return True
        else:
            handleError(t)

def stmtBlock():
    print("------stmtBlock")
    if t.value == tokens.T_LC:
        next_token()
        if t.value == tokens.T_RC:
            return True
        else:
            stmtBlockParam = variableDecl_2() and t.value == tokens.T_RC
            next_token()
            return stmtBlockParam

def variableDecl():
    print("------variableDecl")
    if(t.value == tokens.T_SemiColon):
        return True
    else:
        handleError(t)

def variableDecl_2():
    print("------variableDecl_2")
    #if t.value == tokens.T_RC:
    #        return True
    if t.value in tokens.type_list and next_token() and t.type == tokens.T_Identifier:
        next_token()
        return variableDecl() and next_token() and variableDecl_2()
    else:
        while True:
            if stmt():
                if t.value == tokens.T_RC:
                    print("true from varDecl_2")
                    return True
                if(t.value == tokens.T_Else):
                    print("else found")
                    return True
                next_token()
                pass
            else:
                return True


def stmt():
    print("------stmt")
    print(t)
    if t.value == tokens.T_RC:
        print("True Stmt for RightCurly")
        return True
    #next_token()
    if t.value == tokens.T_If:
        print("If found from Stmt")
        if next_token() and ifStmt():
            if t.value == tokens.T_RC:
                print("RightCurly found after ifStmt")
                return True
            else:
                print("stmt from ifStmt")
                return stmt()
    
    elif t.value == tokens.T_While:
        print("While found from Stmt")
        if next_token() and whileStmt():
            if t.value == tokens.T_RC:
                print("RightCurly found after whileStmt")
                return True
            else:
                print("stmt from whileStmt")
                return stmt()
    
    elif t.value == tokens.T_For:
        print("For found from Stmt")
        return  next_token() and forStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_Break:
        print("Break found from Stmt")
        return  next_token() and breakStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_Return:
        print("Return found from Stmt")
        return  next_token() and returnStmt() # and next_token() and stmt()
    
    elif t.value == tokens.T_Print: # and next_token() and t.value == tokens.T_LP:
        print("Print found from Stmt")
        return  next_token() and printStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_LC:
        return stmtBlock()
    
    elif t.value == tokens.T_SemiColon:
        print("Semicolon found from stmt")
        return True
    
    elif expr() and t.value == tokens.T_SemiColon: #need to work:  prev work expr() semi nexttok stmt
        print("Expr and Semicolon found from stmt ", t.value)
        return True
        #print("ret from stmt ")
        #var = expr() and t.value == tokens.T_SemiColon and next_token()     
        #work for single statement
    #elif t != None:
    #    print("true from stmt last else")
    #    return stmt()

def ifStmt():
    print("----XXXXXXXXXXXXXXXXXXXXXXXXXx--ifStmt")
    if t.value == tokens.T_LP:
        ifParam = next_token() and expr() and t.value == tokens.T_RP
        if not ifParam:
            print("error from if ")
            return False
        
        print("inside ifParam true",t.value)
        
        if next_token() and not stmt():
            print("false from ifStmt")
            return False

        #if(t!=None and t.value != tokens.T_Else):
        if t.value == tokens.T_SemiColon:
            next_token()
        
        if t != None and t.value == tokens.T_Else:
            print("else found----------------------------------------------------------------------")
            next_token()
            if not stmt():
                print("False from if.. else..")
                return False
            else:
                print("true for if with else----------------------")
                return True
        else:
            print("true for if----------------------")
            return True
    else:
        handleError(t)
        return False


def whileStmt():
    print("------whileStmt")
    if t.value == tokens.T_LP:
        whileParam = next_token() and expr() and t.value == tokens.T_RP
        if not whileParam:
            print("error from whileStmt")
            return False
        if next_token() and not stmt():
            print("returnning false from whileStmt")
            return False
        print("true for while----------------------")
        return True
    else:
        return False 

def forStmt():
    print("------forStmt")
    if t.value == tokens.T_LP:
        print("LeftParen found forStmt")
        #1 for( ; )
        if next_token() and t.value == tokens.T_SemiColon:
            print("First expr not present inside forStmt")
            pass
        #1 for( i = 1 )
        elif not expr() or (next_token() and t.value != tokens.T_SemiColon):
            print("false for wrong first expr part inside forStmt")
            return False
        
        #2 for( i = 1; i > 5; )
        print("inside forStmt token -> ", t)
        next_token()
        if not expr() or not t.value == tokens.T_SemiColon:
            print("False for wrong second part inside forStmt")
            return False

        #3 for( i = 1; i > 5; )
        next_token()
        print("start forStmt last part -> ", t)
        if t.value == tokens.T_RP:
            print("No third part inside forStmt")
            return next_token() and stmt()
        elif expr() and t.value == tokens.T_RP:
            return next_token() and stmt()
    else:
        return False

def breakStmt():
    print("------breakStmt")
    if t.value == tokens.T_SemiColon:
        print("True from breakStmt", t)
        return True

def returnStmt():
    print("------returnStmt")
    if t.value == tokens.T_SemiColon:
        print("return done without expr", t)
        return True
    elif expr() and t.value == tokens.T_SemiColon and next_token(): # next_token should be removed?
        print("return done with expr", t)
        return True
    else:
        return False
        
def printStmt():
    print("------printStmt")
    if t.value == tokens.T_LP:
        while True:
            print("enter print loop--")
            next_token()        
            if not expr():
                print("false from printStmt")
                return False
            if t.value == tokens.T_Comma:
                print("Comma inside printStmt")
                continue
            elif t.value == tokens.T_RP:
                print("RightParen found in printStmt")
                next_token()
                if t != None and t.value == tokens.T_SemiColon:
                    print("semicolon after print")
                    return True
                else:
                    return False
    else:
        return False


def expr():
    print("------expr ", t)

    """if t.value == tokens.T_ReadInteger:
        return True
    elif t.value == tokens.T_ReadLine:
        return True"""
    
    if t.value == tokens.T_Minus:
        return next_token() and expr()
    
    elif t.value == tokens.T_LP:
        print("LeftParen found from expr")
        if next_token() and expr() and t.value == tokens.T_RP:
            next_token()
            if t.value in tokens.op_list:
                print("op_list found inside LeftParen expr")
                return next_token() and expr()
            else:
                print("true from expr LeftParen cond")
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
            print("ture from expr Identifier", t.value)
            return True
    
    elif t.type in tokens.const_list:
        next_token()
        if (t.value in tokens.op_list): 
            return next_token() and expr()
        else:
            print("ture from expr Constant", t.value)
            return True
    
    elif t.value == tokens.T_ReadInteger or t.value == tokens.T_ReadLine:
        print("ReadInteger or ReadLine found")
        if (next_token() and t.value == tokens.T_LP) and (next_token() and t.value == tokens.T_RP):
            next_token()
            return True

    else:
        print("exit expr false ", t.value)
        return False


def actuals():
    print("------actuals")
    if t.value == tokens.T_RP:
        return True
    next_token()
    
    if not expr():
        return False
    next_token()
    
    if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
        return next_token() and actuals()
    elif t.value == tokens.T_RP:
        return True
    else:
        return False



#start program
def main():
    print(program_start())

if __name__ == "__main__":
    main()