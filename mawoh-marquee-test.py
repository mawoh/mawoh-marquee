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

COLORS = {
    "grey_light":  pygame.Color(200, 200, 200),
    "grey_dark" :  pygame.Color(100, 100, 100),
    "green"     :  pygame.Color(50, 255, 63),
    "red"       :  pygame.Color(220, 30, 30),
    "blue"      :  pygame.Color(50, 75, 245),
    "black"     :  pygame.Color(0, 0, 0),
}


###

class MarqueeText(object):

    def __init__(self, text="mawoh marquee", color=COLORS['red']):
        """
        create an internal Font Surface
        """
        self.text = text
        self.color = color
        log.info("text created: ({}) {}".format(self.color,self.text))

    def set_marquee(self, marquee):
        """
        marquee is of class MarqueeText
        """
        self.marquee = marquee
        self.screen = marquee.get_surface()

        style = freetype.STYLE_OBLIQUE
        font = marquee.get_font()
        (textsurface, rect) = font.render(self.text, self.color, size=marquee.get_fontsize(), style=style)
        # (paddingsurface, rect) = font.render(" +++ ", color, size=size, style=style)
        self.surface = textsurface
        self.rect = rect
        log.debug("text surface created: {}".format(textsurface))

    def get_text(self):
        return self.text

    def put_offscreen(self, delta_x, delta_y):
        """
        put the text surface just outside of the is_offscreen
        delta_x, delta_y are used to determine the scrolling direction to place the text correctly
        """
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

    def __init__(self, width=800, height=200, X=0,Y=0, decorations=False, autosize=True, autoposition=True, maxfps=30, bgcolor=COLORS["black"], timeout=0, exit_on_keypress=True, fontfile=None, fontsize=64, delta_x=-5, delta_y=0):
        """
        set up marquee. does not display window yet until run() is called.
        """

        # let the show begin
        pygame.init()

        #
        # ## should there be a declaration block?
        #

        #
        # Declarations:
        #

        # texts will be a list of MarqueeText instances
        self.texts = []

        # delta is the movement speed
        self.delta_x=delta_x
        self.delta_y=delta_y

        # counter is the rolling position
        self.counter_x=0
        self.counter_y=0

        self.exit_on_keypress = exit_on_keypress
        self.bgcolor = bgcolor
        self.fontsize = fontsize

        #
        # End of declarations
        #

        # prepare font
        if fontfile:
            self.font = freetype.Font(fontfile)
        else:
            fontdir = os.path.dirname(os.path.abspath (__file__))
            self.font = freetype.Font(os.path.join (fontdir, "data", "sans.ttf"))

        # we need a clock to time fps
        self.clock = pygame.time.Clock()
        self.maxfps = maxfps

        # prepare the screen
        if autosize:
            # TODO:
            # if autosize, also scale the fontsize to match it!
            # also we need padding around the window borders
            log.info("detect optimal size")
            modes = pygame.display.list_modes()
            log.debug("modes: {}".format(modes))
            Y = modes[0][1] - height
            oursize = (modes[0][0], height)

        self.oursize = oursize
        # moving the screen window to the desired position
        log.info("display size {}".format(oursize))
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X,Y)

        # now set the display decorations mode
        if decorations:
            self.display_options = 0
        else:
            self.display_options = pygame.NOFRAME

    def run(self):
        log.info("running!")
        log.debug("size: {}".format(self.oursize))
        log.debug("options: {}".format(self.display_options))
        screen = pygame.display.set_mode(self.oursize, self.display_options)

        #enter the looooop
        going = True
        count = 0
        while going:
            # bail out on any key
            events = pygame.event.get()
            for e in events:
                if e.type in (QUIT, KEYDOWN):
                    going = False
                    log.info("sane exit condition. bye bye.")

            # calculate marquee position
            # posx += scroll_speed
            # curx = posx
            #
            # screen.fill(0)
            # screen.blit(textsurface,(posx,posy))
            #
            # # Now display as many of the texts as needed to fill the screen
            # # width.
            # # if pos+text width is completely outside of the screen reset posx to the x position of the next copy.
            #
            #
            # # if posx+textsurface.get_width() < screen.get_width():
            # #     curx += textsurface.get_width()
            # #     screen.blit(textsurface,(curx,posy))
            #

            for text in self.texts:
                count += 1
                # if text would be outside screen, reattach to the end of list
                log.info("({}) text: {}".format(count,text.get_text()))
                if text.is_offscreen():
                    pass



            pygame.display.update()
            self.clock.tick(self.maxfps)
        pygame.quit()


    def add_text(self,marqueetext,timeout=0,count=0):

        # link the marqueetext to us
        marqueetext.set_marquee(self)

        # add the text to the list

        self.texts.append(marqueetext)
        log.info("added text {} '{}' to list.".format(len(self.texts), marqueetext.get_text()))


    def get_font(self):
        return self.font

    def get_fontsize(self):
        return self.fontsize

    def get_surface(self):
        """
        return the marquee surface
        """

# define commandline
#
def cmd_line():
    """
    create commandline, return args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', default=['mawoh marquee'], nargs='+')
    parser.add_argument('--font', default='')
    parser.add_argument('--size', default=40, type=int)
    parser.add_argument('--width',default=800, type=int)
    parser.add_argument('--height',default=400, type=int)
    parser.add_argument('--color',default='red')
    parser.add_argument('--X', default=0, type=int)
    parser.add_argument('--Y', default=0, type=int)
    parser.add_argument('--autosize', action="store_true")
    parser.add_argument('-v', action="store_true")

    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.DEBUG)
        log.debug("debug logging enabled")

    return args


# logging!
# TODO: evaluate the correct way to establish lib logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("marquee")

# main
#
if __name__ == "__main__":

    log.info('starting up')

    args = cmd_line()

    # TODO:
    # transfer command line
    marquee = Marquee()
    text1 = MarqueeText("hello world")
    text2 = MarqueeText("second marquee text", color=COLORS["green"])

    # add some demo text
    marquee.add_text(text1)
    marquee.add_text(text2)

    # start the loop
    marquee.run()

    log.info('done')
