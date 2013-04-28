import random

random.seed()
class TestingShapes:

    # template values
    EMPTY = '.'
    BLOCK = 'O'
    TEMPLATEWIDTH = 5
    TEMPLATEHEIGHT = 5

    # block shapes
    I = 'I'
    O = 'O'

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
    O_TEMPLATE = [['.....',
                   '..OO.',
                   '..OO.',
                   '.....',
                   '.....']]

    SHAPES = [I, O]
    TEMPLATES = {I: I_TEMPLATE, O: O_TEMPLATE}

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

    SHAPECOLORS = {I: ORANGE, O: GRAY}

    def __init__(self):
        self = None

    def getRandomShape(self):
        # all shapes
        return random.choice(TestingShapes.SHAPES)

    def getColor(self, shapeType):
        return TestingShapes.SHAPECOLORS[shapeType]

    def getTemplate(self, shapeType, configuration=None):
        if configuration == None:
            return TestingShapes.TEMPLATES[shapeType]
        else:
            return TestingShapes.TEMPLATES[shapeType][configuration]
