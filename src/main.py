import pygame
from os import path
from memory import Memory
from display import DisplayAndKeyboard
from cpu import CPU
from time import sleep


class Chip8:

    def __init__(self):
        self.mem = Memory('TICTAC')
        self.dspkb = DisplayAndKeyboard()
        keymap = self.dspkb.init_keypad()
        self.cpu = CPU(self.mem, self.dspkb, keymap)
        while True:
            sleep(0.002)
            self.cpu.cycle()





c = Chip8()
