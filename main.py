import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector
from settings import *
from player import Player
from sprite import Sprite, Bullet
from monster import Coffin, Cactus

pygame.init()


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('graphics/other/bg.png').convert()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        self.display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center - self.offset)
            self.display_surface.blit(sprite.image, offset_rect)


class Game():
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Western Shooter")
        self.clock = pygame.time.Clock()
        self.special_graphic = False

        if self.special_graphic:
            self.can_rotate = True
            self.bullet_surf = pygame.image.load('graphics/other/adolf.png').convert_alpha()
        else:
            self.can_rotate = False
            self.bullet_surf = pygame.image.load('graphics/other/particle.png').convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        self.setup()
        self.music = pygame.mixer.Sound('sound/music.mp3')
        self.music.set_volume(0.5)
        self.music.play(loops=-1)

    def create_bullet(self, pos, direction):
        Bullet(pos, direction,self.can_rotate, self.bullet_surf, [self.all_sprites, self.bullets])

    def bullet_collision(self):
        for obstacle in self.obstacles:
            pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask)

        for bullet in self.bullets:
            sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)
            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()


        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.damage()


    def setup(self):
        tmx_map = load_pygame('data/map.tmx')
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet)
            if obj.name == 'Coffin':
                self.coffin = Coffin(
                    pos=(obj.x, obj.y),
                    groups=(self.all_sprites, self.monsters),
                    path=PATHS['coffin'],
                    collision_sprites=self.obstacles,
                    player=self.player)
            if obj.name == 'Cactus':
                self.cactus = Cactus(
                    pos=(obj.x, obj.y),
                    groups=(self.all_sprites, self.monsters),
                    path=PATHS['cactus'],
                    collision_sprites=self.obstacles,
                    player=self.player,
                    create_bullet=self.create_bullet)

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT or len(self.monsters) == 0:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000

            # update groups
            self.all_sprites.update(dt)
            self.bullet_collision()

            # draw groups
            self.all_sprites.customize_draw(self.player)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
