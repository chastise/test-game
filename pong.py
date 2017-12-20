import pygame, sys, random
from pygame.locals import *


DISPLAY_HEIGHT = 512
DISPLAY_WIDTH = 512
PADDLE_HEIGHT = 64
PADDLE_WIDTH = 16
BALL_RADIUS = 10

colors = {
    "BLACK" : (0, 0, 0), #background
    "WHITE" : (255, 255, 255), #score text
    "RED" : (255, 0, 0), #ball
    "GREEN" : (0, 255, 0), #p1
    "BLUE" : (0, 0, 255) #p2
}

class Board(object):
    def __init__(self, board_height, board_width, paddle_height, paddle_width, ball_radius):
        self.surface = pygame.display.set_mode((board_height, board_width), 0, 32)
        self.font = pygame.font.SysFont(None, 48)
        self.paddle_height = paddle_height
        self.paddle_width = paddle_width
        self.p1_score, self.p2_score = 0, 0
        self.p1_paddle = [16, 255]
        self.p2_paddle = [495, 255]
        self.ball_position = [255, 255]
        self.paddle_speed = 6
        self.ball_speed = 6
        self.ball_max_speed = 20
        self.ball_velocity = [0, 0]


    def draw_board(self):
        self.surface.fill(colors['BLACK'])
        #Draw p1
        pygame.draw.rect(self.surface, colors['GREEN'],
                         (self.p1_paddle[0] - self.paddle_width / 2, self.p1_paddle[1] - self.paddle_height / 2, 16, 64))

        #Draw p2
        pygame.draw.rect(self.surface, colors['BLUE'],
                         (self.p2_paddle[0] - self.paddle_width / 2, self.p2_paddle[1] - self.paddle_height / 2, 16, 64))

        #Draw ball
        pygame.draw.circle(self.surface, colors['RED'], self.ball_position, 10, 0)


    def draw_score(self):
        text = self.font.render('{p1_score} : {p2_score}'.format(p1_score=self.p1_score, p2_score=self.p2_score),
                                True, colors['WHITE'], colors['BLACK'])
        textRect = text.get_rect()
        textRect.centerx = self.surface.get_rect().centerx
        textRect.centery = 24
        self.surface.blit(text, textRect)


    def draw_fps(self, fps):
        text = self.font.render('{fps}'.format(fps=int(fps)),
                                True, colors['WHITE'], colors['BLACK'])
        textRect = text.get_rect()
        textRect.centerx = self.surface.get_rect().centerx
        textRect.centery = 512-24
        self.surface.blit(text, textRect)


    def start_ball(self):
        self.ball_position = [255, 255]
        if random.random() < 0.5:
            self.ball_velocity[0] = 2.0 + random.random() * (self.ball_speed - 2)
        else:
            self.ball_velocity[0] = -2.0 - random.random() * (self.ball_speed - 2)
        self.ball_velocity[1] = (random.random() - 0.5) * self.ball_speed * 2


    def update_paddles(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w]:
            self.p1_paddle[1] -= self.paddle_speed
        if keys_pressed[pygame.K_s]:
            self.p1_paddle[1] += self.paddle_speed
        if keys_pressed[pygame.K_UP]:
            self.p2_paddle[1] -= self.paddle_speed
        if keys_pressed[pygame.K_DOWN]:
            self.p2_paddle[1] += self.paddle_speed


    def update_ball(self):
        new_y = int(self.ball_position[1] + self.ball_velocity[1])
        new_x = int(self.ball_position[0] + self.ball_velocity[0])
        # Check top:
        if new_y < 0:
            new_y = new_y * -1
            self.ball_velocity[1] = self.ball_velocity[1] * -1
        elif new_y > self.surface.get_height():
            new_y = self.surface.get_height() - (new_y - self.surface.get_height())
            self.ball_velocity[1] = self.ball_velocity[1] * -1

        # Check paddle collision:
        if new_x  <= (self.p1_paddle[0] + self.paddle_width / 2) and \
            (self.p1_paddle[1] + self.paddle_height / 2) > new_y > (self.p1_paddle[1] - self.paddle_height / 2):
            new_x = int(
                (self.p1_paddle[0] + self.paddle_width / 2) + (new_x - (self.p1_paddle[0] + self.paddle_width / 2)))
            self.ball_velocity[0] = (self.ball_velocity[0] * -1) + 1

        if new_x >= (self.p2_paddle[0] - self.paddle_width / 2) and \
            (self.p2_paddle[1] + self.paddle_height / 2) > new_y > (self.p2_paddle[1] - self.paddle_height / 2):
            new_x = int(
                (self.p2_paddle[0] + self.paddle_width / 2) + (new_x - (self.p2_paddle[0] + self.paddle_width / 2)))
            self.ball_velocity[0] = (self.ball_velocity[0] * -1) - 1

        # Check for scoring:
        if new_x < 0:
            self.p2_score += 1
            return True
        elif new_x > self.surface.get_width():
            self.p1_score += 1
            return True
        else:
            self.ball_position[0] = new_x
            self.ball_position[1] = new_y
            return False


def main_game_loop(FPS=30):
    pygame.init()
    pygame.display.set_caption('A pong')
    clock = pygame.time.Clock()
    board = Board(DISPLAY_HEIGHT, DISPLAY_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH, BALL_RADIUS)
    board.start_ball()
    # Run the game loop.
    while True:
        pygame.event.pump()
        clock.tick(FPS)
        board.draw_board()
        board.update_paddles()
        if board.update_ball():
            # Figure out how to pause a little here
            board.start_ball()
        board.draw_score()
        board.draw_fps(clock.get_fps())
        pygame.display.update()



main_game_loop(30)