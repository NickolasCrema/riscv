from CPU import CPU
from Instruction import Instruction
from Parser import Parser

program = """add 1, 2, 3
lw 4, 0(5)
sub 6, 7, 8
sw 9, 4(10)
and 11, 12, 13
or 14, 15, 16
beq 17, 18, 4"""
parser = Parser()
instructions = parser.parse(text=program)
cpu = CPU(instructions)
cpu.run()