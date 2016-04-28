__author__ = 'daniel.madden'
import pygame
RESOURCES = {"red_resource": pygame.transform.scale(pygame.image.load("../assets/images/resources/red_resource.png"), (10,10))}


class Resource:

    def __init__(self, pos, velocity, name, value):
        self.pos = pos
        self.name = name
        self.value = value
        self.velocity_vector = velocity
        self.image = RESOURCES[name]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def collide_point(self, point):
        return self.rect.collidepoint(point)

    def collide_rect(self, rect):
        return self.rect.colliderect(rect)

    def update(self, dt):
        self.pos = self.pos[0] + self.velocity_vector.x * dt, self.pos[1] + self.velocity_vector.y * dt
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)