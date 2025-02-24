#initialise all the fields to an empty string 
op = ''
rs = ''
rt = ''
rd = ''
shamt = ''
funct = ''
imm = ''
target = ''
pc = 4194304  #start address of the program

#control signals
RegDst = 0
ALUSrc = 0
MemReg = 0
RegWr  = 0
MemRd  = 0
MemWr  = 0
Branch = 0
ALUOp1 = 0
ALUOp0 = 0
Jmp    = 0
zero   = 0

#dictionary that stores the register values according to the register numbers
register_file = {
0 : 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0,
24: 0, 25: 0, 26: 0, 27: 0, 28: 268468224, 29: 2147479548,
30: 0, 31: 0
}

'''
Uncomment the following code for the factorial program
'''

#-------------------------FACTORIAL MEMORY--------------------------
'''
#data memory factorial
data_memory = {
    268500992 : 0 , #number who's factorial is being calculated
    268501024 : 0   #factorial result
}

#instruction memory factorial
instruction_memory = { 
    4194304 : '00100000000010000000000000001010',
    4194308 : '00111100000000010001000000000001',
    4194312 : '00110100001000010000000000000000',
    4194316 : '00000000000000010100100000100000',
    4194320 : '10101101001010000000000000000000',
    4194324 : '10001101001100000000000000000000',
    4194328 : '00100000000100010000000000000001',
    4194332 : '00100000000100100000000000000001',
    4194336 : '00001000000100000000000000001001',
    4194340 : '00010110001100000000000000000010',
    4194344 : '01110010010100001001000000000010', 
    4194348 : '00001000000100000000000000001111',
    4194352 : '01110010010100011001000000000010', 
    4194356 : '00100010001100010000000000000001', 
    4194360 : '00001000000100000000000000001001',
    4194364 : '00111100000000010001000000000001',
    4194368 : '00110100001000010000000000100000',
    4194372 : '00000000000000010100000000100000',
    4194376 : '10101101000100100000000000000000',
    4194380 : '00100000000000100000000000001010',
    4194384 : '00000000000000000000000000001100'  #syscall
}
'''

'''
Uncomment the following code for the binary search program
'''

#-------------------------BINARY SEARCH MEMORY--------------------------


#data memory binary search
data_memory = {
    268500992 : 11 , 
    268500996 : 20 , 
    268501000 : 34 ,
    268501004 : 45 ,
    268501008 : 56 ,
    268501024 : 0    # result stored here
}

#instruction memory binary search
instruction_memory = {
    4194304 : '00100000000100000000000000000101',
    4194308 : '00100000000100010000000000101101',
    4194312 : '00111100000000010001000000000001',
    4194316 : '00110100001010010000000000000000',
    4194320 : '00100000000011110000000000000000',
    4194324 : '00100010000011101111111111111111',
    4194328 : '00000001110011110000100000101010',
    4194332 : '00010100001000000000000000010001',
    4194336 : '00000001111011100110100000100000',
    4194340 : '00000000000011010110100001000010',
    4194344 : '00000000000011010110000010000000',
    4194348 : '00000001100010010110000000100000',
    4194352 : '10001101100010110000000000000000',
    4194356 : '00010001011100010000000000000110',
    4194360 : '00000001011100010000100000101010',
    4194364 : '00010100001000000000000000000010',
    4194368 : '00100001101011101111111111111111',
    4194372 : '00001000000100000000000000000110',
    4194376 : '00100001101011110000000000000001',
    4194380 : '00001000000100000000000000000110',
    4194384 : '00111100000000010001000000000001',
    4194388 : '00110100001000010000000000100000',
    4194392 : '00000000000000010100000000100000',
    4194396 : '10101101000011010000000000000000',
    4194400 : '00001000000100000000000000011110',
    4194404 : '00100000000011011111111111111111',
    4194408 : '00111100000000010001000000000001',
    4194412 : '00110100001000010000000000100000',
    4194416 : '00000000000000010100000000100000',
    4194420 : '10101101000011010000000000000000',
    4194424 : '00100000000000100000000000001010',
    4194428 : '00000000000000000000000000001100'  #syscall
}


#function to convert binary string to signed decimal number
def convert_immediate(imm):
    if imm[0]=='0':        #positive number
        return int(imm,2)
    else:                  #negative number
        n=len(imm)
        val = (-1)*(2**(n-1))
        for i in range(n-1,0,-1):
            val = val + ((2 **(i-1))*int(imm[n - i]))
        return val
    
