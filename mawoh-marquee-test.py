#!/usr/bin/python3

"""
"""

import os
import sys
import logging
import argparse
import pygame
from random import randint
from pprint import pformat,pprint
from pygame.locals import *
import pygame.freetype as freetype

# pip install randomwords
from random_words import LoremIpsum

###

COLORS = {
    "grey_light":  pygame.Color(200, 200, 200),
    "grey_dark" :  pygame.Color(100, 100, 100),
    "green"     :  pygame.Color(50, 255, 63),
    "red"       :  pygame.Color(220, 30, 30),
    "blue"      :  pygame.Color(50, 75, 245),
    "black"     :  pygame.Color(0, 0, 0),
    "white"     :  pygame.Color(255, 255, 255),
}


###

class MarqueeText(object):

    def __init__(self, text="mawoh marquee", textcolor=COLORS['red'],size=None):
        """
        create an internal Font Surface
        """
        self.text = text
        self.textcolor = textcolor
        self.size = size
        log.debug("text created: ({}) {}".format(self.textcolor,self.text))

    def set_marquee(self, marquee):
        """
        marquee is of class MarqueeText
        """
        self.marquee = marquee

        #style = freetype.STYLE_OBLIQUE
        style = 0
        font = marquee.get_font()
        if not self.size:
            self.size = marquee.get_fontsize()

        #TODO: alpha does not work this way with bgcolor...?!
        #(surface, rect) = font.render(self.text, pygame.Color(255,0,0,255), size=self.size, style=style, bgcolor=pygame.Color(0,0,0,255))

        log.debug("textcolor: {}".format(self.textcolor))
        (surface, rect) = font.render(self.text, self.textcolor, size=self.size, style=style)


        self.surface = surface
        log.debug("MarqueeText initialized ({}x{}): {}".format(surface.get_width(),surface.get_height(),self.text))

    def get_text(self):
        return self.text

    def get_surface(self):
        return self.surface


