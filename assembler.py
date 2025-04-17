'''
MIPS Assembler:-
This script converts MIPS basic assembly language instructions into machine code.
'''

import os

class MIPSAssembler:
    def __init__(self):
        # MIPS instruction formats
        self.r_format = {'add': '100000', 'sub': '100010', 'and': '100100', 
                        'or': '100101', 'slt': '101010', 'srl': '000010', 
                        'sll': '000000', 'mul': '000010'}
        
        self.i_format = {'addi': '001000', 'lw': '100011', 'sw': '101011', 
                        'beq': '000100', 'bne': '000101', 'lui': '001111',
                        'ori': '001101'}
        
        self.j_format = {'j': '000010'}

        # Register mapping - expanded to include all basic registers
        self.registers = {
            '$0': '00000',  '$zero': '00000',
            '$1': '00001',  '$at': '00001',
            '$2': '00010',  '$v0': '00010',
            '$3': '00011',  '$v1': '00011',
            '$4': '00100',  '$a0': '00100',
            '$5': '00101',  '$a1': '00101',
            '$6': '00110',  '$a2': '00110',
            '$7': '00111',  '$a3': '00111',
            '$8': '01000',  '$t0': '01000',
            '$9': '01001',  '$t1': '01001',
            '$10': '01010', '$t2': '01010',
            '$11': '01011', '$t3': '01011',
            '$12': '01100', '$t4': '01100',
            '$13': '01101', '$t5': '01101',
            '$14': '01110', '$t6': '01110',
            '$15': '01111', '$t7': '01111',
            '$16': '10000', '$s0': '10000',
            '$17': '10001', '$s1': '10001',
            '$18': '10010', '$s2': '10010',
            '$19': '10011', '$s3': '10011',
            '$20': '10100', '$s4': '10100',
            '$21': '10101', '$s5': '10101',
            '$22': '10110', '$s6': '10110',
            '$23': '10111', '$s7': '10111',
            '$24': '11000', '$t8': '11000',
            '$25': '11001', '$t9': '11001',
            '$26': '11010', '$k0': '11010',
            '$27': '11011', '$k1': '11011',
            '$28': '11100', '$gp': '11100',
            '$29': '11101', '$sp': '11101',
            '$30': '11110', '$fp': '11110',
            '$31': '11111', '$ra': '11111'
        }

    def convert_immediate_to_binary(self, imm, bits=16):
        """Convert immediate value to binary representation"""
        try:
            imm = int(imm)
            if imm < 0:
                imm = (1 << bits) + imm
            return format(imm & ((1 << bits) - 1), f'0{bits}b')
        except ValueError:
            return '0' * bits

    def assemble_instruction(self, instruction):
        """Convert a single MIPS instruction to machine code"""
        parts = instruction.strip().replace(',', '').split()
        opcode = parts[0].lower()

        # Handle syscall instruction
        if opcode == 'syscall':
            return '00000000000000000000000000001100'

        # R-format instructions
        if opcode in self.r_format:
            if opcode == 'mul':
                op = '011100'
            else:
                op = '000000'
            
            if opcode in ['srl', 'sll']:
                rd = self.registers[parts[1]]
                rt = self.registers[parts[2]]
                shamt = format(int(parts[3]), '05b')
                rs = '00000'
            else:
                rd = self.registers[parts[1]]
                rs = self.registers[parts[2]]
                rt = self.registers[parts[3]]
                shamt = '00000'
            
            funct = self.r_format[opcode]
            return op + rs + rt + rd + shamt + funct

        # I-format instructions
        elif opcode in self.i_format:
            op = self.i_format[opcode]
            
            if opcode in ['beq', 'bne']:
                rs = self.registers[parts[1]]
                rt = self.registers[parts[2]]
                imm = self.convert_immediate_to_binary(parts[3])
            elif opcode == 'lui':
                rs = '00000'
                rt = self.registers[parts[1]]
                imm = self.convert_immediate_to_binary(parts[2])
            else:
                rt = self.registers[parts[1]]
                if '(' in parts[2]:  # Memory operations
                    offset, reg = parts[2].replace(')', '').split('(')
                    rs = self.registers[reg]
                    imm = self.convert_immediate_to_binary(offset)
                else:
                    rs = self.registers.get(parts[2], '00000')
                    imm = self.convert_immediate_to_binary(parts[-1])
            
            return op + rs + rt + imm

        # J-format instructions
        elif opcode in self.j_format:
            op = self.j_format[opcode]
            addr = format(int(parts[1]) >> 2, '026b')
            return op + addr

        return '0' * 32  # Invalid instruction

    def assemble_file(self, input_file, output_file):
        """Assemble MIPS assembly file to machine code"""
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for line in f_in:
                line = line.strip()
                if line and not line.startswith('//'):
                    machine_code = self.assemble_instruction(line)
                    f_out.write(machine_code + '\n')

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_message():
    """Display welcome message and status"""
    print("="*50)
    print("\tMIPS Assembler")
    print("="*50)
    print("\nAssembling files...")
    print("- Factorial program")
    print("- Binary Search program")
    print("\nDone! Output files created successfully.\n")

def main():
    assembler = MIPSAssembler()
    
    # Clear screen and show welcome message
    clear_screen()
    show_message()
    
    # Assemble programs
    assembler.assemble_file('Factorial_basic_code.asm', 'factorial.txt')
    assembler.assemble_file('Binary_Search_basic_code.asm', 'binary_search.txt')

if __name__ == "__main__":
    main()