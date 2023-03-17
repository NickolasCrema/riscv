from Instruction import Instruction
class CPU:
    def __init__(self, memory):
        self.reg = [0] * 32
        self.pc = 0
        self.memory = memory

    def fetch(self):
        # buscar a instrução apontada pelo PC
        instr = self.memory[self.pc]
        self.pc += 1
        return instr

    def decode(self, instr):
        # decodificar a instrução
        opcode = (instr >> 0) & 0b1111111
        rd = (instr >> 7) & 0b11111
        funct3 = (instr >> 12) & 0b111
        rs1 = (instr >> 15) & 0b11111
        rs2 = (instr >> 20) & 0b11111
        funct7 = (instr >> 25) & 0b1111111
        imm = ((instr >> 20) & 0xfff) | ((instr >> 31) * 0xfffff000)
        return Instruction(opcode, rd, rs1, rs2, imm, funct3, funct7)

    def execute(self, instr):
        # executar a instrução
        opcode = instr.opcode
        rd = instr.rd
        rs1 = instr.rs1
        rs2 = instr.rs2
        funct3 = instr.funct3
        funct7 = instr.funct7
        imm = instr.imm

        if opcode == 0b0110011:
            # R-type instruction
            if funct3 == 0b000:
                # add
                self.reg[rd] = self.reg[rs1] + self.reg[rs2]
            elif funct3 == 0b001:
                # sll
                self.reg[rd] = self.reg[rs1] << self.reg[rs2]
            elif funct3 == 0b010:
                # slt
                self.reg[rd] = int(self.reg[rs1] < self.reg[rs2])
            elif funct3 == 0b011:
                # sltu
                self.reg[rd] = int((self.reg[rs1] & 0xffffffff) < (self.reg[rs2] & 0xffffffff))
            elif funct3 == 0b100:
                # xor
                self.reg[rd] = self.reg[rs1] ^ self.reg[rs2]
            elif funct3 == 0b101:
                # srl/sra
                if funct7 == 0b0000000:
                    # srl
                    self.reg[rd] = self.reg[rs1] >> self.reg[rs2]
                elif funct7 == 0b0100000:
                    # sra
                    self.reg[rd] = (self.reg[rs1] >> self.reg[rs2]) | (self.reg[rs1] & 0x80000000)
            elif funct3 == 0b110:
                # or
                self.reg[rd] = self.reg[rs1] | self.reg[rs2]
            elif funct3 == 0b111:
                # and
                self.reg[rd] = self.reg[rs1] & self.reg[rs2]
        elif opcode == 0b0000011:
            # lw
            address = self.reg[rs1] + imm
            self.reg[rd] = self.memory[address]

        elif opcode == 0b0100011:
            # sw
            address = self.reg[rs1] + imm
            self.memory[address] = self.reg[rs2]
        elif opcode == 0b1100011:
            # beq
            if self.reg[rs1] == self.reg[rs2]:
                self.pc += imm
        else:
            raise Exception('opcode não suportado')

    def run(self):
        while True:
            instr = self.fetch()
            if instr == 0:
                break
            instr = self.decode(instr)
            self.execute(instr)