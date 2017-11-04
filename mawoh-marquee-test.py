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
    "grey_light"    :   pygame.Color(200, 200, 200),
    "grey_dark"     :   pygame.Color(100, 100, 100),
    "green"         :   pygame.Color(50, 255, 63),
    "red"           :   pygame.Color(220, 30, 30),
    "blue"          :   pygame.Color(50, 75, 245),
    "black"          :   pygame.Color(0, 0, 0),
}


###




def cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', default='+++ mawoh marquee +++')
    parser.add_argument('--font', default='')
    parser.add_argument('--size', default=40, type=int)
    parser.add_argument('--width',default=800, type=int)
    parser.add_argument('--height',default=400, type=int)
    parser.add_argument('--X', default=320, type=int)
    parser.add_argument('--Y', default=200, type=int)

    return parser.parse_args()


def run(args):
    pygame.init()
    clock = pygame.time.Clock()

    fontdir = os.path.dirname(os.path.abspath (__file__))
    font = freetype.Font(os.path.join (fontdir, "data", "sans.ttf"))
    screen = pygame.display.set_mode((args.X, args.Y))

    color=colors["black"]
    posx=0
    posy=0
    dx=0
    max_fps = 30
    scroll_speed=-5
    color = colors["red"]
    size = 64
    style = freetype.STYLE_OBLIQUE
    (textsurface, rect) = font.render(args.text, color, size=size, style=style)

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

        screen.fill(0)
        screen.blit(textsurface,(posx,posy))

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
