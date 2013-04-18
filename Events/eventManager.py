import events

# Point of control for debugging
def debug(msg):
    print msg

class EventManager:
    '''This object is responsible for the coordinating most communication
    between the Model, View, and Controller.'''
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []

    def registerListener(self, listener):
        self.listeners[listener] = 1

    def unregisterListener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    def post(self, event):
        if not isinstance(event, events.TickEvent):
            debug("    Message: " + event.name)
        for listener in self.listeners.keys():
            listener.notify(event)
