import standardShapes as shapes
# import testingShapes as shapes

SHAPETYPES = shapes.StandardShapes()

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
BLACK = (0, 0, 0)

FPS = 30

WINDOWCOLOR = BLACK
BLOCKCOLOR = GREEN

DIRECTION_DOWN = 0
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
ROTATE_RIGHT = 4
ROTATE_LEFT = 5

KEYREPEAT = 0.1

BLOCKSIZE = 20
WIDTH = 10
HEIGHT = 20

WINDOWWIDTH = 640
WINDOWHEIGHT = 480

BOARDTOP = 30
BOARDLEFT = WINDOWWIDTH / 4
BOARDER = 10

PREVIEWWIDTH = SHAPETYPES.TEMPLATEWIDTH * BLOCKSIZE
PREVIEWHEIGHT = SHAPETYPES.TEMPLATEHEIGHT * BLOCKSIZE
PREVIEWTOP = 100
PREVIEWLEFT = BOARDLEFT + (WIDTH * BLOCKSIZE) + 50

OPPOSITE = {DIRECTION_DOWN: DIRECTION_UP,
            DIRECTION_UP: DIRECTION_DOWN,
            DIRECTION_LEFT: DIRECTION_RIGHT,
            DIRECTION_RIGHT: DIRECTION_LEFT,
            ROTATE_RIGHT: ROTATE_LEFT,
            ROTATE_LEFT: ROTATE_RIGHT}

PREVIEW = 0
HOLD = 1
