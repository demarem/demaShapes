from constants import *
import pygame
from pygame.locals import *

class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, block, color, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        # pylint: disable-msg=E1121
        self.pieceSurf = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
        # pylint: enable-msg=E1121

        self.color = color
        self.pieceSurf = self.pieceSurf.convert_alpha()
        self.pieceSurf.fill ((0, 0, 0, 0))  # make transparent
        self.rect = pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.pieceSurf, color, self.rect)
        self.image = self.pieceSurf

        self.block = block
        self.moveTo = None

    def update(self):

        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
