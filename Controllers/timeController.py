from time import time
import events

class TimeController:
    '''Signals time based events.'''
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)
        self.lastTime = time()
        self.dropRate = 2.0

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            currentTime = time()
            if currentTime - self.lastTime > self.dropRate:
                self.lastTime = currentTime
                self.eventManager.post(events.ShapeFallEvent())

