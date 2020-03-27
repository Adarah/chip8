from os import path
from utils import from_hex
from memory import Memory
from display import Display
from cpu import CPU

base_path = path.dirname("disassembler.py")
file_path = path.abspath(path.join("..", "c8games", "15PUZZLE"))

class Chip8:

    def __init__(self):
        self.mem = Memory()
        self.disp = Display()
        self.cpu = CPU(self.mem, self.disp)
        self.init_keypad()


    @classmethod
    def init_keypad(cls):
        return [1, 2, 3, 4, "q", "w", "e", "r", "a", "s", "d", "f", "z", "x", "c", "v"]



c = Chip8()
c.mem.load_rom(file_path)
print(c.PC)
# print(c.memory[START_ADDRESS:])
print(c.keypad)
print(c.mem.memory[from_hex(50) : from_hex(50) + 81])
