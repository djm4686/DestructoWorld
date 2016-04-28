__author__ = 'Admin'
import pygame
SPRITES = [pygame.transform.scale(pygame.image.load("../assets/images/sprites/explosion0{}.png".format(x)), (10,10)) for x in range(9)]

# Class for making explosions
# Takes the position it would be created at
class Explosion:

    def __init__(self, pos, size = (10,10)):
        self.pos = pos
        self.sprites = SPRITES
        self.active_sprite = self.sprites[0]
        self.rect = pygame.Rect(pos, size)
        self.rect.center = pos
        self.sprite_index = 0
        self.ttl = 100

    # Changes the sprite and lowers the ttl
    def update(self, dt):
        if dt > .03:
            if self.sprite_index < 8:
                self.sprite_index += 1
            else:
                self.sprite_index = 0
            self.ttl -= 10

    def draw(self, surface):
        surface.blit(self.sprites[self.sprite_index], self.rect)