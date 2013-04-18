from constants import *
from time import time
import events

class MoveDetector:

    STATE_MOVING = 0
    STATE_NOT_MOVING = 1

    def __init__(self, player, board, eventManager):

        self.eventManager = eventManager
        self.eventManager.registerListener(self)

        self.state = MoveDetector.STATE_NOT_MOVING
        self.currentDirection = None
        self.player = player
        self.board = board
        self.lastRepeat = time()

    def tryMove(self, direction):
        currentShape = self.player.activeShape
        result = currentShape.move(direction)

        if result == False:
            return False

        for placedBlock in self.player.inactiveBlocks:
            for activeBlock in currentShape.blocks:
                if activeBlock.space == placedBlock.space:
                    return False
        return True

    def fallResponse(self):
        moveSuccessful = self.tryMove(DIRECTION_DOWN)
        if not moveSuccessful:
            currentShape = self.player.activeShape
            currentShape.unmove()
            event = events.ShapePlacedEvent(currentShape)
            self.eventManager.post(event)

        event = events.BoardChanged(self.player.activeShape.blocks,
                                    self.player.inactiveBlocks)
        self.eventManager.post(event)

    def moveResponse(self, direction):
        moveSuccessful = self.tryMove(direction)
        if not moveSuccessful:
            currentShape = self.player.activeShape
            currentShape.unmove()

        event = events.BoardChanged(self.player.activeShape.blocks,
                                    self.player.inactiveBlocks)
        self.eventManager.post(event)

    def dropShape(self):
        moveSuccessful = self.tryMove(DIRECTION_DOWN)
        while moveSuccessful:
            moveSuccessful = self.tryMove(DIRECTION_DOWN)

        currentShape = self.player.activeShape
        currentShape.unmove()
        event = events.ShapePlacedEvent(currentShape)
        self.eventManager.post(event)

        event = events.BoardChanged(self.player.activeShape.blocks,
                                    self.player.inactiveBlocks)
        self.eventManager.post(event)


    def notify(self, event):
        if isinstance(event, events.ShapeStartMoveRequest):
            self.moveResponse(event.direction)
            self.state = MoveDetector.STATE_MOVING
            self.currentDirection = event.direction
            self.lastRepeat = time()

        elif isinstance(event, events.ShapeStopMoveRequest):
            self.state = MoveDetector.STATE_NOT_MOVING

        elif isinstance(event, events.TickEvent):
            if self.state == MoveDetector.STATE_MOVING and \
                    time() - self.lastRepeat > KEYREPEAT:
                self.lastRepeat = time()
                self.moveResponse(self.currentDirection)

        elif isinstance(event, events.ShapeRotateRequest):
            self.moveResponse(event.direction)

        elif isinstance(event, events.ShapeFallEvent):
            self.fallResponse()

        elif isinstance(event, events.ShapeDropRequest):
            self.dropShape()
