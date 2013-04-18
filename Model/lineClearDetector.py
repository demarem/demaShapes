import events

class LineClearDetector:
    def __init__(self, board, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.board = board

    def checkLines(self, blocks):
        fullRows = []
        for i in range(len(self.board.spaces)):
            row = self.board.spaces[i]
            if set(row).issubset(set([block.space for block in blocks])):
                fullRows.append(i)

        if len(fullRows) > 0:
            event = events.ClearedBlocksEvent(fullRows)
            self.eventManager.post(event)

    def notify(self, event):
        if isinstance(event, events.BoardChanged):
            self.checkLines(event.inactiveBlocks)
