import space
import events
from constants import *

class Board:

    def __init__(self, eventManager):
        self.eventManager = eventManager
        # self.eventManager.registerListener(self)

        self.spaces = []
        self.startIndex = 3  # top middle of board

    def build(self):
        '''
        [[shape shape shape ...]
        [shape shape ...]
        [shape shape ...]]
        '''

        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                row.append(space.Space(self.eventManager))
            self.spaces.append(row)


        # assign left and right neighbors
        for i in range(HEIGHT):
            for j in range(WIDTH - 1):
                self.spaces[i][j].neighbors[DIRECTION_RIGHT] = self.spaces[i][j + 1]
                self.spaces[i][j + 1].neighbors[DIRECTION_LEFT] = self.spaces[i][j]

        for i in range(HEIGHT - 1):
            for j in range(WIDTH):
                self.spaces[i][j].neighbors[DIRECTION_DOWN] = \
                    self.spaces[i + 1][j]
                self.spaces[i + 1][j].neighbors[DIRECTION_UP] = \
                    self.spaces[i][j]

        event = events.BoardBuiltEvent(self)
        self.eventManager.post(event)

    def printBoard(self, activeBlocks, inactiveBlocks):
        print '\n'
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.spaces[i][j] in [block.space for block in activeBlocks]:
                    print "X",
                elif self.spaces[i][j] in [block.space for block in inactiveBlocks]:
                    print "I",
                else:
                    print "O",
            print ''
        print '\n\n'
