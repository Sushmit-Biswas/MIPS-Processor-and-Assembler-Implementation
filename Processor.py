"""
MIPS Processor Simulator with visualization of pipeline stages
"""

import os
from colorama import init, Fore, Style
import time

# Initialize colorama
init()

class MIPSProcessor:
    def __init__(self):
        # Program counter and components
        self.pc = 4194304  # Start address
        
        # Instruction components
        self.op = ''
        self.rs = ''
        self.rt = ''
        self.rd = ''
        self.shamt = ''
        self.funct = ''
        self.imm = ''
        self.target = ''
        
        # Control signals
        self.RegDst = 0
        self.ALUSrc = 0
        self.MemReg = 0
        self.RegWr = 0
        self.MemRd = 0
        self.MemWr = 0
        self.Branch = 0
        self.ALUOp1 = 0
        self.ALUOp0 = 0
        self.Jmp = 0
        self.zero = 0
        
        # Initialize register file
        self.register_file = {i: 0 for i in range(32)}
        self.register_file[28] = 268468224  # $gp
        self.register_file[29] = 2147479548  # $sp

        # Program choice
        self.choice = ""
        
        # Choose program
        self.load_program()

    def print_stage(self, stage, info):
        """Print pipeline stage information with color"""
        colors = {'IF': Fore.GREEN, 'ID': Fore.YELLOW, 'EX': Fore.BLUE, 
                 'MEM': Fore.MAGENTA, 'WB': Fore.CYAN}
        print(f"{colors.get(stage, '')}{stage}: {info}{Style.RESET_ALL}")
        time.sleep(0.3)  # Add small delay to see stages

    def load_program(self):
        """Load program memory based on user choice"""
        print("\nSelect Program:")
        print("1. Factorial")
        print("2. Binary Search")
        self.choice = input("Enter choice (1/2): ")
        
        if self.choice == "1":
            # Factorial program memory
            self.data_memory = {
                268500992: 0,  # Input number
                268501024: 0   # Result location
            }
            
            # Factorial instructions - complete set from factorial.txt
            self.instruction_memory = {
                4194304: '00100000000010000000000000001010',
                4194308: '00111100000000010001000000000001',
                4194312: '00110100001000010000000000000000',
                4194316: '00000000000000010100100000100000',
                4194320: '10101101001010000000000000000000',
                4194324: '10001101001100000000000000000000',
                4194328: '00100000000100010000000000000001',
                4194332: '00100000000100100000000000000001',
                4194336: '00001000000100000000000000001001',
                4194340: '00010110001100000000000000000010',
                4194344: '01110010010100001001000000000010',
                4194348: '00001000000100000000000000001111',
                4194352: '01110010010100011001000000000010',
                4194356: '00100010001100010000000000000001',
                4194360: '00001000000100000000000000001001',
                4194364: '00111100000000010001000000000001',
                4194368: '00110100001000010000000000100000',
                4194372: '00000000000000010100000000100000',
                4194376: '10101101000100100000000000000000',
                4194380: '00100000000000100000000000001010',
                4194384: '00000000000000000000000000001100'  # syscall
            }
            self.program_end = 4194388  # Updated to include syscall
            
        else:
            # Binary search program memory  
            self.data_memory = {
                # Array of numbers
                268500992: 11,
                268500996: 20,
                268501000: 34,
                268501004: 45,
                268501008: 56,
                268501024: 0    # Result location
            }
            
            # Binary search instructions - complete set from binary_search.txt
            self.instruction_memory = {
                4194304: '00100000000100000000000000000101',
                4194308: '00100000000100010000000000101101',
                4194312: '00111100000000010001000000000001',
                4194316: '00110100001010010000000000000000',
                4194320: '00100000000011110000000000000000',
                4194324: '00100010000011101111111111111111',
                4194328: '00000001110011110000100000101010',
                4194332: '00010100001000000000000000010001',
                4194336: '00000001111011100110100000100000',
                4194340: '00000000000011010110100001000010',
                4194344: '00000000000011010110000010000000',
                4194348: '00000001100010010110000000100000',
                4194352: '10001101100010110000000000000000',
                4194356: '00010001011100010000000000000110',
                4194360: '00000001011100010000100000101010',
                4194364: '00010100001000000000000000000010',
                4194368: '00100001101011101111111111111111',
                4194372: '00001000000100000000000000000110',
                4194376: '00100001101011110000000000000001',
                4194380: '00001000000100000000000000000110',
                4194384: '00111100000000010001000000000001',
                4194388: '00110100001000010000000000100000',
                4194392: '00000000000000010100000000100000',
                4194396: '10101101000011010000000000000000',
                4194400: '00001000000100000000000000011110',
                4194404: '00100000000011011111111111111111',
                4194408: '00111100000000010001000000000001',
                4194412: '00110100001000010000000000100000',
                4194416: '00000000000000010100000000100000',
                4194420: '10101101000011010000000000000000',
                4194424: '00100000000000100000000000001010',
                4194428: '00000000000000000000000000001100'  # syscall
            }
            self.program_end = 4194432  # Updated to include all instructions

    def convert_immediate(self, imm):
        """Convert binary immediate to signed decimal"""
        if imm[0] == '0':
            return int(imm, 2)
        else:
            n = len(imm)
            val = (-1) * (2 ** (n-1))
            for i in range(n-1, 0, -1):
                val = val + ((2 ** (i-1)) * int(imm[n - i]))
            return val

    def control_lines(self):
        """Set control lines based on opcode"""
        if self.op == '000000' or self.op == '011100':  # R-format and mul
            self.RegDst = 1
            self.ALUSrc = 0
            self.MemReg = 0
            self.RegWr = 1
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 0
            self.ALUOp1 = 1
            self.ALUOp0 = 0
            self.Jmp = 0
        elif self.op == '100011':  # lw
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemReg = 1
            self.RegWr = 1
            self.MemRd = 1
            self.MemWr = 0
            self.Branch = 0
            self.ALUOp1 = 0
            self.ALUOp0 = 0
            self.Jmp = 0
        elif self.op == '101011':  # sw
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemReg = 0
            self.RegWr = 0
            self.MemRd = 0
            self.MemWr = 1
            self.Branch = 0
            self.ALUOp1 = 0
            self.ALUOp0 = 0
            self.Jmp = 0
        elif self.op == '001000':  # addi
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemReg = 0
            self.RegWr = 1
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 0
            self.ALUOp1 = 0
            self.ALUOp0 = 0
            self.Jmp = 0
        elif self.op == '001101':  # ori
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemReg = 0
            self.RegWr = 1
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 0
            self.ALUOp1 = 0
            self.ALUOp0 = 0
            self.Jmp = 0
        elif self.op == '001111':  # lui
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemReg = 0
            self.RegWr = 1
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 0
            self.ALUOp1 = 0
            self.ALUOp0 = 0
            self.Jmp = 0
        elif self.op == '000101':  # bne
            self.RegDst = 0
            self.ALUSrc = 0
            self.MemReg = 0
            self.RegWr = 0
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 1
            self.ALUOp1 = 1
            self.ALUOp0 = 1
            self.Jmp = 0
        elif self.op == '000100':  # beq
            self.RegDst = 0
            self.ALUSrc = 0
            self.MemReg = 0
            self.RegWr = 0
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 1
            self.ALUOp1 = 0
            self.ALUOp0 = 1
            self.Jmp = 0
        elif self.op == '000010':  # j
            self.RegDst = 0
            self.ALUSrc = 0
            self.MemReg = 0
            self.RegWr = 0
            self.MemRd = 0
            self.MemWr = 0
            self.Branch = 0
            self.ALUOp1 = 0
            self.ALUOp0 = 0
            self.Jmp = 1

    def implement_ALU_control_unit(self):
        """Get ALU control signals"""
        if self.op == '011100':  # mul
            return '010'
        elif self.ALUOp1 == 1 and self.ALUOp0 == 0:  # R-format
            if self.funct == '100000':    # add
                return '010'
            elif self.funct == '100010':  # sub  
                return '011'
            elif self.funct == '100100':  # and
                return '000'
            elif self.funct == '100101':  # or
                return '001'
            elif self.funct == '101010':  # slt
                return '100'
            elif self.funct == '000010':  # srl
                return '101'
            elif self.funct == '000000':  # sll
                return '110'
        elif self.ALUOp1 == 0 and self.ALUOp0 == 0:  # lw, sw, addi
            return '010' 
        elif self.ALUOp1 == 1 and self.ALUOp0 == 1:  # bne
            return '011'
        elif self.ALUOp1 == 0 and self.ALUOp0 == 1:  # beq
            return '011'

    def ALU(self, operand1, operand2, ALU_control_input):
        """
        Arithmetic Logic Unit (ALU) performs the actual computation.
        Inputs:
            operand1: First input operand
            operand2: Second input operand  
            ALU_control_input: 3-bit control signal determining operation
            
        Control signals:
            010: Addition (add, addi, lw, sw)
            011: Subtraction (sub, beq, bne)  
            001: Bitwise OR (or, ori)
            101: Shift right logical (srl)
            110: Shift left logical (sll)
            100: Set less than (slt)
            
        Updates zero flag if result is 0.
        """
        result_ALU = 0
        
        if ALU_control_input == '010':       # Addition
            result_ALU = operand1 + operand2
        elif ALU_control_input == '011':     # Subtraction
            result_ALU = operand1 - operand2
        elif ALU_control_input == '001':     # Bitwise OR
            result_ALU = operand1 | operand2
        elif ALU_control_input == '101':     # Shift right logical
            result_ALU = operand1 >> operand2
        elif ALU_control_input == '110':     # Shift left logical
            result_ALU = operand1 << operand2
        elif ALU_control_input == '100':     # Set less than
            result_ALU = int(operand1 < operand2)

        # Update zero flag based on result
        self.zero = 1 if result_ALU == 0 else 0
        return result_ALU

    def instruction_fetch(self):
        """Fetch instruction"""
        instruction = self.instruction_memory[self.pc]
        self.print_stage('IF', f"PC = {self.pc}, Instruction = {instruction}")
        self.pc += 4
        return instruction

    def instruction_decode(self, instruction):
        """Decode instruction"""
        self.op = instruction[0:6]
        
        if self.op == '000000' or self.op == '011100':  
            # R format and mul
            self.rs = instruction[6:11]
            self.rt = instruction[11:16]
            self.rd = instruction[16:21]
            self.shamt = instruction[21:26]
            self.funct = instruction[26:32]
            self.print_stage('ID', f"op={self.op}, rs={self.rs}, rt={self.rt}, rd={self.rd} [R-format]")
        elif self.op == '000010':  
            # J format
            self.target = '0000' + instruction[6:32] + '00'  # 32-bit jump address
            self.print_stage('ID', f"op={self.op}, target={instruction[6:32]} [J-format]")
        else: 
            # I format
            self.rs = instruction[6:11]
            self.rt = instruction[11:16]

            # sign extend
            if instruction[16] == '0':    # non-negative
                self.imm = '0'*16 + instruction[16:32]
            elif instruction[16] == '1':  # negative
                self.imm = '1'*16 + instruction[16:32]
            self.print_stage('ID', f"op={self.op}, rs={self.rs}, rt={self.rt}, imm={instruction[16:32]} [I-format]")
        
        self.control_lines()

    def execute(self):
        """
        Execute stage of the pipeline. Performs the following:
        1. Gets operands from registers or immediate field
        2. Routes operands to ALU based on instruction type
        3. Performs ALU operation
        4. Handles special cases:
           - Jump instructions: Updates PC directly
           - Branch instructions: Updates PC if condition is met
           - Shifts: Uses immediate shamt field
           - Multiplication: Special handling for mul instruction
        """

        # Get operands
        operand1 = self.register_file[int(self.rs, 2)]
        operand2 = self.register_file[int(self.rt, 2)] if not self.ALUSrc else self.convert_immediate(self.imm)
        ALU_control = self.implement_ALU_control_unit()
        result_ALU = 0

        # Handle special instructions
        if self.op == '001101':  # ori
            ALU_control = '001'  # Force OR operation
        
        if self.shamt != '00000' and self.shamt != '':  # Shift operations
            operand1 = self.register_file[int(self.rt, 2)]  # rt is source for shifts
            operand2 = int(self.shamt, 2)  # shamt field specifies shift amount
            result_ALU = self.ALU(operand1, operand2, ALU_control)
        else:
            if self.Jmp:  # Jump instructions
                result_ALU = int(self.target, 2)
                self.pc = result_ALU  # Direct PC update
                return result_ALU
            
            if self.op == '001111':  # lui (Load Upper Immediate)
                result_ALU = operand2 * (2**16)  # Shift immediate into upper 16 bits
            elif self.op == '011100':  # mul instruction
                result_ALU = operand1 * operand2  # Direct multiplication
            elif self.Branch:  # Branch instructions
                result_ALU = self.ALU(operand1, operand2, ALU_control)
                if self.op == '000101':  # bne
                    if result_ALU != 0:  # Branch if operands not equal
                        offset = self.convert_immediate(self.imm)
                        self.pc = self.pc + (offset << 2)  # PC-relative addressing
                elif self.op == '000100':  # beq
                    if result_ALU == 0:  # Branch if operands equal
                        offset = self.convert_immediate(self.imm)
                        self.pc = self.pc + (offset << 2)  # PC-relative addressing
            else:  # Regular ALU operation
                result_ALU = self.ALU(operand1, operand2, ALU_control)

        self.print_stage('EX', f"ALU Result = {result_ALU}")
        return result_ALU

    def memory_access(self, address):
        """Access memory"""
        if self.MemRd:      # Load
            data = self.data_memory.get(address, 0)
            self.print_stage('MEM', f"Read M[{address}] = {data}")
            return data
        elif self.MemWr:    # Store
            value = self.register_file[int(self.rt, 2)]
            self.data_memory[address] = value
            self.print_stage('MEM', f"Write M[{address}] = {value}")
            return value    # Return stored value rather than address
        return address

    def writeback(self, data):
        """
        Write back stage of the pipeline. Responsible for writing results back to registers.
        If RegWr is enabled, writes data to the destination register specified by rd (R-format) or rt (I-format).
        Never writes to $zero (register 0) as per MIPS architecture requirements.
        """
        if self.RegWr:
            reg_num = int(self.rd if self.RegDst else self.rt, 2)
            if reg_num != 0:  # Don't write to $zero register
                self.register_file[reg_num] = data
                self.print_stage('WB', f"Writing {data} to R[{reg_num}]")
                
    def run(self):
        """
        Main execution loop implementing the 5-stage pipeline:
        1. Instruction Fetch (IF) 
        2. Instruction Decode (ID)
        3. Execute (EX)
        4. Memory Access (MEM) 
        5. Write Back (WB)
        
        For each instruction:
        - Fetches from instruction memory at current PC
        - Decodes and sets control signals
        - Executes operation in ALU
        - Accesses data memory if needed
        - Writes results back to registers
        """
        print("\nStarting MIPS Processor Simulation...")
        
        try:
            while self.pc < self.program_end:
                print("\n" + "="*66)
                print(f"Current PC: {self.pc}")
                
                # Check if the current PC exists in instruction memory
                if self.pc not in self.instruction_memory:
                    print(f"Warning: No instruction found at PC {self.pc}, skipping...")
                    self.pc += 4
                    continue
                
                instruction = self.instruction_fetch()
                self.instruction_decode(instruction)
                result = self.execute()
                data = self.memory_access(result)
                self.writeback(data)
                
                # Print current processor state
                print("\nProcessor State:")
                print("Active Registers:", {k: v for k, v in self.register_file.items() if v != 0})
                print("Memory Contents:", {k: v for k, v in self.data_memory.items() if v != 0})
                print("-" * 110)
                time.sleep(0.5)  # Slow down simulation for visibility

            print("\nProgram Execution Complete")
            print("-" * 40)
            
            # Format final results based on program type
            if self.choice == "1":
                factorial_result = self.register_file[18]  # Get factorial result from $s2 (R18)
                self.data_memory[268501024] = factorial_result  # Store in memory
                print(f"Factorial of 10 = {factorial_result} (stored at memory address 268501024)")
            elif self.choice == "2":
                search_index = self.data_memory[268501024]  # Get search result
                if search_index == -1:
                    print("Binary Search: Number not found in array")
                else:
                    print(f"Binary Search: Found number at index {search_index}")
            else:
                print("Invalid choice. Please select either '1' for factorial or '2' for binary search.")
            print()
            
        except KeyboardInterrupt:
            print("\nSimulation interrupted by user")
        except Exception as e:
            print(f"\nError occurred: {e}")
            
if __name__ == "__main__":
    processor = MIPSProcessor()
    processor.run()