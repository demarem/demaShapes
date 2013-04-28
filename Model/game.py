import player
import board
import events
import moveDetector
import lineClearDetector
import miniBoard
from constants import *

class Game:

    STATE_PREPARING = 'preparing'
    STATE_RUNNING = 'running'
    STATE_PAUSED = 'paused'

    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.state = Game.STATE_PREPARING

        self.players = [player.Player(eventManager)]
        self.board = board.Board(eventManager)
        self.previewBoard = miniBoard.MiniBoard(eventManager, PREVIEW)

        self.moveDetector = None
        self.lineClearDetector = None

    def start(self):
        self.board.build()
        self.previewBoard.build()
        self.state = Game.STATE_RUNNING
        self.moveDetector = moveDetector. \
            MoveDetector(self.players[0], self.board, self.eventManager)
        self.lineClearDetector = lineClearDetector. \
            LineClearDetector(self.board, self.eventManager)
        event = events.GameStartedEvent(self)
        self.eventManager.post(event)

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            if self.state == Game.STATE_PREPARING:
                self.start()

        elif isinstance(event, events.BoardChanged):
            pass
            self.board.printBoard(self.players[0].activeShape.blocks,
                                  self.players[0].inactiveBlocks)
            # print self.players[0].activeShape.topLeft
