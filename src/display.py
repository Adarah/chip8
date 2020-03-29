import pygame
from time import sleep


class DisplayAndKeyboard:
    black = (0, 0, 0)
    white = (255, 255, 255)

    def __init__(self):
        self.width, self.height = 64, 32
        self.video = [0] * 64 * 32
        self.scaling = 20
        self.screen = pygame.display.set_mode(
            (self.width * self.scaling, self.height * self.scaling)
        )
        self.delay = 1000 // 60
        pygame.init()
        # self.start_rendering()

    def start_rendering(self):
        running = True
        while running:
            # pygame.time.wait(self.delay)  # 60Hz
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                print("quit")
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.draw_pixels()
        pygame.quit()

    def set_caption(self, name: str) -> None:
        pygame.display.set_caption(name)

    def draw_pixels(self):
        pygame.display.flip()
        for row in range(64):
            for col in range(32):
                if self.video[row + col * 64] != 0:
                    pygame.draw.rect(
                        self.screen,
                        DisplayAndKeyboard.white,
                        [
                            row * self.scaling,
                            col * self.scaling,
                            1 * self.scaling,
                            1 * self.scaling,
                        ],
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        DisplayAndKeyboard.black,
                        [
                            row * self.scaling,
                            col * self.scaling,
                            1 * self.scaling,
                            1 * self.scaling,
                        ],
                    )
        self.update()

    def update(self):
        pygame.display.flip()


    @classmethod
    def init_keypad(cls):
        mapping = {
            '1': 0x01,
            '2': 0x02,
            '3': 0x03,
            '4': 0x0C,
            'q': 0x04,
            'w': 0x05,
            'e': 0x06,
            'r': 0x0D,
            'a': 0x07,
            's': 0x08,
            'd': 0x09,
            'f': 0x0E,
            'z': 0x0A,
            'x': 0x00,
            'c': 0x0B,
            'v': 0x0F,
        }
        return mapping



d = DisplayAndKeyboard()
