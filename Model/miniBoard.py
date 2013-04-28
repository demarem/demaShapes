import space
import events
from constants import *

class MiniBoard:

    def __init__(self, eventManager, name):
        self.eventManager = eventManager
        self.name = name

        self.startIndex = 0
        self.spaces = []

    def build(self):
        '''
        [[shape shape shape ...]
        [shape shape ...]
        [shape shape ...]]
        '''

        for i in range(SHAPETYPES.TEMPLATEHEIGHT):
            row = []
            for j in range(SHAPETYPES.TEMPLATEWIDTH):
                row.append(space.Space(self.eventManager))
            self.spaces.append(row)

        event = events.MiniBoardBuiltEvent(self, self.name)
        self.eventManager.post(event)
