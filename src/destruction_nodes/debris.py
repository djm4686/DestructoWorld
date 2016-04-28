__author__ = 'daniel.madden'
import pygame, random
DEBRIS_SPRITE = pygame.transform.scale(pygame.image.load("../assets/images/asteroid_debris.png"), (5,5))
DEBRIS_SPRITE2 = pygame.transform.scale(pygame.image.load("../assets/images/asteroid_debris2.png"), (5,5))


# Class for making the debris from weapon hits
# Takes the position it will be at, and the vector of movement
class Debris:

    def __init__(self, pos, vector):
        self.velocity_vector = vector
        self.image = random.choice([DEBRIS_SPRITE, DEBRIS_SPRITE2])
        self.rect = pygame.Rect(pos, (self.image.get_rect().width, self.image.get_rect().height))
        self.pos = pos
        self.initial_mag = self.velocity_vector.get_magnitude()
        self.image = self.image.convert()
        self.alpha = 255

    def update(self, dt):
        self.rect.x += self.velocity_vector.x * .1
        self.rect.y += self.velocity_vector.y * .1
        self.pos = self.pos[0] + self.velocity_vector.x * dt, self.pos[1] + self.velocity_vector.y * dt
        self.velocity_vector.x *= .98
        self.velocity_vector.y *= .98
        self.alpha *= .9
        self.image.set_alpha(self.alpha)

    def draw(self, surface):
        surface.blit(self.image, self.rect)