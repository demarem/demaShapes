import pygame, sys
from pygame.locals import *
from standardShapes import standardShapes

#### GLITCHES ####
# 1) Removing > 2 rows leaves blanks
##################

#### FEATURES ####
# 3) gameover when top is reached
# 4) preview next piece
# 5) reserve?
# 6) speedup (levels), increase score?
##################

PIECES = standardShapes

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLOCKSIZE = 20  # pixels
BOARDWIDTH = 10 * BLOCKSIZE
BOARDHEIGHT = 20 * BLOCKSIZE
SCOREWIDTH = 125
SCOREHEIGHT = 100
XMARG = int((WINDOWWIDTH / 2) - (BOARDWIDTH / 2))
YMARG = int((WINDOWHEIGHT / 2) - (BOARDHEIGHT / 2))
PLAYRECT = pygame.Rect(XMARG, YMARG, BOARDWIDTH, BOARDHEIGHT)
SCORERECT = pygame.Rect(WINDOWWIDTH - (XMARG / 2) - (SCOREWIDTH / 2), YMARG,
                         SCOREWIDTH, SCOREHEIGHT)
LEVELRECT = SCORERECT.move(0, 100)
STARTPOS = (WINDOWWIDTH / 2, 0)

# timing constants
DROPDELAY = 1000  # 1 seconds
DROPEVENT = USEREVENT + 1  # signals the time to drop a block
KEY_REPEAT_DELAY = 5
KEY_REPEAT_INTERVAL = 50

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTYELLOW = (175, 175, 20)
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
PLAYRECTCOLOR = WHITE
SCOREWRITINGCOLOR = LIGHTYELLOW
SCORECOLOR = GRAY
SCORING = {0: 0, 1: 100, 2: 200, 3: 400, 4: 800}

# scores = (numLines, numPts)
scores = [0, 0]

def main():
    global DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('DemaBlocks')

    DISPLAYSURF.fill(BGCOLOR)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 14)
    activeShape = makeShape(PIECES.getRandomShape())

    # completed box set
    completedBlocks = []

    # Start drop timer
    pygame.time.set_timer(DROPEVENT, DROPDELAY)

    # Key repeat speed
    pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

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
                    # Key repeat speed
                    pygame.key.set_repeat(1000, 1000)
                    # rotate right
                    activeShape = tryRotate(activeShape, completedBlocks)
                elif event.key == K_RSHIFT:
                    # Key repeat speed
                    pygame.key.set_repeat(1000, 1000)
                    activeShape = tryRotate(activeShape, completedBlocks, False)
                elif event.key == K_SPACE:
                    # Key repeat speed
                    pygame.key.set_repeat(1000, 1000)
                    activeShape = toBottom(activeShape, completedBlocks)
            elif event.type == KEYUP:
                # Key repeat speed
                pygame.key.set_repeat(5, 50)
            elif event.type == DROPEVENT:
                tempShape = dropShape(activeShape, completedBlocks)  # drops or sticks block (none)
                print activeShape['topLeft']
                if tempShape == None:
                    for block in activeShape['blocks']:
                        completedBlocks.append((block, activeShape['color']))
                    activeShape = tempShape
                    # check for cleared lines
                    completedBlocks = clearLines(completedBlocks)
                else:
                    activeShape = tempShape
                pygame.time.set_timer(DROPEVENT, DROPDELAY)

            # Allocate new block
            if activeShape == None:
                activeShape = makeShape(PIECES.getRandomShape())

        DISPLAYSURF.fill(BGCOLOR)
        pygame.draw.rect(DISPLAYSURF, PLAYRECTCOLOR, PLAYRECT)
        pygame.draw.rect(DISPLAYSURF, SCORECOLOR, SCORERECT)
        displayScore(scores, BASICFONT)
        displayActiveBlock(activeShape)
        displayCompletedBlocks(completedBlocks)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def newBlock(POS):
    rect = pygame.Rect(POS, (BLOCKSIZE, BLOCKSIZE))
    return rect


def displayScore(scores, BASICFONT):
    string = "\n SCORE:\n                  " + str(scores[1]) + "\n\n LINES:\n                  " + str(scores[0])

    scoreSurfaceObj = renderTextBlock(string, BASICFONT, True, LIGHTYELLOW)
    DISPLAYSURF.blit(scoreSurfaceObj, SCORERECT)



