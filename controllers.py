#! /usr/bin/env python
'''
@author: Matthew Demarest
@version: 1.1
@summary: Controls from user, running ticks, and timer to signal events.
'''

import events  # from events.py
import pygame
from pygame.locals import *

DIRECTION_DOWN = 0
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
ROTATE_RIGHT = 3
ROTATE_LEFT = 4
DROPDELAY = 1000  # 1 seconds
DROPEVENT = USEREVENT + 1  # signals the time to drop a block

class KeyboardController:
    '''KeyboardController takes Pygame events generated by the keyboard and
    uses them to control the model, by sending requests or to control the
    Pygame display directly, as with the QuitEvent
    '''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

    #--------------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, events.TickEvent()):
            # Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = events.QuitEvent()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ev = events.QuitEvent()
                    elif event.key == K_UP:
                        ev = events.ShapeRotateRequest(ROTATE_RIGHT)
                    elif event.key == K_RSHIFT:
                        ev = events.ShapeRotateRequest(ROTATE_LEFT)
                    elif event.key == K_LEFT:
                        ev = events.ShapeStartMoveRequest(DIRECTION_LEFT)
                    elif event.key == K_RIGHT:
                        ev = events.ShapeStartMoveRequest(DIRECTION_RIGHT)
                    elif event.key == K_DOWN:
                        ev = events.ShapeStartMoveRequest(DIRECTION_DOWN)
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        ev = events.ShapeStopMoveRequest(DIRECTION_LEFT)
                    elif event.key == K_RIGHT:
                        ev = events.ShapeStopMoveRequest(DIRECTION_RIGHT)
                    elif event.key == K_DOWN:
                        ev = events.ShapeStopMoveRequest(DIRECTION_DOWN)
                elif event.type == DROPEVENT:
                    ev = events.ShapeFallEvent()

        if ev:
            self.evManager.Post(ev)

class RunController:
    '''...'''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.keepGoing = True

    #--------------------------------------------------------------------------
    def run(self):
        while self.keepGoing:
            event = events.TickEvent()
            self.evManager.post(event)

    #--------------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, events.QuitEvent()):
            # this stops the while loop from running
            self.keepGoing = False

class TimeController:
    '''Signals time based events.'''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
