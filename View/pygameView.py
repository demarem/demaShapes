import pygame
from pygame.locals import *
from constants import *
import spaceSprite
import blockSprite
import events

class PygameView:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('DemaShapes')

        # pylint: disable-msg=E1121
        self.background = pygame.Surface(self.window.get_size())
        # pylint: enable-msg=E1121

        self.background.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = """L O A D I N G . . ."""
        textImg = font.render(text, 1, (255, 0, 0))
        self.background.blit(textImg, (0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()

    def showBoard(self, board):
        # clear screen
        self.background.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

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
                newSprite = None

    def showBlock(self, block):
        spaceBlock = block.space
        blockSpr = blockSprite.BlockSprite(block, self.frontSprites)
        spaceSpr = self.getSpaceSprite(spaceBlock)

        if spaceSpr:
            blockSpr.rect.center = spaceSpr.rect.center

    def moveBlock(self, block):
        blockSpr = self.getBlockSprite(block)
        space = block.space
        spaceSpr = self.getSpaceSprite(space)

        if spaceSpr and blockSpr:
            blockSpr.moveTo = spaceSpr.rect.center

    def getBlockSprite(self, block):
        for s in self.frontSprites:
            if hasattr(s, "block") and s.block == block:
                return s
        return None

    def getSpaceSprite(self, space):
        for s in self.backSprites:
            if hasattr(s, "space") and s.space == space:
                return s
        return None

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            # Draw Everything
            self.backSprites.clear(self.window, self.background)
            self.frontSprites.clear(self.window, self.background)

            self.backSprites.update()
            self.frontSprites.update()

            dirtyRects1 = self.backSprites.draw(self.window)
            dirtyRects2 = self.frontSprites.draw(self.window)

            dirtyRects = dirtyRects1 + dirtyRects2
            pygame.display.update(dirtyRects)

        elif isinstance(event, events.BoardBuiltEvent):
            board = event.board
            self.showBoard(board)

        elif isinstance(event, events.BoardChanged):
            self.frontSprites.empty()
            for block in event.activeBlocks + event.inactiveBlocks:
                self.showBlock(block)

        elif isinstance(event, events.ShapeAddedEvent):
            for block in event.shape.blocks:
                self.showBlock(block)

