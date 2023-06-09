from Instruction import Instruction
import os

class CPU:
    """@Class which represents the RISCV Machine"""

    def __init__(self,  instruction_memory):
        self.reg = {}
        for i in range(32):
            self.reg[i] = 0
        self.pc = 0
        self.memory = {}
        self.instruction_memory = instruction_memory

    def fetch(self):
        """@Fetch instruction at PC in instruction memory \n
        @Params: None \n
        @Return: Instruction found \n
        @Precondition: Must have at least one instruction at instruction memory \n
        @Postcondition: Returns instruction found at PC"""
        buf_size = len(self.instruction_memory)
        if self.pc == buf_size:
            return
        instr = self.instruction_memory[self.pc]
        return instr

    def execute(self, instr):
        """@Simulates instruction execute \n
        @Params:
           - instr: String to represent instruction
        @Return: Void \n
        @Precondition: Fetch Method must had found at least one instruction \n
        @Postcondition: Execute instruction and print his details to console"""

        # executar a instrução
        opcode = instr.opcode
        rd = instr.rd
        rs1 = instr.rs1
        rs2 = instr.rs2
        funct3 = instr.funct3
        funct7 = instr.funct7
        imm = instr.imm
        result_instruction_literal = ''
        instruction_literal = ''

        #r-type
        if opcode == '0110011':
            if funct3 == '000' and funct7 == '0000000':
                # add
                print('---------Instrução add---------')
                self.reg[rd] = self.reg[rs1] + self.reg[rs2]
                instruction_literal = 'add x{0}, x{1}, x{2}'.format(rd, rs1, rs2)
                result_instruction_literal = 'x{0} = {1} + {2}'.format(rd, self.reg[rs1], self.reg[rs2])
                print('literal: ', instruction_literal)
                print('resultado: ', result_instruction_literal)
                instr.controlSignals()
            elif funct3 == '000' and funct7 == '0100000':
                #sub
                print('---------Instrução sub---------')
                self.reg[rd] = self.reg[rs1] - self.reg[rs2]
                instruction_literal = 'sub x{0}, x{1}, x{2}'.format(rd, rs1, rs2)
                result_instruction_literal = 'x{0} = {1} - {2}'.format(rd, self.reg[rs1], self.reg[rs2])
                print('literal: ', instruction_literal)
                print('resultado: ', result_instruction_literal)
                instr.controlSignals()
            elif funct3 == '110':
                # or
                print('---------Instrução or---------')
                self.reg[rd] = self.reg[rs1] | self.reg[rs2]
                instruction_literal = 'or x{0}, x{1}, x{2}'.format(rd, rs1, rs2)
                result_instruction_literal = 'x{0} = {1} OR {2}'.format(rd, self.reg[rs1], self.reg[rs2])
                print('literal: ', instruction_literal)
                print('resultado: ', result_instruction_literal)
                instr.controlSignals()
            elif funct3 == '111':
                # and
                print('---------Instrução and---------')
                self.reg[rd] = self.reg[rs1] & self.reg[rs2]
                instruction_literal = 'and x{0}, x{1}, x{2}'.format(rd, rs1, rs2)
                result_instruction_literal = 'x{0} = {1} AND {2}'.format(rd, self.reg[rs1], self.reg[rs2])
                print('literal: ', instruction_literal)
                print('resultado: ', result_instruction_literal)
                instr.controlSignals()
            self.pc += 1
        #lw
        elif opcode == '0000011':
            print('---------Instrução lw---------')
            address = self.reg[rs1] + imm
            if self.memory.get(address) == None:
                self.reg[rd] = 0
            else:
                self.reg[rd] = self.memory.get(address)
            instruction_literal = 'lw x{0}, x{1}({2})'.format(rd, imm, rs1)
            result_instruction_literal = "loaded: '{0}' from memory[{1}] to x{2}".format(self.reg[rd], address, rd)
            print('literal: ', instruction_literal)
            print('resultado: ', result_instruction_literal)
            instr.controlSignals()
            self.pc += 1
        #sw
        elif opcode == '0100011':
            print('---------Instrução sw---------')
            address = self.reg[rs1] + imm
            self.memory[address] = self.reg[rs2]
            instruction_literal = 'sw x{0}, x{1}({2})'.format(rs2, imm, rs1)
            result_instruction_literal = "stored: '{0}' at memory[{1}]".format(self.memory[address], address)
            print('literal: ', instruction_literal)
            print('resultado: ', result_instruction_literal)
            instr.controlSignals()
            self.pc += 1
        #b-type
        elif opcode == '1100011':
            # beq
            if funct3 == '000':
                print('---------Instrução beq---------')
                if funct7 == '0000000':
                    if self.reg[rs1] == self.reg[rs2]:
                        self.pc += imm//4
                        instruction_literal = 'beq x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} == {1}, PC + {2}'.format(self.reg[rs1], self.reg[rs2], imm)
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()
                    else:
                        self.pc += 1
                        instruction_literal = 'beq x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} != {1}, PC + 4'.format(self.reg[rs1], self.reg[rs2])
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()
                elif funct7 == '1111111':
                    if self.reg[rs1] == self.reg[rs2]:
                        self.pc -= imm//4
                        instruction_literal = 'beq x{0}, x{1}, -{2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} == {1}, PC - {2}'.format(self.reg[rs1], self.reg[rs2],imm)
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()
                    else:
                        self.pc += 1
                        instruction_literal = 'beq x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} == {1}, PC + 4'.format(self.reg[rs1], self.reg[rs2])
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()
            #bne
            elif funct3 == '001':
                print('---------Instrução bne---------')
                if funct7 == '0000000':
                    if self.reg[rs1] != self.reg[rs2]:
                        self.pc += imm//4
                        instruction_literal = 'beq x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} != {1}, PC + {2}'.format(self.reg[rs1], self.reg[rs2],imm)
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()
                    else:
                        self.pc += 1
                        instr.controlSignals()
                        instruction_literal = 'bne x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} == {1}, PC + 4'.format(self.reg[rs1], self.reg[rs2])
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                if funct7 == '1111111':
                    if self.reg[rs1] != self.reg[rs2]:
                        self.pc -= imm//4
                        instruction_literal = 'beq x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} != {1}, PC - {2}'.format(self.reg[rs1], self.reg[rs2],imm)
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()
                    else:
                        self.pc += 1
                        instruction_literal = 'beq x{0}, x{1}, {2}'.format(rs1, rs2, imm)
                        result_instruction_literal = '{0} != {1}, PC + 4'.format(self.reg[rs1], self.reg[rs2])
                        print('literal: ', instruction_literal)
                        print('resultado: ', result_instruction_literal)
                        instr.controlSignals()

        #addi
        elif opcode == '0010011':
            if funct3 == '000':
                print('---------Instrução addi---------')
                self.reg[rd] = self.reg[rs1] + imm
                instruction_literal = 'addi x{0}, x{1}, {2}'.format(rd, rs1, imm)
                result_instruction_literal = 'x{0} = {1} + {2}'.format(rd, self.reg[rs1], imm)
                print('literal: ', instruction_literal)
                print('resultado: ', result_instruction_literal)
                instr.controlSignals()

            self.pc += 1
        else:
            raise Exception('opcode não suportado')


    def run(self, i):
        """@Auxiliary method to recursively iterate program execute \n
        @Params:
           - i: Integer that represents current cpu cycle
        @Return: None \n
        @Precondition: None \n
        @Postcondition: Run program"""
        instr = self.fetch()
        if instr is None:
            print('PROGRAMA ENCERRADO')
            return
        print('------------------ Ciclo {0} ------------------'.format(i + 1))
        print('PC:', self.pc * 4)
        self.execute(instr)
        i+=1
        print('-----REGISTRADORES-----')
        count=0
        for key, value in self.reg.items():
            print('x{0} = {1}\t\t'.format(key, value), end='')
            count+=1
            if count%4 == 0:
                print('')
        print('-----MEMÓRIA------')
        print(self.memory)
        print('\nAPERTER [ENTER] PARA PRÓXIMA INSTRUÇÃO')
        input()
        os.system('cls') or None
        self.run(i)