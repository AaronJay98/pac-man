import pygame
import sys
import copy
from settings import *
from player_class import *
from enemy_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        # Initial variables for the game screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.e_pos = []
        self.p_pos = None
        self.high_score = 0
        # Variables for the size of the cells of the grid of the maze
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        # Loads maze image
        self.walls = []
        self.coins = []
        self.enemies = []
        self.load()
        # Initializes the player
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()


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
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
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

    # Function to load the images
    def load(self):
        # Maze Loading
        self.background = pygame.image.load('whitemaze1.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        # Creates a list of walls in the maze
        with open('walls.txt', 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(x_index, y_index))
                    elif char == "C":
                        self.coins.append(vec(x_index, y_index))
                    elif char == "P":
                        self.p_pos = [x_index, y_index]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([x_index, y_index])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (x_index * self.cell_width, y_index * self.cell_height, self.cell_width, self.cell_height))


        #Coins Loading
        self.coin_image = pygame.image.load('blackcoinflower.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (self.cell_width, self.cell_height))

    # Function to make the enemies
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    # Function to draw a grid over the maze
    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for y in range(WIDTH // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, y * self.cell_height), (WIDTH, y * self.cell_height))
        for wall in self.walls:
            pygame.draw.rect(self.background, (112, 55, 163), (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height))

    # Resets the game to be played again
    def reset(self):
        self.player.lives = 3

        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open('walls.txt', 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(x_index, y_index))
        self.state = "playing"

    ####################### INTRO FUNCTIONS #########################

    # Start Events
    def start_events(self):
        for event in pygame.event.get():
            # Closes game on exit
            if event.type == pygame.QUIT:
                self.running = False
            # Chooses difficulty speed based on user input and enters playing stage
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.player.set_speed(2)
                for enemy in self.enemies:
                    enemy.set_speed(2, 1)
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.player.set_speed(4)
                for enemy in self.enemies:
                    enemy.set_speed(4, 2)
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.player.set_speed(8)
                for enemy in self.enemies:
                    enemy.set_speed(8, 4)
                self.state = 'playing'

    # Updates in start state
    def start_update(self):
        pass

    # Draws starting screen
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH 1 FOR EASY', self.screen, [WIDTH // 2, HEIGHT // 2 - 100], START_TEXT_SIZE,
                       GREEN, START_FONT, centered=True)
        self.draw_text('PUSH 2 FOR NORMAL', self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE,
                       YELLOW, START_FONT, centered=True)
        self.draw_text('PUSH 3 FOR HARD', self.screen, [WIDTH // 2, HEIGHT // 2 + 100], START_TEXT_SIZE,
                       RED, START_FONT, centered=True)
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
        for enemy in self.enemies:
            enemy.update()

        # Decrease life when hit by enemy
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            if(self.player.current_score > self.high_score):
                self.high_score = self.player.current_score
            print(self.high_score)
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0;

    # Draws the main game screen
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text('CURRENT SCORE : {}'.format(self.player.current_score), self.screen, [10, 1], START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text('HIGH SCORE : {}'.format(self.high_score), self.screen, [WIDTH // 2, 1], START_TEXT_SIZE, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        #self.coins.pop()

    def draw_coins(self):
        for coin in self.coins:
            #pygame.draw.circle(self.screen, (124, 123, 7),
            #                    (int(coin.x*self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
            #                    int(coin.y*self.cell_height) + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 5)
            self.screen.blit(self.coin_image, (int(coin.x * self.cell_width) + (self.cell_width - self.coin_image.get_width())/2 + TOP_BOTTOM_BUFFER//2,
                                               int(coin.y * self.cell_height) + (self.cell_height - self.coin_image.get_height())/2 + TOP_BOTTOM_BUFFER//2))

    ####################### GAME OVER FUNCTIONS #########################

    def game_over_events(self):
            for event in pygame.event.get():
                # Closes game on exit
                if event.type == pygame.QUIT:
                    self.running = False
                # Chooses difficulty speed based on user input and enters playing stage
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.player.set_speed(2)
                    for enemy in self.enemies:
                        enemy.set_speed(2, 1)
                    self.reset()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.player.set_speed(4)
                    for enemy in self.enemies:
                        enemy.set_speed(4, 2)
                    self.reset()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.player.set_speed(8)
                    for enemy in self.enemies:
                        enemy.set_speed(8, 4)
                    self.reset()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False


    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH 1 FOR EASY', self.screen, [WIDTH // 2, HEIGHT // 2 - 100], START_TEXT_SIZE,
                       GREEN, START_FONT, centered=True)
        self.draw_text('PUSH 2 FOR NORMAL', self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE,
                       YELLOW, START_FONT, centered=True)
        self.draw_text('PUSH 3 FOR HARD', self.screen, [WIDTH // 2, HEIGHT // 2 + 100], START_TEXT_SIZE,
                       RED, START_FONT, centered=True)
        self.draw_text('PUSH ESCAPE TO QUIT', self.screen, [WIDTH // 2, HEIGHT // 2 + 200], START_TEXT_SIZE,
                       WHITE, START_FONT, centered=True)
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 300], 72, RED, "arial", centered=True)
        self.draw_text('CURRENT SCORE : {}'.format(self.player.current_score), self.screen, [WIDTH//2, 400], START_TEXT_SIZE, WHITE, START_FONT, centered=True)
        self.draw_text('HIGH SCORE : {}'.format(self.high_score), self.screen, [WIDTH//2, 450], START_TEXT_SIZE, WHITE, START_FONT, centered=True)
        pygame.display.update()
