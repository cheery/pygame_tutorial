import pygame, sys
from time import time
from math import sin, pi
from random import random

black = 0,0,0
white = 0xFF, 0xFF, 0xFF
background_color = 0x12, 0x0E, 0x1C
front_color = 0xE7, 0xF5, 0x6E

class Player(object):
    img = pygame.image.load('assets/ship.png')
    mask = pygame.mask.from_surface(img)
    offset_x = 32
    offset_y = 32
    group = 'ally'
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ctl = []
        self.fire_delay = 0

    def update(self, dt):
        self.fire_delay -= dt
        motion_y = 0
        firing = False
        for cmd in self.ctl:
            if cmd == pygame.K_DOWN:
                motion_y = 200
            if cmd == pygame.K_UP:
                motion_y = -200
            if cmd == pygame.K_SPACE:
                firing = True
        self.y += motion_y * dt
        if firing and self.fire_delay <= 0:
            insertions.add(Bullet(self.x+8, self.y+4))
            self.fire_delay = 0.1

class Bullet(object):
    img = pygame.image.load('assets/bullet.png')
    mask = pygame.mask.from_surface(img)
    offset_x = 0
    offset_y = 1
    group = 'ally'
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.travel = 0

    def update(self, dt):
        motion = 500 * dt
        self.x += motion
        self.travel += motion
        if self.travel > 1000:
            removals.add(self)

class Asteroid(object):
    img = pygame.image.load('assets/asteroid.png')
    mask = pygame.mask.from_surface(img)
    offset_x = 32
    offset_y = 32
    group = 'enemy'
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, dt):
        self.x -= 200 * dt
        if self.x < -32:
            removals.add(self)

scene = set()
removals = set()
insertions = set()

ship = Player(50, 200)
scene.add(ship)

enemy_delay = 0

def check_collision(obj, other):
    x = int((obj.x - obj.offset_x) - (other.x - other.offset_x))
    y = int((obj.y - obj.offset_y) - (other.y - other.offset_y))
    return other.mask.overlap_area(obj.mask, (x,y)) > 0

def collision(obj, other):
    if obj.group == 'ally' and other.group == 'enemy':
        if check_collision(obj, other):
            removals.add(obj)
            removals.add(other)

def update(dt):
    global enemy_delay
    for obj in scene:
        obj.update(dt)
        for other in scene:
            collision(obj, other)
    scene.difference_update(removals)
    removals.clear()
    scene.update(insertions)
    insertions.clear()
    
    enemy_delay -= dt
    if enemy_delay <= 0:
        scene.add(Asteroid(1024+32, 768*random()))
        enemy_delay = 0.5

def animation_frame(screen):
    screen.fill(background_color)
    now = time()
    (width, height) = screen.get_size()
    for phase in [0.0, 0.2, 0.5, 0.8, 0.7]:
        x = 512 + sin(2*pi*((now*0.02) + phase)) * 512
        thickness = 10
        screen.fill(front_color, (x-thickness/2, 0, thickness, height))
    for obj in scene:
        screen.blit(obj.img, (obj.x - obj.offset_x, obj.y - obj.offset_y))

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)
    if event.type == pygame.KEYDOWN:
        if not event.key in ship.ctl:
            ship.ctl.append(event.key)
    if event.type == pygame.KEYUP:
        if event.key in ship.ctl:
            ship.ctl.remove(event.key)

pygame.display.init()
screen = pygame.display.set_mode((1024, 768))
dt, now = 0, time()
while 1:
    for event in pygame.event.get():
        dispatch(event)
    animation_frame(screen)
    update(dt)
    pygame.display.flip()
    last, now = now, time()
    dt = now - last
