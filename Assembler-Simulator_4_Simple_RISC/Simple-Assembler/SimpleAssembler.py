import sys
file= sys.stdin.read().splitlines()
global error
global Flag 
error=False

Registeraddress={
    "R0":"000","R1":"001","R2":"010","R3":"011",
    "R4":"100","R5":"101","R6":"110",
    "FLAGS":"111"
}
Instructions={
    "add":["A","10000"],"sub":["A","10001"],"mul":["A","10110"],"xor":["A","11010"],"or":["A","11011"],"and":["A","11100"],
    "mov1":["B","10010"],"ls":["B","11001"],"rs":["B","11000"],
    "mov2":["C","10011"],"div":["C","10111"],"not":["C","11101"],"cmp":["C","11110"],
    "ld":["D","10100"],"st":["D","10101"],
    "jmp":["E","11111"],"jlt":["E","01100"],"jgt":["E","01101"],"je":["E","01111"],
    "hlt":["F","01010"]   
}
symbol = ["ld","st","mul",
        "add","sub","mov",
        "div","rs","ls",
        "xor","or","and",
        "not","cmp","jmp",
        "jlt","jgt","je","hlt"]

register=["R0","R1","R2","R3","R4","R5","R6"]
flagreg=["R0",
        "R1",
        "R2",
        "R3",
        "R4","R5","R6"
        "FLAGS"]
variable=[]
label=['hlt']
def checkA(lst,i):
    if(len(lst)==4):
        pass
    else:
        raise SyntaxError(f"Invalid syntax for {lst[0]} in line no {i+1}")
    for i in range(1,len(lst)):
        if(lst[i] in register):
            pass
        else:
            raise SyntaxError(f"Invalid name of  register like {lst[i]} in line no {i+1}")
        if(lst[i]!="FLAGS"):
            pass
        else:
            error=True
            raise SyntaxError(f"Invalid use of flag in line no {i+1}")
def checkB(lst,i):
        if(len(lst)==3):
            pass
        else:
            raise SyntaxError(f"Invalid syntax for {lst[0]} in line no {i+1}")
        if lst[1] in register and lst[1] != 'FLAGS':
                if 0<= int(lst[2][1:]) <=255:
                    pass
                else:
                    raise SyntaxError(f'Syntax error: Illegal immediate value at line {i+1}')
        else:
            raise SyntaxError(f'Syntax error: Typos in instruction name or register at line {i+1}')

def checkC(lst,i):
    if(len(lst)!=3):
        raise SyntaxError(f"Invalid syntax for {lst[0]} in line no{i+1}")
    if(lst[0]=="mov2" and lst[1]=="FLAGS" and lst[2]=="FLAGS"):
        raise SyntaxError(f"Invalid register or flag is defined in line no {i+1}")
    if(lst[0]!="mov2" and lst[1] not in register or lst[2] not in register):
        raise SyntaxError(f"Invalid syntax in line no {i+1}")

def checkD(lst,i):
    if(len(lst)!=3):
        raise SyntaxError(f"syntax error invalid syntax for {lst[0]} in line no{i+1}")
    if(lst[1] not in register):
        raise SyntaxError(f"Invalid register  is defined {i+1}")
    if(lst[2] not in variable):
        raise SyntaxError(f"invalid variable is {lst[2]} defined in line no {i+1}")
    elif(lst[2] in label):
        raise SyntaxError(f"labels cannot used in place of varaibles  in line no {i+1}")


def checkE(lst,i):
    if(len(lst)!=2):
        raise SyntaxError(f"syntax error invalid syntax for {lst[0]} in line no{i+1}")
    if(lst[1] not in label):
        raise SyntaxError(f"invalid label is {lst[1]} defined in line no {i+1}")
    elif(lst[1] in variable):
       raise SyntaxError(f"varaible is not defined in place of label in this  line no {i+1}")


def checkF(lst,i):

    if(len(lst)!=1):
        raise SyntaxError(f"syntax error invalid syntax for {lst[0]} in line no{i+1}")


def varChecker(lst,i):
    if(len(lst)==0):
        pass
    else:
        if len(lst) == 2 and lst[0]=="var":
            if lst[1].isdigit() or not lst[1].isalnum() or lst[1][0].isdigit():
                raise SyntaxError(f'Invalid variable name in line {i+1}')
            if lst[1] not in variable:
                variable.append(lst[1])
            else:
                raise SyntaxError(f'Same variable name already used at line {i+1}')

