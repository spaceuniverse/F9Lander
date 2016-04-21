# -------------------------------------------------- #
# --------------------_F9_Lander_------------------- #
# ----------------------SERVER---------------------- #
# -------------------------------------------------- #
# imports

import pygame
from pygame.locals import *
import numpy as np
import argparse

# for external control commands
import socket

# for delay in debug launch
import time

# -------------------------------------------------- #
# physics

import Box2D
from Box2D.b2 import *

# -------------------------------------------------- #
# drawing and mode options


class Options(object):
    def __init__(self, mode, ip, port):
        self.pixels_per_meter = 10
        self.screen_width = 1024
        self.screen_height = 768
        self.target_fps = 90   # 60
        # SOCKET, PIPE OR KEYBOARD PARAMETER HERE
        # socket address ('127.0.0.1', 50007)
        self.commands = "socket" if mode else "keyboard"   # "keyboard" "socket" | in future "fifo" and "rest"
        #
        self.address = (ip, port)
        #
        self.colors = {staticBody: (255, 255, 255, 255), dynamicBody: (0, 0, 255, 255)}


# -------------------------------------------------- #


class World(object):
    def __init__(self, options):
        self.screen_width = options.screen_width
        self.screen_height = options.screen_height
        self.pixels_per_meter = options.pixels_per_meter
        self.colors = options.colors
        #
        self.wind = True
        self.wind_str = np.random.random_integers(-39, 39) * 1.0   # 70
        #
        self.gravity = -30.0
        #
        self.world = world(gravity=(0, self.gravity), doSleep=False)


# -------------------------------------------------- #


class Platform(object):
    def __init__(self, world_obj):
        self.type = "decoration"
        self.color = (255, 255, 255, 255)
        self.position_x = (world_obj.screen_width / world_obj.pixels_per_meter) / 2
        self.position_y = 3.1   # 3
        self.position_angle = 0
        #
        self.height = 0.8
        self.width = 12
        #
        self.vel_x = 0.0
        self.vel_y = 0.0
        # CreateDynamicBody CreateStaticBody
        # b2PolygonShape(vertices=[(-1,0),(1,0),(0,2)])
        self.body = world_obj.world.CreateKinematicBody(position=(self.position_x, self.position_y),
                                                        angle=self.position_angle,
                                                        # shapes=polygonShape(box=(12, 0.8)),
                                                        userData="decoration_body")
        # box=(self.width, self.height),   # 0.8
        self.box = self.body.CreatePolygonFixture(vertices=[(-self.width, 0),
                                                            (-self.width, self.height),
                                                            (self.width, self.height),
                                                            (self.width, 0),
                                                            (self.width - 2.2, -self.height),
                                                            (-self.width + 2.2, -self.height)],
                                                  density=0,
                                                  friction=0.3,
                                                  restitution=0, userData="platform")
        self.live = True
        self.report()

    def __inc_angle__(self):
        self.position_angle += 0.025
        if self.position_angle >= 360:
            self.position_angle = 0

    def __angle_flow__(self):
        self.body.angle = np.sin(self.position_angle) / 30

    def __position_go__(self):
        self.vel_x = np.sin(self.position_angle) * 1.3   # / 30
        self.vel_y = np.sin(self.position_angle) * 1.5   # / 50
        self.body.linearVelocity = (self.vel_x, self.vel_y)

    def act(self):
        self.__inc_angle__()
        self.__angle_flow__()
        self.__position_go__()

    def report(self):
        # delete returning of fixture and body
        # return {"type": "decoration", "p_body": self.body, "angle": self.body.angle,
        #        "px": self.body.position[0], "py": self.body.position[1], "fixtures": self.body.fixtures}
        return {"type": "decoration", "angle": self.body.angle, "px": self.body.position[0],
                "py": self.body.position[1], "vx": self.body.linearVelocity[0], "vy": self.body.linearVelocity[1]}


# -------------------------------------------------- #


