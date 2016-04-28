from __future__ import division
__author__ = 'daniel.madden'

import tools.vector
import pygame
import math


# Holds things needed for a player's ship
# Takes the initial position. In this game it'll always be the middle of the screen
class Ship:

    def __init__(self, pos):
        self.velocity_vector = tools.vector.Vector(0,0)
        self.start_pos = pos
        self.rect = pygame.Rect(pos, (30, 30))
        self.speed_factor = 2
        self.direction = 0
        self.sprite = pygame.transform.scale(pygame.image.load("../assets/images/red_ship.png"), (25,25))
        self.original_sprite = pygame.transform.scale(pygame.image.load("../assets/images/red_ship.png"), (25,25))
        self.rect.center = self.start_pos
        self.laser_cap = 1000
        self.max_cap = 1000
        self.gun_cap = 1000
        self.destroyed = False
        self.resources = {"red_resource" : 0}
        self.make_weapon_bar()

    def pickup_resource(self, resource):
        self.resources[resource.name] += resource.value

    # Makes the rects for the laser and gun capacity
    def make_weapon_bar(self):
        self.laser_bar_rect = pygame.Rect(10, 10, 150, 25)
        self.gun_bar_rect = pygame.Rect(10, 40, 150, 25)
        self.laser_cap_rect = pygame.Rect(12, 12, int((self.laser_cap/self.max_cap)*146), 21)
        self.gun_cap_rect = pygame.Rect(12, 42, int((self.gun_cap/self.max_cap)*146), 21)

    def make_resource_pane(self):
        pass

    # Updates everything needed for the ship
    def update(self, dt):
        self.make_weapon_bar()
        self.laser_cap += 100 * dt
        if self.laser_cap >= self.max_cap:
            self.laser_cap = self.max_cap
        self.gun_cap += 50 * dt
        if self.gun_cap >= self.max_cap:
            self.gun_cap = self.max_cap

    # Changes the gun capacity
    def fire_gun(self):
        if self.gun_cap - 100 <= 0:
            return False
        else:
            self.gun_cap -= 100
            return True

    # Changes the laser capacity
    def fire_laser(self, dt):
        self.laser_cap -= 1000 * dt
        if self.laser_cap <= 0:
            return False
        else:
            return True

    # A function found online for rotating an image about its center
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    # Actually rotates the ship to point to the point passed
    def face_point(self, point):
        dx = point[0] - self.start_pos[0]
        dy = point[1] - self.start_pos[1]
        if dx:
            if dx > 0:
                self.sprite = self.rot_center(self.original_sprite, math.degrees(math.atan(-dy/dx))-90)
            if dx < 0:
                self.sprite = self.rot_center(self.original_sprite, math.degrees(math.atan(-dy/dx))+90)

    # Updates ship velocity
    def thrust(self, pos):
        dist = distance(pos, self.start_pos)
        dx = pos[0] - self.start_pos[0]
        dy = pos[1] - self.start_pos[1]
        vx = self.velocity_vector.x + dx/dist * .2
        vy = self.velocity_vector.y + dy/dist * .2
        if abs(vx) > 10:
            if abs(vy) > 10:
                pass
            else:
                self.velocity_vector.y = vy
        elif abs(vy) > 10:
            self.velocity_vector.x = vx
        else:
            self.velocity_vector.x = vx
            self.velocity_vector.y = vy


    #Draws the ship and weapon capacity bars
    def draw(self, surface):
        #print self.rect.x, self.rect.y
        pygame.draw.rect(surface, (255,255,255), self.laser_bar_rect,2)
        pygame.draw.rect(surface, (0,255,0), self.laser_cap_rect)
        pygame.draw.rect(surface, (255,255,255), self.gun_bar_rect,2)
        pygame.draw.rect(surface, (255,0,0), self.gun_cap_rect)

        if not self.destroyed:
            surface.blit(self.sprite, self.rect)

# Basic Pythagorean distance formula
def distance(pos, pos2):
        dx = pos[0] - pos2[0]
        dy = pos[1] - pos2[1]
        return math.sqrt(dx**2 + dy**2)