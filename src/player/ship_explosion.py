__author__ = 'daniel.madden'
import pygame
import destruction_nodes.explosion
EXPLOSIONS = [pygame.transform.scale(pygame.image.load("../assets/images/sprites/explosion0{}.png".format(x)), (20,20)) for x in range(9)]


# Extends Explosion. Simply changes the sprite for a ship explosion
# Takes the point the explosion happened
class ShipExplosion(destruction_nodes.explosion.Explosion):

    def __init__(self, pt):
        destruction_nodes.explosion.Explosion.__init__(self, pt, (20,20))
        self.sprites = EXPLOSIONS
