

import os
import sys
from pathlib import Path

smallLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
capLetters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
arithmetics = ['+','-','*','/']
compares=['=','<','>', '<=', '>=', '<>']
symbols = [':=', ';',',']
otherSymbols = ['(',')','[',']','{','}']
keywords = ['program','declare','if','loop','else','while','doublewhile','exit','forcase','incase','when','default']
otherKeywords = ['not','and','or','function','procedure','call','return','in','inout','input','print']
allKeys=keywords+otherKeywords
whitespace =[" ","\t","\n"]
ALPHABET = smallLetters + capLetters + numbers + arithmetics + symbols + otherSymbols + keywords + otherKeywords + compares + [':'] + whitespace
allSymbols=arithmetics+symbols+otherSymbols+compares

f = ""
#filepath= ("C:/Users/nickk/Desktop/test9.min")
#f = open(filepath,"r")

#lexical analyzer
token = -1
tokenid = -1
wordID = 21
numberID = 100
error=-1
state0=0
state1=1
state2=2
state3=3
state4=4
state5=5
state6=6
ok=-2
pos=0
state=state0

#intermediate
quadline = 0
tempnumber = 0 #T0..T1..TN for temporary variables
quadlist = []

#syntax analyzer
head = 0
decl = [] #all declarations
declareID = "" #constant name
stack = [] #id of every par (empties every time a new function is called)
allDeclarations = [] #tsekarei an uparxei declare variable idio me statement variable
seenDeclarations = set()
allFunctions = []
func = 0
funcName = ""
progName = ""
frame = 0
currentLevel = 0 #current scope level

cCode = []

#symbol table
symbolTable = []

#final code initializers
finalCode = []
counter = 0
funcDict = {}
lineNumDict = {}
linenum = 0
position = 0
visited = []


############################################################
#                       LEXICAL                            #
############################################################


def tokenize(tokens,ids):#pou anikoun kai ti arithmo exoun
    global token,tokenid
    token=tokens
    tokenid=ids

    
def lexical():
    global state,wordID,numberID,f,pos
    lex=''
    stri=''
    f.seek(pos)
    while(state!=ok and state!=error):
        c=f.read(1)
        if(c in whitespace and state==state0):
        
            continue
        if((c in capLetters or c in smallLetters)and state==state0):
            state=state1
            lex+=c
            continue
        if ((c in capLetters or c in smallLetters or c in numbers)and state==state1):
            state=state1
            lex+=c
            continue
        if((c not in capLetters or c in smallLetters or c in numbers)and state==state1):
            state=ok
            if(lex=="program"):
                tokenize("program",1)
                pos=f.tell()-1
            elif(lex=="declare"):
                tokenize("declare",2)
                pos=f.tell()-1
            elif(lex == "if"):
                tokenize("if",3)
                pos=f.tell()-1
            elif(lex=="else"):
                tokenize("else",4)
                pos=f.tell()-1
            elif(lex=="while"):
                tokenize("while",5)
                pos=f.tell()-1
            elif(lex=="forcase"):
                tokenize("forcase",6)
                pos=f.tell()-1
            elif(lex=="incase"):
                tokenize("incase",7)
                pos=f.tell()-1
            elif(lex=="when"):
                tokenize("when",8)
                pos=f.tell()-1
            elif(lex=="default"):
                tokenize("default",9)
                pos=f.tell()-1
            elif(lex=="not"):
                tokenize("not",10)
                pos=f.tell()-1
            elif(lex=="and"):
                tokenize("and",11)
                pos=f.tell()-1	
            elif(lex=="or"):
                tokenize("or",12)
                pos=f.tell()-1	
            elif(lex=="function"):
                tokenize("function",13)
                pos=f.tell()-1	
            elif(lex=="procedure"):
                tokenize("procedure",14)
                pos=f.tell()-1	
            elif(lex=="call"):
                tokenize("call",15)
                pos=f.tell()-1		
            elif(lex=="return"):
                tokenize("return",16)
                pos=f.tell()-1
            elif(lex=="in"):
                tokenize("in",17)
                pos=f.tell()-1
            elif(lex=="inout"):
                tokenize("inout",18)
                pos=f.tell()-1
            elif(lex=="input"):
                tokenize("input",19)
                pos=f.tell()-1
            elif(lex=="print"):
                tokenize("print",20)
                pos=f.tell()-1		
            else:    
                tokenize(lex,wordID)
                wordID += 1
                pos=f.tell()-1
        if(c in numbers and state==state0):
            state=state2
            lex+=c
            continue
        if(c in numbers and state==state2):
            lex+=c
            continue
        if(c not in numbers and state==state2):
            tokenize(lex,numberID)
            state=ok
            pos=f.tell()-1
        if(c == '+' and state==state0):
            tokenize('+',151)
            state=ok
            pos=f.tell()
        if(c == '-' and state==state0):
            tokenize('-',152)
            state=ok
            pos=f.tell()
        if(c == '*' and state==state0):
            tokenize('*',153)
            state=ok
            pos=f.tell()
        if(c=='/' and state==state0):
            lex+=c
            c=f.read(1)
            lex+=c
            if(lex!='/*' and lex!='//'):
                tokenize('/',154)
                state=ok
                pos=f.tell()-1
            elif(lex=="//"):
                f.readline()
                state=state0
                pos=f.tell()
                lex=''
            else:
                c=f.read(1)
                while("*/" not in lex):
                    c=f.read(1)
                    if(c==''):
                        state=error
                        break
                    lex+=c 
                pos=f.tell()
                state=state0
                lex=''
        if(c == '=' and state==state0):
            tokenize('=',155)
            state=ok
            pos=f.tell()
        if(c == '<' and state==state0):
            state=state3
            lex+=c
            continue
        if(c == '=' and state==state3):
            tokenize("<=",156)
            state=ok
            pos=f.tell()
        if(c == '>' and state==state3):
            tokenize("<>",157)
            state=ok
            pos=f.tell()
        if(state==state3):
            tokenize('<',158)
            state=ok
            pos=f.tell()-1
        if(c == '>' and state==state0):
            state=state4
            lex+=c
            continue
        if(c == '=' and state==state4):
            tokenize(">=",159)
            state=ok
            pos=f.tell()
        if(state==state4):
            tokenize('>',160)
            state=ok
            pos=f.tell()-1
        if(c == ':' and state==state0):
            state=state5
            lex+=c
            continue
        if(c == '=' and state==state5):
            tokenize(":=",161)
            state=ok
            pos=f.tell()
        if(state == state5):
            tokenize(lex,162)
            state=ok
            pos=f.tell()-1
        if(state==state5):
            state=error
            pos=f.tell()
        if(c == ';' and state==state0):
            tokenize(';',163)
            state=ok
            pos=f.tell()
        if(c == ',' and state==state0):
            tokenize(',',164)
            state=ok
            pos=f.tell()
        if(c == '(' and state==state0):
            tokenize('(',165)
            state=ok
            pos=f.tell()
        if(c == ')' and state==state0):
            tokenize(')',166)
            state=ok
            pos=f.tell()
        if(c == '[' and state==state0):
            tokenize('[',167)
            state=ok
            pos=f.tell()
        if(c == ']' and state==state0):
            tokenize(']',168)
            state=ok
            pos=f.tell()
        if(c=='{' and state==state0):
            tokenize('{',169)
            state=ok
            pos=f.tell()
        if(c=='}' and state==state0):
            tokenize('}',170)
            state=ok
            pos=f.tell()
        if(c=='' and state==state0):
            tokenize("EOF",171)
            state=ok
            pos=f.tell()
            sys.exit("EOF")
        if(c not in ALPHABET):
            state=error
            pos = f.tell()
        
    if(state==error):
        sys.exit("Invalid syntax in this (" + repr(pos) + ") position")
        
    state=state0

    
