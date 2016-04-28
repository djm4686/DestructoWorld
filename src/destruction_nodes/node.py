__author__ = "Dan Madden"


# Currently unused. Used to be for determining which pixels to destroy but was too slow.
# Accessing the pixels directly now.
class Node:

    def __init__(self, pos, ide):
        self.neighbors = []
        self.pos = pos
        self.id = ide
        self.destroyed = False

    def get_id(self):
        return self.id

    def add_neighbor(self, n):
        self.neighbors.append(n)

    def remove_neighbor(self, n_id):
        for i, n in enumerate(self.neighbors):
            if n.get_id() == n_id:
                self.neighbors.pop(i)
                return True
        return False

    def destroy(self):
        for n in self.neighbors:
            n.remove_neighbor(self.id)
        self.destroyed = True

    def draw(self, surface, change_in_pos = (0,0), color = (0,0,0)):
        if not self.destroyed:
            surface.set_at((self.pos[0] + change_in_pos[0], self.pos[1] + change_in_pos[1]), color)