import standardShapes as shapes

SHAPETYPES = shapes.StandardShapes()

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

BOARDTOP = 0
BOARDLEFT = 0

OPPOSITE = {DIRECTION_DOWN: DIRECTION_UP,
            DIRECTION_UP: DIRECTION_DOWN,
            DIRECTION_LEFT: DIRECTION_RIGHT,
            DIRECTION_RIGHT: DIRECTION_LEFT,
            ROTATE_RIGHT: ROTATE_LEFT,
            ROTATE_LEFT: ROTATE_RIGHT}
