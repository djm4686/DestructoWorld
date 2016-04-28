from __future__ import division
__author__ = 'daniel.madden'
import pygame
import time
from pygame.locals import *
import destruction_nodes.image_node_map
import destruction_nodes.explosion
import player.ship
import player.bullet
import player.laser
import player.ship_explosion
import random
import destruction_nodes.debris
import tools.vector
import resources.resource
ASTEROID_SPRITE = pygame.image.load("../assets/images/asteroid.png")


# The main world (Actually a space game but you get the idea). Handles logic and holds variables.
class World:

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.width = 1280
        self.height = 1024
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.ship = player.ship.Ship((self.width/2, self.height/2))
        self.cursor = pygame.image.load("../assets/images/cursor.png")
        self.cursor_rect = pygame.Rect((0, 0),(25, 25))
        self.mouse_pos = (0, 0)
        self.last_update = time.clock()
        self.held_keys = []
        self.origin = (0, 0)
        self.ship_destroyed = False
        self.destroy_time = 0
        self.bullets = []
        self.last_laser_update = time.clock()
        self.explosions = []
        self.resources = []
        self.debris = []
        self.asteroids = [destruction_nodes.image_node_map.ImageNodeMap(
            (600 * x + 100, 100 * x), pygame.transform.scale2x(ASTEROID_SPRITE)) for x in range(1)]
        self.viewable_objects = []
        self.laser_weapon = None
        self.holding = False
        self.main()

    def main(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def determine_resource_drop(self, pixel_colors, mag, pos):
        rcs = []
        for color in pixel_colors:
            if random.randrange(0,1000) > 995:
                red = color.r
                green = color.g
                blue = color.b
                rcs.append(resources.resource.Resource(pos, tools.vector.Vector(mag[1]*.1, mag[0]*.1), "red_resource", 10))

        return rcs

    # Changes position of all camera elements based on how much the origin changed
    # (Setting the ship back to it's original start point)
    def restart(self):
        for x in self.asteroids:
            x.rect.x -= int(self.origin[0])
            x.rect.y -= int(self.origin[1])
            x.start_pos = x.start_pos[0] - int(self.origin[0]), x.start_pos[1] - int(self.origin[1])
        for x in self.explosions:
            x.rect.x -= int(self.origin[0])
            x.rect.y -= int(self.origin[1])
        self.bullets = []
        self.viewable_objects = []
        self.laser_weapon = None
        self.origin = (0, 0)
        self.ship.velocity_vector.x = 0
        self.ship.velocity_vector.y = 0
        self.ship_destroyed = False
        self.ship.destroyed = False

    # Currently unused
    def update_asteroids(self):
        new_asteroids = []
        for asteroid in self.asteroids:
            if destruction_nodes.image_node_map.ImageNodeMap.distance(asteroid.rect.center,
                                                                          self.ship.rect.center) > 4000:
                pass
            else:
                new_asteroids.append(asteroid)
        self.asteroids = new_asteroids
        while len(self.asteroids) < 5:
            r = random.randrange(0, 4)
            if r == 0:
                self.asteroids.append(destruction_nodes.image_node_map.ImageNodeMap(
                    (random.randrange(0, 800), -random.randrange(300, 500)), ASTEROID_SPRITE))
            if r == 1:
                self.asteroids.append(destruction_nodes.image_node_map.ImageNodeMap(
                    (random.randrange(900, 1100), random.randrange(0, 600)), ASTEROID_SPRITE))
            if r == 2:
                self.asteroids.append(destruction_nodes.image_node_map.ImageNodeMap(
                    (random.randrange(0, 800), random.randrange(700, 900)), ASTEROID_SPRITE))
            if r == 3:
                self.asteroids.append(destruction_nodes.image_node_map.ImageNodeMap(
                    (-random.randrange(300, 500), random.randrange(0, 600)), ASTEROID_SPRITE))

    # Handles the updating of all variables
    def update(self):
        currtime = time.clock()
        self.ship.update(currtime - self.last_update)
        for x in self.debris:
            x.update(currtime-self.last_update)
        self.ship.face_point(self.mouse_pos)
        if self.holding and self.laser_weapon:
            self.laser_weapon.end_point = self.mouse_pos
        if self.laser_weapon and not self.ship_destroyed:
            if not self.ship.fire_laser(currtime - self.last_laser_update):
                self.laser_weapon = None
        new_resources = []
        for r in self.resources:
            r.update(currtime-self.last_update)
            if r.collide_rect(self.ship.rect):
                self.ship.pickup_resource(r)
            else:
                new_resources.append(r)
        self.resources = new_resources

        new_debris = []
        for d in self.debris:
            if not d.alpha < 1:
                new_debris.append(d)
        self.debris = new_debris
        for asteroid in self.asteroids:
            if not asteroid.out_of_range:
                if self.laser_weapon and not self.ship_destroyed:
                    self.last_laser_update = time.clock()
                    pt = self.laser_weapon.cast(asteroid)
                    if pt:
                        pixel_colors = asteroid.destroy_px_original(pt, asteroid.find_angle_to_center(pt), 2)
                        rise, run = mag = self.laser_weapon.rise, self.laser_weapon.run
                        resources = self.determine_resource_drop(pixel_colors, mag, pt)
                        self.resources += resources
                        self.explosions.append(destruction_nodes.explosion.Explosion(pt))
                        # Make some somewhat random debris
                        self.debris.append(destruction_nodes.debris.Debris(
                            pt, tools.vector.Vector(run*.1, rise*.1)))
                        self.debris.append(destruction_nodes.debris.Debris(
                            pt, tools.vector.Vector(run*random.randrange(100, 400)*.001, rise*.1)))
                        self.debris.append(destruction_nodes.debris.Debris(
                            pt, tools.vector.Vector(run*.1, rise*random.randrange(100, 400)*.001)))
                        break
                else:
                    self.laser_weapon = None
                    break
        if not self.ship_destroyed:
            for asteroid in self.asteroids:
                if not asteroid.out_of_range:
                    collide = asteroid.collide_point(self.ship.start_pos)
                    if collide:
                        pixel_colors = asteroid.destroy_px_original(
                            self.ship.start_pos, asteroid.find_angle_to_center(self.ship.start_pos), 10)
                        self.explosions.append(player.ship_explosion.ShipExplosion(self.ship.start_pos))
                        self.ship_destroyed = True
                        self.ship.destroyed = True
                        self.destroy_time = time.clock()
                        self.debris.append(destruction_nodes.debris.Debris(
                            self.ship.start_pos, tools.vector.Vector(-self.ship.velocity_vector.x*.1,
                                                                         -self.ship.velocity_vector.y*.1)))
        for asteroid in self.asteroids:
            asteroid.update(destruction_nodes.image_node_map.ImageNodeMap.distance(self.ship.rect.center,
                                                                                       asteroid.rect.center))
        currtime = time.clock()
        new_bullets = []
        # Loops through held-down keys and determines what to do
        for x in self.held_keys:
            if x == K_LCTRL and not self.ship_destroyed:
                self.ship.thrust(self.mouse_pos)
        for b in self.bullets:
            if b.ttl < 0 or self.ship_destroyed:
                pass
            else:
                b.update(currtime - self.last_update)
                throw_away = False
                for asteroid in self.asteroids:
                    if not asteroid.out_of_range:
                        if asteroid.collide_point(b.pos):
                            pixel_colors = asteroid.destroy_px_original((int(b.pos[0]), int(b.pos[1])),
                                                                        asteroid.find_angle_to_center(b.pos), 5)
                            if not pixel_colors:
                                break
                            else:
                                resources = self.determine_resource_drop(
                                    pixel_colors, (-b.velocity_vector.y * b.speed_factor, -b.velocity_vector.x * b.speed_factor), b.pos)
                                for x in resources:
                                    self.resources.append(x)
                                self.explosions.append(destruction_nodes.explosion.Explosion(b.pos))
                                # Make some somewhat random debris
                                self.debris.append(destruction_nodes.debris.Debris(b.pos, tools.vector.Vector(
                                    -b.velocity_vector.x * b.speed_factor * .4,
                                    -b.velocity_vector.y * b.speed_factor * .4)))
                                self.debris.append(destruction_nodes.debris.Debris(b.pos, tools.vector.Vector(
                                    -b.velocity_vector.x * b.speed_factor * .004*random.randrange(100, 400),
                                    -b.velocity_vector.y * b.speed_factor * .4)))
                                self.debris.append(destruction_nodes.debris.Debris(b.pos, tools.vector.Vector(
                                    -b.velocity_vector.x * b.speed_factor * .4,
                                    -b.velocity_vector.y * b.speed_factor * .004 * random.randrange(100, 400))))
                                throw_away = True
                                break
                if not throw_away:
                    new_bullets.append(b)
        self.bullets = new_bullets
        for e in self.explosions:
            e.update(currtime - self.last_update)
        if self.ship_destroyed and currtime - self.destroy_time > 1:
            self.restart()
        if currtime - self.last_update > .03:
            self.update_camera()
            self.last_update = currtime

    # Handles the camera movement and changes the position of all objects on the screen to match
    def update_camera(self):
        camera_center = self.width/2, self.height/2
        dx = self.ship.velocity_vector.x
        dy = self.ship.velocity_vector.y
        if self.ship_destroyed:
            dx /= 2
            dy /= 2
        self.origin = self.origin[0] - int(dx), self.origin[1] - int(dy)
        for x in self.bullets:
            x.pos = x.pos[0] - int(dx), x.pos[1] - int(dy)

        for d in self.debris:
            d.pos = d.pos[0] - int(dx), d.pos[1] - int(dy)
            d.rect.y -= int(dy)
            d.rect.x -= int(dx)
        for r in self.resources:
            r.pos = r.pos[0] - int(dx), r.pos[1] - int(dy)
            r.rect.y -= int(dy)
            r.rect.x -= int(dx)
        for x in self.asteroids:
            x.rect.x -= int(dx)
            x.start_pos = x.start_pos[0] - int(dx), x.start_pos[1] - int(dy)
            x.rect.y -= int(dy)
        new_explosions = []
        for x in self.explosions:
            x.rect.x = x.rect.x - dx
            x.rect.y = x.rect.y - dy
            if x.ttl <= 0:
                pass
            else:
                new_explosions.append(x)
        self.explosions = new_explosions
        self.ship.start_pos = camera_center

    # Event loop duh
    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEMOTION:
                self.mouse_pos = event.pos
                self.cursor_rect.center = self.mouse_pos
                if self.laser_weapon:
                    self.laser_weapon.end_point = self.mouse_pos
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.holding = True
                    self.laser_weapon = player.laser.Laser(self.ship.start_pos, event.pos)
                    self.last_laser_update = time.clock()
                if event.button == 1:
                    if self.ship.fire_gun():
                        self.bullets.append(player.bullet.Bullet(self.ship.start_pos, event.pos))

            if event.type == MOUSEBUTTONUP:
                self.laser_weapon = None
                self.holding = False
            if event.type == KEYDOWN:
                self.held_keys.append(event.key)
            if event.type == KEYUP:
                self.held_keys.remove(event.key)

    # Draws all objects on the screen
    def draw(self):
        self.surface.fill((0, 0, 15))

        for asteroid in self.asteroids:
            asteroid.draw(self.surface)
        for b in self.bullets:
            b.draw(self.surface)
        for e in self.explosions:
            e.draw(self.surface)
        if self.laser_weapon:
            self.laser_weapon.draw(self.surface)
        for d in self.debris:
            d.draw(self.surface)
        for r in self.resources:
            r.draw(self.surface)
        self.ship.draw(self.surface)
        self.surface.blit(self.cursor, self.cursor_rect)
        pygame.display.update()

if __name__ == "__main__":
    w = World()
