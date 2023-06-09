from Instruction import Instruction
from ControlUnit import ControlUnit

class Parser:
    """@RISC_V PARSER"""

    def parser(self, text):
        """@Parses binary instructions to type 'Instruction' instructions \n
        @Params:
          - text: String that represents full text of an instructions file \n
        @Return:
          - instructions: List containing all the parsed instructions \n
        @Precondition: File read correctly \n
        @Postcondition: Parsed instructions"""
        instructions = []
        lines = text.split('\n')
        for line in lines:
            opcode = line[-7:]
            #addi
            if opcode == '0010011':
                imm = int(line[:12], 2)
                rs1 = int(line[12:17], 2)
                funct3 = line[17:20]
                rd = int(line[20:25], 2)
                if funct3 == '000':
                    instructions.append(Instruction(opcode, rd, rs1, 0, imm, funct3, 'X', control_unit=ControlUnit(0, 0, 0, b'10', 0, 1, 1)))
            #lw
            elif opcode == '0000011':
                imm = int(line[:12], 2)
                rs1 = int(line[12:17], 2)
                funct3 = line[17:20]
                rd = int(line[20:25], 2)
                if funct3 == '010':
                    instructions.append(Instruction(opcode, rd, rs1, 0, imm, funct3, 0, control_unit=ControlUnit(0, 1, 1, b'10', 0, 1, 1)))
            #r-type
            elif opcode == '0110011':
                funct7 = line[:7]
                rs2 = int(line[7:12], 2)
                rs1 = int(line[12:17], 2)
                funct3 = line[17:20]
                rd = int(line[20:25], 2)

                #add
                if funct7 == '0000000' and funct3 == '000':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=ControlUnit(0, 0, 0, b'00', 0, 0, 1)))
                #sub
                elif funct7 == '0100000' and funct3 == '000':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=ControlUnit(0, 0, 0, b'01', 0, 0, 1)))
                #and
                elif funct7 == '0000000' and funct3 == '111':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=ControlUnit(0, 0, 0, b'10', 0, 0, 1)))
                #or
                elif funct7 == '0000000' and funct3 == '110':
                    instructions.append(Instruction(opcode, rd, rs1, rs2, 0, funct3, funct7, control_unit=ControlUnit(0, 0, 0, b'10', 0, 0, 1)))
            #sw
            elif opcode == '0100011':
                funct7 = 'X'
                rs2 = int(line[7:12], 2)
                rs1 = int(line[12:17], 2)
                funct3 = line[17:20]
                imm = int(line[20:25], 2)
                if funct3 == '010':
                    instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, funct7, control_unit=ControlUnit(0, 0, 0, b'10', 1, 1, 0)))
            #b-type
            elif opcode == '1100011':
                flag = line[:7]
                rs2 = int(line[7:12], 2)
                rs1 = int(line[12:17], 2)
                funct3 = line[17:20]
                imm = str(line[20:25])
                if flag == '1111111':
                    if funct3 == '000':
                        imm = int(self.reverse_2_complement(imm), 2)
                        instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, flag, control_unit=ControlUnit(1, 0, 0, b'01', 0, 0, 0)))
                    elif funct3 == '001':
                        imm = int(self.reverse_2_complement(imm), 2)
                        print('imm', imm)
                        instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, flag, control_unit=ControlUnit(1, 0, 0, b'11', 0, 0, 0)))
                if flag == '0000000':
                    if funct3 == '000':
                        imm = int(self.reverse_2_complement(imm), 2)
                        instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, flag, control_unit=ControlUnit(1, 0, 0, b'01', 0, 0, 0)))
                    elif funct3 == '001':
                        imm = int(self.reverse_2_complement(imm), 2)
                        instructions.append(Instruction(opcode, 0, rs1, rs2, imm, funct3, flag, control_unit=ControlUnit(1, 0, 0, b'11', 0, 0, 0)))
        return instructions

    def reverse_2_complement(self, text):
        """@Decode 2s complement binary to an unsigned representation binary \n
        @Params:
           - text: String representing binary to be decoded \n
        @Return:
           - str_bin: String that represents the binary decoded \n
        @Precondition: Input binary string must be at 2s complement representation \n
        @Postcondition: Returns the unsigned representation of the binary"""
        list = []
        for i in text:
            list.append(i)
        if list[len(list) - 1] == '1':
            list[len(list) - 1] = '0'
            for i in range(len(list)):
                if list[i] == '1':
                    list[i] = '0'
                else:
                    list[i] = '1'
            if list[len(list) - 1] == '0':
                list[len(list) - 1] = '1'
            else:
                for j in reversed(range(len(list))):
                    if list[j] == '0':
                        list[j] = '1'
                        break
                    else:
                        list[j] = '0'
        elif list[len(list)-1] == '0':
            for i in reversed(range(len(list))):
                if list[i] == '0':
                    list[i] = '1'
                else:
                    list[i] = '0'
                    break
            for i in range(len(list)):
                if list[i] == '1':
                    list[i] = '0'
                else:
                    list[i] = '1'
            if list[len(list) - 1] == '0':
                list[len(list) - 1] = '1'
            else:
                for j in reversed(range(len(list))):
                    if list[j] == '0':
                        list[j] = '1'
                        break
                    else:
                        list[j] = '0'

        str_bin = ''.join(list)
        return str_bin