###################################################
#                    FINAL CODE                   #      
###################################################

def searchEntities(name):
    global symbolTable,progName
    currentScope = symbolTable[-1]
    for i in currentScope.entities:
        if(name == i.name):
            return i
    else:
        while(currentScope.functionName != progName and currentScope.enclosingScope.functionName != "global"):
            currentScope = currentScope.enclosingScope
            entities = currentScope.entities
            for i in entities:
                if(i.name == name):
                    return i
    

def searchLevelScopeOfEntity(name):
    global symbolTable,progName
    currentScope = symbolTable[-1]
    scopeLevel = 0 
    for i in currentScope.entities:
        if(name == i.name):
            return scopeLevel
    else:
        while(currentScope.functionName != progName and currentScope.enclosingScope.functionName != "global"):
            scopeLevel += 1
            currentScope = currentScope.enclosingScope
            entities = currentScope.entities
            for i in entities:
                if(i.name == name):
                    return scopeLevel
    

def gnvlcode(name):
    global finalCode
    entity = searchEntities(name)
    finalCode.append("\t" +"lw $t0,-4($sp)\n")
    numberOfLoops = searchLevelScopeOfEntity(name) - 1
    for i in range(0,numberOfLoops):
        finalCode.append("\t" +"lw $t0,-4($t0)\n")
    finalCode.append("\t" +"addi $t0,$t0,-" +str(entity.offset) + "\n")

def loadvr(name,reg):
    global finalCode,symbolTable
    entity = searchEntities(name)
    if(name.isdigit()):#if entity is a constant
        finalCode.append("\t" +"li $t" + reg + "," + name + "\n")
    elif(globalVar(name) and (entity.typeOf != "par")):#if entity belongs to main
        finalCode.append("\t" +"lw $t" + reg + ",-" + str(calcOffset(name)) + "($s0)\n")
    elif(searchLevelScopeOfEntity(name) == 0 and (entity.typeOf == "var" or entity.typeOf == "temp" or (entity.typeOf == "par" and entity.parMode == "cv"))):#if entity is a local variable in the function
        finalCode.append("\t" +"lw $t" + reg + ",-" + str(calcOffset(name)) + "($sp)\n")#or parameter of type in
    elif(searchLevelScopeOfEntity(name) == 0 and (entity.typeOf == "par" and entity.parMode == "ref")):#same scope and par type "inout"
        finalCode.append("\t" +"lw $t0" + ",-" +  str(calcOffset(name)) + "($sp)\n")
        finalCode.append("\t" + "lw $t" + reg + "," + "($t0)\n")
    elif((searchLevelScopeOfEntity(name) > 0) and ((entity.typeOf == "var") or (entity.typeOf == "par" and entity.parMode == "cv"))):#check parenthesis
        gnvlcode(name)  #if entity in parent scopes and local var or par type "in" in this parent scope  
        finalCode.append("\t" +"lw $t" + reg + "," + "($t0)\n")
    elif((searchLevelScopeOfEntity(name) > 0) and (entity.typeOf == "par" and entity.parMode == "ref")):#entity in parent scopes and par type "inout"
        gnvlcode(name)
        finalCode.append("\t" +"lw $t0" + "," + "($t0)\n")
        finalCode.append("\t"+ "lw $t" + reg + "," + "($t0)\n")
        
def globalVar(name):
    global symbolTable
    for i in symbolTable[0].entities:
        if(i.name == name):
            return True
    return False

