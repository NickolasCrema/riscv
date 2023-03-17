from Instruction import Instruction
class Parser:
    def parse(self, text):
        instructions = []
        lines = text.strip().split('\n')
        for line in lines:
            opcode, args = line.split(' ', 1)
            if opcode == 'add':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(0b0110011, rd, rs1, rs2, 0, 0b000, 0b0000000))
            elif opcode == 'sub':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(0b0110011, rd, rs1, rs2, 0, 0b000, 0b0100000))
            elif opcode == 'and':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(0b0110011, rd, rs1, rs2, 0, 0b111, 0b0000000))
            elif opcode == 'or':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(0b0110011, rd, rs1, rs2, 0, 0b110, 0b0000000))
            elif opcode == 'lw':
                rd, imm, rs1 = map(int, args.replace('(', ',').replace(')', '').split(','))
                instructions.append(Instruction(0b0000011, rd, rs1, 0, imm, 0b010, 0b0000000))
            elif opcode == 'sw':
                rs2, imm, rs1 = map(int, args.replace('(', ',').replace(')', '').split(','))
                instructions.append(Instruction(0b0100011, 0, rs1, rs2, imm, 0b010, 0b0000000))
            elif opcode == 'beq':
                rs1, rs2, imm = map(int, args.split(','))
                instructions.append(Instruction(0b1100011, 0, rs1, rs2, imm, 0b000, 0b0000000))
            else:
                raise Exception('Opcode não suportado')
        return instructions