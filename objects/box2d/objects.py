from objects.all_import import *

from Box2D.b2 import (polygonShape, circleShape, staticBody, dynamicBody)
from Box2D.b2 import world as world_p

class Game(object):
    def __init__(self, fps, ppm, gravity=(0, -15)):
        self.meter = ppm
        self.fps = fps
        self.time_step = 1/self.fps
        self.world = world_p(gravity, doSleep=True)
        self.kinematic_bodies = []
        self.static_bodies = []
        self.dynamic_bodies = []
        self.player_body = []
    def add_body(self, type_body, position, box, density=1, angle=15, friction=0.3, mass=1):
        if type_body == "d":
            body = self.world.CreateDynamicBody(position=position, angle=angle)
            body.mass=mass
            # self.dynamic_bodies.append(self.world.CreateDynamicBody(position, angle))
            # self.dynamic_bodies[len(self.dynamic_bodies)-1].CreatePolygonFixture(box, density, friction)
            self.dynamic_bodies.append((body,
            body.CreatePolygonFixture(box=box, density=density, friction=friction)))
            # self.dynamic_bodies.insert(-1, [self.world.CreateDynamicBody(position=position, angle=angle)])
            # self.dynamic_bodies[-1].insert(1, self.dynamic_bodies[-1][0].CreatePolygonFixture(box=box, density=density, friction=friction))
            # print(self.dynamic_bodies)
            return len(self.dynamic_bodies)-1
        if type_body == "s":
            self.static_bodies.append(
                (
                self.world.CreateStaticBody(
                position=position,
                shapes=polygonShape(box=box)))
                )
            return len(self.static_bodies)
        if type_body == "k":
            self.kinematic_bodies.append(
                self.world.CreateKinematicBody(
                    position=position,
                    shapes=polygonShape(box=box)
                )
            )
            return len(self.kinematic_bodies)
        if type_body == "p":
            body = self.world.CreateDynamicBody(position=position, angle=angle)
            body.mass=mass
            # self.dynamic_bodies.append(self.world.CreateDynamicBody(position, angle))
            # self.dynamic_bodies[len(self.dynamic_bodies)-1].CreatePolygonFixture(box, density, friction)
            self.player_body.append((body,
            body.CreatePolygonFixture(box=box, density=density, friction=friction)))
    def update(self, step1=10, step2=10):
        self.world.Step(self.time_step, step1, step2)


def outline_mask(img, loc):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n += 1
    return mask_outline