def storerv(reg,name):
    global finalCode,symbolTable
    entity = searchEntities(name)
    if(globalVar(name) and (entity.typeOf != "par")):
        finalCode.append("\t" +"sw $t" + reg + ",-" + str(calcOffset(name)) + "($s0)\n")
    elif(searchLevelScopeOfEntity(name) == 0 and (entity.typeOf == "var" or entity.typeOf == "temp" or (entity.typeOf == "par" and entity.parMode == "cv"))):#if entity is a local variable in the function
        finalCode.append("\t" +"sw $t" + reg + ",-" + str(calcOffset(name)) + "($sp)\n")
    elif(searchLevelScopeOfEntity(name) == 0 and (entity.typeOf == "par" and entity.parMode == "ref")):
        finalCode.append("\t" +"lw $t0" + ",-" +  str(calcOffset(name)) + "($sp)\n")
        finalCode.append("\t" + "sw $t" + reg + "," + "($t0)\n")
    elif((searchLevelScopeOfEntity(name) > 0) and ((entity.typeOf == "var") or (entity.typeOf == "par" and entity.parMode == "cv"))):
        gnvlcode(name)  #if entity in parent scopes and local var or par type "in" in this parent scope  
        finalCode.append("\t" +"sw $t" + reg + "," + "($t0)\n")
    elif((searchLevelScopeOfEntity(name) > 0) and (entity.typeOf == "par" and entity.parMode == "ref")):#entity in parent scopes and par type "inout"
        gnvlcode(name)
        finalCode.append("\t" +"lw $t0" + "," + "($t0)\n")
        finalCode.append("\t" + "sw $t" + reg + "," + "($t0)\n")

def allOperators(op):
    if (op == "="):
        return "beq"
    elif (op == "<>"):
        return "bne"
    elif (op == ">"):
        return "bgt"
    elif (op == "<"):
        return "blt"
    elif (op == ">="):
        return "bge"
    elif (op == "<="):
        return "ble"
    elif (op == "+"):
        return "add"
    elif (op == "-"):
        return "sub"
    elif (op == "*"):
        return "mul"
    elif (op == "/"):
        return "div"

def insertPars(quad,i):
    global finalCode
    entity = searchEntities(quad[1])
    if(quad[2] == "CV"):
        loadvr(quad[1],str(0))
        finalCode.append("\t" +"sw $t0" + "," + str(-(12+4*i)) + "($fp)\n")
    elif((quad[2] == "REF") and (searchLevelScopeOfEntity(quad[1]) == 0) and (entity.typeOf == "var" or entity.typeOf == "temp" or (entity.typeOf == "par" and entity.parMode == "cv"))):
        finalCode.append("\t" +"addi $t0,$sp" + ",-" + str(calcOffset(quad[1])) + "\n")
        finalCode.append("\t" + "sw $t0" + "," + str(-(12+4*i)) + "($fp)\n")
    elif((quad[2] == "REF") and (searchLevelScopeOfEntity(quad[1]) == 0) and (entity.typeOf == "par" and entity.parMode == "ref")):
        finalCode.append("\t" +"lw $t0" + ",-" + str(calcOffset(quad[1])) + "($sp)\n")
        finalCode.append("\t" + "sw $t0" + "," + str(-(12+4*i)) + "($fp)\n")
    elif((quad[2] == "REF") and (searchLevelScopeOfEntity(quad[1]) > 0) and (entity.typeOf == "var" or entity.typeOf == "temp" or (entity.typeOf == "par" and entity.parMode == "cv"))):
        gnvlcode(quad[1])
        finalCode.append("\t" +"sw $t0" + "," + str(-(12+4*i)) + "($fp)\n")
    elif((quad[2] == "REF") and (searchLevelScopeOfEntity(quad[1]) > 0) and (entity.typeOf == "par" and entity.parMode == "ref")):
        gnvlcode(quad[1])
        finalCode.append("\t" +"lw $t0" + "," + "($t0)\n")
        finalCode.append("\t"+ "sw $t0" + "," + str(-(12+4*i)) + "($fp)\n")
    elif(quad[2] == "RET"):
        finalCode.append("\t" +"addi $t0" + "," + "$sp" + ",-" + str(calcOffset(quad[1])) + "\n")
        finalCode.append("\t" + "sw $t0" + ",-8($fp)" + "\n")


       
def calcOffset(name):
    global visited
    prevScope = symbolTable[-1]
    counter = 0
    posOfFunc = 0
    entity = searchEntities(name)
    if(prevScope.functionName != "global"):
        for j,i in enumerate(prevScope.entities):
            if(i.typeOf == "func"):
                counter += 1
                posOfFunc = j
    if(prevScope.functionName != "global"):            
        for i,j in enumerate(prevScope.entities):
            if(entity.name == j.name and entity.typeOf != "func" and  i > posOfFunc and (entity.name not in visited)):
                entity.offset = entity.offset - 4*counter
                visited.append(entity.name)
                return entity.offset
            else:
                continue        
        return entity.offset                       
                

            
