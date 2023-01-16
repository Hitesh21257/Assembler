from sys import stdin
import matplotlib as mat
x=[]
y=[]
cycle=0
Instructions={
    "add":["A","10000"],"sub":["A","10001"],"mul":["A","10110"],"xor":["A","11010"],"or":["A","11011"],"and":["A","11100"],
    "mov1":["B","10010"],"ls":["B","11001"],"rs":["B","11000"],
    "mov2":["C","10011"],"div":["C","10111"],"not":["C","11101"],"cmp":["C","11110"],
    "ld":["D","10100"],"st":["D","10101"],
    "jmp":["E","11111"],"jlt":["E","01100"],"jgt":["E","01101"],"je":["E","01111"],
    "hlt":["F","01010"]
}

Registeraddress={
    "R0":["000",0],"R1":["001",0],"R2":["010",0],"R3":["011",0],
    "R4":["100",0],"R5":["101",0],"R6":["110",0],
    "FLAGS":["111",0,0,0,0]
}

def Set_Bin8(num):
    num = str(decimal_to_binary(num))
    num1 = 8 - len(num)
    lst = []
    for i in range(0, num1):
        lst.append("0")

    num2 = "".join(lst)
    num = num2 + num
    return num

def Set_Bin16(num):
    num = str(decimal_to_binary(num))
    num1 = 16 - len(num)
    lst = []
    for i in range(0, num1):
        lst.append("0")

    num2 = "".join(lst)
    num = num2 + num
    return num

def binary_to_decimal(n):
    a=str(n)
    a=list(map(int,a))
    a.reverse()
    s=0
    j=0
    for i in a:
        s=s+i*(2**j)
        j=j+1
    return s

def decimal_to_binary(x):
    n=int(x)
    l=[]
    while(n>0):
        a=n%2
        l.append(str(a))
        n=n//2
    l.reverse()
    l = "".join(l)
    return l

def PrintIt():
    for i in Registeraddress.keys():
        if i == "FLAGS":
            print("000000000000"+str(Registeraddress["FLAGS"][1])+str(Registeraddress["FLAGS"][2])+str(Registeraddress["FLAGS"][3])+str(Registeraddress["FLAGS"][4]))
        else:
            print(Set_Bin16(int(Registeraddress[i][-1])), end=" ")

def Flag_Reset():
    Registeraddress["FLAGS"][1] = 0
    Registeraddress["FLAGS"][2] = 0
    Registeraddress["FLAGS"][3] = 0
    Registeraddress["FLAGS"][4] = 0

def TypesA(instruction, type):
     temp2, temp3, i, temp1 = "","","",""   
     operand1 = instruction[13:]
     operand2 = instruction[10:13]
     operand3 = instruction[7:10]
     for i in Registeraddress.keys():
        if Registeraddress[i][0] == operand1:
            temp1 = i
        if Registeraddress[i][0] == operand2:
            temp2 = Registeraddress[i][-1]
        if Registeraddress[i][0] == operand3:
            temp3 = Registeraddress[i][-1]

     if type == "add":
         Flag_Reset()
         temp4  = temp2 + temp3
         ## To check overflow
         if temp4 >= 65535:
             Registeraddress["FLAGS"][1] = 1
             Registeraddress[temp1][-1] = temp4%65536
         else:
             Registeraddress[temp1][-1] = temp4

     elif type == "sub":
         Flag_Reset()
         temp4 = temp3 - temp2
         ## To check underflow
         if temp4 < 0:
             Registeraddress["FLAGS"][1] = 1
             Registeraddress[temp1][-1] = 0
         else:
             Registeraddress[temp1][-1] = temp4

     elif type == "mul":
         Flag_Reset()
         temp4 = (temp2 * temp3)
         ## To check overflow
         if temp4 >= 65535:
             Registeraddress["FLAGS"][1] = 1
             Registeraddress[temp1][-1] = temp4%65536
         else:
             Registeraddress[temp1][-1] = temp4


     elif type == "and":

         Flag_Reset()
         temp4 = temp2 & temp3
         Registeraddress[temp1][-1] = temp4

     elif type == "or":
         Flag_Reset()
         temp4 = temp2 | temp3
         Registeraddress[temp1][-1] = temp4

     elif type == "xor":
         temp4 = temp2 ^ temp3
         Registeraddress[temp1][-1] = temp4

def TypeB(Instruction, type):

    global i, temp
    operand = Instruction[5:8]
    imm = binary_to_decimal(int(Instruction[8:]))

    for i in Registeraddress.keys():
        if Registeraddress[i][0] == operand:
            temp = i

    if type == "mov1":
        Flag_Reset()
        Registeraddress[temp][-1] = imm
    # Do by your self
    elif type == "ls":
        Flag_Reset()
        Registeraddress[temp][-1] = Registeraddress[temp][-1] << imm
    elif type == "rs":
        Flag_Reset()
        Registeraddress[temp][-1] = Registeraddress[temp][-1] >> imm

