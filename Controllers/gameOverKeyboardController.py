from constants import *
import events
import pygame
from pygame.locals import *

class GameOverKeyboardController:
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
                elif event.key == K_r:
                    ev = events.ResetEvent()
            return ev
