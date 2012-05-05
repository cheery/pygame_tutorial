import pygame, sys

black = 0,0,0
white = 0xFF, 0xFF, 0xFF
background_color = 0x12, 0x0E, 0x1C

width = 64
height = 32
scale = 8
canvas = pygame.Surface((width, height), pygame.SRCALPHA)
canvas.set_at((0,0), white)
canvas.set_at((width-1,height-1), black)

def animation_frame(screen):
    screen.fill(background_color)
    view = pygame.transform.scale(canvas, (width*scale, height*scale))
    screen.blit(view, (0, 0))

def plot((x,y)):
    x = int(x/scale)
    y = int(y/scale)
    if 0 <= x < width and 0 <= y < height:
        canvas.set_at((x,y), white)

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)
    if event.type == pygame.MOUSEBUTTONDOWN:
        plot(event.pos)
    if event.type == pygame.MOUSEMOTION and event.buttons != (0,0,0):
        plot(event.pos)
    global canvas
    if event.type == pygame.KEYDOWN:
        if event.unicode == 'w':
            pygame.image.save(canvas, 'canvas.png')
        elif event.unicode == 'r':
            canvas = pygame.image.load('canvas.png')

pygame.display.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    for event in pygame.event.get():
        dispatch(event)
    animation_frame(screen)
    pygame.display.flip()
