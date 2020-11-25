from pygame.math import Vector2 as vec

# screen settings
FPS = 60
TOP_BOTTOM_BUFFER = 100
#WIDTH, HEIGHT = 610, 670
WIDTH, HEIGHT = 1220, 1340
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER

# color settings
BLACK = (0, 0, 0)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOR = (190, 194, 15)
RED = (208, 22, 22)

# font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# player settings
STARTING_POS = vec(1, 1)

# mod settings
