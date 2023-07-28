import pygame, sys
from settings import *
from player import Player

pygame.init()


class Game():
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Western Shooter")
        self.clock = pygame.time.Clock()

        #groups
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        Player((200,200), self.all_sprites, PATHS['player'], None)

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            self.display_surface.fill((124, 23, 1))

            #update groups
            self.all_sprites.update(dt)

            #draw groups
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
