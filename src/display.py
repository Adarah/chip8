import pygame
from time import sleep


class Display:
    black = (0, 0, 0)
    white = (255, 255, 255)

    def __init__(self):
        self.width, self.height = 64, 32
        self.video = [0] * 64 * 32
        self.scaling = 10
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
        # self.screen.fill(Display.black)
        pygame.display.flip()
        pygame.display.update()
        for row in range(64):
            for col in range(32):
                if self.video[row + col * 64] != 0:
                    pygame.draw.rect(self.screen, Display.white, [row*self.scaling, col*self.scaling, 1*self.scaling, 1*self.scaling])
                else:
                    pygame.draw.rect(self.screen, Display.black, [row*self.scaling, col*self.scaling, 1*self.scaling, 1*self.scaling])
        pygame.display.flip()
        pygame.display.update()
        sleep(1)


d = Display()
