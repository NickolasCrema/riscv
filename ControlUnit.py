class ControlUnit:
    """@Class for control unit"""
    def __init__(self, branch, mem_read, mem_to_reg, alu_op, mem_write, alu_src, reg_write):
        self.branch =  branch
        self.mem_read = mem_read
        self.mem_to_reg = mem_to_reg
        if alu_op == b'10' or alu_op == b'11':
            self.alu_op2 = 1
        else:
            self.alu_op2 = 0
        if alu_op == b'01' or alu_op == b'11':
            self.alu_op1 = 1
        else:
            self.alu_op1 = 0
        self.mem_write = mem_write
        self.alu_src = alu_src
        self.reg_write = reg_write

    def __repr__(self):
        """@Object string representation"""
        return '-----Signals----- \nBranch = {0}\t\tMemRead = {1}\nAluOp1 = {2}\t\tMemToReg = {3}\nALUOp2 = {4}\t\tMemWrite = {5}\nALUSrc = {6}\t\tRegWrite = {7}'.format(self.branch, self.mem_read, self.alu_op1, self.mem_to_reg, self.alu_op2, self.mem_write, self.alu_src, self.reg_write)

