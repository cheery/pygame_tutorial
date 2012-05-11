#Cheery's Pygame Tutorial
(This tutorial is still a draft)

The title is a bit of a misnomer, as this tutorial is not so much about pygame as it is about a project workflow and problem solving. This tutorial should help people who handle the basics but are struggling if they were to make anything nontrivial.

The basic premise here is that it's quite much impossible to come up with a high-quality well-optimized software by designing it all in single pass before writing the source code. Writing programs is a puzzle of sort, and you need to open the problem space to yourself before you can work your way through.

I just told what I want to teach you with this tutorial. An one problem is that such skills cannot be learned by reading. You'll have to learn this yourself as best this text can do is to show the way.

If you are the target audience for this tutorial you should already know a little bit about python the programming language. Here's a glossary of concepts and grammatical constructs you should understand about python:

* Function
* Function call
* Import statement
* List
* If statement
* While statement
* Module
* Tuple
* Variable

If you don't understand the meaning of some words in that list. Go study an another python tutorial first. I'll explain the rest of python constructs if, and whenever we need them.

Prepare to fail numerous times before really getting what I just told. This tutorial should provide just enough material for you to play on. Imitate these things, play with the code, and fail many times and ways.

##Table of Contents
* [Rolling Columns](#rolling-columns)
* [Avoid Work](#avoid-work)
* [TOC](#TOC)

##Rolling Columns
This is the only section that particularly tells about the pygame library. People who understand how pygame beats can just skip this section. The program of this section draws some animated, rolling columns.

Pygame is a python's wrapper library for Simple DirectMedia Layer. SDL is a cross-platform multimedia library which provides access to audio, input peripherals and video systems.

I wrote something that gets you started up in pygame, lets study it:

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

This code opens a display device through pygame and goes into an event polling loop. For every event, that was being received during last frame, it calls our dispatch -function which determines what happens when it gets an event. We can see that a request to quit causes the process to exit.

Pygame gives our process either a real or virtual [framebuffer device](http://en.wikipedia.org/wiki/Framebuffer). Process gets a memory buffer to fill with whatever we want. Actually it gets two such buffers to prevent [screen tearing](http://en.wikipedia.org/wiki/Screen_tearing) while animating. One buffer gets filled when an another is shown on the screen. Event loop calls display.flip at the end, which switches the roles of buffers, causing our animation to show up on the screen.

A plain color is something boring, so lets add some rolling columns. We are about to need some functions that'd be hard to make ourselves. Fortunately those can be found from the standard python modules, so lets import them. Insert this to the beginning of the source file:

    from time import time
    from math import sin, pi

We need to determine how fast the animation is playing, for that we need time() in our process. To get spinning motion our process needs to rely on a [trigonometric sine function](http://en.wikipedia.org/wiki/Trigonometry). Full circle is 2 pi, so we get the pi too.

We need a new color for our columns, put this after other colors:

    front_color = 0xE7, 0xF5, 0x6E

To make such rolling columns the process needs to do couple more fills. Lets add those fills. Append this to the end of the animation_frame function:

    now = time()
    (width, height) = screen.get_size()
    for phase in [0.0, 0.2, 0.5, 0.8, 0.7]:
        x = 512 + sin(2*pi*((now*0.02) + phase)) * 512
        thickness = 10
        screen.fill(front_color, (x-thickness/2, 0, thickness, height))

The animation may stutter a bit at the edges of the screen, because of [alialising](http://en.wikipedia.org/wiki/Aliasing). screen.fill is unable to smooth away the [pixel](http://en.wikipedia.org/wiki/Pixel) boundaries. You may experience further stutter because of other, unknown, reasons. SDL and pygame are a bit old-mannered as a library and may not be the most efficient access to the hardware you have.

![rolling columns](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/rolling_columns.png)

Here's the code for glancing:

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

This is about the way how pygame works. If you'd like some more colors or anything else, do it yourself. Anything such is irrelevant for the rest of the tutorial though.

You may have had a play with the source code by this far. Already wondering how will you ever learn to use rest of pygame? I'm not documenting those functions in this tutorial any way. The answer is simple. I have left it up to you to study [pygame](http://www.pygame.org/docs/) reference manual. You can read the documentation there and I don't need to repeat it.

##Avoid Work
Obviously, take breaks often. It's not the kind of work avoidance I want you to do though, well unless you use the break to play with the code. My work avoidance guide crystallizes on two important instructions: Do not Repeat Yourself, and Do not Repeat Others.

Do not Repeat Yourself is quite simple principle. If you have a piece of complex code that does some important thing. Avoid copying and pasting this all around in your source code. Every copy/paste makes it harder to change the complex behaviour you created. Every duplication causes the bugs inside that complex code to multiply.

It's still okay to repeat some things. But they should be small things in general or some kind of templates. Anything else, and you're better off by rewriting the thing such that you don't need to duplicate the code.

One thing yet. You should not duplicate things that are conceptually same. Such things are magical numbers that appear in the middle of code. If you use such magic number twice, it's better if you assign a variable to that number and use the variable instead. This allows you to alter the magic number, or alter the logic of the program easier.

Do not Repeat Others might be equally simple principle. Though sometimes you cannot follow this rule because of copyright-monopoly restrictions. In generic you should use and work on other people's code though, especially if they're already well done things. Work done by another means you don't need to work on it yourself.

Python provides a large collection of standard libraries which you should use whenever you need them. For example that [math](http://docs.python.org/library/math.html)-module we used is from python stdlib.

There's an exception to this rule as well. If using work of others takes longer time or requires more code than rolling one on your own, then you are probably doing better without others code. 

##Brute Paint
We could write graphics to our games in Gimp of course. But there are two issues here, actually three. First I designed this tutorial for Raspberry Pi, and Gimp is not exactly the most lightweight image manipulation software there could be. Also, Gimp tools have been designed for image manipulation, not so much for drawing sprites. Third, to extend Gimp you'd need to write scripts to Gimp, and it'd require more indepth understanding about scripting Gimp.

Because of issues mentioned here, we take a different route. Lets copy the piece of code we started from into paint/main.py! Lets make a program we can use to draw sprites.

We need something to draw on. A pygame.Surface should do well enough for this purpose. For debugging we'll also want to see whether the `set_at`-method is working like we expect. Remove the old `animation_frame` and `dispatch` and insert this code to their place:

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

Now you can paint on the opened window, as if you had a white blocky crayon in place of your mouse. The code is pretty much self-explanatory except on the `plot`-function. You see I call it twice, and without it I'd have three levels of indentation there. The `plot` transforms the mouse coordinates to canvas coordinates. Notice also how I'm using the variables. They help a bit in understanding the program but essentially they avoid repeating, straining changes on the code.

You see we are still missing something essential from our painting gadget. Fortunately that part has been made really easy by `pygame.image`-module. Append this code to your `dispatch`-function:

    global canvas
    if event.type == pygame.KEYDOWN:
        if event.unicode == 'w':
            pygame.image.save(canvas, 'canvas.png')
        elif event.unicode == 'r':
            canvas = pygame.image.load('canvas.png')

Now we have some syntax you might not readily know. `global canvas` is a safety keywoard which you are using when you want to set a global variable instead of local. Python does not let you to poison global namespace without this keyword.

Still thinking it is missing something? Before that nice usable program we needed to make an one unusable. Yes we really want something to use, but that happens to be very hard to make straight from nothing. It is much easier to make an unusable program and then make it more usable in iterations, until it is usable enough.

![brute paint](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/brute_paint.png)

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

Concluding this part as it's something cool enough. Obviously, some of the coolest things you can create are tools for creating things. Just don't hang into this recursive coolness loop for too long. Other kinds of people won't notice your coolness before you exit the loop.

##Divide and Conquer
I need to explain a new concept before we go on. We have 13 global variables, modules and functions in the program we just did. It is going to do lot of things so we are going to need much more variables about soon. Many of these variables will be related to another in a way. There wouldn't be one without another variable or a function wouldn't make sense without this one and so on. At this point we'll find classes useful.

Python `class` syntax lets you create an object that can create instances of itself. When you call a class, it creates an object and calls a special initializer function to create a new instance. A valid class looks like this:

    class myclass(object):
        nom = "nom nom nom"
        def __init__(self, value):
            self.value = value

        def useless(self):
            print "An useless", self.value

    mya = myclass("hello")
    myb = myclass("cat")

    mya.useless()
    myb.useless()

    print myclass.nom
    print mya.nom
    print myb.nom

This particular example shows a bit how the syntax goes. You'll see more examples later. Right now it's important to understand that classes are useful for grouping (encapsulating) things together. If you are wondering what that `(object)` is doing, I can tell you it's pointing out a class to inherit from. I won't explain inheritance now as I'm not using it this example. You can read it yourself from the python manual if you're interested. In the next part we'll be making our useless brute painting app into useful brute painting app.

##From Useless to Useful
I'm afraid other projects are going to catch my attention very soon so I have to write a shorter conclusion for this tutorial than what I anticipated. Lets make this editor useful fast and get something done before I move on. You might have been wondering how to make that useless brute useful. I'd say it's useless because you can't change a color or choose a file. Lets fix this fast one problem at a time.

The program starts having lot of conditional clauses under that keydown event. It's okay to keep them where they are, but doing like this makes it bit easier to follow. This function should go somewhere before the process enters eventloop:

    def shortcut(unicode):
        global canvas, color
        if unicode == 'w':
            pygame.image.save(canvas, 'canvas.png')
        elif unicode == 'r':
            canvas = pygame.image.load('canvas.png')
        elif unicode in palette:
            color = palette[unicode]

The following should be nothing out of ordinary, but if it is.. The palette is a dictionary object and you can access it like an array. You'll find a value behind each key. Dictionaries are very common in python and they exist just because they're more efficient than if same thing was attempted to be done with lists alone.

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

That's it. You should be able to select some colors even if they're not that pretty really. Now it's going to be tedious to remember these all colors so lets make them visible, add this to the end of `animation_frame`:

    for index, key in enumerate('1234567890'):
        keycolor = palette[key]
        area = (index*40+2, screen.get_height()-22, 40, 20)
        screen.fill(keycolor, area)
        complement = 255-keycolor[0], 255-keycolor[1], 255-keycolor[2], 0xFF
        screen.blit(font.render(key, True, complement), area)

This is not the beautiest code I've written. But it almost does the job. You can perhaps see that I'm running out of nice variable names.

Now it's usable! eh.. wait. We probably want to color other things than just "canvas.png" there. The author might also like to select the size of the canvas that's being used. We'd like to get some arguments in to change the behavior of this program. We'll also want to check whether a file exists, to automaticly open a file if given. Lets introduce optparse and os in the start of the file:

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

Now we can insert arguments into a console or terminal of our choice, and select how are we using the program. The app exits early if there's no useful commands. The `parse_size` is enclosed in a function just to avoid messing up the global namespace.

Lets remove this piece of code, as it is useless now:

    elif unicode == 'r':
        canvas = pygame.image.load('canvas.png')

Replace the line with `pygame.Surface` on it with these:

    if os.path.exists(filename):
        canvas = pygame.image.load(filename)
    else:
        canvas = pygame.Surface(parse_size(), pygame.SRCALPHA)

Also be free, and remove globals `width`, and `height`. Oh and replace the `'canvas.png'` with `filename`!

Only on thing left. Lets add this piece just before into two places where those two globals were used.

    width, height = canvas.get_size()

Well, I'm generous enough to include 1:1 image on the screen as well, it's up to you to figure out where it is going to:

    screen.blit(canvas, (screen.get_width()-width, 0))

![slightly less brute paint](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/slightly_less_brute_paint.png)

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

You can see we have arrived to something that's slightly less brute than the earlier version we had. We can choose a color from fixed palette and where to save the results. Oooh! Real artists would still rather draw on a toilet paper than this! You cannot write a nice paint out of a tutorial you know. :-) But there was an other point in this exercise than to get a nice brute painting app. The point of this exercise was to give you an idea that you can make your own tools, and that existing ones aren't magical artifacts you couldn't change somehow to your liking.

You might want to learn scripting gimp or blender, if you're not running them off a shoestring or expect to embed them into your games. Things like gimp or blender can't do everything for you though. If you'll find yourself in position that you need a some sort of tool, open this tutorial again and remind yourself that toolwriting isn't different from any other kind of programming.

So uh.. Maybe we'd like to make a game with our newly created tool next?

##To The Battle Stations
Doing the actual game would be pretty much repetition of the instructions I already gave. So I just made it without typing much instructions while working on it. The resulting game can be seen in the main.py of this directory.

Most of the time games are just programs like everything else. They have some state that gets modified by the game events. The state itself might be transmitted over the network or stored on the disk. Overall it's not hard or anything. The hard things come from actual concrete workings of the game. How does this menu work for the player? What happens when player presses this key? How does the enemy behave? It's okay to do something at first and then return later on the issue, similar to how it's with that painting application we wrote.

My example is bit of like the painting program in the sense that it's not polished in any way, or complete. It's some steps away from that. If you cared about doing this kind of game, you'd add some more enemies, make the game itself re-entrable that you could add a menu and a scoreboard.. cause game over when player dies.. add parallax background.. and so on.

![battle stations](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/battle_stations.png)

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

There's not anything too odd in the source code. You can see I've separated the game logic of each object into it's own block, along the graphic and other information related to the game object. I keep the active objects in a scene-set. The removals/insertions set are there, because you cannot reliably remove or insert items in python set while you're iterating through it. This way the removals are being done just in the very end of the last update. The game doesn't interact much between objects because there's no need for such stuff. If it were to interact in more complex way, then the interaction scheme might be slightly more complex than it is now. There's not a scoreboard, player lives or anything other such.

##Conclusion
Not much to say to the conclusion. If you were doing a real game you might like to embed an editor into your game, that you could tune the game details while the game itself is playing. It isn't a jump into unknown since you've read this tutorial. You work on a state of some kind so just turn the malleable part of the game into a state of some sort, that'll make it more flexible too as well.

What I've told will hopefully get you to do games if you are interested about that sort of things. If you're unfamiliar with programming, you will fail. But that's the idea. This tutorial is supposed to show you the way as I'm unable to just flush all this knowledge down your throat. You'll need to mess it up multiple times before you really figure how to do it right.

I hope you liked the tutorial. Please file an issue if you hate it from some reason. If you want to study pygame more, you could try reading sources of different finished games, by different authors.

If you have ideas of how to improve or continue this tutorial, tell about it in [issues page](https://github.com/cheery/pygame_tutorial/issues). You're also free to fork your own tutorial from this one.
