import shape
import events
from constants import *

class Player(object):
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.name = ""

        self.activeShape = None
        self.inactiveBlocks = []
        self.board = None
        self.score = None  # TODO

    def __str__(self):
        return '<Player %s %s>' % (self.name, id(self))

    def start(self):
        self.activeShape = shape.Shape(self.eventManager, \
                                       SHAPETYPES.getRandomShape(), \
                                       self.board)
        self.eventManager.post(events.ShapeAddedEvent(self.activeShape))

    def shapePlaced(self, oldShape):
        for block in oldShape.blocks:
            self.inactiveBlocks.append(block)
        self.activeShape = shape.Shape(self.eventManager, \
                                       SHAPETYPES.getRandomShape(), \
                                       self.board)
        self.eventManager.post(events.ShapeAddedEvent(self.activeShape))

    def clearLines(self, rows):
        spacesToClear = [space for row in rows for space in self.board.spaces[row]]
        self.inactiveBlocks = [block for block in self.inactiveBlocks
                                if block.space not in spacesToClear]

        event = events.BoardChanged(self.activeShape.blocks, self.inactiveBlocks)
        self.eventManager.post(event)

        self.shiftLinesDown(rows)

    def shiftLinesDown(self, rows):
        numberOfShifts = 0
        for i in reversed(range(HEIGHT)):
            if rows and i == max(rows):
                numberOfShifts += 1
                rows.remove(max(rows))
            blocksInRow = [block for block in self.inactiveBlocks if block.space
                           in self.board.spaces[i]]
            for block in blocksInRow:
                for j in range(numberOfShifts):
                    block.move(DIRECTION_DOWN)

        event = events.BoardChanged(self.activeShape.blocks, self.inactiveBlocks)
        self.eventManager.post(event)

    def notify(self, event):
        if isinstance(event, events.GameStartedEvent):
            self.board = event.game.board
            self.start()

        elif isinstance(event, events.ShapePlacedEvent):
            self.shapePlaced(event.shape)

        elif isinstance(event, events.ClearedBlocksEvent):
            self.clearLines(event.rows)


