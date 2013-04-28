from time import time
import events

class TimeController:
    STATE_RUNNING = 'running'
    STATE_PAUSED = 'paused'

    '''Signals time based events.'''
    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)
        self.lastTime = time()
        self.dropRate = 2.0
        self.state = TimeController.STATE_PAUSED

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            if self.state == TimeController.STATE_RUNNING:
                currentTime = time()
                if currentTime - self.lastTime > self.dropRate:
                    self.lastTime = currentTime
                    self.eventManager.post(events.ShapeFallEvent())

        elif isinstance(event, events.GameOverEvent):
            self.state = TimeController.STATE_PAUSED

        elif isinstance(event, events.GameStartedEvent) or \
                isinstance(event, events.ResetEvent):
            self.state = TimeController.STATE_RUNNING


