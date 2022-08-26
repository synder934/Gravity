from math import *
from random import randint
import pygame as pg

vec = pg.Vector2
clock = pg.time.Clock()


def map_(n, s1, e1, s2, e2):
    return ((n-s1)/(e1-s1))*(e2-s2)+s2

def cap_(n, low, high):
    if n < low:
        return low
    elif n > high:
        return high
    return n

def dist_(from_:vec | float, to_:vec | float):
    return ((to_.x-from_.x)**2+(to_.y-from_.y)**2)**0.5

def pull_(G, M1, M2, D):
    try:
        return G*((M1*M2)/D**2)
    except:
        return G*((M1*M2)/1)



class Object():
    def __init__(self, mass, pos, vel) -> None:
        self.mass = mass
        self.pos = vec(pos)
        self.vel = vec(vel)
        self.acc = vec(0,0)

    def update(self):            
        for obj in objects:
            if obj == self: continue
            f = cap_(pull_(GRAVITY, self.mass, obj.mass, dist_(self.pos, obj.pos)), 0, 0.5)

            a = atan2((obj.pos.y-self.pos.y), (obj.pos.x-self.pos.x))
            self.acc+=vec(
                f*cos(a),f*sin(a)
            )

        if self == objects[0]:
            print(self.acc)
            print(self.vel)
            print(f)
            pg.draw.line(disp, (255, 0, 0), self.pos, (self.acc*500)+self.pos)

        print((self.vel.x**2+self.vel.y**2)**0.5)
        if (self.vel.x**2+self.vel.y**2)**0.5 < 8:
            self.vel+= self.acc
        self.pos += self.vel + self.acc/2

        if self.pos.x > DIM[0] or self.pos.x < 0:
            self.vel.x = -self.vel.x 
        elif self.pos.y > DIM[1] or self.pos.y < 0:
            self.vel.y = -self.vel.y

        self.acc = vec(0,0)



class Pixel():
    def __init__(self, pos, col = (255,255,255)) -> None:
        self.pos = pos
        self.col = col

    def update(self):
        f= cap_(map_(sum([pull_(GRAVITY, 1, x.mass, dist_(self.pos, x.pos)) for x in objects]), 0, 0.5, 0, 255), 0, 255)
        self.col = (f,f,f)
        # disp.fill(self.col, (self.pos, (DRAWVAL,DRAWVAL)))
        pg.draw.circle(disp, self.col, self.pos, DRAWVAL/2)







GRAVITY = 10
FPS = 30
DIM = (2**10, 2**9)
objects = [
    Object(10, (310, 180), (0,0)),
    Object(10, (0, 180), (5,0)),
    Object(10, (310, 0), (0,5))
]

objects = [Object(
    randint(5,8), 
    (randint(0, DIM[0]), 
    randint(0, DIM[1])), 
    (randint(-5, 5), randint(-5, 5))
    ) for i in range(5)]

# objects = [
#     Object(50, (DIM[0]/2, DIM[1]/2), (0,0)),
#     Object(5, (DIM[0]/4, DIM[1]/2), (0,1))
# ]

objects = [
    Object(10, (DIM[0]/2, DIM[1]/2-100), (1.5,0)),
    Object(10, (DIM[0]/2, DIM[1]/2+100), (-1.5, 0))
]

# objects = [
#     Object(20, (DIM[0]/2, DIM[1]/2), (0,0)),
#     Object(5,  (DIM[0]/4, DIM[1]/4), (0,0)),
#     Object(5,  (DIM[0]/4*3, DIM[1]/4*3), (0,0)),
#     Object(5,  (DIM[0]/4, DIM[1]/4*3), (0,0)),
#     Object(5,  (DIM[0]/4*3, DIM[1]/4), (0,0)),
# ]

DRAWVAL = 16

# F = G*((M1-M2)/D**2)

# objects = [
#     Object(5,  (DIM[0]/4, DIM[1]/4), (1,0)),
#     Object(5,  (DIM[0]/4*3, DIM[1]/4*3), (-1,0)),
#     Object(5,  (DIM[0]/4, DIM[1]/4*3), (0,-1)),
#     Object(5,  (DIM[0]/4*3, DIM[1]/4), (0,1)),
# ]

# objects = [
#     Object(10, (DIM[0]/2, DIM[1]/2), (0,0)),
#     Object(10, (200, DIM[1]/2+200), (0,0))
# ]


if __name__ == '__main__':
    pg.init()

    disp = pg.display.set_mode(DIM)
    pixels = [Pixel(vec(x,y)) for x in range(0, DIM[0], DRAWVAL) for y in range(0, DIM[1], DRAWVAL)]

    running = 1

    while running:
        disp.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 0

        list(map(lambda x: x.update(), pixels))
        list(map(lambda x: x.update(), objects))


        # for x in objects: x.update()
        # for x in pixels: x.update()

        pg.display.update()
        #clock.tick(FPS)
