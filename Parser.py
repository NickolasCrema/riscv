from Instruction import Instruction
from Control_unit import Control_unit
class Parser:
    def parse(self, text):
        instructions = []
        lines = text.strip().split('\n')
        for line in lines:
            opcode, args = line.split(' ', 1)
            if opcode == 'add':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(b'0110011', rd, rs1, rs2, 0, b'000', b'0000000', control_unit=Control_unit(0, 0, 0, b'00', 0, 0, 1)))
            elif opcode == 'sub':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(b'0110011', rd, rs1, rs2, 0, b'000', b'0100000', control_unit=Control_unit(0, 0, 0, b'01', 0, 0, 1)))
            elif opcode == 'and':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(b'0110011', rd, rs1, rs2, 0, b'111', b'0000000', control_unit=Control_unit(0, 0, 0, b'10', 0, 0, 1)))
            elif opcode == 'or':
                rd, rs1, rs2 = map(int, args.split(','))
                instructions.append(Instruction(b'0110011', rd, rs1, rs2, 0, b'110', b'0000000', control_unit=Control_unit(0, 0, 0, b'10', 0, 0, 1)))
            elif opcode == 'addi':
                rd, rs1, imm = map(int, args.split(','))
                instructions.append(Instruction(b'0010011', rd, rs1, 0, imm, b'000', b'0000000', control_unit=Control_unit(0, 0, 0, b'10', 0, 1, 1)))
            elif opcode == 'lw':
                rd, imm, rs1 = map(int, args.replace('(', ',').replace(')', '').split(','))
                instructions.append(Instruction(b'0000011', rd, rs1, 0, imm, b'010', b'0000000', control_unit=Control_unit(0, 1, 1, b'10', 0, 1, 1)))
            elif opcode == 'sw':
                rs2, imm, rs1 = map(int, args.replace('(', ',').replace(')', '').split(','))
                instructions.append(Instruction(b'0100011', 0, rs1, rs2, imm, b'010', b'0000000', control_unit=Control_unit(0, 0, 0, b'10', 1, 1, 0)))
            elif opcode == 'beq':
                rs1, rs2, imm = map(int, args.split(','))
                instructions.append(Instruction(b'1100111', 0, rs1, rs2, imm, b'000', b'0000000', control_unit=Control_unit(1, 0, 0, b'01', 0, 0, 0)))
            elif opcode == 'bne':
                rs1, rs2, imm = map(int, args.split(','))
                instructions.append(Instruction(b'1100111', 0, rs1, rs2, imm, b'001', b'0000000', control_unit=Control_unit(1, 0, 0, b'11', 0, 0, 0)))
            else:
                raise Exception('Opcode não suportado')
        return instructions


    def parser(self, text):
        instructions = []
        lines = text.split('\n')
        for line in lines:
            opcode = line[-7:]
            #addi
            if opcode == '0010011':
                imm = line[:12]
                rs1 = line[11:16]
                funct3 = line[16:19]
                rd = line[19:24]
                if funct3 == '000':
                    instructions.append(Instruction(opcode, rd, rs1, 0, imm, funct3, 0, control_unit=Control_unit(0, 0, 0, b'10', 0, 1, 1) ))
            #lw
            elif opcode == '0000011':
                imm = line[:12]
                rs1 = line[11:16]
                funct3 = line[16:19]
                rd = line[19:24]
                if funct3 == '010':
                    instructions.append(Instruction(opcode, rd, rs1, 0, imm, funct3, 0, control_unit=Control_unit(0, 1, 1, b'10', 0, 1, 1)))
            #r-type
            elif opcode == '0110011':
                funct7 = line[:7]
                rs2 = line[6:11]
                rs1 = line[11:16]
                funct3 = line[16:19]
                rd = line[19:24]
                #add
                if funct7 == '0000000' and funct3 == '000':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'00', 0, 0, 1)))
                #sub
                elif funct7 == '0100000' and funct3 == '000':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'01', 0, 0, 1)))
                #and
                elif funct7 == '0000000' and funct3 == '111':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'10', 0, 0, 1)))
                #or
                elif funct7 == '0000000' and funct3 == '110':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'10', 0, 0, 1)))
            #sw
            elif opcode == '0100011':
                funct7 = 'X'
                rs2 = line[6:11]
                rs1 = line[11:16]
                funct3 = line[16:19]
                imm = line[19:24]
                if funct3 == '010':
                    instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'10', 1, 1, 0)))
            #b-type
            elif opcode == '1100011':
                flag = line[:7]
                rs2 = line[6:11]
                rs1 = line[11:16]
                funct3 = line[16:19]
                imm = line[19:24]
                if flag == '1111111':
                    '''C-2 in immediate'''
                if funct3 == '000':
                    instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, 'X', control_unit=Control_unit(1, 0, 0, b'01', 0, 0, 0)))
                elif funct3 == '001':
                    instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, 'X', control_unit=Control_unit(1, 0, 0, b'11', 0, 0, 0)))
    def parser(self, text):
        instructions = []
        lines = text.split('\n')
        for line in lines:
            buf = lines.split(' ')
            if len(buf[0]) == 12:
                opcode = buf[4]
                funct3 = buf[2]
                #addi
                if opcode == '0010011' and funct3 == '000':
                    rd = buf[3]
                    imm = int(buf[0],2)
                    rs1 = int(buf[1], 2)
                    instructions.append(Instruction(opcode, rd, rs1, 0, imm, funct3, 0, control_unit=Control_unit(0, 0, 0, b'10', 0, 1, 1)))
                #lw
                elif opcode == '0000011' and funct3 == '010':
                    rd = buf[3]
                    imm = int(buf[0],2)
                    rs1 = int(buf[0],2)
                    instructions.append(Instruction(opcode, rd, rs1, 0, imm, funct3, 0, control_unit=Control_unit(0, 0, 0, b'10', 0, 1, 1)))
                else:
                    print('instrução não suportada - PARSE ERROR')
                    return
            else:
                opcode = buf[5]
                funct3 = buf[3]
                #r-type
                if opcode == '0110011':
                    funct7 = buf[0]
                    rs2 = buf[1]
                    rs1 = buf[2]
                    rd = buf[4]
                    if funct7 == '0000000':
                        #add
                        if funct3 == '000':
                            instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'00', 0, 0, 1) ))
                        #and
                        elif funct3 == '111':
                            instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'10', 0, 0, 1)))
                        #or
                        elif funct3 == '110':
                            instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'10', 0, 0, 1)))
                        else:
                            print('instrução não suportada - PARSE ERROR')
                            return
                    elif funct7 == '0100000':
                        #sub
                        if funct3 == '000':
                            instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'01', 0, 0, 1)))
                        else:
                            print('instrução não suportada - PARSE ERROR')
                            return
                #sw
                elif opcode == '0100011':
                    if funct3 == '010':
                        funct7 = buf[0]
                        rs2 = buf[1]
                        rs1 = buf[2]
                        imm = buf[4]
                        instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, funct7, control_unit=Control_unit(0, 0, 0, b'10', 1, 1, 0)))
                #b-type
                elif opcode == '1100111':
                    funct7 = buf[0]
                    #beq
                    if funct3 == '000':
                        if funct7 == '0000000':
                            ''''do something'''
                        elif funct7 == '1111111':
                            ''''do something'''
                        else:
                            print("erro 'funct7' - PARSE ERROR")
                    #bne
                    elif funct3 == '001':
                        if funct7 == '0000000':
                            ''''do something'''
                        elif funct7 == '1111111':
                            '''do something'''
                        else:
                            print("erro 'funct7' - PARSE ERROR")
                    else:
                        print('instrução não suportada - PARSE ERROR')
