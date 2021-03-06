import pygame
from settings import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        # sets initial variables
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3
        self.avatar_image = pygame.image.load('redpanda.png')
        self.avatar_image = pygame.transform.scale(self.avatar_image, (self.app.cell_width, self.app.cell_height))


    def update(self):
        # Moves the position based on the direction
        if self.able_to_move:
            self.pix_pos += (self.speed * self.direction)
        if self.time_to_move():
            if None != self.stored_direction:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Sets the grid position in reference to the pixel position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width//2)//self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height//2)//self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

    # Draws the player image
    def draw(self):
        self.app.screen.blit(self.avatar_image, (int(self.pix_pos.x) - self.app.cell_width//2,
                                                 int(self.pix_pos.y) - self.app.cell_height//2))

        # Drawing Player lives
        for x in range(self.lives):
            self.app.screen.blit(self.avatar_image, (15 + 40 * x, HEIGHT - 50))
            #pygame.draw.circle(self.app.screen, PLAYER_COLOR, (40 + 40 * x, HEIGHT - 30), 15)

        # Draws the circle
        #pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)),
        #                   self.app.cell_width//2 - 2)
        # Draws a rectangle of the grid the player is on
        #pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER//2,
        #                                        self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER//2,
        #                                        self.app.cell_width, self.app.cell_height), 1)

    # Checks if there is coin in current position
    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    # Gets the pixel position based on the grid position
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    # Sets direction movement when player inputs an arrow key
    def move(self, direction):
        self.stored_direction = direction

    # Only allows movement when player is in center of a grid box
    # Makes sure player gets locked onto the grid
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0,0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0,0):
                return True
        return False

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    def set_speed(self, new_speed):
        self.speed = new_speed
        #print(self.speed)
