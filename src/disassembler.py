from typing import List
from os import path
from sys import byteorder
import struct

def dissasemble(mem: List[int]):
    pass


def load_rom(file) -> bytearray:
    data = []
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(2), b""):
            print(chunk)
            d = struct.unpack(">H", chunk)[0]  # get values in big-endian
            d = hex(d)
            data.append(d)



    print(data)

base_path = path.dirname("disassembler.py")
file_path = path.abspath(path.join("c8games", "15PUZZLE"))
read_rom(file_path)

print(byteorder)
