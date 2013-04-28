import pygame
from pygame.locals import *
from constants import *

class GameOverView:
    def __init__(self, eventManager, window, background):
        self.eventManager = eventManager

        self.window = window
        self.background = background
        self.gameOverFont = pygame.font.Font(None, 30)
        self.optionsFont = pygame.font.Font(None, 20)

        # pylint: disable-msg=E1121
        backDrop = pygame.Surface((200, 200))
        # pylint: enable-msg=E1121

        backDrop = backDrop.convert_alpha()
        backDrop.fill ((0, 0, 0, 0))  # make transparent
        rect = pygame.Rect(0, 0, 200, 200)
        pygame.draw.rect(backDrop, BLACK, rect)
        pygame.draw.rect(backDrop, GREEN, rect, 10)
        self.image = backDrop

    def draw(self):
        center = self.window.get_rect().center
        backDropPos = self.image.get_rect()
        backDropPos.center = center
        self.window.blit(self.image, backDropPos)

        gameOverText = self.gameOverFont.render("GAME OVER", 0, GREEN)
        textpos = gameOverText.get_rect()
        textpos.center = center
        self.window.blit(gameOverText, textpos)
        pygame.display.flip()
