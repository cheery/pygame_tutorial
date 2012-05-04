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

Those columns might like some colors, but I leave that as an exercise to a reader as it's irrelevant for the rest of the tutorial and should not cause any difficulties. We will proceed to graphics. Before that there's a thing you might want to know.

##Avoid Work
You could take a break now, sit and think about what you've read this far. Perhaps play with the code I introduced. After a successful break get back and keep reading.

If you need something that is not specific to your project, it might be someone has already written a module that matches your needs. Although it isn't a requirement to use existing modules. Use works of others to avoid work yourself. Although, if you need something very simple then do not waste time searching it and do it yourself.

You may have had a play with the source code by this far. Already wondering how will you ever learn to use those modules? I'm not documenting those functions in this tutorial any way. The answer is simple. I have left it up to you to study [pygame](http://www.pygame.org/docs/) and [math](http://docs.python.org/library/math.html) reference manuals.

The title of this tutorial is a bit of a misnomer. I'm not teaching you pygame. Pygame itself provides that documentation you could follow. I am teaching you project workflow, problem solving, programming techniques. Sort of things really good hackers understand and use routinely.

You may have also noticed I didn't told you what we are actually doing in this tutorial. You could scroll this tutorial down to the bottom, but there's no point. What we are doing in this tutorial isn't really important. The goal of this tutorial is to show effective techniques in programming which you will imitate and fail at, yet numerous times hopefully.

You will become skilled in hacking only through exercising hacker skills. Problem analysis and solving: These skills will let you breach barriers you might not otherwise bypass. Though they itself involve a problem that they aren't particularly easy to teach. I hope I handle it well enough and help you learning the necessary techniques faster than usual.
