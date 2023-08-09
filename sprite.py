import pygame
from pygame.math import Vector2 as vector


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, can_rotate, surf, group):
        super().__init__(group)
        bullet_size = vector(surf.get_size())
        self.scaled_surf = pygame.transform.scale(surf, (round(bullet_size.x), round(bullet_size.y)))
        self.image = self.scaled_surf
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = vector(self.rect.center)
        self.direction = direction
        self.speed = 400

        #rotation
        self.rotation = 0
        self.rotation_speed = 300
        self.can_rotate = can_rotate

    def rotate(self, dt):
        if self.direction == vector(-1,0):
            self.rotation += self.rotation_speed * dt
        else:
            self.rotation -= self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.scaled_surf, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        if self.can_rotate:
            self.rotate(dt)
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

