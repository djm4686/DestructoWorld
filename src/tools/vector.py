__author__ = 'daniel.madden'

import math


# Basic 2D Vector
# Takes x and y vector magnitudes
class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_vector(self, v):
        self.x += v.x
        self.y += v.y

    # Just Pythagorean things
    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)