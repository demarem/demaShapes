import pygame
from pygame.locals import *
from constants import *
import spaceSprite
import blockSprite
import events

class BoardView:
    def __init__(self, eventManager, window, background):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.background = background
        self.window = window
        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()
        self.boardRect = None

    def showBoard(self, board):
        squareRect = pygame.Rect(BOARDLEFT, BOARDTOP, BLOCKSIZE, BLOCKSIZE)

        column = 0
        for row in board.spaces:
            for space in row:
                if column < WIDTH:
                    squareRect = squareRect.move(BLOCKSIZE, 0)
                else:
                    column = 0
                    squareRect = squareRect.move(-(BLOCKSIZE * (WIDTH - 1)), BLOCKSIZE)
                column += 1
                newSprite = spaceSprite.SpaceSprite(space, self.backSprites)
                newSprite.rect = squareRect
                if self.boardRect == None:
                    self.boardRect = pygame.Rect(newSprite.rect)
                self.boardRect = newSprite.rect.union(self.boardRect)
                newSprite = None

        self.boardRect = self.boardRect.inflate(BOARDER, BOARDER)
        pygame.draw.rect(self.window, GREEN, self.boardRect)

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
        if isinstance(event, events.BoardBuiltEvent):
            board = event.board
            self.showBoard(board)

        elif isinstance(event, events.BoardChanged):
            self.frontSprites.empty()
            for block in event.activeBlocks + event.inactiveBlocks:
                self.showBlock(block, block.color)

        elif isinstance(event, events.ShapeAddedEvent):
            for block in event.newShape.blocks:
                self.showBlock(block, block.color)
