#Cheery's Pygame Tutorial
This tutorial is a draft, it will change. If you have ideas of how to improve or continue this tutorial, tell about it in [issues page](https://github.com/cheery/pygame_tutorial/issues). Oh, and if you disagree with me about something then fork your own tutorial. ;-)

Before you start this tutorial, it'd be good to understand little bit of python already. What is a function, variable, loop, tuple, list, function call, import? At least I expect you understand those things. I explain the rest as we go through this tutorial. I provide a link for more reading whenever I mention something you might not understand readily.

##Rolling Columns
We start from this piece of code:

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

This code opens a display device through pygame and goes into an event polling loop. For every event, that was being received during last frame, it calls our dispatch -function, which determines what happens when it gets an event. We can see that a request to quit causes the process to exit.

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

The animation may stutter a bit at the edges of the screen, because of [alialising](http://en.wikipedia.org/wiki/Aliasing). screen.fill is unable to smooth away the [pixel](http://en.wikipedia.org/wiki/Pixel) boundaries. You may experience further stutter because of other, unknown, reasons.

![rolling columns](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/rolling_columns.png)

Those columns might like some more colors, but I leave that as an exercise to a reader as it's irrelevant for the rest of the tutorial and should not cause any difficulties. We will proceed to graphics. Before that there's a thing you might want to know.

##Avoid Work
You could take a break now, sit and think about what you've read this far. Perhaps play with the code I introduced. After a successful break get back and keep reading.

If you need something that is not specific to your project, it might be someone has already written a module that matches your needs. Although it isn't a requirement to use existing modules. Use works of others to avoid work yourself. Although, if you need something very simple then do not waste time searching it and do it yourself.

You may have had a play with the source code by this far. Already wondering how will you ever learn to use those modules? I'm not documenting those functions in this tutorial any way. The answer is simple. I have left it up to you to study [pygame](http://www.pygame.org/docs/) and [math](http://docs.python.org/library/math.html) reference manuals.

The title of this tutorial is a bit of a misnomer. I'm not teaching you pygame. Pygame itself provides that documentation you could follow. I am teaching you project workflow, problem solving, programming techniques. Sort of things really good hackers understand and use routinely.

You may have also noticed I didn't told you where we will be ending up in this tutorial. You could scroll this tutorial down to the bottom, but there's no point. What we are doing in this tutorial isn't really important. The goal of this tutorial is to show effective techniques in programming which you will imitate and fail at, yet numerous times hopefully.

You will become skilled in hacking only through exercising hacker skills. Problem analysis and solving: These skills will let you breach barriers you might not otherwise bypass. Though they itself involve a problem that they aren't particularly easy to teach. I hope I handle it well enough and help you learning the necessary techniques faster than usual.

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

![rolling columns](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/brute_paint.png)

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

    screen.blit(canvas, (screen.get_width()-width, screen.get_height()-height))

![slightly less brute paint](http://github.com/cheery/pygame_tutorial/raw/master/screenshots/slightly_less_brute_paint.png)

You can see we have arrived to something that's slightly less brute than the earlier version we had. We can choose a color from fixed palette and where to save the results. Oooh! Real artists would still rather draw on a toilet paper than this! You cannot write a nice paint out of a tutorial you know. :-) But there was an other point in this exercise than to get a nice brute painting app. The point of this exercise was give you an idea, that you can make your own tools and they aren't magical things you couldn't change.

You might want to learn scripting gimp or blender, if you're not running them off a shoestring or expect to embed them into your games. Things like gimp or blender can't do everything for you though. If you'll find yourself in position that you need a some sort of tool, open this tutorial again and remind yourself that toolwriting isn't different from any other kind of programming.

So uh.. Maybe we'd like to make a game with our newly created tool next?