def finalCodeAsm():
    global finalCode,quadlist,position,linenum,funcDict
    for i in range(position,len(quadlist)):
        item = quadlist[i].split('\n')
        finalCode.append("L" + str(linenum) + ":")
        for j in item:
            quad = j.split(",")
            if(quad[0] == "begin_block"):
                lineNumDict [quad[1]] = linenum-1
                    
            if(quad[0] == "begin_block" or quad[0] == "end_block" or quad[0] == "halt"):
                linenum -= 1
                del finalCode[-1]
            if(quad[0] == "jump"):
                finalCode.append("\t" + "j " + "L" + quad[3] + "\n")
            elif(quad[0] in compares):
                loadvr(quad[1],str(1))
                loadvr(quad[2],str(2))
                finalCode.append("\t" + allOperators(quad[0]) + " $t1,$t2,L" + quad[3] + "\n")
            elif(quad[0] == ":="):
                loadvr(quad[1],str(1))
                storerv(str(1),quad[3])
            elif(quad[0] in arithmetics):
                loadvr(quad[1],str(1))
                loadvr(quad[2],str(2))
                finalCode.append("\t" + allOperators(quad[0]) + " $t1,$t1,$t2" + "\n")
                storerv(str(1),quad[3])
            elif(quad[0] == "out"):
                finalCode.append("\t" + "li $v0,1\n")
                loadvr(quad[1],str(0))
                finalCode.append("\t" + "move $a0, $t0\n")
                finalCode.append("\t" + "syscall\n")
            elif(quad[0] == "inp"):
                finalCode.append("\t" + "li $v0,5\n")
                finalCode.append("\t" + "syscall\n")
                finalCode.append("\t" + "move $t1, $v0\n")
                storerv(str(1),quad[1])
            elif(quad[0] == "retv"):
                loadvr(quad[1],str(1))
                finalCode.append("\t" + "lw $t0,-8($sp)\n")
                finalCode.append("\t" + "sw $t1,($t0)\n")
            elif(quad[0] == "par"):
                del finalCode[-1]
            elif(quad[0] == "call"):
                func = searchEntities(quad[1])
                del finalCode[-1]
                start = position - 1
                p = linenum
                quadPars = quadlist[start].split(",")
                while(quadPars[0]== "par"):
                    start -= 1
                    quadPars = quadlist[start].split(",")
                    p = p-1
                j = 0
                p = p-1
                for i in range(p,linenum-1):
                    if(i == p):
                        finalCode.append("L" + str(i+1) + ":\t")
                        finalCode.append("addi $fp,$sp," + str(func.framelength) + "\n")
                        insertPars(quadlist[i].split(","),j)
                        finalCode.append("\n")
                        j += 1
                    else:
                        finalCode.append("L" + str(i+1) + ":")
                        insertPars(quadlist[i].split(","),j)
                        finalCode.append("\n")
                        j += 1
                if(funcDict.get(func.name) == 0):
                    finalCode.append("L" + str(linenum))
                    finalCode.append("\t" + "lw $t0, -4($sp)\n")
                    finalCode.append("\t" + "sw $t0, -4($fp)\n")
                    linenum+=1
                else:
                    finalCode.append("L" + str(linenum))
                    finalCode.append("\t" + "sw $sp, -4($fp)\n")
                    linenum+=1
                finalCode.append("\t" + "addi $sp, $sp," + str(func.framelength) + "\n")
                if quad[1] in lineNumDict:
                    finalCode.append("\t" + "jal L" + str(lineNumDict.get(quad[1])) + " \n")
                finalCode.append("\t" + "addi $sp, $sp,-" + str(func.framelength) + "\n")
                linenum -=1
        position +=1            
        linenum +=1    
        finalCode.append("\n")   
            
    
def assemblyFile():
    global finalCode
    assemblyFile = "assemblyFile.asm"
    assemblyOpenFile = open(assemblyFile,"w+")
    for i in finalCode:
        assemblyOpenFile.write(i)
            




    
###################################################
#                   SYMBOL TABLE                  #
###################################################


class Scope:
    def __init__(self,entities,nestingLevel,enclosingScope,functionName):
        self.entities = entities
        self.nesting = nestingLevel 
        self.enclosingScope = enclosingScope
        self.functionName = functionName

class Entity:
    name = ""
    value = ""
    offset = ""
    typeOf = ""
    startQuad = ""
    args = []
    framelength=0
    nextEnt = None
    parMode = ""

class Argument:
    parMode = ""
    typeOf = ""
    nextArg = None
	
def addScope(scope):
    global symbolTable
    symbolTable.append(scope)

def deleteScope():
    global symbolTable,allDeclaration,allFunctions,seenDeclarations,seenFunctions,progName,position,linenum,funcDictfunc
    doublesCheck()
    allDeclarations = []
    seenDeclarations = set()
    funcDict [symbolTable[-1].functionName] = symbolTable[-1].nesting
    if(symbolTable[-1].functionName == progName):
        mainlen = str((len(symbolTable[0].entities)-1)*4+12)
        linenum += 1
        finalCode.append("\nLmain: \n")
        if(func == 1):
            finalCode.append("\nL" + str(linenum)+ ":\t" + "addi $sp,$sp," + mainlen + "\n")
        else:
            linenum = 0
            finalCode.append("\nL" + str(linenum)+ ":\t" + "addi $sp,$sp," + mainlen + "\n")
        linenum += 1
        finalCode.append("\t" + "move $s0,$sp\n\n")
        finalCodeAsm()
    else:
        entities = symbolTable[-1].enclosingScope.entities
        linenum += 1
        finalCode.append("\nL" + str(linenum) + ":\t" + "sw $ra,($sp)\n")
        linenum += 1
        entities[-1].framelength = len(symbolTable[-1].entities)*4 + 12
        finalCodeAsm()
        finalCode.append("L"+ str(linenum) + ":\t" + "lw $ra,($sp)\n")
        finalCode.append("\t" + "jr $ra\n")
		
        
    for i in symbolTable[-1].entities:
        if(i.typeOf == "func"):
            for j in i.args:
                del j
        del i
    
    del symbolTable[-1]

def searchEntity(name):
    global symbolTable
    for i in symbolTable:
        for j in i.entities:
            if(j.name == name):
                return j
        if(name not in j.name):
            return 0

        
def doublesCheck():
    global symbolTable,allDeclarations,seen
    seen = set()
    notseen = []
    for i in allDeclarations:
        if i not in seenDeclarations:
            seenDeclarations.add(i)
        else:
            sys.exit("Error: same name declaration in the same Scope")
            
