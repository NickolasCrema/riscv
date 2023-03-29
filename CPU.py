from Instruction import Instruction
class CPU:
    def __init__(self,  instruction_memory):
        self.reg = {}
        for i in range(32):
            self.reg[i] = 0
        self.pc = 0
        self.memory = {}
        self.instruction_memory = instruction_memory

    def fetch(self):
        # buscar a instrução apontada pelo PC
        buf_size = len(self.instruction_memory)
        if self.pc == buf_size:
            return
        instr = self.instruction_memory[self.pc]
        self.pc += 1
        return instr

    def execute(self, instr):
        # executar a instrução
        opcode = instr.opcode
        rd = instr.rd
        rs1 = instr.rs1
        rs2 = instr.rs2
        funct3 = instr.funct3
        funct7 = instr.funct7
        imm = instr.imm

        # Tipo R
        if opcode == b'0110011':
            if funct3 == b'000' and funct7 == b'0000000':
                # add
                print('---------Instrução add---------')
                self.reg[rd] = self.reg[rs1] + self.reg[rs2]
                print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                      self.reg[rs2])
                instr.controlSignals()
            elif funct3 == b'000' and funct7 == b'0100000':
                #sub
                print('---------Instrução sub---------')
                self.reg[rd] = self.reg[rs1] - self.reg[rs2]
                print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                      self.reg[rs2])
                instr.controlSignals()
            elif funct3 == b'110':
                # or
                print('---------Instrução or---------')
                self.reg[rd] = self.reg[rs1] | self.reg[rs2]
                print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                      self.reg[rs2])
                instr.controlSignals()
            elif funct3 == b'111':
                # and
                print('---------Instrução and---------')
                self.reg[rd] = self.reg[rs1] & self.reg[rs2]
                print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                      self.reg[rs2])
                instr.controlSignals()

        #lw
        elif opcode == b'0000011':
            print('---------Instrução lw---------')
            address = self.reg[rs1] + imm
            if self.memory.get(address) == None:
                self.reg[rd] = 0
            else:
                self.reg[rd] = self.memory.get(address)
            print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=', self.reg[rs2])
            instr.controlSignals()
        #sw
        elif opcode == b'0100011':
            print('---------Instrução sw---------')
            print(self.reg[rs1], self.reg[rs2], self.memory, imm)

            address = self.reg[rs1] + imm
            self.memory[address] = self.reg[rs2]
            print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=', self.reg[rs2])
            instr.controlSignals()
        #Tipo B
        elif opcode == b'1100111':
            # beq
            if funct3 == b'000':
                print('---------Instrução beq---------')
                if self.reg[rs1] == self.reg[rs2]:
                    self.pc += imm
                    print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                          self.reg[rs2])
                    instr.controlSignals()
            elif funct3 == b'001':
                print('---------Instrução bne---------')
                if self.reg[rs1] != self.reg[rs2]:
                    self.pc += imm
                    print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                          self.reg[rs2])
                    instr.controlSignals()
        #Tipo I
        elif opcode == b'0010011':
            if funct3 == b'000':
                # addi
                print('---------Instrução addi---------')
                self.reg[rd] = self.reg[rs1] + imm
                print('rd:', rd, '=', self.reg[rd], '\trs1:', rs1, '=', self.reg[rs1], '\trs2:', rs2, '=',
                      self.reg[rs2])
                instr.controlSignals()
        else:
            raise Exception('opcode não suportado')

    def run(self):
        while True:
            instr = self.fetch()
            if instr is None:
                break
            self.execute(instr)