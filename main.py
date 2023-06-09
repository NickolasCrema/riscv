from tkinter import filedialog
from CPU import CPU
from Parser import Parser


#@Read input file, parse instructions and initiate program
filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
f = open(filename)
program = f.read()
parser = Parser()
instructions = parser.parser(text=program)
cpu = CPU(instructions)
cpu.run(0)