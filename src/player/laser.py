from __future__ import division

__author__ = 'Admin'

import pygame
import destruction_nodes.node_map


# Object for handling the player's laser weapon
# Takes the ship's position, and the point of the player's mouse
class Laser:

    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.width = 2
        self.max_distance = 4000
        self.color = (0, 255, 0)
        self.rise = 0
        self.run = 0

    # Probably a bad ray casting function but fuck it it works.
    def cast(self, asteroid):
        # If the asteroid is too far away, ignore it
        if destruction_nodes.node_map.NodeMap.distance(asteroid.rect.center, self.start_point) > self.max_distance:
            return False
        dx = self.start_point[0] - self.end_point[0]
        dy = self.start_point[1] - self.end_point[1]
        self.rise = rise = (self.start_point[1] - self.end_point[1])
        self.run = run = (self.start_point[0] - self.end_point[0])
        # If the slope is infinite, need to check for which pixels it hits. Can't really use the line eq here
        if dx == 0:
            if dy > 0:
                i = -1
            else:
                i = 1
            cury = self.start_point[1]
            while cury != self.end_point[1]:
                if asteroid.collide_point((self.start_point[0], cury)):
                    self.end_point = self.start_point[0], cury
                    return self.start_point[0], cury
                cury += i
            return False

        m = rise/run
        b = -(self.start_point[0] * m - self.start_point[1])
        curr_point = self.start_point
        y = lambda x: m * x + b
        # Weird interactions occurred if the slope is too small or large. Had to make an edge-case for this
        if m > 2 or m < -2:
            iterator = 0
            if m > 0:
                if dx > 0:
                    ix = -1
                    iy = -1
                else:
                    ix = 1
                    iy = 1
            if m < 0:
                if dx > 0:
                    ix = -1
                    iy = 1
                else:
                    ix = 1
                    iy = -1
            # Basically loops through each individual possible pixel the line could possibly land inside.
            # Previously I only checked for when it overlaps perfectly.
            while 1000 > abs(curr_point[1] - self.end_point[1]) > 1:
                curr_point = curr_point[0], curr_point[1] + iy
                if asteroid.collide_point(curr_point):
                    self.end_point = curr_point
                    return curr_point
                iterator += iy
                if abs(iterator) >= abs(m):
                    iterator = 0
                    curr_point = curr_point[0] + ix, curr_point[1]
            return curr_point
        if dx < 0:
            i = 1
        else:
            i = -1
        # Finds the first point in the asteroid the laser hits, sets it to it's end point,
        # and returns that pixel's point
        while abs(curr_point[0] - self.end_point[0]) > 1:
            if asteroid.collide_point(curr_point):
                self.end_point = curr_point
                return curr_point
            curr_point = curr_point[0] + i, y(curr_point[0] + i)
        return False


    # Draws the laser
    def draw(self, surface):
        pygame.draw.aaline(surface, self.color, self.start_point, self.end_point, self.width)