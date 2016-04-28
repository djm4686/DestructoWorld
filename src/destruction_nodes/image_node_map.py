__author__ = 'daniel.madden'
import node_map
import px_node
import pygame
import time
import math
from pygame.locals import *


# Class for all destructible images.
# Takes the position and the image it will use
class ImageNodeMap(node_map.NodeMap):

    def __init__(self, pos, image):
        self.image = image
        self.pixel_array = pygame.PixelArray(image)
        self.original_image = image.copy()
        self.original_px_array = pygame.PixelArray(self.original_image)
        self.rotation = 1
        self.last_time = time.clock()
        self.image = self.pixel_array.make_surface()
        self.out_of_range = False
        node_map.NodeMap.__init__(self, self.image.get_rect().width, self.image.get_rect().height, pos)

    # "Destroys" a pixel
    def set_px_transparent(self, px_pos):
        self.pixel_array[px_pos[0]][px_pos[1]] = 0

    # Checks if the pixel is transparent
    def is_px_active(self, px_pos):
        if px_pos[0] < 0 or px_pos[1] < 0:
            return False
        if self.pixel_array[px_pos[0]][px_pos[1]] != 0:
            return True
        else:
            return False

    # Checks if the point given overlaps a non-transparent pixel
    def collide_point(self, point):
        try:
            return self.is_px_active((int(point[0]) - int(self.start_pos[0]), int(point[1]) - int(self.start_pos[1])))
        except IndexError:
            return False

    # Rotation function stolen from the internet
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    # Finds the angle from the point given to the center of the asteroid
    def find_angle_to_center(self, point):

        center = self.image.get_rect().center

        p = point[0] - self.start_pos[0], point[1] - self.start_pos[1]
        dx = p[0] - center[0]
        dy = p[1] - center[1]

        if dx:
            if dx > 0:
                angle = math.degrees(math.atan2(-dy,dx))
            if dx < 0:
                angle = math.degrees(math.atan2(-dy,dx))
            return angle
        else:
            return 0

    # Pythagoras you rascal
    def distance_to_center(self, point):
        return node_map.NodeMap.distance(point, self.image.get_rect().center)

    # Function currently used for pixel destruction.
    # Because of an odd interaction with rotation, I needed to do it this way.
    # Got the idea from Star Trek. "I never thought to imagine space as the thing that was moving"
    # Returns a list of pixel colors that were destroyed
    def destroy_px_original(self, original_point, bullet_angle, radius):
        # Finds the angle that the bullet would have hit at if the asteroid wasn't rotating
        displacement_angle = bullet_angle-self.rotation
        distance = self.distance_to_center((original_point[0] - self.start_pos[0], original_point[1] - self.start_pos[1]))
        # Too far away; fuck it throw it out
        if distance > self.width:
            return False
        original_center = self.original_image.get_rect().center
        # These are the distances to the center of the original image (not rotated)
        y_distance = -math.sin(math.radians(displacement_angle)) * distance
        x_distance = math.cos(math.radians(displacement_angle)) * distance
        pixel_pos = int(original_center[0] + x_distance), int(original_center[1] + y_distance)
        point = pixel_pos

        # If the point is out of range anyway, nothing found
        try:
            px_array = pygame.PixelArray(self.original_image)
            x = px_array[point[0]][point[1]]

        except IndexError:
            return False
        nodes_to_destroy = [point]
        pixels = []
        # Actually destroys the pixels in a Dijkstra way
        while len(nodes_to_destroy) > 0:
            curr_node = nodes_to_destroy.pop(0)
            try:
                if (curr_node[0] + 1, curr_node[1]) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and px_array[curr_node[0] + 1][curr_node[1]] != 0:
                    nodes_to_destroy.append((curr_node[0] + 1, curr_node[1]))
            except IndexError:
                pass
            try:
                if (curr_node[0] - 1, curr_node[1]) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and px_array[curr_node[0] - 1][curr_node[1]] != 0:
                    nodes_to_destroy.append((curr_node[0] - 1, curr_node[1]))
            except IndexError:
                pass
            try:
                if (curr_node[0], curr_node[1] + 1) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and px_array[curr_node[0]][curr_node[1]+1] != 0:
                    nodes_to_destroy.append((curr_node[0], curr_node[1]+1))
            except IndexError:
                pass
            try:
                if (curr_node[0], curr_node[1] - 1) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and px_array[curr_node[0]][curr_node[1]-1] != 0:
                    nodes_to_destroy.append((curr_node[0], curr_node[1]-1))
            except IndexError:
                pass
            pixels.append(self.original_image.unmap_rgb(px_array[curr_node[0]][curr_node[1]]))
            # Make the pixel have no data
            px_array[curr_node[0]][curr_node[1]] = 0
        return pixels

    # Rotates the image
    def rotate(self):
        curtime = time.clock()
        if curtime - self.last_time > .05:
            try:
                self.pixel_array = pygame.PixelArray(self.rot_center(self.original_image, self.rotation))

            except ValueError:
                pass
            self.image = self.pixel_array.make_surface()
            self.rotation -= .08
            self.last_time = curtime

    # Not used, old destruction function
    def destroy_nodes2(self, point, radius):
        max_size = (radius + 1)**2 + radius**2
        point = int(point[0]) - self.start_pos[0], int(point[1]) - self.start_pos[1]
        try:
            x = self.pixel_array[point[0]][point[1]]
        except IndexError:
            return False
        pixels = []
        nodes_to_destroy = [point]
        while len(nodes_to_destroy) > 0:
            curr_node = nodes_to_destroy.pop(0)
            try:
                if (curr_node[0] + 1, curr_node[1]) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and self.pixel_array[curr_node[0] + 1][curr_node[1]] != 0:
                    nodes_to_destroy.append((curr_node[0] + 1, curr_node[1]))
            except IndexError:
                pass
            try:
                if (curr_node[0] - 1, curr_node[1]) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and self.pixel_array[curr_node[0] - 1][curr_node[1]] != 0:
                    nodes_to_destroy.append((curr_node[0] - 1, curr_node[1]))
            except IndexError:
                pass
            try:
                if (curr_node[0], curr_node[1] + 1) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and self.pixel_array[curr_node[0]][curr_node[1]+1] != 0:
                    nodes_to_destroy.append((curr_node[0], curr_node[1]+1))
            except IndexError:
                pass
            try:
                if (curr_node[0], curr_node[1] - 1) not in nodes_to_destroy and node_map.NodeMap.distance((curr_node[0], curr_node[1]), point) < radius and self.pixel_array[curr_node[0]][curr_node[1]-1] != 0:
                    nodes_to_destroy.append((curr_node[0], curr_node[1]-1))
            except IndexError:
                pass

            self.pixel_array[curr_node[0]][curr_node[1]] = 0
        for p in pixels:
            print self.image.unmap_rgb(p)
        return True
    # Not used, old destruction function
    def destroy_nodes(self, point, radius):
        try:

            start_node = self.nodes[point[0]-self.start_pos[0]][point[1]-self.start_pos[1]]

            if not self.is_px_active((point[0]-self.start_pos[0], point[1]-self.start_pos[1])) and start_node.destroyed:
                return False
        except IndexError:
            return False
        nodes_to_destroy = [start_node]
        i = 0
        while len(nodes_to_destroy) > 0 and len(nodes_to_destroy):
            curr_node = nodes_to_destroy.pop(0)
            for x in curr_node.neighbors:
                if x not in nodes_to_destroy and node_map.NodeMap.distance((x.pos[0] + self.start_pos[0], x.pos[1] + self.start_pos[1]), point) < radius:
                    nodes_to_destroy.append(x)
            self.pixel_array[curr_node.pos[0]][curr_node.pos[1]] = 0
            curr_node.destroy()
            i += 1
        return True

    # Another... pixel destroying... function... I guess.
    def destroy_at_pos(self, pos):
        self.pixel_array[pos[0]][pos[1]] = 0

    # Unused. Used to be for when I was making a map of all pixels for easier destruction. Turned out to be really slow
    def make_map(self):
        ide = 0
        for i, w in enumerate(self.pixel_array):
            self.nodes.append([])
            for i2, h in enumerate(w):
                n = px_node.PXNode((i, i2), ide, h)
                self.nodes[i].append(n)
                try:
                    n.add_neighbor(self.nodes[i][i2-1])
                    self.nodes[i][i2-1].add_neighbor(n)
                except IndexError:
                    pass
                try:
                    n.add_neighbor(self.nodes[i-1][i2-1])
                    self.nodes[i-1][i2-1].add_neighbor(n)
                except IndexError:
                    pass
                ide += 1

    def update(self, distance):
        if distance > 4000:
            self.out_of_range = True
        else:
            self.out_of_range = False
            self.rotate()
            

    def draw(self, surface):
        surface.blit(self.image, self.rect)


if __name__ == "__main__":
    pygame.init()
    i = ImageNodeMap((0,0), pygame.image.load("../../assets/images/asteroid.png"))
    s = pygame.display.set_mode((800,600))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                pass
        s.fill((122,122,122))
        i.draw(s)
        pygame.display.update()