def doublesCheckFunc(name):
    global allFunction
    if name not in allFunctions:
        allFunctions.append(name)
    else:
        sys.exit("Error: same function name detected.")


###################################################
#                   C FILE                        #
###################################################


def c_file():
    global cCode
    c_code()
    cfile = "cfile.c"
    cCodeFile = open(cfile,"w+")
    for i in cCode:
        cCodeFile.write(i)
        
def c_code():
    global quadlist,cCode,decl,func
    cCode = []
    pnt = "#include <stdio.h>\n\n"
    cCode.append(pnt)
    pnt = "int main()\n{\n"
    cCode.append(pnt)
    pnt = "\tint "
    for i in decl:
        pnt = pnt + i
        if(decl.index(i) < (len(decl) - 1)):
            pnt = pnt + ","
        else:
            pnt = pnt + ";\n"
    cCode.append(pnt)    
    linenum = 0
    linenum += 1
    line = "\tL_%d:\n" %(linenum)
    cCode.append(line)
    for i in quadlist:
        item = i.split(",")
        if(item[0] != "begin_block" and item[0] != "end_block"):
            pnt = " "
            linenum += 1
            line = "\tL_%d:" %(linenum)
            pnt = pnt + line
            last = item[3].strip("\n")
            if(item[0] == ":="):
                pnt = pnt + last + " = " + item[1] + ";\n"
            elif(item[0] == "+"):
                pnt = pnt + last + " = " + item[1] + " + " + item[2] + ";\n"	
            elif(item[0] == "-"):
                pnt = pnt + last + " = " + item[1] + " - " + item[2] + ";\n"	
            elif(item[0] == "*"):
                pnt = pnt + last + " = " + item[1] + " * " + item[2] + ";\n"	
            elif(item[0] == "/"):
                pnt = pnt + last + " = " + item[1] + " / " + item[2] + ";\n"	
            elif(item[0] == "="):
                pnt = pnt + "if (" + item[1] + " == " + item[2] + ") goto L_" + last + ";\n"
            elif(item[0] == "<="):
                pnt = pnt + "if (" + item[1] + " <= " + item[2] + ") goto L_" + last + ";\n"
            elif(item[0] == ">="):
                pnt = pnt + "if (" + item[1] + " >= " + item[2] + ") goto L_" + last + ";\n"
            elif(item[0] == ">"):
                pnt = pnt + "if (" + item[1] + " > " + item[2] + ") goto L_" + last + ";\n"  
            elif(item[0] == "<"):
                pnt = pnt + "if (" + item[1] + " < " + item[2] + ") goto L_" + last + ";\n"	
            elif(item[0] == "<>"):
                pnt = pnt + "if (" + item[1] + " != " + item[2] + ") goto L_" + last + ";\n"
            elif(item[0] == "jump"):
                pnt = pnt + "goto L_" + last + ";\n"
            elif(item[0] == "out"):
                pnt = pnt + 'printf("%d",' + item[1] + ");\n"
            elif(item[0] == "inp"):
                pnt = pnt + 'scanf("%d",&' + item[1] + ");\n"
            elif(item[0] == "ret"):
                pnt = pnt + 'return ' + item[1] + ";\n"
            elif(item[0] == "halt"):
                pnt = pnt + "{}\n"
            cCode.append(pnt)
    pnt = "\n}"
    cCode.append(pnt)
    if(func == 1):
        print("Error while making C file. Function detected.")

    
###################################################
#               INTERMEDIATE CODE                 #
###################################################



def nextquad():
    global quadline
    temp = quadline + 1
    return(temp)

def genquad(op,x,y,z):
    global quadline,quadlist
    quadline += 1
    temptext = (str(op) + "," + str(x) + "," + str(y) + "," + str(z) + "\n")
    quadlist.append(temptext)

def newtemp():
    global tempnumber,decl,stack
    tempnumber += 1
    newtemp = "T_%d" %(tempnumber)
    decl.append(newtemp)
    stack.append(newtemp)
    tmp = Entity()
    tmp.name = newtemp
    tmp.typeOf = "temp"
    tmp.offset = (len(symbolTable[-1].entities) * 4) + 12
    if(len(symbolTable[-1].entities)>0):
        symbolTable[-1].entities[-1].nextEnt = tmp
    symbolTable[-1].entities.append(tmp)
    return newtemp


def emptylist():
	empty = []
	return empty

def makelist(x):
	newlist = [x]
	return newlist

def mergelist(list1,list2):
	temp = list1 + list2
	return temp

def backpatch(list,z):
	global quadlist
	for i in list:
		line = quadlist[i-1]
		items = line.split(',')
		items[3] = str(z)
		line = items[0] + "," + items[1] + "," + items[2] + "," + items[3] + "\n"
		quadlist[i-1] = line

def int_file():
    intfile = "intermediate.int"
    intermediate_file = open(intfile,"w+")
    for i,j in enumerate(quadlist):
        intermediate_file.write(str(i+1) + " : " + j)    

    
###################################################
#               SYNTAX ANALYZER                   #
###################################################


def program():
    global progName,currentLevel,symbolTable,finalCode
    lexical()
    if(token=='program'):
        lexical()
        if(tokenid >= 21 and tokenid <= 100):
            progName = token
            lexical()
            if(token=='{'):
                entities = []
                initiateScope = Scope([],"global",None,"global") #the previous scope of main
                scp = Scope(entities,currentLevel,initiateScope,progName)
                addScope(scp)
                lexical()
                block()
                deleteScope()
                if(token == '}'):
                    genquad("halt","_","_","_") 
                    print("Everything ran smoothly")
                else:
                    sys.exit("Error: expected '}'")
                genquad("end_block",progName,"_","_")
            else:
                sys.exit("Error: expected '{'")
        else:
            sys.exit("Error: program name expected")
    else:
        sys.exit("Error: expected keyword 'program'")
            
    
