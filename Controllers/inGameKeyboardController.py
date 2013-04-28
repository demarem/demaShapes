from constants import *
import events
import pygame
from pygame.locals import *

DROPDELAY = 1000  # 1 seconds

class InGameKeyboardController:
    def __init__(self):
        pass

    def read(self):
        for event in pygame.event.get():
            ev = None
            if event.type == QUIT:
                ev = events.QuitEvent()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
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
                elif event.key == K_SPACE:
                    ev = events.ShapeDropRequest()
                elif event.key == K_r:
                    ev = events.ResetEvent()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    ev = events.ShapeStopMoveRequest(DIRECTION_LEFT)
                elif event.key == K_RIGHT:
                    ev = events.ShapeStopMoveRequest(DIRECTION_RIGHT)
                elif event.key == K_DOWN:
                    ev = events.ShapeStopMoveRequest(DIRECTION_DOWN)
            return ev
