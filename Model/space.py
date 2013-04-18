from constants import *

class Space:
    def __init__(self, eventManager):
        self.eventManager = eventManager
        # self.eventManager.registerListener(self)

        self.neighbors = range(4)

        self.neighbors[DIRECTION_UP] = None
        self.neighbors[DIRECTION_DOWN] = None
        self.neighbors[DIRECTION_LEFT] = None
        self.neighbors[DIRECTION_RIGHT] = None

    def movePossible(self, direction):
        if self.neighbors[direction]:
            return True
        return False
