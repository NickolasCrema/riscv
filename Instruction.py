class Instruction:
    """@Instructions object"""

    def __init__(self, opcode, rd, rs1, rs2, imm, funct3, funct7, control_unit):
        self.opcode = opcode
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm
        self.funct3 = funct3
        self.funct7 = funct7
        self.control_unit = control_unit

    def controlSignals(self):
        """@Print all control signals at console \n
        @Params: None \n
        @Return: None \n
        @Precondition: None \n
        @Postcondition: All control signals written at console"""
        print('opcode: ', self.opcode)
        print('funct7: ', self.funct7)
        print('funct3: ', self.funct3)
        print('imm: ', self.imm)
        print(self.control_unit)
