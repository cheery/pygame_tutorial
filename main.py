import pygame, sys

black = 0,0,0
white = 0xFF, 0xFF, 0xFF
background_color = 0x12, 0x0E, 0x1C

def animation_frame(screen):
    screen.fill(background_color)

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
