from constants import *
import pygame
from pygame.locals import *

class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, block, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        # pylint: disable-msg=E1121
        pieceSurf = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
        # pylint: enable-msg=E1121

        pieceSurf = pieceSurf.convert_alpha()
        pieceSurf.fill ((0, 0, 0, 0))  # make transparent
        self.rect = pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(pieceSurf, (255, 0, 0), self.rect)
        self.image = pieceSurf

        self.block = block
        self.moveTo = None

    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
