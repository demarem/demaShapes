import pygame, sys
from pygame.locals import *
from standardShapes import standardShapes

#### GLITCHES ####
# 1) edge collisions
##################

#### FEATURES ####
# 1) Add key repeat
# 2)
##################

PIECES = standardShapes

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
WINDOWRECT = pygame.Rect(0, 0, 640, 480)
FPS = 30
BLOCKSIZE = 20  # pixels
BOARDWIDTH = 10 * BLOCKSIZE
BOARDHEIGHT = 20 * BLOCKSIZE
MARG = int((WINDOWWIDTH / 2) - (BOARDWIDTH / 2))
STARTPOS = (WINDOWWIDTH / 2, 0)
DELAY = 1000  # .1 seconds
DROPEVENT = USEREVENT + 1  # signals the time to drop a block

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5
LEFTGAP = 3 * BLOCKSIZE
RIGHTGAP = 2 * BLOCKSIZE

EMPTY = '.'
BLOCK = 'O'

BGCOLOR = NAVYBLUE
BLOCKCOLOR = WHITE


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('DemaBlocks')

    DISPLAYSURF.fill(BGCOLOR)

    activeShape = makeShape(PIECES.getRandomShape())

    # completed box set
    completedBlocks = []

    # Start drop timer
    pygame.time.set_timer(DROPEVENT, DELAY)

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                print "--QUITTING--"
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_RIGHT, K_DOWN):
                    activeShape = moveBlock(event.key, activeShape, completedBlocks)
                elif event.key == K_UP:
                    # rotate right
                    activeShape = tryRotate(activeShape, completedBlocks)
                elif event.key == K_RSHIFT:
                    activeShape = tryRotate(activeShape, completedBlocks, False)
                elif event.key == K_SPACE:
                    activeShape = toBottom(activeShape, completedBlocks)
            elif event.type == DROPEVENT:
                tempShape = dropShape(activeShape, completedBlocks)  # drops or sticks block (none)
                if tempShape == None:
                    for block in activeShape['blocks']:
                        completedBlocks.append(block)
                    activeShape = tempShape
                else:
                    activeShape = tempShape
                pygame.time.set_timer(DROPEVENT, DELAY)

            # Allocate new block
            if activeShape == None:
                activeShape = makeShape(PIECES.getRandomShape())

            print activeShape['topLeft']

        DISPLAYSURF.fill(BGCOLOR)
        displayActiveBlock(activeShape)
        displayCompletedBlocks(completedBlocks)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def newBlock(POS):
    rect = pygame.Rect(POS, (BLOCKSIZE, BLOCKSIZE))
    return rect


def tryRotate(activeShape, completedBlocks, isRightRotate=True):
    shapeType = activeShape['type']
    shapeTemplates = PIECES.getTemplate(shapeType)  # TEMPLATES[shapeType]
    numTemplates = len(shapeTemplates)

    if isRightRotate:
        nextTemplate = activeShape['configuration'] + 1
        # reset the template if next configuration > total configurations
        if numTemplates <= nextTemplate:
            nextTemplate = 0
    else:
        nextTemplate = activeShape['configuration'] - 1
        # reset the template if next configuration < 0
        if nextTemplate < 0:
            nextTemplate = numTemplates - 1

    topLeft = activeShape['topLeft']
    testBlocks = []
    y = topLeft[1]
    for row in shapeTemplates[nextTemplate]:
        x = topLeft[0]
        for pos in row:
            if pos == EMPTY:
                x += 1
            else:
                testBlocks.append(pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE))
            x += BLOCKSIZE
        y += BLOCKSIZE

    # this could probably be abstracted out to a collisions function
    for testBlock in testBlocks:
        if not WINDOWRECT.contains(testBlock):
            return activeShape
        else:
            for completedBlock in completedBlocks:
                for testBlock in testBlocks:
                    # this might be colliding too soon, not allowing touching
                    if completedBlock.colliderect(testBlock):
                        return activeShape
    activeShape['blocks'] = testBlocks
    activeShape['configuration'] = nextTemplate
    return activeShape


def moveBlock(keystroke, activeShape, completedBlocks):
    blocks = activeShape['blocks']
    testBlocks = []
    testPos = activeShape['topLeft']
    if keystroke == K_LEFT:
        for block in blocks:
            testBlocks.append(block.move(-1 * BLOCKSIZE, 0))
        testPos = (testPos[0] - BLOCKSIZE, testPos[1])
    elif keystroke == K_RIGHT:
        for block in blocks:
            testBlocks.append(block.move(BLOCKSIZE, 0))
        testPos = (testPos[0] + BLOCKSIZE, testPos[1])
    elif keystroke == K_DOWN:
        for block in blocks:
            testBlocks.append(block.move(0, BLOCKSIZE))
        testPos = (testPos[0], testPos[1] + BLOCKSIZE)

    for testBlock in testBlocks:
        if not WINDOWRECT.contains(testBlock):
            return activeShape
        else:
            for completedBlock in completedBlocks:
                for testBlock in testBlocks:
                    if completedBlock.colliderect(testBlock):
                        return activeShape
    activeShape['blocks'] = testBlocks
    activeShape['topLeft'] = testPos
    return activeShape


def toBottom(activeShape, completedBlocks):
    blocks = activeShape['blocks']
    testBlocks = []
    isCollision = False
    while not isCollision:
        pos = activeShape['topLeft']
        for block in blocks:
            testBlocks.append(block.move(0, BLOCKSIZE))
        for testBlock in testBlocks:
            if (not WINDOWRECT.contains(testBlock)):  # completedBlock.colliderect(testBlock):
                    isCollision = True
            for completedBlock in completedBlocks:
                if completedBlock.colliderect(testBlock):
                    isCollision = True
        if isCollision == False:
            blocks = testBlocks
            activeShape['topLeft'] = (pos[0], pos[1] + BLOCKSIZE)
            testBlocks = []
            print "toBottom: " + str(activeShape['topLeft'])
            assert pos[1] < 10000, "Problem...."
    activeShape['blocks'] = blocks
    return activeShape


def dropShape(activeShape, completedBlocks):

    # shift all blocks down
    blocks = activeShape['blocks']
    testBlocks = []
    for block in blocks:
        testBlocks.append(block.move(0, BLOCKSIZE))

    for block in completedBlocks:
        for testBlock in testBlocks:
            if testBlock.colliderect(block):
                return None

    for testBlock in testBlocks:
        if not WINDOWRECT.contains(testBlock):
            return None

    activeShape['blocks'] = testBlocks
    oldPos = activeShape['topLeft']
    activeShape['topLeft'] = (oldPos[0], oldPos[1] + BLOCKSIZE)
    return activeShape


def displayActiveBlock(activeShape):
    blocks = activeShape['blocks']
    color = activeShape['color']
    for block in blocks:
        pygame.draw.rect(DISPLAYSURF, color, block)


def displayCompletedBlocks(completedBlocks):
    for block in completedBlocks:
        pygame.draw.rect(DISPLAYSURF, BLOCKCOLOR, block)


def makeShape(shape):
    newShape = {'type': shape, 'configuration': 0,
                'color': PIECES.getColor(shape),
                'topLeft': (MARG + LEFTGAP, 0), 'blocks': None}
    blocks = []
    y = 0
    for row in PIECES.getTemplate(shape, 0):
        x = MARG + LEFTGAP
        for pos in row:
            if pos == EMPTY:
                x += 1
            else:
                blocks.append(pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE))
            x += BLOCKSIZE
        y += BLOCKSIZE
    newShape['blocks'] = blocks
    return newShape

if __name__ == '__main__':
    main()

