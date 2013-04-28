import pygame
from pygame.locals import *
from constants import *

class SpaceSprite(pygame.sprite.Sprite):
    def __init__(self, space, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        # pylint: disable-msg=E1121
        self.image = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
        # pylint: enable-msg=E1121

        self.image.fill(BLACK)

        self.space = space
