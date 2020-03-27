from utils import from_hex
from consts import START_ADDRESS


class Memory:
    def __init__(self):
        self.memory = [0] * 4096
        self.stack = [0] * 16
        self.load_fonts()

    def load_rom(self, file):
        # files should be in big-endian format
        data = []
        with open(file, "rb") as f:
            address = START_ADDRESS
            for byte in iter(lambda: f.read(1), b""):
                self.memory[address] = byte
                address += 1

    def load_fonts(self):
        # some programs expect fonts to be in the memory position $50
        # this fmt comment is added so Black ignores this block
        # fmt: off
        # if you write these in binary, they represent letters/numbers, below is "F"
        # 11110000
        # 10000000
        # 11110000
        # 10000000
        # 10000000
        fonts = [
            b"\xF0", b"\x90", b"\x90", b"\x90", b"\xF0", # 0
            b"\x20", b"\x60", b"\x20", b"\x20", b"\x70", # 1
            b"\xF0", b"\x10", b"\xF0", b"\x80", b"\xF0", # 2
            b"\xF0", b"\x10", b"\xF0", b"\x10", b"\xF0", # 3
            b"\x90", b"\x90", b"\xF0", b"\x10", b"\x10", # 4
            b"\xF0", b"\x80", b"\xF0", b"\x10", b"\xF0", # 5
            b"\xF0", b"\x80", b"\xF0", b"\x90", b"\xF0", # 6
            b"\xF0", b"\x10", b"\x20", b"\x40", b"\x40", # 7
            b"\xF0", b"\x90", b"\xF0", b"\x90", b"\xF0", # 8
            b"\xF0", b"\x90", b"\xF0", b"\x10", b"\xF0", # 9
            b"\xF0", b"\x90", b"\xF0", b"\x90", b"\x90", # A
            b"\xE0", b"\x90", b"\xE0", b"\x90", b"\xE0", # B
            b"\xF0", b"\x80", b"\x80", b"\x80", b"\xF0", # C
            b"\xE0", b"\x90", b"\x90", b"\x90", b"\xE0", # D
            b"\xF0", b"\x80", b"\xF0", b"\x80", b"\xF0", # E
            b"\xF0", b"\x80", b"\xF0", b"\x80", b"\x80"  # F
        ]
        # fmt: on
        address = from_hex(50)
        for byte in fonts:
            self.memory[address] = byte
            address += 1