def block():
    global progName,func,symbolTable
    if(token == 'declare'):
        declarations() 
    if(token == 'function' or token == 'procedure'):
        subprograms()
    if((tokenid < 100 or token == '{' ) and token != 'declare' and token != 'function' ):
        if(func == 0):
            genquad("begin_block",progName,"_","_")
        statements()

def declarations():
    while(1):
        if(token == 'declare'):
            lexical()
            varlist()
            if(token == ';'):
                lexical()
            else:
                sys.exit("Error: Expected ;")
        else:
            return
       
    
def varlist():
    global decl,symbolTable,stack,allDeclaratations
    if(tokenid >= 21 and tokenid <= 100):
        stack = []
        name = token
        allDeclarations.append(name)
        declaration = Entity()
        declaration.name = name
        declaration.typeOf = "var"
        declaration.offset = (len(symbolTable[-1].entities)*4) + 12
        if(len(symbolTable[-1].entities)>0):
            symbolTable[-1].entities[-1].nextEnt = declaration
        symbolTable[-1].entities.append(declaration)
        decl.append(name)
        lexical()
        while(1):
            if(token == ','):
                lexical()
                name = token
                
                if(tokenid < 21 and tokenid > 100):
                    sys.exit("Error: expected identifier")
                else:
                    allDeclarations.append(name)
                    declaration1 = Entity()
                    declaration1.name = name
                    declaration1.typeOf = "var"
                    declaration1.offset = (len(symbolTable[-1].entities)*4) + 12
                    if(len(symbolTable[-1].entities)>0):
                        symbolTable[-1].entities[-1].nextEnt = declaration1
                    symbolTable[-1].entities.append(declaration1)
                    decl.append(name)
                    lexical()                               
            else:
                return

def subprograms():
        global func
        func = 1 #c file(vgazei error)
        while(1):
            if(token == 'function'):
                lexical()
                subprogram()
            elif(token == 'procedure'):
                lexical()
                subprogram()
            else:
                return
            
def subprogram():
    global funcName,symbolTable,stack,head,frame,allFunctions,finalCode,counter
    if(tokenid >= 21 and tokenid <= 100):
        doublesCheckFunc(token)
        stack = []
        head = 0
        funcName = token
        function = Entity()
        counter += 1
        function.name = funcName
        function.typeOf = "func"
        function.startQuad = nextquad()
        function.args = []
        function.framelength = 0
        if(len(symbolTable[-1].entities) > 0):
            symbolTable[-1].entities[-1].nextEnt = function
        symbolTable[-1].entities.append(function)
        genquad("begin_block",funcName,"_","_")
        lexical()
        funcbody()
        if(counter == 1):
            finalCode.append("L0:\t" + "j Lmain\n")
        deleteScope() 
    else:
        sys.exit("Error: id expected")

def funcbody():
    ## FIX INOUTS
    global funcName,func,progName,currentLevel,symbolTable,head,frame
    formalpars()
    if(token == '{'):
        currentLevel += 1
        inouts = []
        function =  Scope([],currentLevel,symbolTable[-1],funcName)
        addScope(function)
        previousScope = function.enclosingScope
        entitiesOfPreviousScope = previousScope.entities
        for i in entitiesOfPreviousScope:
            if(i.name ==funcName):
                inouts = i.args
        
        if(head > 0):
            for i in range(head):
                parID = Entity()
                parID.name = stack[i]
                parID.typeOf = "par"
                parID.offset = 12 + len(symbolTable[-1].entities)*4
                parID.parMode = inouts[i].parMode
                if(len(symbolTable[-1].entities) > 0):
                    symbolTable[-1].entities[-1].nextEnt = parID
                symbolTable[-1].entities.append(parID)
        lexical()
        block()
        if(token != '}'):
            sys.exit("Error: expected '}'")
        genquad("end_block",funcName,"_","_")
        lexical()
        if(func == 1 and token != 'function' and token != 'procedure'):
            genquad("begin_block",progName,"_","_")
    else:
        sys.exit("Error: expected '{'")

def formalpars():
    if(token == '('):
        lexical()
        formalparlist()
        if(token == ')'):
            lexical()
            return
        else:
            sys.exit("Error: expected ')'")
    else:
        sys.exit("Error: expected '('")

def formalparlist():
    if(token == 'in' or token == 'inout'):
        parameter = Argument()
        if(token == "in"):
            parameter.parMode = "cv"
        else:
            parameter.parMode = "ref"
        parameter.typeOf = "var"
        if(len(symbolTable[-1].entities[-1].args) > 0):
            symbolTable[-1].entities[-1].args[-1].nextArg = parameter
        symbolTable[-1].entities[-1].args.append(parameter)
        lexical()
        formalparitem()
        while(1):
            if(token == ","):
                lexical()
                if(token == "in" or token == "inout"):
                    parameter1 = Argument()
                    if(token == "in"):
                        parameter1.parMode = "cv"
                    else:
                        parameter1.parMode = "ref"
                    parameter1.typeOf = "var"
                    if(len(symbolTable[-1].entities[-1].args) > 0):
                        symbolTable[-1].entities[-1].args[-1].nextArg = parameter1
                    symbolTable[-1].entities[-1].args.append(parameter1)
                    lexical()
                    formalparitem()
                else:
                    sys.exit("Error: expected in or inout")
            else:
                return

def formalparitem():
    global stack,head
    if(tokenid >= 21 and tokenid <= 100):
        head += 1
        stack.append(token)
        lexical()
        return
    else:
        sys.exit("Error: expected identifier")
        
