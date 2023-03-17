class Instruction:
    def __init__(self, opcode, rd, rs1, rs2, imm, funct3, funct7):
        self.opcode = opcode
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm
        self.funct3 = funct3
        self.funct7 = funct7

