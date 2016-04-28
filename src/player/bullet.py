__author__ = 'daniel.madden'
import pygame
import math
import tools.vector
BULLET_SPRITE = pygame.transform.scale(pygame.image.load("../assets/images/bullet.png"), (4, 10))


# Holds logic and data for bullets
# Takes the ship's position and the point of the players mouse when the click is issued
class Bullet:

    def __init__(self, pos, click_point):
        self.pos = pos
        self.image = BULLET_SPRITE
        dx = pos[0] - click_point[0]
        dy = pos[1] - click_point[1]
        dist = distance(pos, click_point)

        # Makes the velocity the same regardless of distance to the click
        velocity = tools.vector.Vector(-dx/dist, -dy/dist)

        self.velocity_vector = velocity
        self.speed_factor = 125
        self.ttl = 15
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.face_point(click_point)

    def face_point(self, point):
        dx = point[0] - self.pos[0]
        dy = point[1] - self.pos[1]
        if dx:
            if dx > 0:
                self.image = pygame.transform.rotate(self.image, math.degrees(math.atan(-dy/dx))-90)
            if dx < 0:
                self.image = pygame.transform.rotate(self.image, math.degrees(math.atan(-dy/dx))+90)
    def update(self, dt):
        self.pos = self.pos[0] + (self.velocity_vector.x * dt * self.speed_factor), self.pos[1] + (self.velocity_vector.y  * dt * self.speed_factor)
        self.rect.center = self.pos
        self.ttl -= dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def distance(pos, pos2):
        dx = pos[0] - pos2[0]
        dy = pos[1] - pos2[1]
        return math.sqrt(dx**2 + dy**2)