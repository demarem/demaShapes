import pygame
from pygame.locals import *
from constants import *
import events
import boardView
import previewView

class MainView:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('DemaShapes')

        # pylint: disable-msg=E1121
        self.background = pygame.Surface(self.window.get_size())
        # pylint: enable-msg=E1121

        self.background.fill(BLACK)
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.boardView = boardView.BoardView(self.eventManager, self.window, self.background)
        self.previewView = previewView.PreviewView(self.eventManager, self.window, self.background)

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            self.boardView.draw()
            self.previewView.draw()
