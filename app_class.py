import pygame
import sys
from settings import *
from player_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        # Initial variables for the game screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        # Variables for the size of the cells of the grid of the maze
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 31
        # Initializes the player
        self.player = Player(self, STARTING_POS)
        # Loads maze image
        self.walls = []
        self.coins = []
        self.load()


    def run(self):
        while self.running:
            # Calls functions for when game is in start screen
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            # Calls functions for when game is in playing mode
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ####################### HELPER FUNCTIONS ########################

    # Function to draw test
    # words is the text to draw
    # screen is the screen to draw the text on
    # pos is pix    el position to draw text
    # size is text size
    # color is text color
    # font_name is font of text
    # centered is bool to center text which is false by defult
    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] / 2
            pos[1] = pos[1] - text_size[1] / 2
        screen.blit(text, pos)

    # Function to load the maze
    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        # Creates a list of walls in the maze
        with open('walls.txt', 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(x_index, y_index))
                    elif char == "C":
                        self.coins.append(vec(x_index, y_index))

    # Function to draw a grid over the maze
    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for y in range(WIDTH // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, y * self.cell_height), (WIDTH, y * self.cell_height))
        for wall in self.walls:
            pygame.draw.rect(self.background, (112, 55, 163), (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height))

    ####################### INTRO FUNCTIONS #########################

    # Start Events
    def start_events(self):
        for event in pygame.event.get():
            # Closes game on exit
            if event.type == pygame.QUIT:
                self.running = False
            # Enters playing state when space pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.player.set_speed(2)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.player.set_speed(4)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.player.set_speed(8)

    # Updates in start state
    def start_update(self):
        pass

    # Draws starting screen
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR TO START', self.screen, [WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE,
                       (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH // 2, HEIGHT // 2 + 30], START_TEXT_SIZE, (44, 167, 198),
                       START_FONT, centered=True)
        self.draw_text('PUSH 1 FOR EASY', self.screen, [WIDTH // 2, HEIGHT // 2 + 110], START_TEXT_SIZE,
                       (170, 132, 58), START_FONT, centered=True)
        self.draw_text('PUSH 2 FOR NORMAL', self.screen, [WIDTH // 2, HEIGHT // 2 + 190], START_TEXT_SIZE,
                       (170, 132, 58), START_FONT, centered=True)
        self.draw_text('PUSH 3 FOR HARD', self.screen, [WIDTH // 2, HEIGHT // 2 + 270], START_TEXT_SIZE,
                       (170, 132, 58), START_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [3, 0], START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()

    ####################### PLAYING FUNCTIONS #########################

    def playing_events(self):
        for event in pygame.event.get():
            # Closes game on exit
            if event.type == pygame.QUIT:
                self.running = False
            # Moves the player based on the arrow key input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(vec(0, 1))

    # Updates in playing state
    def playing_update(self):
        self.player.update()

    # Draws the main game screen
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.draw_grid()
        self.draw_text('CURRENT SCORE : 0', self.screen, [10, 1], START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text('HIGH SCORE : 0', self.screen, [WIDTH // 2, 1], START_TEXT_SIZE, WHITE, START_FONT)
        self.player.draw()
        pygame.display.update()
        #self.coins.pop()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                                (int(coin.x*self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height) + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 5)