def labChecker(lst,i):
    if(len(lst)==0):
        pass
    else:
        if(lst[0][-1]==":"):
            if(lst[0][:-1] not in label):
                label.append(lst[0][:-1])
            else:
                raise SyntaxError(f'multiple declaration cannot be used for label')

def hltCheck():
    p=0
    q=1
    count_halt = 0
    for line in file:
        if(len(line)==0):
            pass
        else:
            if line.split(":")[-1].strip()=="hlt":
                count_halt+=1
                q=0
            elif q:
                p+=1
    if count_halt==0:
        raise SyntaxError(f"No halt found at line {len(file)}")
    elif count_halt>1 or not file[-1].split(":")[-1].strip()=="hlt":
        raise SyntaxError(f'Invalid halt at line {p+1}')

hltCheck()

i=0
for line in file:
    if(len(line)==0):
        pass
    else:
        lst=list(map(str,line.split()))

## handle all the case of variable 

        varChecker(lst,i)

## handle all the case of labels

        labChecker(lst,i)
        i+=1

j=0
for line in file:
    line=line.strip()
    if(len(line)==0):
        pass
    else:
        lst=list(map(str,line.split()))
        if lst[0]=="var":
            pass
        
        else:
            if(lst[0][:-1] in label):
                lst.pop(0)
            if(len(lst)==0):
                raise SyntaxError(f'invalid syntax for label is used in line no {j+1}')
            if(lst[0] not in symbol):
                raise SyntaxError(f"invalid instruction is used in line no{j+1}")
            if(lst[0]=="mov"):
                if(lst[2][0]=="$"):
                    lst[0]="mov1"
                else:
                    lst[0]="mov2"
            if(Instructions[lst[0]][0]=="A"):
                checkA(lst,j)
            elif(Instructions[lst[0]][0]=="B"):
                checkB(lst,j)
            elif(Instructions[lst[0]][0]=="C"):
                checkC(lst,j)
            elif(Instructions[lst[0]][0]=="D"):
                checkD(lst,j)
            elif(Instructions[lst[0]][0]=="E"):
                checkE(lst,j)
            elif(Instructions[lst[0]][0]=="F"):
                checkF(lst,j)
            else:
                SyntaxError(f"invalid syntax used in line no{j+1}")
        j+=1


def binaryConverter(n):
    l=[]
    while(n>0):
        a=n%2
        l.append(a)
        n=n//2
    l.reverse()
    s=""
    for i in l:
        s=s+str(i)
    if(len(s)==8):
        return s
    else:
        lst = []
        for i in range(1, 8-len(s)+1):
            lst.append('0')
        lst.append(str(s))
        return "".join(lst)

variables={}
labels={}
address=-1

for line in file:
    if(len(line)==0):
        pass
    else:
        lst=list(line.split())
        if(lst[0] in symbol):
            address+=1
        if(lst[0][-1]==":"):
            address+=1
            labels[lst[0][:-1]]=address

for line in file:
    if(len(line)==0):
        pass
    else:
        lst=list(line.split())
        if(lst[0]=='var'):
            address+=1
            variables[lst[1]]=address
        
for line in file:
    line=line.strip()
    if(len(line)==0):
        continue

    else:
        lst=list(line.split())
        if(len(lst)>1 and lst[0][:-1] in labels and lst[1] in symbol):
            lst.pop(0)
        if(lst[0] in symbol):
            if(lst[0]=="mov"):
                if(lst[2][0]!="$"):
                    lst[0]='mov2'
                else:
                    lst[0]='mov1'
            
            if(Instructions[lst[0]][0]=="A"):
                ans=Instructions[lst[0]][1]+"00"+Registeraddress[lst[1]]+Registeraddress[lst[2]]+Registeraddress[lst[3]]
            elif(Instructions[lst[0]][0]=="B"):
                ans=Instructions[lst[0]][1]+Registeraddress[lst[1]]+binaryConverter(int(lst[2][1:]))
            elif(Instructions[lst[0]][0]=="C"):
                ans=Instructions[lst[0]][1]+"00000"+Registeraddress[lst[1]]+Registeraddress[lst[2]]
            elif(Instructions[lst[0]][0]=="D"):
                ans=Instructions[lst[0]][1]+Registeraddress[lst[1]]+binaryConverter(variables[lst[2]])
            elif(Instructions[lst[0]][0]=="E"):
                ans=Instructions[lst[0]][1]+"000"+binaryConverter(int(labels[lst[1]]))
            elif(Instructions[lst[0]][0]=="F"):
                ans=Instructions[lst[0]][1]+"00000000000"
            print(ans)