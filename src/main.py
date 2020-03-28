from os import path
from memory import Memory
from display import Display
from cpu import CPU


class Chip8:

    def __init__(self):
        self.mem = Memory('PONG')
        self.disp = Display()
        self.cpu = CPU(self.mem, self.disp)
        self.init_keypad()
        while True:
            pass


    @classmethod
    def init_keypad(cls):
        return [1, 2, 3, 4, "q", "w", "e", "r", "a", "s", "d", "f", "z", "x", "c", "v"]



c = Chip8()
# c.mem.load_rom(file_path)
# print(c.PC)
# # print(c.memory[START_ADDRESS:])
# print(c.keypad)
# print(c.mem.memory[0x50: 0x50 + 81])