class Rocket(object):
    def __init__(self, world_obj):
        self.type = "actor"
        self.world_obj = world_obj   # not optimal
        self.color = (np.random.random_integers(50, 150), np.random.random_integers(50, 150), 255, 255)
        self.position_x = (world_obj.screen_width / world_obj.pixels_per_meter) / 2 + np.random.random_integers(-21, 21)
        self.position_y = (world_obj.screen_height / world_obj.pixels_per_meter) / 4 * 4
        self.position_angle = 0
        #
        self.wind = world_obj.wind
        self.wind_str = world_obj.wind_str
        #
        self.height = 7.1
        self.width = 0.7
        # rocket architecture | boxes and blocks
        self.body = world_obj.world.CreateDynamicBody(position=(self.position_x, self.position_y),
                                                      angle=self.position_angle,
                                                      userData="actor_body")
        self.box = self.body.CreatePolygonFixture(box=(self.width, self.height),
                                                  density=1,
                                                  friction=0.3,
                                                  userData="frame")   # 0.3
        # self.box2 = self.body.CreatePolygonFixture(box=(4, 2), density=1, friction=0.3)
        self.box2 = self.body.CreatePolygonFixture(vertices=[(-2, -self.height),
                                                             (2, -self.height),
                                                             (1.2, -self.height + 0.9),
                                                             (-1.2, -self.height + 0.9)],
                                                   density=1,
                                                   friction=0.3,
                                                   userData="wings")   # for naming this fixture
        self.fuel = 999.9   # 100.0
        self.consumption = 1.0   # 0.1
        # add penalty to durability depending on the fuel balance | in order to make strategy more complex
        self.durability = 9.0   # 1.0
        #
        self.body.linearVelocity[1] = -39.0   # -30.0
        self.body.linearVelocity[0] = np.random.random_integers(-39, 39) * 1.0   # -20.0 | -30.0 in video
        #
        self.body.angle += 0.2999 * (self.body.linearVelocity[0] / 39.0)   # np.sign(self.body.linearVelocity[0])
        #
        self.enj = True
        self.left_enj_power = 500.0
        self.right_enj_power = 500.0
        self.main_enj_power = 700.0   # default 500.0 if 599.0 or 700.0 minus to fuel
        #
        self.live = True
        self.contact = False
        self.dist1 = 999.0   # placeholder for 1 fixture
        self.dist2 = 999.0   # placeholder for 2 fixture
        self.contact_time = 0
        # for using box2d contacts instead of measure dist < 0.00001
        self.frame_c = False
        self.wings_c = False
        #
        # previous v storage
        self.bvx = self.body.linearVelocity[0]
        self.bvy = self.body.linearVelocity[1]
        #
        self.debug = False
        self.debug_p = (world_obj.screen_width / world_obj.pixels_per_meter / 2,
                        world_obj.screen_height / world_obj.pixels_per_meter / 2)   # center
        #
        # self.body.bullet = True
        # print self.body
        self.report()

    def __debug_prints__(self, comment=" "):
        print "\n", "---------------------> " + comment
        print "_contacts_number_", len(self.body.contacts)
        print "_distance_", self.dist1, self.dist2
        print "-------"
        print "_current_velocity_y_x_", self.body.linearVelocity[1], self.body.linearVelocity[0]
        print "-------"
        print "_previous_velocity_y_x_", self.bvy, self.bvx
        print "-------"
        print "_velocity_gap_", np.fabs(np.fabs(self.body.linearVelocity[1]) - np.fabs(self.bvy)), \
            np.fabs(np.fabs(self.body.linearVelocity[0]) - np.fabs(self.bvx)), self.durability
        print "-------"

    def __is_alive__(self):
        self.contact = False
        #
        self.frame_c = False
        self.wings_c = False
        #
        # self.__debug_prints__("_start_")
        #
        # collided fixtures
        if len(self.body.contacts) > 0:
            for b2e in self.body.contacts:
                tb2e = b2e.contact.touching
                if tb2e:
                    # print b2e.contact.fixtureA.userData, b2e.contact.fixtureB.userData, tb2e
                    if b2e.contact.fixtureA.userData == "frame":
                        self.frame_c = True
                    if b2e.contact.fixtureA.userData == "wings":
                        self.wings_c = True
        # print "_part_c_", self.frame_c, self.wings_c
        #
        if len(self.body.contacts) > 0 and self.wings_c:
            # supports are stronger than the body | + uadd | 7.9
            uadd = 3.9
            #
            # self.__debug_prints__("_wings_")
            #
            if np.fabs(np.fabs(self.body.linearVelocity[1]) - np.fabs(self.bvy)) > (self.durability + uadd) or \
                    np.fabs(np.fabs(self.body.linearVelocity[0]) - np.fabs(self.bvx)) > (self.durability + uadd):
                self.live = False
        if len(self.body.contacts) > 0 and (self.frame_c or self.dist1 < 0.021):   # 0.5 | 0.39 | 0.021 meter - 21 mm
            # real fixture contacts | not AABB as we used | more info and links in "t o d o . t x t" file
            # for b2e in self.body.contacts:
            #    print b2e
            #    print b2e.contact
            #    tb2e = b2e.contact.touching
            #    print tb2e
            self.contact = True
            self.contact_time += 0.01   # 2.5 sec * 90 iteration = 225 iteration * 0.01 = 2.25 # + 0.5 for 3 sec
            print self.contact_time
            #
            if np.fabs(np.fabs(self.body.linearVelocity[1]) - np.fabs(self.bvy)) > self.durability or \
                    np.fabs(np.fabs(self.body.linearVelocity[0]) - np.fabs(self.bvx)) > self.durability:
                #
                # self.__debug_prints__("_frame_")
                #
                self.live = False
        else:
            self.contact_time = 0
        # previous v
        self.bvx = self.body.linearVelocity[0]
        self.bvy = self.body.linearVelocity[1]

    def __dist__(self):
        polygonA1 = self.box.shape
        polygonA2 = self.box2.shape
        polygonATransform = self.body.transform
        polygonB = None
        polygonBTransform = None
        for b in self.world_obj.world.bodies:
            if b.userData == "decoration_body":
                polygonB = b.fixtures[0].shape
                polygonBTransform = b.transform
        self.dist1 = Box2D.b2Distance(shapeA=polygonA1, shapeB=polygonB,
                                      transformA=polygonATransform, transformB=polygonBTransform).distance
        self.dist2 = Box2D.b2Distance(shapeA=polygonA2, shapeB=polygonB,
                                      transformA=polygonATransform, transformB=polygonBTransform).distance

    def act(self, keys=[0, 0, 0, 0]):
        if keys[0] != 0:
            self.__up__()
        if keys[1] != 0:
            self.__left__()
        if keys[2] != 0:
            self.__right__()
        if self.wind:
            self.__wind__()
        self.__dist__()
        self.__is_alive__()

    def __up__(self):
        if self.fuel > 0 and self.enj:
            f = self.body.GetWorldVector(localVector=(0.0, self.main_enj_power))
            p = self.body.GetWorldPoint(localPoint=(0.0, 0.0 - self.height))
            if self.debug:
                self.debug_p = p
                # print p, "\n"
            self.body.ApplyForce(f, p, True)
            self.fuel -= (self.consumption + 0.25)   # + 0.15 if 599.0 + 0.25 if 700.0
        else:
            self.enj = False

    def __left__(self):
        if self.fuel > 0 and self.enj:
            f = self.body.GetWorldVector(localVector=(0.0, self.left_enj_power))
            p = self.body.GetWorldPoint(localPoint=(2.0, 0.0 - self.height))
            self.body.ApplyForce(f, p, True)
            # dynamic_body.ApplyTorque(500.0, True)
            self.fuel -= self.consumption
        else:
            self.enj = False

    def __right__(self):
        if self.fuel > 0 and self.enj:
            f = self.body.GetWorldVector(localVector=(0.0, self.right_enj_power))
            p = self.body.GetWorldPoint(localPoint=(-2.0, 0.0 - self.height))
            self.body.ApplyForce(f, p, True)
            # dynamic_body.ApplyTorque(-500.0, True)
            self.fuel -= self.consumption
        else:
            self.enj = False

    def __wind__(self):
        # not optimal | might work bad in horizontal position | push down
        f = self.body.GetWorldVector(localVector=(self.wind_str, 0.0))
        p = self.body.GetWorldPoint(localPoint=(0.0, 0.0))
        self.body.ApplyForce(f, p, True)

    def report(self):
        # delete returning of fixture and body
        # return {"type": "actor", "p_body": self.body, "angle": self.body.angle, "fuel": self.fuel,
        #        "vx": self.body.linearVelocity[1], "vy": self.body.linearVelocity[0],
        #        "px": self.body.position[0], "py": self.body.position[1], "fixtures": self.body.fixtures,
        #        "dist": self.dist1, "live": self.live, "enj": self.enj, "contact": self.contact, "wind": self.wind_str,
        #        "contact_time": self.contact_time}
        return {"type": "actor", "angle": self.body.angle, "fuel": self.fuel,
                "vx": self.body.linearVelocity[0], "vy": self.body.linearVelocity[1],
                "px": self.body.position[0], "py": self.body.position[1], "dist": np.amin([self.dist1, self.dist2]),
                "live": self.live, "enj": self.enj, "contact": self.contact, "wind": self.wind_str,
                "contact_time": self.contact_time}