class Marquee(object):

    def __init__(self, width=800, height=100, X=0,Y=0, decorations=False, autosize=True, autoposition=True, fps=60, bgcolor=COLORS["black"], textcolor=COLORS["white"], timeout=0, exit_on_keypress=True, fontfile=None, fontsize=64, speed=10, paddingtext="+++", paddingcolor=COLORS["white"]):
        """
        set up marquee. does not display window yet until run() is called.
        """

        # let the show begin
        pygame.init()

        # texts will be a list of MarqueeText instances
        self.texts = []

        # carrot is the current x position of the scroller
        self.carrot = 0

        # delta_x will be calculated at runtime
        self.delta_x=0

        # scroller speed in pixels per second
        self.speed = speed

        self.exit_on_keypress = exit_on_keypress
        self.bgcolor = bgcolor
        self.fontsize = fontsize
        self.textcolor = textcolor
        self.paddingtext = paddingtext
        self.paddingcolor = paddingcolor

        # we need a clock to time fps
        self.clock = pygame.time.Clock()
        self.fps = fps

        # prepare the screen
        if autosize:
            # TODO:
            # if autosize, also scale the fontsize to match
            # ...or scale window to font size?
            # also we need padding around the window borders
            log.debug("detect optimal size")
            modes = pygame.display.list_modes()
            log.debug("modes: {}".format(modes))
            Y = modes[0][1] - height
            self.oursize = (modes[0][0], height)
        else:
            self.oursize = (width,height)

        log.info("display size {}".format(self.oursize))

        # move the screen window to the desired position
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X,Y)

        # prepare font
        if fontfile:
            self.font = freetype.Font(fontfile)
        else:
            fontdir = os.path.dirname(os.path.abspath (__file__))
            self.font = freetype.Font(os.path.join (fontdir, "data", "sans.ttf"))

        # the display decorations mode
        if decorations:
            self.display_options = 0
        else:
            self.display_options = pygame.NOFRAME

        ##
        ## does not work :( opengl does not work for this and hwsurface
        ## is not available in window mode. bummer.
        #
        #self.display_options = self.display_options|pygame.DOUBLEBUF|pygame.OPENGL

    def update_texts(self):
        """
        - In LoremIpsum mode, generates new texts.

        Other Ideas:
        - Server mode, check for new texts from tcp socket
        - File Mode, monitor a directory for one or more files with lines of text

        """
        if args.lorem:
            self.texts=[]
            li = LoremIpsum()
            for l in li.get_sentences_list(args.lorem):
                lt = MarqueeText(l,textcolor=self.textcolor)
                self.add_text(lt)
            return True

        return False



    def generate_scroller(self):
        """
        - create a scroller surface, containing all available text surfaces.
        - iterate until at least screen is filled
        """

        # TODO: add cmdline args for padding

        # while debugging make the padding text colorful :)
        if args.v:
            color = pygame.Color(randint(0,255),randint(0,255),randint(0,255))
        else:
            color = self.paddingcolor

        (paddingtext, rect) = self.font.render(" {} ".format(self.paddingtext), self.paddingcolor, size=self.fontsize)

        # calculate needed surface size (width and height)
        # generates list of positions and text surfaces
        width = 0
        height = paddingtext.get_height()
        index = 0
        scroller = None
        filled = False
        allseen = False
        blitlist = []
        log.debug("texts: {}".format(len(self.texts)))
        while not filled:
            #log.debug("adding text {} to scroller".format(index))
            text = self.texts[index].get_surface()

            blitlist.append((width,paddingtext))
            width += paddingtext.get_width()
            blitlist.append((width,text))
            width += text.get_width()

            if text.get_height() > height:
                height = text.get_height()

            if allseen and width >= self.screen.get_width():
                filled = True

            index += 1
            if index >= len(self.texts):
                allseen = True
                index = 0

        log.debug("adding scroller with size: {}x{}".format(width,height))
        scroller = pygame.Surface((width,height))
        for (posx, text) in blitlist:
            # center on y
            posy = int((scroller.get_height()/2) - (text.get_height()/2))
            #log.debug("add text at {}x{}".format(posx,posy))
            scroller.blit(text,(posx,posy))
        return scroller

    def scroller_outside(self, scroller):

        if self.speed > 0 and abs(self.carrot) >= scroller.get_width():
            log.debug("scroller outside! <---")
            return True
        elif self.speed < 0 and self.carrot >= self.screen.get_width():
            log.debug("scroller outside! <---")
            return True
        else:
            return False

    def scroller_leaving(self, scroller):
        margin = 50
        width = self.screen.get_width()
        posx1 = self.carrot
        posx2 = posx1 + scroller.get_width()
        # calculate remainder scroller surface that is not yet visible
        if self.speed >= 0: # <-----
            remainder = posx2 - width
        else: # ----->
            remainder = posx1 * -1


        if remainder < margin:
            log.debug("remainder < margin: {} < {}".format(remainder,margin))
            return True
        else:
            return False

    def run(self):
        log.debug("running!")
        log.debug("size: {}".format(self.oursize))
        log.debug("options: {}".format(self.display_options))

        screen = pygame.display.set_mode(self.oursize, self.display_options)
        self.screen = screen

        log.debug("display driver: {}".format(pygame.display.get_driver()))
        #log.debug("display features: {}".format(pygame.display.Info()))



        # the x position of the scroller follows the carrot :)
        self.carrot = None
        current_scroller = None
        next_scroller = None
        current_y = 0
        next_y = 0
        speed = self.speed

        #enter the looooop
        going = True
        while going:

            # bail out on any key
            events = pygame.event.get()
            for e in events:
                if e.type in (QUIT, KEYDOWN):
                    going = False
                    log.debug("sane exit condition. bye bye.")
                    going = False

            # TODO: audit these conditionals!
            if not current_scroller:
                # this is the first tick!
                self.update_texts()
                current_scroller = self.generate_scroller()
                if speed >= 0: # <-----
                    self.carrot = screen.get_width()
                else: # ---->
                    self.carrot = current_scroller.get_width() * -1

            # if scroller is completely offscreen in moving direction,
            # replace it with the follow up scroller
            # also reset the carrot to the follow up scroller
            if self.scroller_outside(current_scroller):
                log.debug("scroller outside, next becomes current")
                if speed >= 0:
                    self.carrot += current_scroller.get_width()
                else:
                    self.carrot -= next_scroller.get_width()
                del(current_scroller)
                # TODO: what happens if next_scroller is not defined?
                current_scroller = next_scroller
                next_scroller = None

            # if scroller is about to leave blank space on the end,
            # generate the follow up scroller
            if not next_scroller and self.scroller_leaving(current_scroller):
                log.debug("scroller leaving, adding next one")
                self.update_texts()
                next_scroller = self.generate_scroller()


            screen.fill(self.bgcolor)

            # render some debugging stuff
            if args.v:
                (debugtext, rect) = self.font.render("p:{} fps:{} t:{} dx:{}".format(self.carrot, round(self.clock.get_fps(),1), self.clock.get_time(),self.delta_x), self.textcolor, size=10)


            ms = self.clock.tick(self.fps)
            # is busy loop smoother?
            #ms = self.clock.tick_busy_loop(self.fps)
            self.delta_x = round(-(speed/1000)*ms)
            self.carrot += self.delta_x

            posy = int((screen.get_height()/2) - (current_scroller.get_height()/2))
            screen.blit(current_scroller,(self.carrot,posy))
            if next_scroller:
                posy = int((screen.get_height()/2) - (next_scroller.get_height()/2))
                if speed >= 0:
                    posx = self.carrot+current_scroller.get_width()
                else:
                    posx = self.carrot - next_scroller.get_width()
                screen.blit(next_scroller,(posx,posy))

            if args.v:
                screen.blit(debugtext,(0,0))

            pygame.display.flip()

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