def statements():
    if(token == '{'):
        lexical()
        statement()
        while(1):
            if(token == ';'):
                lexical()
                statement()
            elif(token == '}'):
                lexical()
                return
            else:
                sys.exit("Error: expected ';' or '}' after the statement")
                return
    else:
        statement()

def statement():
    global symbolTable,declareID
    if(tokenid >= 21 and tokenid <= 100):
        declareID = token    
        lexical()
        w = assignmentStat()
        genquad(":=",w,"_",declareID)
    elif(token == 'if'):
        lexical()
        ifStat()
    elif(token == 'while'):
        lexical()
        whileStat()
    elif(token == 'doublewhile'):
        lexical()
        doublewhileStat()
    elif(token == 'loop'):
        lexical()
        loopStat()
    elif(token == 'exit'):
        lexical()
        exitStat()
    elif(token == 'forcase'):
        lexical()
        forcaseStat()
    elif(token == 'incase'):
        lexical()
        incaseStat()
    elif(token == 'call'):
        lexical()
        callStat()
    elif(token == 'return'):
        lexical()
        returnStat()
    elif(token == 'input'):
        lexical()
        inputStat()
    elif(token == 'print'):
        lexical()
        printStat()
    else:
        lexical()
        sys.exit("Error: expected statement")
    

def assignmentStat():
    if(token == ':='):
        lexical()
        e = expression()
        return e
    else:
        sys.exit("Error: expected ':='")

def ifStat():
    if(token == '('):
        lexical()
        B = condition()
        B_true = B[0]
        B_false = B[1]
        if(token == ')'):
            lexical()
            if(token == 'then'):
                lexical()
                backpatch(B_true,nextquad())
                statements()
                iflist = makelist(nextquad())
                genquad("jump","_","_","_")
                backpatch(B_false,nextquad())
                elsepart()
                backpatch(iflist,nextquad())
            else:
                sys.exit("Error: expected 'then'")
        else:
            sys.exit("Error: expected ')'")
    else:
        sys.exit("Error: expected '('")

def elsepart():
    if(token == 'else'):
        lexical()
        statements()
    else:
        return

def whileStat():
    Bquad = nextquad()
    if(token == '('):
        lexical()
        B = condition()
        B_true = B[0]
        B_false = B[1]
        if(token == ')'):
            backpatch(B_true,nextquad())
            lexical()
            statements()
            genquad("jump","_","_",str(Bquad))
            backpatch(B_false,nextquad())
            return
        else:
            sys.exit("Error: expected ')'")
    else:
        sys.exit("Error: expected '('")

def doublewhile():
#removed
    if(token == '('):
        lexical()
        condition()
        if(token == ')'):
            lexical()
            statements()
            elsepart()
        else:
            sys.exit("Error: expected ')'")
    else:
        sys.exit("Error: expected '('")
        
def loopStat():
#removed
    statements()

def exit():
#removed
    return

def forcaseStat():
    Bquad = nextquad()
    lista = []
    while(1):
        if(token == 'when'):
            lexical()
            if(token == '('):
                lexical()
                B = condition()
                B_true = B[0]
                B_false = B[1]
                if(token == ')'):
                    lexical()
                    if(token == ':'):
                        backpatch(B_true,nextquad())
                        lexical()
                        statements()
                        m = makelist(nextquad())
                        lista = mergelist(lista,m)
                        genquad("jump","_","_","_")
                        backpatch(B_false,nextquad())
                    else:
                        sys.exit("Error: expected ':'")
                else:
                    sys.exit("Error: expected ')'")
            else:
                sys.exit("Error: expected '('")
        else:
            break
    if(token=='default'):
        lexical()
        if(token == ':'):
            lexical()
            statements()
            genquad("jump","_","_",str(Bquad))
            backpatch(lista,nextquad())
            return
        else:
            sys.exit("Error: expected ':'")
    else:
        sys.exit("Error: expected 'default'")
    

def incaseStat():
#removed
    while(1):
        if(token == 'when'):
            lexical()
            if(token == '('):
                lexical()
                condition()
                if(token == ')'):
                    lexical()
                    if(token == ':'):
                        lexical()
                        statements()
                    else:
                        sys.exit("Error: expected ':'")
                else:
                    sys.exit("Error: expected ')'")
            else:
                sys.exit("Error: expected '('")
        else:
            sys.exit("Error: expected 'when'")

def returnStat():
    e = expression()
    genquad("retv",e,"_","_")
    
def callStat():
    if(tokenid >= 21 and tokenid <= 100):
        name = token
        lexical()
        actualpars()
        genquad("call",name,"_","_")
    else:
        sys.exit("Error: expected identifier")

def printStat():
    if(token == '('):
        lexical()
        e = expression()
        if(token == ')'):
            lexical()
            genquad("out",e,"_","_")
        else:
            sys.exit("Error: expected ')'")
    else:
        sys.exit("Error: expected '('")

def inputStat():
    if(token == '('):
        lexical()
        if(tokenid >= 21 and tokenid <= 100):
            name = token
            lexical()
            if(token == ')'):
                lexical()
                genquad("inp",name,"_","_")
            else:
                sys.exit("Error: expected ')'")
        else:
            sys.exit("Error: expected identifier")
    else:
        sys.exit("Error: expected '('")
            
def actualpars():
    global func
    func = 1
    if(token == '('):
        lexical()
        a = actualparlist()
        if(token == ')'):
            w = newtemp()
            genquad("par",w,"RET","_")
            lexical()
            return w
        else:
            sys.exit("Error: expected ')'")
    else:
        sys.exit("Error: expected '('")
                
