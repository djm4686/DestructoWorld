__author__ = "Dan Madden"

import math

import pygame
from pygame.locals import *
from destruction_nodes import node

# Original class for a node map. Pretty much nothing but a variable container now.
class NodeMap:

    def __init__(self, width, height, start_pos=(0, 0)):
        self.width = width
        self.height = height
        self.totalNodes = width*height
        self.nodes = []
        self.start_pos = start_pos
        self.rect = pygame.Rect(start_pos, (width, height))
        self.surface = pygame.Surface((width, height))
        #self.make_map()

    def collide_point(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def make_map(self):
        i = 0
        for w in range(self.width):
            self.nodes.append([])
            for h in range(self.height):
                n = node.Node((w + self.start_pos[0], h + self.start_pos[1]), i)
                try:
                    n.add_neighbor(self.nodes[w][h-1])
                    self.nodes[w][h-1].add_neighbor(n)
                except IndexError:
                    pass
                try:
                    n.add_neighbor(self.nodes[w-1][h-1])
                    self.nodes[w-1][h-1].add_neighbor(n)
                except IndexError:
                    pass
                self.nodes[w].append(n)
                i += 1

    def destroy_nodes(self, point, radius):
        try:
            start_node = self.nodes[point[0]-self.start_pos[0]][point[1]-self.start_pos[1]]
            if start_node.destroyed:
                return False
        except IndexError:
            return False
        if not start_node.destroyed:
            nodes_to_destroy = [start_node]
            while len(nodes_to_destroy) > 0 and len(nodes_to_destroy):
                curr_node = nodes_to_destroy.pop(0)
                for x in curr_node.neighbors:
                    if x not in nodes_to_destroy and NodeMap.distance(x.pos, point) < radius:
                        nodes_to_destroy.append(x)
                curr_node.draw(self.surface, (-self.start_pos[0], -self.start_pos[1]), (255,255,255))
                curr_node.destroy()
        return True

    @staticmethod
    def distance(pos, pos2):
        dx = pos[0] - pos2[0]
        dy = pos[1] - pos2[1]
        return math.sqrt(dx**2 + dy**2)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


def main_loop(nmap):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == MOUSEBUTTONDOWN:
                nmap.destroy_nodes(event.pos, 10)
            surface.fill((255,255,255))
            nmap.draw(surface)
            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((300,300))
    nmap = NodeMap(150, 150, (100, 100))
    main_loop(nmap)
