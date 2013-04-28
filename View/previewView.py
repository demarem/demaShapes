import pygame
from pygame.locals import *
from constants import *
import spaceSprite
import blockSprite
import events

class PreviewView:
    def __init__(self, eventManager, window, background):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.window = window
        self.background = background
        self.font = pygame.font.Font(None, 30)

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()

    def showPreviewPane(self, board):
        squareRect = pygame.Rect(PREVIEWLEFT, PREVIEWTOP, BLOCKSIZE, BLOCKSIZE)

        print board.spaces
        column = 0
        for row in board.spaces:
            for space in row:
                if column < SHAPETYPES.TEMPLATEWIDTH:
                    squareRect = squareRect.move(BLOCKSIZE, 0)
                else:
                    column = 0
                    squareRect = squareRect.move(-(BLOCKSIZE * (SHAPETYPES.TEMPLATEWIDTH - 1)), BLOCKSIZE)
                column += 1
                newSprite = spaceSprite.SpaceSprite(space, self.backSprites)
                newSprite.rect = squareRect
                newSprite = None

    def showBlock(self, block, blockColor):
        spaceBlock = block.space
        blockSpr = blockSprite.BlockSprite(block, blockColor, self.frontSprites)
        spaceSpr = self.getSpaceSprite(spaceBlock)

        if spaceSpr:
            blockSpr.rect.center = spaceSpr.rect.center

    def getSpaceSprite(self, space):
        for s in self.backSprites:
            if hasattr(s, "space") and s.space == space:
                return s
        return None

    def draw(self):
        self.backSprites.clear(self.window, self.background)
        self.frontSprites.clear(self.window, self.background)

        self.backSprites.update()
        self.frontSprites.update()

        dirtyRects1 = self.backSprites.draw(self.window)
        dirtyRects2 = self.frontSprites.draw(self.window)

        dirtyRects = dirtyRects1 + dirtyRects2
        pygame.display.update(dirtyRects)

    def notify(self, event):
        if isinstance(event, events.MiniBoardBuiltEvent):
            if event.boardName == PREVIEW:
                self.showPreviewPane(event.board)

        elif isinstance(event, events.ShapeAddedEvent):
            self.frontSprites.empty()
            for block in event.nextShape.blocks:
                self.showBlock(block, event.nextShape.color)

