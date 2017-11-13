#!/usr/bin/python3

"""

# first iteration

- [ ] create static window
- [ ] create text as surface in memory
- loop
    - [ ] project text surface onto window
    - [ ] loop
        - [ ] if text surface blit does not fill screen to the right, add another blit of text at this position
    - [ ] increment position by delta X
    - [ ] tick at fps rate

"""

import os
import sys
import logging
import argparse
import pygame
from pprint import pformat,pprint
from pygame.locals import *
import pygame.freetype as freetype


###

colors = {
    "grey_light":  pygame.Color(200, 200, 200),
    "grey_dark" :  pygame.Color(100, 100, 100),
    "green"     :  pygame.Color(50, 255, 63),
    "red"       :  pygame.Color(220, 30, 30),
    "blue"      :  pygame.Color(50, 75, 245),
    "black"     :  pygame.Color(0, 0, 0),
}


###

class MarqueeText(object):

    def __init__(self, marquee, text="mawoh marquee", fontsize=64,color='red'):
        """
        create an internal Font Surface

        marquee is of class MarqueeText
        """
        self.marquee = marquee
        self.screen = marquee.get_surface()

    def put(self, x=0, y=0):
        pass

    def move(self, delta_x, delta_y):
        pass

    def is_offscreen(self):
        """
        returns True, if text will be out of screen after applying delta_x,delta_y
        """

    def render(self):
        """
        render the marquee text to the marquee surface
        """
        pass


class Marquee(object):
    def __init__(self, width=800, height=400, X=0,Y=0, decorations=False, autosize=True, autoposition=True, maxfps=30, color='red', timeout=0, exit_on_keypress=True):
        pass

    def initpygame(self):
        pass

    def run(self):
        pass

    def add_text(self,marquetext,timeout=0,count=0):
        pass

    def get_surface(self):
        """
        return the marquee surface
        """



def cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', default=['mawoh marquee'], nargs='+')
    parser.add_argument('--font', default='')
    parser.add_argument('--size', default=40, type=int)
    parser.add_argument('--width',default=800, type=int)
    parser.add_argument('--height',default=400, type=int)
    #parser.add_argument('--color',default='red')
    parser.add_argument('--X', default=0, type=int)
    parser.add_argument('--Y', default=0, type=int)
    parser.add_argument('--autosize', action="store_true")

    return parser.parse_args()


def run(args):
    pygame.init()
    clock = pygame.time.Clock()

    fontdir = os.path.dirname(os.path.abspath (__file__))
    font = freetype.Font(os.path.join (fontdir, "data", "sans.ttf"))

    oursize =(args.width, args.height)
    if args.autosize:
        modes = pygame.display.list_modes()
        log.info("modes: {}".format(modes))
        args.Y = modes[0][1]-args.height
        oursize = (modes[0][0],args.height)



    log.info("creating screen with size {}".format(oursize))

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (args.X,args.Y)
    screen = pygame.display.set_mode(oursize, pygame.NOFRAME)

    color=colors["black"]
    posx = screen.get_width()
    posy = 0
    dx = 0
    max_fps = 30
    scroll_speed = -5
    color = colors["red"]
    size = 64
    style = freetype.STYLE_OBLIQUE
    (textsurface, rect) = font.render(args.text, color, size=size, style=style)
    (paddingsurface, rect) = font.render(" +++ ", color, size=size, style=style)

    log.info("surface pformat: {}".format(textsurface))

    going = True
    while going:

        # bail out on any key
        events = pygame.event.get()
        for e in events:
            if e.type in (QUIT, KEYDOWN):
                going = False
                log.info("sane exit condition. bye bye.")

        # calculate marquee position

        posx += scroll_speed
        curx = posx

        screen.fill(0)
        screen.blit(textsurface,(posx,posy))

        # Now display as many of the texts as needed to fill the screen
        # width.
        # if pos+text width is completely outside of the screen reset posx to the x position of the next copy.


        # if posx+textsurface.get_width() < screen.get_width():
        #     curx += textsurface.get_width()
        #     screen.blit(textsurface,(curx,posy))

        pygame.display.update()
        clock.tick(max_fps)

    pygame.quit()



#
# main
#
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.info('starting up')
args = cmd_line()
run(args)
log.info('done')
