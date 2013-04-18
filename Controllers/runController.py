import events

class RunController:
    '''...'''
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.registerListener(self)

        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            event = events.TickEvent()
            self.evManager.post(event)

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            # this stops the while loop from running
            self.keepGoing = False
