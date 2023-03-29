class Control_unit:
    def __init__(self, branch, mem_read, mem_to_reg, alu_op, mem_write, alu_src, reg_write):
        self.branch = branch
        self.mem_read = mem_read
        self.mem_to_reg = mem_to_reg
        self.alu_op = alu_op
        self.mem_write = mem_write
        self.alu_src = alu_src
        self.reg_write = reg_write

    def __repr__(self):
        return '-----Signals----- \nBranch = {0}\t\tMemRead = {1}\nMemToReg = {2}\tALUOp = {3}\nMemWrite = {4}\tALUSrc = {5}\nRegWrite = {6}\n'.format(self.branch, self.mem_read, self.mem_to_reg, self.alu_op, self.mem_write, self.alu_src, self.reg_write)

