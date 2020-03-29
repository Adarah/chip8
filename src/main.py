from time import time

import pygame

from cpu import CPU
from display_keyboard import DisplayAndKeyboard
from memory import Memory

tone = pygame.mixer.Sound("sfx_sounds_button6.wav")


class Chip8:
    def __init__(self):
        self.mem = Memory("BRIX")
        self.dspkb = DisplayAndKeyboard()
        keymap = self.dspkb.init_keypad()
        self.cpu = CPU(self.mem, self.dspkb, keymap)
        tick = time()
        while True:
            pygame.time.wait(1)
            self.cpu.cycle()
            if time() - tick > 0.0167:
                if self.cpu.delay_timer > 0:
                    self.cpu.delay_timer -= 1
                if self.cpu.sound_timer > 0:
                    self.cpu.sound_timer -= 1
                    tone.play()
                tick = time()


c = Chip8()
