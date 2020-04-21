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

def program_start():
    print("------program")
    if not t:
        print("Empty program is syntactically incorrect.")
        return False
    return decl() and program()

def program():
    next_token()
    if not t:
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

def stmtBlock():
    print("------stmtBlock")
    if t.value == tokens.T_LC:
        next_token()
        if t.value == tokens.T_RC:
            return True
        else:
            return variableDecl_2()

def variableDecl_2():
    print("------variableDecl_2")
    if t.value == tokens.T_RC:
            return True
    if t.value in tokens.type_list and next_token() and t.type == tokens.T_Identifier:
        next_token()
        return variableDecl() and next_token() and variableDecl_2()
    else:
        while True:
            if stmt() and next_token():
               """ if(t.value == tokens.T_Else):
                    print("else found")
                    return True"""
                print("go to next stmt-----")
                pass
            else:
                return True



def variableDecl():
    print("------variableDecl")
    if(t.value == tokens.T_SemiColon):
        return True


def stmt():
    print("------stmt")
    print(t)
    if t.value == tokens.T_RC:
        return True
    #next_token()
    if t.value == tokens.T_If:
        return next_token() and ifStmt() and next_token() and stmt()
    elif t.value == tokens.T_While:
        return next_token() and whileStmt() and next_token() and stmt()
    elif t.value == tokens.T_For:
        return  next_token() and forStmt() and next_token() and stmt()
    elif t.value == tokens.T_Break:
        return  next_token() and breakStmt() and next_token and stmt()
    elif t.value == tokens.T_Return:
        return  next_token() and returnStmt()# and next_token() and stmt()
    elif t.value == tokens.T_Print: # and next_token() and t.value == tokens.T_LP:
        return  next_token() and printStmt() and next_token and stmt()
    elif t.value == tokens.T_LC:
        return stmtBlock()
    elif t.value == tokens.T_SemiColon:
        print("semi found ret from stmt")
        return True
    elif expr() and t.value == tokens.T_SemiColon: #need to work:  prev work expr() semi nexttok stmt
        print("ret from stmt ", t.value)
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
        ifparam = next_token() and expr() and t.value == tokens.T_RP
        if not ifparam:
            print("error from if ")
            return False
        print("inside ifparam true",t.value)
        if next_token() and not stmt():
            print("returnning false from if")
            return False

        if(t!=None and t.value != tokens.T_Else):
            next_token()
        
        if t != None and t.value == tokens.T_Else:
            print("else found----------------------------------------------------------------------")
            next_token()
            if not stmt():
                return False
            else:
                print("true for if with else----------------------")
                return True
        
        print("true for if----------------------")
        return True
    else:
        return False


def whileStmt():
    print("------whileStmt")
    if t.value == tokens.T_LP:
        while_param = next_token() and expr() and t.value == tokens.T_RP
        if not while_param:
            print("error from while")
            return False
        if next_token() and not stmt():
            print("returnning false from while")
            return False
        print("true for while----------------------",t.value)
        return True
    else:
        return False 

def forStmt():
    print("------forStmt")
    if t.value == tokens.T_LP:
        
        next_token()
        if t.value == tokens.T_SemiColon:
            pass
        next_token()
        if not stmt():
            return False
    else:
        return False

def breakStmt():
    print("------breakStmt")
    if t.value == tokens.T_SemiColon and next_token():
        return True

def returnStmt():
    print("------returnStmt")
    if t.value == tokens.T_SemiColon:
        print("return done without expr")
        return True
    elif expr() and t.value == tokens.T_SemiColon and next_token():
        print("return done with expr")
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
                continue
            elif t.value == tokens.T_RP:
                next_token()
                if t!=None and t.value == tokens.T_SemiColon:
                    print("semicolon after print")
                    return True
                else:
                    False
    else:
        False


def expr():
    print("------expr")
    if t.value == tokens.T_ReadInteger:
        return True
    elif t.value == tokens.T_ReadLine:
        return True
    elif t.value == tokens.T_Minus:
        return next_token() and expr()
    elif t.value == tokens.T_LP:
        print("inside lp ")
        if next_token() and expr() and t.value == tokens.T_RP:
            next_token()
            print("before semi inside expr")
            if t.value in tokens.op_list:
                return next_token() and expr()
            else:
                print("tru from expr lp cond")
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
            print("ture from expr ", t.value)
            return True
    
    elif t.type in tokens.const_list:
        next_token()
        if (t.value in tokens.op_list): 
            return next_token() and expr()
        else:
            print("exit expr true ")
            return True
    
    else:
        print("exit expr false ")
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