# define commandline
#
def cmd_line():
    """
    create commandline, return args
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--font', default=None, help="font file")
    parser.add_argument('--size', default=50, type=int, help="Font size")
    parser.add_argument('--width',default=800, type=int, help="Window width")
    parser.add_argument('--height',default=100, type=int, help="Window Height")
    parser.add_argument('--speed',default=250, type=int, help="Pixels per second scrolling speed")
    parser.add_argument('--fps',default=60, type=int, help="Frames per second rate limit")
    parser.add_argument('--textcolor',default='green', choices=COLORS.keys(), help="Text Color")
    parser.add_argument('--bgcolor',default='black', choices=COLORS.keys(), help="Background Color")
    parser.add_argument('--paddingcolor',default='red', choices=COLORS.keys(), help="Padding text Color")
    parser.add_argument('--paddingtext',default=' +++ ', choices=COLORS.keys(), help="Padding text")
    parser.add_argument('--X', default=0, type=int, help="Window X position")
    parser.add_argument('--Y', default=0, type=int, help="Window Y position")
    parser.add_argument('--autosize', action="store_true", help="Autosize window to screen width.")
    parser.add_argument('-v', action="store_true", help="Show verbose output")
    parser.add_argument('--lorem', type=int, help="(for debugging) generate lines of random text - overrides any other text input")
    parser.add_argument('text', default=['mawoh marquee'], nargs='*', help="Lines of text to display")

    args = parser.parse_args()

    if args.v:
        logging.basicConfig(level=logging.DEBUG)
        log.setLevel(logging.DEBUG)
        log.debug("debug logging enabled")


    # generate some lines of lorem ipsum! :)
    if not args.text:
        args.lorem = 3

    return args




# main
#
if __name__ == "__main__":

    # logging!
    # TODO: evaluate the correct way to establish lib logging
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("marquee")


    args = cmd_line()

    log.debug('starting up')

    # TODO#:
    # transfer command line
    marquee = Marquee(fps=args.fps,width=args.width,height=args.height, autosize=args.autosize,X=args.X,Y=args.Y,fontsize=args.size, textcolor=COLORS[args.textcolor], bgcolor=COLORS[args.bgcolor], speed=args.speed,paddingtext=args.paddingtext, paddingcolor=COLORS[args.paddingcolor])
    for t in  args.text:
        mtext = MarqueeText(t,textcolor=COLORS[args.textcolor])
        marquee.add_text(mtext)

    # start the loop
    marquee.run()

    log.info('done')