def actualparlist():
    if(token == 'in' or token == 'inout'):
        a = actualparitem()
        while(1):
            if(token == ','):
                lexical()
                if(token == 'in' or token == 'inout'):
                    actualparitem()
                else:
                    sys.exit("Error: expected in or inout")
            else:
                return a

def actualparitem():
    a = ""
    if(token == 'in'):
        a = token
        lexical()
        e = expression()
        genquad("par",e,"CV","_")
        return a
    elif(token == 'inout'):
        a = token
        lexical()
        if(tokenid >= 21 and tokenid <= 100):
            e = token
            genquad("par",token,"REF","_")
            lexical()
            return a
        else:
            sys.exit("Error: expected identifier")
    else:
        sys.exit("Error: expected 'in' or 'inout'")

def condition():
    Q1 = boolterm()
    B_false = Q1[1]
    B_true = Q1[0]
    while(1):
        if(token == 'or'):
            lexical()
            backpatch(B_false,nextquad())
            Q2 = boolterm()
            Q2_true = Q2[0]
            Q2_false = Q2[1]
            B_true = mergelist(B_true,Q2_true)
            B_false = Q2_false
        else:
            B = [B_true,B_false]
            return B

def boolterm():
    R1 = boolfactor()
    Q_true = R1[0]
    Q_false = R1[1]
    while(1):
        if(token == 'and'):
            lexical()
            backpatch(Q_true,nextquad())
            R2 = boolfactor()
            R2_false = R2[1]
            R2_true = R2[0]
            Q_false = mergelist(Q_false,R2_false)
            Q_true = R2_true
        else:
            Q = [Q_true,Q_false]
            return Q
        
def boolfactor():
    if(token == 'not'):
        lexical()
        if(token == '['):
            lexical()
            B = condition()
            if(token == ']'):
                lexical()
                R_true = B[1]
                R_false = B[0]
                R = [R_true,R_false]
                return R
            else:
                sys.exit("Error: expected ']'")
        else:
            sys.exit("Error: expected '['")
    elif(token == '['):
        lexical()
        R = condition()
        if(token == ']'):
            lexical()
            return R
        else:
            sys.exit("Error: expected ']'")
    else:
        E1 = expression()
        relop = relationalOper()
        E2 = expression()
        R_true = makelist(nextquad())
        genquad(str(relop),E1,E2,"_")
        R_false = makelist(nextquad())
        genquad("jump","_","_","_")
        R = [R_true,R_false]
        return R
    
def expression():
    optionalSign()
    t1 = term()
    while(1):
        if(token == '+' or token == '-'):
            op = token
            lexical()
            t2 = term()
            w = newtemp()
            genquad(op,t1,t2,w)
            t1 = w
        else:
            t = t1
            return t

def term():
    f1 = factor()
    while(1):
        if(token == '*' or token == '/'):
            op = token
            lexical()
            f2 = factor()
            w = newtemp()
            genquad(op,f1,f2,w)
            f1 = w
        else:
            f = f1
            return f
            

def factor():
    global symbolTable,declareID
    if(token == '('):
        lexical()
        e = expression()
        if(token == ')'):
            lexical()
            return e
        else:
            sys.exit("Error: expected ')'")
    elif(tokenid >= 21 and tokenid <100):
        name = token
        lexical()
        w=idtail()
        if(w == 0):
#           if(searchEntity(declareID)!=0):    
#               e = searchEntity(declareID)
#               if(searchEntity(name)!=0):
#                   valueOf = searchEntity(name)
#                   print(valueOf.typeOf)
#                  print(valueOf.name)
#                  print(valueOf.value)
#                 e.value = valueOf.value
                #else:
                   #print("Error in valueOf")
           #else:
            entity = Entity()
            entity.name = declareID
            entity.typeOf = "var"
            entity.offset = len(symbolTable[-1].entities)*4 + 12
                #if(searchEntity(name)!=0):
                    #values probably not working properly
                    #valueOf = searchEntity(name)
                    #entity.value = valueOf.value
            symbolTable[-1].entities.append(entity)
            return name
        else:
            genquad("call",name,"_","_")
            return w
    elif(tokenid >= 100 and tokenid <= 150 ):
        constant = token
        if(searchEntity(declareID)!=0):
            e = searchEntity(declareID)
            e.value = constant
            lexical()
            return constant
        else:
            entity = Entity()
            entity.name = declareID
            entity.typeOf = "constant"
            entity.offset = len(symbolTable[-1].entities)*4 + 12
            entity.value = constant
            symbolTable[-1].entities.append(entity)
            lexical()
            return constant  
    else:
        sys.exit("Error: invalid syntax")
        return
        
def idtail():
    if(token == '('):
        a = actualpars()
        return a
    else:
        return 0

def relationalOper():
    if(token == '='):
        op = token
        lexical()
        return op
    elif(token == '<='):
        op = token
        lexical()
        return op
    elif(token == '>='):
        op = token
        lexical()
        return op
    elif(token == '>'):
        op = token
        lexical()
        return op
    elif(token == '<'):
        op = token
        lexical()
        return op
    elif(token == '<>'):
        op = token
        lexical()
        return op

def optionalSign():
    if(token == "+" or token == "-"):
        lexical()
    else:
        return


#we don't use mulOper and addOper 
def mulOper():
    if(token == '*'):
        lexical()
        return
    elif(token == '/'):
        lexical()
        return

def addOper():
    if(token == '+'):
        lexical()
        return
    elif(token == '-'):
        lexical()
        return


def main(argv):
    global f
    path = Path().absolute()
    filepath=(Path(path,argv[1]))
    
    try:
        f = open(filepath,"r")
    except IOError:
        print("Give the whole path for the example.min file.")
    program()
    assemblyFile()
    int_file()
    c_file()
    f.close()
if __name__ == "__main__":
    main(sys.argv)