# -------------------------------------------------- #


class Simulation(object):
    def __init__(self, options):
        self.screen_width = options.screen_width
        self.screen_height = options.screen_height
        self.target_fps = options.target_fps
        self.pixels_per_meter = options.pixels_per_meter
        self.colors = options.colors
        #
        self.commands = options.commands
        self.address = options.address
        #
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        pygame.display.set_caption("_F9_Lander_")
        self.clock = pygame.time.Clock()
        #
        self.myfont = pygame.font.SysFont(None, 29)
        # self.bg = pygame.transform.scale(pygame.image.load("canvas.png"), (self.screen_width, self.screen_height))
        #
        self.running = True
        #
        self.label = None
        #
        self.step_number = 0
        #
        self.message = ""
        #
        self.win = "none"   # "none", "landed", "destroyed"
        #
        if self.commands == "socket":
            self.sock = socket.socket()
            self.sock.bind(self.address)
            self.sock.listen(1)
            print "Waiting for client"
            self.conn, self.addr = self.sock.accept()
            print self.conn, self.addr

    def __restart__(self, world_obj, simulation_array):
        self.win = "none"
        print "B: Bodies, objects", len(world_obj.world.bodies), len(simulation_array)
        for entity in simulation_array:
            if entity.type == "actor":
                world_obj.world.DestroyBody(entity.body)
                simulation_array.remove(entity)
                # del entity   # manual deleting obj
                world_obj.wind_str = np.random.random_integers(-39, 39) * 1.0
                simulation_array.append(Rocket(world_obj))
        return simulation_array

    def __global_report__(self, simulation_array):
        report_list = []
        for entity in simulation_array:
            report_list.append(entity.report())
        return report_list

    def step(self, world_obj, simulation_array=[]):
        keys = [0, 0, 0, 0]
        # keys map [up, left, right, new]
        if self.commands == "keyboard":
            key = pygame.key.get_pressed()
            keys = [key[pygame.K_w], key[pygame.K_a], key[pygame.K_d], key[pygame.K_n]]
        elif self.commands == "socket":
            key = self.conn.recv(1024)
            keys = eval(key)   # eval is bad idea but it works
            # print keys, type(keys)
        # INPUT FROM PIPE OR SOCKET HERE
        if keys[3] != 0:
            simulation_array = self.__restart__(world_obj, simulation_array)
        #
        self.screen.fill((0, 0, 0, 0))
        # apply graphic background
        # self.screen.blit(self.bg, (0, 0))
        # drawing
        for entity in simulation_array:
            # world.bodies
            if entity.type == "actor":
                entity.act(keys=keys)
                # self position
                # self.message += str(entity.body.position)
                self.message += "| Dist: " + str(np.round(np.amin([entity.dist1, entity.dist2]), 1))   # \
                #                + " " + str(np.round(entity.dist1, 1)) + " " + str(np.round(entity.dist2, 1))
                self.message += " | Fuel: " + str(np.round((entity.fuel * entity.enj), 1)) + " | Eng: " + str(entity.enj)\
                                + " | Live: " + str(entity.live) + " | Cnt: " + str(entity.contact)\
                                + " | VX: " + str(np.round(entity.body.linearVelocity[0], 1))\
                                + " | VY: " + str(np.round(entity.body.linearVelocity[1], 1))\
                                + " | A: " + str(np.round(entity.body.angle, 1)) + " | Wind: " + str(entity.wind_str)
            elif entity.type == "decoration":
                entity.act()
            for fixture in entity.body.fixtures:
                # print fixture
                shape = fixture.shape
                # print shape.vertices
                vertices = [(entity.body.transform * v) * self.pixels_per_meter for v in shape.vertices]
                vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                # self.colors[entity.body.type]
                pygame.draw.polygon(self.screen, entity.color, vertices)
                # debug
                if False:
                    for vert in vertices:
                        pygame.draw.circle(self.screen, (255, 255, 0, 255), (int(vert[0]), int(vert[1])), 3, 0)
                    if entity.type == "actor":
                        pygame.draw.circle(self.screen, (0, 255, 0, 255), (int(entity.debug_p[0]) * 10, self.screen_height - int(entity.debug_p[1]) * 10), 3, 0)
                # engines
                if keys[0] != 0 and entity.type == "actor" and entity.enj and fixture.userData != "wings":
                    pygame.draw.polygon(self.screen, (255, np.random.random_integers(100, 200), 0, 150),
                                        (vertices[1], vertices[0],
                                         ((vertices[0][0] + vertices[1][0]) / 2, vertices[0][1] + np.random.random_integers(21, 27))))
                if keys[1] != 0 and entity.type == "actor" and entity.enj and fixture.userData != "wings":
                    pygame.draw.polygon(self.screen, (255, np.random.random_integers(100, 200), 0, 150),
                                        (vertices[1], vertices[0],
                                         (vertices[0][0] - np.random.random_integers(3, 7), vertices[0][1] + np.random.random_integers(11, 17))))
                if keys[2] != 0 and entity.type == "actor" and entity.enj and fixture.userData != "wings":
                    pygame.draw.polygon(self.screen, (255, np.random.random_integers(100, 200), 0, 150),
                                        (vertices[1], vertices[0],
                                         (vertices[1][0] + np.random.random_integers(3, 7), vertices[1][1] + np.random.random_integers(11, 17))))
        # checking status
        for entity in simulation_array:
            if entity.type == "actor":
                if entity.live and entity.contact and entity.contact_time >= 2.75 and -0.29 < entity.body.angle < 0.29:   # why 2.25 read in obj field + 0.5
                    entity.color = (0, 255, 0, 255)
                    self.win = "landed"
                    # entity.wind = False   # stops wind for this obj
                if not entity.live:
                    entity.color = (255, 0, 0, 255)
                    self.win = "destroyed"
                    # entity.wind = False
        world_obj.world.Step(1.0 / self.target_fps, 10, 10)   # 10 10 | 6 2
        world_obj.world.ClearForces()   # but why?
        #
        self.message += " | Step: " + str(self.step_number)
        self.label = self.myfont.render(self.message, True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(self.label, (10, 10))
        pygame.display.flip()
        self.clock.tick(self.target_fps)
        #
        report_list = self.__global_report__(simulation_array)
        report_list.append({"step": self.step_number, "flight_status": self.win, "type": "system"})
        # OUTPUT TO PIPE OR SOCKET HERE
        if self.commands == "socket":
            self.conn.send(str(report_list))
        # print self.win
        #
        self.step_number += 1
        self.message = ""
        #
        # if keys[3] != 0:
        #    simulation_array = self.__restart__(world_obj, simulation_array)
        # events | SPACE works even in external control modes
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.running = False
                if self.commands == "socket":
                    self.conn.close()
                    print "Socket closed"
                pygame.quit()
                print "All engines stopped"
            if event.type == KEYDOWN and event.key == K_SPACE:
                simulation_array = self.__restart__(world_obj, simulation_array)
                print "A: Bodies, objects", len(world_obj.world.bodies), len(simulation_array)
                # here was code from __restart__()
        return report_list

# -------------------------------------------------- #
# example
# -------------------------------------------------- #


def main():
    # Command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--socket", action="store_true", help="Run game in socket mode")
    parser.add_argument("-i", "--ip", type=str, default='127.0.0.1', help="IP address for socket mode")
    parser.add_argument("-p", "--port", type=int, default=50007, help="Port")
    #
    args = parser.parse_args()
    #
    options = Options(args.socket, args.ip, args.port)
    world = World(options)
    simulation = Simulation(options)
    entities = [Rocket(world), Platform(world)]
    #
    print entities
    #
    while simulation.running:
        report = simulation.step(world, entities)
        # print report
        # time.sleep(1.0)
    print entities

if __name__ == "__main__":
    main()

# -------------------------------------------------- #
# --------------- you have landed ------------------ #
# -------------------------------------------------- #
