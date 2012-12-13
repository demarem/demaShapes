#! /usr/bin/env python
'''
@author: Matthew Demarest
@version: 1.1
@summary: Views updated after event signals.
'''

import events
import pygame
from pygame.locals import *

#---------------------------- WINDOW SIZE -------------------------------------
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#---------------------------- BOARD SIZE --------------------------------------
BLOCKSIZE = 20  # pixels
BOARDWIDTH = 10 * BLOCKSIZE
BOARDHEIGHT = 20 * BLOCKSIZE
XMARG = int((WINDOWWIDTH / 2) - (BOARDWIDTH / 2))
YMARG = int((WINDOWHEIGHT / 2) - (BOARDHEIGHT / 2))

#---------------------------- SCORE SIZE --------------------------------------
SCOREWIDTH = 125
SCOREHEIGHT = 100
PLAYRECT = pygame.Rect(XMARG, YMARG, BOARDWIDTH, BOARDHEIGHT)
SCORERECT = pygame.Rect(WINDOWWIDTH - (XMARG / 2) - (SCOREWIDTH / 2), YMARG,
                         SCOREWIDTH, SCOREHEIGHT)

#------------------------------ COLORS ----------------------------------------
#        R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTYELLOW = (175, 175, 20)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
#------------------------------------------------------------------------------


# distance between side of play area and initial template position
LEFTGAP = 3 * BLOCKSIZE
RIGHTGAP = 2 * BLOCKSIZE

# template values
EMPTY = '.'
BLOCK = 'O'

# colors
BGCOLOR = NAVYBLUE
PLAYRECTCOLOR = WHITE
SCOREWRITINGCOLOR = LIGHTYELLOW
SCORECOLOR = GRAY

class ActiveShapeView:
    def __init__(self, evManager):
        
        