import pygame, sys
import os
from optparse import OptionParser

parser = OptionParser(
    usage = "usage: %prog [options] file"
)
parser.add_option("-s", "--size", dest="size",
                  help="SIZE of the canvas, if we need one more.", metavar="SIZE", default="64x64")

(options, args) = parser.parse_args()

if len(args) != 1:
    sys.exit(1)

filename = args[0]

def parse_size():
    width, height = options.size.split('x')
    return int(width), int(height)

black = 0,0,0
white = 0xFF, 0xFF, 0xFF
background_color = 0x12, 0x0E, 0x1C

scale = 8
if os.path.exists(filename):
    canvas = pygame.image.load(filename)
else:
    canvas = pygame.Surface(parse_size(), pygame.SRCALPHA)

color = 0x00,0x00,0x00,0xff

palette = {
    '0': (0x00, 0x00, 0x00, 0x00),
    '1': (0xff, 0x00, 0x00, 0xff),
    '2': (0xff, 0xff, 0x00, 0xff),
    '3': (0x00, 0xff, 0x00, 0xff),
    '4': (0x00, 0xff, 0xff, 0xff),
    '5': (0x00, 0x00, 0xff, 0xff),
    '6': (0xff, 0x00, 0xff, 0xff),
    '7': (0xff, 0xff, 0xff, 0xff),
    '8': (0xff, 0x80, 0x00, 0xff),
    '9': (0x80, 0x80, 0x80, 0xff),
}

pygame.font.init()
font = pygame.font.Font(None, 16)

def animation_frame(screen):
    screen.fill(background_color)
    width, height = canvas.get_size()
    view = pygame.transform.scale(canvas, (width*scale, height*scale))
    screen.blit(view, (0, 0))
    screen.blit(canvas, (screen.get_width()-width, 0))
    screen.fill(color, (0, screen.get_height()-24, screen.get_width(), 24))
    for index, key in enumerate('1234567890'):
        keycolor = palette[key]
        area = (index*40+2, screen.get_height()-22, 40, 20)
        screen.fill(keycolor, area)
        complement = 255-keycolor[0], 255-keycolor[1], 255-keycolor[2], 0xFF
        screen.blit(font.render(key, True, complement), area)
        
def plot((x,y)):
    x = int(x/scale)
    y = int(y/scale)
    width, height = canvas.get_size()
    if 0 <= x < width and 0 <= y < height:
        canvas.set_at((x,y), color)

def shortcut(unicode):
    global canvas, color
    if unicode == 'w':
        pygame.image.save(canvas, filename)
    elif unicode in palette:
        color = palette[unicode]

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)
    if event.type == pygame.MOUSEBUTTONDOWN:
        plot(event.pos)
    if event.type == pygame.MOUSEMOTION and event.buttons != (0,0,0):
        plot(event.pos)
    if event.type == pygame.KEYDOWN:
        shortcut(event.unicode)

pygame.display.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    for event in pygame.event.get():
        dispatch(event)
    animation_frame(screen)
    pygame.display.flip()
