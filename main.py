from CPU import CPU
from Instruction import Instruction
from Parser import Parser

program = """addi 5,0,3
addi 6,0,10
addi 10,0,20
sw  5,0(10)
sw 6,4(10)
lw 11, 0(10)
lw 12,4(10)
add 14, 11, 12
sub 15, 12, 11
sub 16, 11, 12
and 17, 12, 11
or 18, 11, 12"""
parser = Parser()
instructions = parser.parse(text=program)
cpu = CPU(instructions)
cpu.run()