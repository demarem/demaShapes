import events
from constants import *
import block

class Shape:
    def __init__(self, eventManager, shapeType, board):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.blocks = []
        self.board = board

        self.shapeType = shapeType
        self.shapeTemplates = SHAPETYPES.getTemplate(shapeType)
        self.color = SHAPETYPES.getColor(shapeType)
        self.shapeNumber = 0

        self.topLeft = None

        self.lastDirection = None
        self.spawn(board)

    def __str__(self):
        return '<Shape %s>' % id(self)

    def shift(self, direction):
        if direction == DIRECTION_LEFT:
            self.topLeft = (self.topLeft[0] - 1, self.topLeft[1])
        elif direction == DIRECTION_RIGHT:
            self.topLeft = (self.topLeft[0] + 1, self.topLeft[1])
        else:
            self.topLeft = (self.topLeft[0], self.topLeft[1] + 1)
        for b in self.blocks:
            b.move(direction)

    def _nextTemplate(self, rotateDirection):
        shapeNumber = self.shapeNumber
        if rotateDirection == ROTATE_RIGHT:
            shapeNumber += 1
            if shapeNumber >= len(self.shapeTemplates):
                shapeNumber = 0
        else:
            shapeNumber -= 1
            if shapeNumber < 0:
                shapeNumber = len(self.shapeTemplates) - 1
        return shapeNumber

    def rotate(self, direction):
        ''' returns false if the rotation is not possible due to board border
        and was ignored '''

        self.shapeNumber = self._nextTemplate(direction)
        template = self.shapeTemplates[self.shapeNumber]
        savedBlocks = self.blocks
        self.blocks = []
        for i in range(len(template)):
            for j in range(SHAPETYPES.TEMPLATEWIDTH):
                if template[i][j] != SHAPETYPES.EMPTY:
                    if 0 <= i + self.topLeft[1] < HEIGHT and \
                            0 <= j + self.topLeft[0] < WIDTH:
                        newBlock = block.Block(self.eventManager, self.color)
                        newBlock.place(self.board.spaces[i + self.topLeft[1]][j + self.topLeft[0]])
                        self.blocks.append(newBlock)
                    else:
                        self.blocks = savedBlocks
                        return False

        return True

    def move(self, direction):
        if direction in {DIRECTION_UP, DIRECTION_DOWN,
                         DIRECTION_LEFT, DIRECTION_RIGHT}:
            if self._movePossible(direction):
                self.shift(direction)
                self.lastDirection = direction
                return True
            else:
                self.lastDirection = None
                return False
        else:
            result = self.rotate(direction)
            if result:
                self.lastDirection = direction
                return True
            else:
                self.lastDirection = None
                return False

    def unmove(self):
        if self.lastDirection != None:
            direction = OPPOSITE[self.lastDirection]
            for b in self.blocks:
                b.move(direction)
            self.lastDirection = None

    def spawn(self, board):
        index = board.startIndex
        self.topLeft = (index, 0)
        template = self.shapeTemplates[0]
        for i in range(len(template)):
            for j in range(SHAPETYPES.TEMPLATEWIDTH):
                if template[i][j] != SHAPETYPES.EMPTY:
                    newBlock = block.Block(self.eventManager, self.color)
                    newBlock.place(board.spaces[i - 1][index + j])
                    self.blocks.append(newBlock)

    def _movePossible(self, direction):
        for b in self.blocks:
            if not b.space.movePossible(direction):
                return False
        return True

    def notify(self, event):
        if isinstance(event, events.ShapeAddedEvent):
            if event.newShape == self:
                self.board = event.toBoard
                self.blocks = []
                self.spawn(self.board)