#setting the control lines 
def control_lines(op):

    global RegDst, ALUSrc, MemReg, RegWr, MemRd, MemWr, Branch, ALUOp1, ALUOp0, Jmp

    if op == '000000' or op == '011100':  #R-format and mul
        RegDst = 1
        ALUSrc = 0
        MemReg = 0
        RegWr = 1
        MemRd = 0
        MemWr = 0
        Branch = 0
        ALUOp1 = 1
        ALUOp0 = 0
        Jmp = 0

    elif op == '100011': #LW
        RegDst = 0
        ALUSrc = 1
        MemReg = 1
        RegWr = 1
        MemRd = 1
        MemWr = 0
        Branch = 0
        ALUOp1 = 0
        ALUOp0 = 0
        Jmp = 0

    elif op == '101011': #SW
        RegDst = 0
        ALUSrc = 1
        MemReg = 0
        RegWr = 0
        MemRd = 0
        MemWr = 1
        Branch = 0
        ALUOp1 = 0
        ALUOp0 = 0
        Jmp = 0
 
    elif op == '001000': #ADDI
        RegDst = 0
        ALUSrc = 1
        MemReg = 0
        RegWr = 1
        MemRd = 0
        MemWr = 0
        Branch = 0
        ALUOp1 = 0
        ALUOp0 = 0
        Jmp = 0

    elif op == '001101': #ORI
        RegDst = 0
        ALUSrc = 1
        MemReg = 0
        RegWr = 1
        MemRd = 0
        MemWr = 0
        Branch = 0
        ALUOp1 = 0
        ALUOp0 = 0
        Jmp = 0

    elif op == '001111': #LUI
        RegDst = 0
        ALUSrc = 1
        MemReg = 0
        RegWr = 1
        MemRd = 0
        MemWr = 0
        Branch = 0
        ALUOp1 = 0
        ALUOp0 = 0
        Jmp = 0

    elif op == '000101': #BNE
        RegDst = 0
        ALUSrc = 0
        MemReg = 0
        RegWr = 0
        MemRd = 0
        MemWr = 0
        Branch = 1
        ALUOp1 = 1 #defining AlUOp of BNE as 11
        ALUOp0 = 1
        Jmp = 0

    elif op == '000100': #BEQ
        RegDst = 0
        ALUSrc = 0
        MemReg = 0
        RegWr = 0
        MemRd = 0
        MemWr = 0
        Branch = 1
        ALUOp1 = 0
        ALUOp0 = 1
        Jmp = 0

    elif op == '000010': #JMP
        RegDst = 0
        ALUSrc = 0
        MemReg = 0
        RegWr = 0
        MemRd = 0
        MemWr = 0
        Branch = 0
        ALUOp1 = 0
        ALUOp0 = 0
        Jmp = 1

#get the ALU control input according to the operation to be performed by ALU
def implement_ALU_control_unit():

    if op == '011100': #mul
        return '010' #add operation performed
    
    elif ALUOp1==1 and ALUOp0==0: #R-format instruction
        if funct =='100000':   #add 
            return '010'
        elif funct =='100010': #sub
            return '011'
        elif funct =='100100': #and
            return '000'
        elif funct =='100101': #or
            return '001'
        elif funct =='101010': #slt
            return '100'
        elif funct == '000010':#srl
            return '101' 
        elif funct == '000000':#sll
            return '110'

    elif ALUOp1==0 and ALUOp0==0: #lw , sw , addi , lui 
        return '010' #add operation performed

    elif ALUOp1==1 and ALUOp0==1: #bne
        return '011' #sub operation performed

    elif ALUOp1==0 and ALUOp0==1: #beq
        return '011' #sub operation


#operations of the ALU 
def ALU(operand1, operand2, ALU_control_input):
    
    global zero
    
    result_ALU = 0 #stores the result of the ALU operation
    if ALU_control_input == '010': #add
        result_ALU = operand1 + operand2

    elif ALU_control_input == '011': #sub
        result_ALU = operand1 - operand2

    elif ALU_control_input == '001': #or
        result_ALU = operand1 | operand2

    elif ALU_control_input == '101': #shift right
        result_ALU = operand1 >> operand2

    elif ALU_control_input == '110': #shift left
        result_ALU = operand1 << operand2

    elif ALU_control_input == '100': #set on less than
        result_ALU = int(operand1 < operand2)

    if result_ALU == 0: #set the zero flag 
        zero = 1
    else:
        zero = 0
        
    return result_ALU


#the instruction fetch cycle 
def IF():
    global pc,op,rs,rt,rd,funct,target,imm,shamt
    instruction = instruction_memory[pc] 
    pc = pc + 4 
    return instruction

