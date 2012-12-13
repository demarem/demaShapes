import random

random.seed()

# block shapes
I = 'I'


I_TEMPLATE = [['.....',
               'OOOO.',
               '.....',
               '.....',
               '.....'],
             ['..O..',
              '..O..',
              '..O..',
              '..O..',
              '.....']]

SHAPES = [I]
TEMPLATES = {I: I_TEMPLATE}

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

SHAPECOLORS = {I: ORANGE}


class testingShapes:
    def __init__(self):
        self = None

    @staticmethod
    def getRandomShape():
        # all shapes
        return random.choice(SHAPES)

    @staticmethod
    def getColor(shapeType):
        return SHAPECOLORS[shapeType]

    @staticmethod
    def getTemplate(shapeType, configuration=None):
        if configuration == None:
            return TEMPLATES[shapeType]
        else:
            return TEMPLATES[shapeType][configuration]
