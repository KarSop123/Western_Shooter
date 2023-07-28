import pygame
from pygame.math import Vector2 as vector
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)
        self.import_assets(path)
        #self.frame_index = 0
        #self.status = 'down_idle'

        self.image = pygame.surface.Surface((100, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft = pos)

        #float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        #collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        print(path)

    def import_assets(self, path):
        self. animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

        print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

            #horizontal movement
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx

            #vertical movement
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery


    def update(self, dt):
        self.input()
        self.move(dt)