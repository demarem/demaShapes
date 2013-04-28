from constants import *

class Block:

    def __init__(self, eventManager, color):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.space = None
        self.direction = None
        self.color = color

    def __str__(self):
        return '<Block %s>' % id(self)

    def move(self, direction):
        self.space = self.space.neighbors[direction]

    def place(self, space):
        self.space = space

    def notify(self, event):
        pass
