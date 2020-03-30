import pygame


class DisplayAndKeyboard:
    black = (0, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    def __init__(self):
        self.width, self.height = 64, 32
        self.video = [0] * self.width * self.height
        self.video_buffer = [0] * self.width * self.height
        self.scaling = 20
        self.screen = pygame.display.set_mode(
            (self.width * self.scaling, self.height * self.scaling)
        )
        self.kb_to_hex = self.keyboard_to_hex()
        self.hex_to_pygame = self.hex_to_pygame_keys()

    def set_caption(self, name: str) -> None:
        pygame.display.set_caption(name)

    def draw_pixels(self):
        for row in range(self.width):
            for col in range(self.height):
                if (self.video[row + col * self.width] != 0 or self.video_buffer[row + col * self.width] != 0):
                    pygame.draw.rect(
                        self.screen,
                        DisplayAndKeyboard.green,
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
    def keyboard_to_hex(cls):
        mapping = {
            "1": 0x01,
            "2": 0x02,
            "3": 0x03,
            "4": 0x0C,
            "q": 0x04,
            "w": 0x05,
            "e": 0x06,
            "r": 0x0D,
            "a": 0x07,
            "s": 0x08,
            "d": 0x09,
            "f": 0x0E,
            "z": 0x0A,
            "x": 0x00,
            "c": 0x0B,
            "v": 0x0F,
        }
        return mapping

    @classmethod
    def hex_to_pygame_keys(cls):
        pygame_keymap = {
            0x0: pygame.K_x,
            0x1: pygame.K_1,
            0x2: pygame.K_2,
            0x3: pygame.K_3,
            0x4: pygame.K_q,
            0x5: pygame.K_w,
            0x6: pygame.K_e,
            0x7: pygame.K_a,
            0x8: pygame.K_s,
            0x9: pygame.K_d,
            0xA: pygame.K_z,
            0xB: pygame.K_c,
            0xC: pygame.K_4,
            0xD: pygame.K_r,
            0xE: pygame.K_f,
            0xF: pygame.K_v,
        }
        return pygame_keymap