#the instruction decode/register read stage
def ID(instruction):
    global op,rs,rt,rd,funct,target,imm,shamt
    op = instruction[0:6] #opcode of the instruction
    
    control_lines(op)

    if  op == '000000' or op == '011100': #R format and mul
        rs = instruction[6:11]  #rs
        rt = instruction[11:16] #rt
        rd = instruction[16:21] #rd
        shamt = instruction[21:26] #shamt
        funct = instruction[26:32] #function

    elif op == '000010': #J format
        target = '0000' + instruction[6:32] + '00' #32-bit jump address

    else: #I format
        rs = instruction[6:11] #rs
        rt = instruction[11:16] #rt
        #sign extend
        if instruction[16] == '0': #number is non negative
            imm = '0'*16 + instruction[16:32] #immediate value
        elif instruction[16] == '1': #if number is negative
            imm = '1'*16 + instruction[16:32] #immediate value

#the execute stage
def EX():
    global op,rs,rt,rd,funct,target,imm,shamt,pc,instruction

    operand1 = 0
    operand2 = 0
    result_ALU = 0
    ALU_control_input = ''

    if op == '001101': #ori 
        ALU_control_input = '001' #since it will perform or 
    else:
        ALU_control_input = implement_ALU_control_unit() #control signal telling us which operation to perform

    if Jmp == 1: #J-format
        pc = int(target,2)
        return 

    if shamt != '00000' and shamt != '': #shift
        operand1 = register_file[int(rt,2)]  #ALU first input is rt
        operand2 = int(shamt,2)
        result_ALU = ALU(operand1, operand2, ALU_control_input)
    else:
        if rs != '': #R and I format
            operand1 = register_file[int(rs,2)] #ALU first input is rs
        
        if ALUSrc == 0: #take register value
            if rt != '':
                operand2 = register_file[int(rt,2)] #ALU second input is rt
        else: #ALUSrc = 1 , take immm value
            operand2 = convert_immediate(imm)
        
        if op == '001111': #lui  
            return operand2*(2**16)
        
        if op == "011100": #mul instruction
            for i in range(operand2):
                result_ALU = ALU(result_ALU,operand1,ALU_control_input) 
        elif Branch == 1:  #branch instructions

            if ALUOp1 == 1 and ALUOp0 == 1: #BNE
                result_ALU = ALU(operand1,operand2,ALU_control_input)
                if zero == 0: #zero flag is not set (if operand1 != operand2)
                    immtmp = convert_immediate(imm)
                    result_ALU = 0
                    for i in range(4):  #4*imm  
                        result_ALU = ALU(result_ALU,immtmp,'010') #add control input
                    pc = pc + result_ALU #update 
            else:  #BEQ
                result_ALU = ALU(operand1,operand2,ALU_control_input)
                if zero == 1: #zero flag is set (if operand1 == operand2)
                    immtmp = convert_immediate(imm)
                    result_ALU = 0
                    for i in range(4):  #4*imm  
                        result_ALU = ALU(result_ALU,immtmp,'010') #add control input
                    pc = pc + result_ALU #update 

        else:
            result_ALU = ALU(operand1,operand2,ALU_control_input)
                        
    return result_ALU

#memory access stage
def MEM(result_ALU):
    global op,rs,rt,rd,funct,target,imm,shamt

    if MemRd == 1: # for load word
        return data_memory[result_ALU]
    elif MemWr == 1: # for store word 
        data_memory[result_ALU]=register_file[int(rt,2)]
    if MemReg == 0: # retrieves result of ALU 
        return result_ALU
    elif MemReg == 1: # retrieves data fetched from memory
        return data_memory[result_ALU]

#writeback stage
def WB(data):
    global op,rs,rt,rd,funct,target,imm,shamt

    if RegWr == 1: #write to register file
        if RegDst == 1: # R format
            register_file[int(rd,2)] = data #writes back data in rd
        else: # I format
            register_file[int(rt,2)] = data #writes back data in rt


#main function
# Cross-platform clear screen
import os
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    clear_screen()
except:
    print('\n' * 100)  # Fallback if clear screen fails

while(True):

    '''
    Uncomment the following code for the factorial program
    '''
    #if pc > 4194384:  
    
    '''
    Uncomment the following code for the binary search program
    '''
    if pc > 4194428: 

        # break has to be used to stop the program after the last instruction is executed    
        break             #if you reach the end of the instructions break out of the loop

    print("PC:", pc)

    instruction = IF()      #instruction is being fetched
    ID(instruction)         #instruction decode
    result_ALU = EX()       #instruction execute
    data = MEM(result_ALU)  #accessing the memory and retrieving required data
    WB(data)                #writeback of required data
    

    '''
    Unccoment the following code for debugging purposes and to see the register file and data memory values at each step
    '''

    #print("Register file:\n", register_file)
    #print()
    print("Data Memory:\n", data_memory)
    #print()
    print("------------------------------------------------------------------------------------------------")
    #print()

print("Result: ")

'''
Uncomment the following code for the factorial program
'''
#print(data_memory)

'''
Uncomment the following code for the binary search program
'''
print(data_memory[268501024])

print()