def TypeC(Instruction, type):
    temp1, temp2, b, a = 0, 0, "", ""
    operand1 = str(Instruction[10:13])
    operand2 = str(Instruction[13:])

    for i1 in Registeraddress.keys():
        if str(Registeraddress[i1][0]) == operand1:
            temp1 = Registeraddress[i1][-1]
            a = i1
        if str(Registeraddress[i1][0]) == operand2:
            temp2 = Registeraddress[i1][-1]
            b = i1

    if type == "mov2":
        Flag_Reset()
        temp2 = temp1
        Registeraddress[b][-1] = temp2
    elif type == "div":
        Flag_Reset()
        if temp2 != 0:
            Registeraddress["R0"][-1] = temp1//temp2
            Registeraddress["R1"][-1] = temp1%temp2
    elif type == "not":
        Flag_Reset()

        cod = Registeraddress[a][-1]
        cod1 = list(decimal_to_binary(cod).zfill(16))
        for i in range(len(cod1)):
            cod1[i] = "0" if cod1[i] == "1" else "1"
        cod1 = binary_to_decimal("".join(cod1))
        # last = cod1

        # last = ~last
        # last1 = binary_to_decimal(last)
        
        Registeraddress[b][-1] = cod1

    elif type == "cmp":
        Flag_Reset()
        if temp1 > temp2:
            Registeraddress["FLAGS"][3] = 1
        elif temp1 < temp2:
            Registeraddress["FLAGS"][2] = 1
        elif temp1 == temp2:
            Registeraddress["FLAGS"][4] = 1

def TypeD(Instruction, type):
    global temp1
    operand = Instruction[5:8]
    temp = binary_to_decimal(int(Instruction[8:]))

    for i in Registeraddress.keys():
        if Registeraddress[i][0] == operand:
            temp1 = i

    if type == "ld":
        Flag_Reset()
        seti = int(Memory[temp])
        Registeraddress[temp1][-1] = binary_to_decimal(seti)
    elif type == "st":
        Flag_Reset()
        seti = Registeraddress[temp1][-1]
        Memory[temp] = Set_Bin16(seti)

def TypeE(Instruction, type, pc1):
    operand = Instruction[8:]

    if type == "jmp":
        temp = binary_to_decimal(int(operand))
        Flag_Reset()
        return temp
    elif type == "jlt" and Registeraddress["FLAGS"][2] == 1:
        temp = binary_to_decimal(int(operand))
        Flag_Reset()
        return temp
    elif type == "jgt" and Registeraddress["FLAGS"][3] == 1:
        temp = binary_to_decimal(int(operand))
        Flag_Reset()
        return temp
    else:
        Flag_Reset()
        return pc1



l = stdin.readlines()
code = []
j = 0
for i in l:
    j += 1
    code.append(str(i.strip("\n")))
    if (j >= 256):
        break
memory = code.copy()

# for i in range(5):
#     code.append(int(input()))

i = len(code)
Memory = code.copy()
while(i < 256):
    Memory.append("0000000000000000")
    i = i+1

k = 0
pc = 0
flag = 0
while pc < len(code):
    flag = 0
    temp = str(code[pc])
    opcode = "0"
    for i in Instructions.keys():
        if Instructions[i][-1] == temp[0:5]:
            opcode = i
            break
    InstructionsA = ["add", "sub", "mul", "and", "or", "xor"]
    InstructionsB = ["mov1", "ls", "rs"]
    InstructionsC = ["mov2", "div", "not", "cmp"]
    InstructionsD = ["ld", "st"]
    InstructionsE = ["jmp", "jlt", "jgt", "je"]
    InstructionsF = ["hlt"]
    if opcode in InstructionsA:
        TypesA(temp, opcode)
        #PrintIt()

    elif opcode in InstructionsB:
        TypeB(temp, opcode)
        #PrintIt()

    elif opcode in InstructionsC:
        TypeC(temp,opcode)
        #PrintIt()

    elif opcode in InstructionsD:
        TypeD(temp,opcode)
        #PrintIt()

    elif opcode in InstructionsE:
        x = TypeE(temp, opcode, pc)
        if x == pc:
            pc = x
            flag = 0
        else:
            print(Set_Bin8(pc), end=" ")
            PrintIt()
            pc = x
            flag = 1
        #PrintIt()

    ## At the end the Instead of printing the value of pc. I print end of program exceution.
    elif opcode in InstructionsF:
        Flag_Reset()
        print(Set_Bin8(pc), end=" ")
        PrintIt()

        break
    if flag == 0:
        k += 1
        print(Set_Bin8(pc), end=" ")
        pc += 1
        PrintIt()
x.append(cycle)
y.append(pc)
cycle+=1

for i in range(0, 256):
    print(Memory[i])

mat.plot(x,y,'o')
mat.title('Graph')
mat.xlabel("Cycle No")
mat.ylabel("Memory Location")
mat.show()