def renderLines(lines, font, antialias, color, background=None):
    fontHeight = font.get_height()

    surfaces = [font.render(ln, antialias, color) for ln in lines]
    # can't pass background to font.render, because it doesn't respect the alpha

    maxwidth = max([s.get_width() for s in surfaces])
    result = pygame.Surface((maxwidth, len(lines) * fontHeight), pygame.SRCALPHA)
    if background == None:
        result.fill((90, 90, 90, 0))
    else:
        result.fill(background)

    for i in range(len(lines)):
        result.blit(surfaces[i], (0, i * fontHeight))
    return result


def renderTextBlock(text, font, antialias, color, background=None):
    "This is renderTextBlock"
    brokenText = text.replace("\r\n", "\n").replace("\r", "\n")
    return renderLines(brokenText.split("\n"), font, antialias, color, background)
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
            if pos != EMPTY:
                testBlocks.append(pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE))
            x += BLOCKSIZE
        y += BLOCKSIZE

    # this could probably be abstracted out to a collisions function
    for testBlock in testBlocks:
        if not PLAYRECT.contains(testBlock):
            return activeShape
        else:
            for completedBlock in completedBlocks:
                for testBlock in testBlocks:
                    # this might be colliding too soon, not allowing touching
                    if completedBlock[0].colliderect(testBlock):
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
        if not PLAYRECT.contains(testBlock):
            return activeShape
        else:
            for completedBlock in completedBlocks:
                for testBlock in testBlocks:
                    if completedBlock[0].colliderect(testBlock):
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
            if (not PLAYRECT.contains(testBlock)):
                    isCollision = True
            for completedBlock in completedBlocks:
                if completedBlock[0].colliderect(testBlock):
                    isCollision = True
        if isCollision == False:
            blocks = testBlocks
            activeShape['topLeft'] = (pos[0], pos[1] + BLOCKSIZE)
            testBlocks = []
            assert pos[1] < 10000, "Problem...."
    print "toBottom: " + str(activeShape['topLeft'])
    activeShape['blocks'] = blocks
    return activeShape


def dropShape(activeShape, completedBlocks):

    # shift all blocks down
    blocks = activeShape['blocks']
    testBlocks = []
    for block in blocks:
        testBlocks.append(block.move(0, BLOCKSIZE))

    for completedBlock in completedBlocks:
        for testBlock in testBlocks:
            if testBlock.colliderect(completedBlock[0]):
                return None

    for testBlock in testBlocks:
        if not PLAYRECT.contains(testBlock):
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
    for completedBlock in completedBlocks:
        pygame.draw.rect(DISPLAYSURF, completedBlock[1], completedBlock[0])


def makeShape(shape):
    newShape = {'type': shape, 'configuration': 0,
                'color': PIECES.getColor(shape),
                'topLeft': (XMARG + LEFTGAP, YMARG), 'blocks': None}
    blocks = []
    y = YMARG
    for row in PIECES.getTemplate(shape, 0):
        x = XMARG + LEFTGAP
        for pos in row:
            if pos != EMPTY:
                blocks.append(pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE))
            x += BLOCKSIZE
        y += BLOCKSIZE
    newShape['blocks'] = blocks
    return newShape


def clearLines(completedBlocks):
    global scores
    rowCounts = [0] * 20  # watch out here for aliasing
    absTop = PLAYRECT.top
    # count rows
    for completedBlock in completedBlocks:
        row = (completedBlock[0].top - absTop) / BLOCKSIZE
        rowCounts[row] += 1

    # determine full rows
    fullRows = []
    for i in range(len(rowCounts)):
        if rowCounts[i] == 10:
            fullRows.append(i)

    # calculate score
    scores[0] += len(fullRows)
    scores[1] += SCORING[len(fullRows)]

    fullRows.sort(reverse=True)
    print 'fullrows: ' + str(fullRows)

    # get list of remaining rows
    remainingBlocks = []
    for completedBlock in completedBlocks:
        if (completedBlock[0].top - absTop) / BLOCKSIZE not in fullRows:
            remainingBlocks.append(completedBlock)

    completedBlocks = []
    for remainingBlock in remainingBlocks:
        for fullRow in fullRows:
            if (remainingBlock[0].top - absTop) / BLOCKSIZE <= fullRow:
                print 'here'
                remainingBlock = (remainingBlock[0].move(0, BLOCKSIZE),
                                  remainingBlock[1])
        completedBlocks.append(remainingBlock)

    print rowCounts
    print 'Total Lines: ' + str(scores[0])
    print 'Total Points: ' + str(scores[1])

    return completedBlocks

if __name__ == '__main__':
    main()
