import pygame


class Display:
    black = (0, 0, 0)
    white = (255, 255, 255)

    def __init__(self):
        self.width, self.height = 64, 32
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
            self.screen.fill(self.black)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                    print("quit")
                    break
        pygame.quit()

    def set_caption(self, name: str) -> None:
        pygame.display.set_caption(name)


d = Display()
