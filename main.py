import pygame, sys
from time import time
from math import sin, pi

black = 0,0,0
white = 0xFF, 0xFF, 0xFF
background_color = 0x12, 0x0E, 0x1C
front_color = 0xE7, 0xF5, 0x6E

def animation_frame(screen):
    screen.fill(background_color)
    now = time()
    (width, height) = screen.get_size()
    for phase in [0.0, 0.2, 0.5, 0.8, 0.7]:
        x = 512 + sin(2*pi*((now*0.02) + phase)) * 512
        thickness = 10
        screen.fill(front_color, (x-thickness/2, 0, thickness, height))

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)

pygame.display.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    for event in pygame.event.get():
        dispatch(event)
    animation_frame(screen)
    pygame.display.flip()
