from os import path

from consts import START_ADDRESS


class Memory:
    def __init__(self, game_title):
        self.memory = bytearray(4096)
        self.stack = [0] * 16
        self.load_fonts()
        self.load_rom(game_title)

    def load_rom(self, file):
        # files should be in big-endian format
        file_path = path.abspath(path.join("..", "c8games", file))
        with open(file_path, "rb") as f:
            address = START_ADDRESS
            for byte in iter(lambda: f.read(1), b""):
                self.memory[address] = int.from_bytes(byte, "big")
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
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]
        # fmt: on
        address = 0x50
        for byte in fonts:
            self.memory[address] = byte
            address += 1
