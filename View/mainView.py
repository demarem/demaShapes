import pygame
from pygame.locals import *
from constants import *
import events
import boardView
import previewView
import gameOverView

class MainView:
    STATE_INGAME = 'In Game'
    STATE_PAUSED = 'Paused'
    STATE_GAMEOVER = 'Game Over'

    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.state = MainView.STATE_INGAME

        pygame.init()
        self.window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('DemaShapes')

        # pylint: disable-msg=E1121
        self.background = pygame.Surface(self.window.get_size())
        # pylint: enable-msg=E1121

        self.background.fill(BLACK)
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.board = boardView.BoardView(self.eventManager, self.window,
                                        self.background)
        self.preview = previewView.PreviewView(self.eventManager, self.window,
                                              self.background)
        self.gameOver = gameOverView.GameOverView(self.eventManager, self.window,
                                                 self.background)

        self.viewStateMap = {MainView.STATE_INGAME: [self.board, self.preview],
                             MainView.STATE_GAMEOVER:
                                 [self.gameOver]}

    def reset(self):
        self.background.fill(BLACK)
        self.window.blit(self.background, (0, 0))
        self.board.showBoard(True)

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            for view in self.viewStateMap[self.state]:
                view.draw()

        elif isinstance(event, events.GameOverEvent):
            self.state = MainView.STATE_GAMEOVER

        elif isinstance(event, events.ResetEvent):
            self.state = MainView.STATE_INGAME
            self.reset()

