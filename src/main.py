from os import path
from utils import from_hex
from time import time
from memory import Memory
from cpu import CPU

base_path = path.dirname("disassembler.py")
file_path = path.abspath(path.join("..", "c8games", "15PUZZLE"))
DEBUG = True
SEED = int(time.time())
if DEBUG:
    SEED = 0


class Chip8:

    def __init__(self):
        mem = Memory()
        cpu = CPU()
        self.init_keypad()


    @classmethod
    def init_keypad(cls):
        return [1, 2, 3, 4, "q", "w", "e", "r", "a", "s", "d", "f", "z", "x", "c", "v"]



c = Chip8()
c.load_rom(file_path)
print(c.PC)
# print(c.memory[START_ADDRESS:])
print(c.keypad)
print(c.memory[from_hex(50) : from_hex(50) + 81])
