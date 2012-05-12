#Cheery's Pygame Tutorial
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
* [Brute Paint](#brute-paint)
* [Divide and Conquer](#divide-and-conquer)
* [From Useless to Useful](#from-useless-to-useful)
* [To The Battle Stations](#to-the-battle-stations)
* [Game State and Framestep](#game-state-and-framestep)
* [Conclusion](#conclusion)

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
In this section we make a small paint program which we use through the rest of the tutorial. I think it's worth my time to show you that you can make your own tools instead of relying on existing ones. It will also help you to use existing tools if you acknowledge their malleability.

We could also write scripts to Gimp, but it'd require more indepth understanding about scripting Gimp. That'd also require to have some deeper point in our exercise, which might blur the point I'm trying to get through. Also on some systems the Gimp is just way too heavy. You might like to draw sprites in Raspberry Pi, for example. Not that fun if your drawing app takes 80 seconds to start up.

One another thing is that Gimp is designed for image manipulation. If you make your own program it could be designed for whatever you, as the author, want it to do. Because of this we'll write our own "paint" that we could use to draw some sprites. Copy the stub we made earlier into `paint/main.py`

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

![brute paint](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/brute_paint.png)

Here's the code for glancing:

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

Our paint is able to take user input and save the drawn image into a file. It's very much useless program at the moment for anyone else except us. You could try draw something with this toy and recognise what could make it more useful for what we are doing. It looks like really cool if you see the potential that was just exposed.

##Divide and Conquer
This section explains classes, which are useful in further sections because our programs will become more complex. In theory we could go entirely without classes but they are a neat way to thread pieces of our code together into groups that make sense together. Fancy people call this encapsulation. 

Class in python is an object, which can produce instantiations of itself. A `class` declares a pattern by which new objects are created. ..And.. that's about it. Lets look at an example:

    class myclass(object):
        nom = "nom nom nom"
        def __init__(self, value):
            self.value = value

        def useless(self):
            print "An useless", self.value

    mya = myclass("hello")
    myb = myclass("cat")

    mya.useless()           # "An useless hello"
    myb.useless()           # "An useless cat"

    mya.nom = "chomp"

    print myclass.nom       # "nom nom nom"
    print mya.nom           # "chomp"
    print myb.nom           # "nom nom nom"

Comments point out what each line is printing, so you won't need to run the code yourself to find that out. The `myclass` is being instantiated by calling it. The instance gets the methods and variables inside that class. Methods are like functions except that their first argument `self` gets bounded to the instance they're part of. They get bundled prettily along the data they work on and get divided apart from the rest of the program.

You might wonder what the `(object)` -piece is doing in the class declaration. It's an another class which this class is inheriting from. I don't explain it further as it's more complex subject and not really needed at the moment. Read it up from the python manual if it bothers you. Otherwise I won't mention of it again during this tutorial.

##From Useless to Useful
I told about the potential in brute paint, but I'm afraid other projects are going to catch my attention very soon. This tutorial needs a conclusion of some kind, after all. In this section we'll make this editor useful quite quickly and get a move on. The first things you might have noticed is that you couldn't change a color or choose a file. We'll address those two issues in this section.

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

Now it's quite bit more usable! eh.. wait. We probably want to color other things than just "canvas.png" there. The author might also like to select the size of the canvas that's being used. We'd like to get some arguments in to change the behavior of this program. We'll also want to check whether a file exists, to automaticly open a file if given. Lets introduce optparse and os in the start of the file:

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

Here's the full source for glancing:

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

You can see we have arrived to something that's slightly less brute than the earlier version we had. We can choose a color from fixed palette and where to save the results. Oooh! Real artists would still rather draw on a toilet paper than this! Given the time constraints we had, I couldn't get it further from this. But you can! And that is the point of this tutorial. You could keep adding the features in small increments like I did, and get something useful eventually.

At some point the size of the program would become daunting. If you were to fail your development would stop there. Otherwise the program gets designed such that it can be written further from the critical mass where it'd otherwise become too big to maintain. 

One point of this exercise was to show that you can make your own tools. And that existing ones aren't magical artifacts that couldn't be changed in any way. You might want to learn scripting gimp or blender, if you're not going to run them off a shoestring or expect to embed them into your games. Things like gimp or blender can't do everything for you though. If you'll find yourself in position that you need a some sort of tool that doesn't fit into blender/gimp -world, open this tutorial again and remind yourself that toolwriting isn't different from any other kind of programming.

##To The Battle Stations
Writing an actual game would be pretty much repetition of the instructions I already told in earlier sections. Aside having short on time, this is why I just decided to write the game and splatter it here.

Most of the time games are just programs like everything else. They have some state that gets modified by the game events. The state itself might be transmitted over the network or stored on the disk. Overall it's not hard or anything. The hard things come from actual concrete workings of the game. How does this menu work for the player? What happens when player presses this key? How does the enemy behave? It's okay to do something at first and then return later on the issue, similar to how it's with that painting application we wrote.

My example is bit of like the painting program in the sense that it's not polished in any way, or complete. It's some steps away from that. If you cared about doing this kind of game, you'd add some more enemies, make the game itself re-entrable that you could add a menu and a scoreboard.. cause game over when player dies.. add parallax background.. and so on.

![battle stations](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/battle_stations.png)

Full source code:

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

There's not anything too odd in the source code. You can see I've separated the game logic of each object into it's own block, along the graphic and other information related to the game object. I keep the active objects in a scene-set. The removals/insertions set are there, because you cannot reliably remove or insert items in python set while you're iterating through it. This way the removals are being done just in the very end of the last update. The game doesn't interact much between objects because there's no need for such stuff. If it were to interact in more complex way, then the interaction scheme might be slightly more complex than it is now. There's not a scoreboard, player lifes or anything other such.

If you grasped this tutorial you might see the potential of this program code... Maybe, where could you take it to?

##Game State and Framestep
If you've played classic games like tetris, nibbles, pacman, bomber man or boulder dash. You might have noticed that the characters are running on grids and never stop or change direction on a grid boundary. They might be made so well that you don't really even notice there were any grids!

You might think these kind of games are hard to do, as they require animating state changes between transition and there's that input messing up the thing as well. There you might not be farther away from the truth, unless you happen to be a corporation. The appearance on this kind of games is just a cream on the top, and it is really simple to prepare.

These kind of games are so simple that people occassionally end up writing a bare tetris or nibbles as an impulsive behaviour. Most of them struggle at creating the topping though. If you break it all into frames of sort, you can see the topping itself is really trivial as well.

You could first think about a simple sprite animation. Such animation would be broken into frames. Each frame has an associated image and a duration value which tells when the next frame is played. You could do this in your sleep but may not have an idea of how to mix the animation into the sort of games this section is about.

It gets way much easier when you realise the game state itself goes in sort of frames too. Each frame has some duration and whenever a frame gets entered the code gets run, which changes the state of the game. Just animate/interpolate between the state transitions and there's your polished graphics. The cream on the top is just pretty visuals with minor changes in game logic. 

##Conclusion
Not much to say to the conclusion. If you were doing a real game you might like to embed an editor into your game, that you could tune the game details while the game itself is playing. It isn't a jump into unknown since you've read this tutorial. You work on a state of some kind so just turn the malleable part of the game into a state of some sort, that'll make it more flexible too as well.

What I've told will hopefully get you to do games if you are interested about that sort of things. If you're unfamiliar with programming you will fail, but that's the idea. This tutorial is supposed to show you the way as I'm unable to just flush all this knowledge down your throat. You'll need to mess it up multiple times before you really figure how to do it right.

I hope you liked the tutorial. Please file an issue on the [issues page](https://github.com/cheery/pygame_tutorial/issues) if you hate it for some reason. If you want to study pygame more, you could try reading sources of different finished games, by different authors. Oh. I won't close this tutorial. If you have ideas on how to improve or continue this tutorial, go on and file an issue! You can also fork this tutorial in github.com and write your own version.

###License

The license for this tutorial? I think I won't define anything but I'd like to be acknowledged as the original author of the text I wrote for this tutorial and allow that for the future authors as well. If you keep sharing your changes without a compensation that's great too, but I don't require it.
