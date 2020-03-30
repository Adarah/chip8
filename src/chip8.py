import argparse
from os import listdir, path
from time import time

import pygame

from cpu import CPU
from display_keyboard import DisplayAndKeyboard
from memory import Memory


class Chip8:
    def __init__(self, game_title, sounds, clock_speed, test):
        self.mem = Memory(game_title, test)
        self.dspkb = DisplayAndKeyboard()
        self.dspkb.set_caption(game_title)
        self.cpu = CPU(self.mem, self.dspkb)

        tick = time()
        running = True
        while running:
            pygame.time.wait(1000 // clock_speed)
            self.cpu.cycle()
            if time() - tick > 0.0167:
                if self.cpu.delay_timer > 0:
                    self.cpu.delay_timer -= 1
                if self.cpu.sound_timer > 0:
                    self.cpu.sound_timer -= 1
                    if sounds:
                        tone.play()
                tick = time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break


if __name__ == "__main__":
    pygame.init()

    tone = pygame.mixer.Sound(
        path.join(path.dirname(__file__), "sfx_sounds_button6.wav")
    )
    parser = argparse.ArgumentParser(description="Emulates Chip-8 programs")
    parser.add_argument(
        "-s", "--sound", help="toggle Chip-8 sounds. Default ON", action="store_false"
    )
    parser.add_argument(
        "-f",
        "--frequency",
        help="controls the clock speeed in Hz. Maximum value allowed is 1000Hz",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="loads test files instead of usual games",
        action="store_true",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("game_title", help="name of the game to be played", nargs="?")
    group.add_argument(
        "-l", "--list", help="lists all available games", action="store_true"
    )
    args = parser.parse_args()
    if args.list:
        file_path = path.join(path.abspath(path.dirname(__file__)), "..", "c8games")
        # getting only the files
        games = [f for f in listdir(file_path) if path.isfile(path.join(file_path, f))]
        for game in games:
            print(game)
    if args.game_title:
        if args.sound is None:
            args.sound = 1
        if args.frequency is None:
            args.frequency = 1000
        chip8 = Chip8(args.game_title, args.sound, args.frequency, args.test)
