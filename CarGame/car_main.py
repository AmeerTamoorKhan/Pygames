import numpy as np
import pygame as pg
import sys
import csv
from sklearn.neural_network import MLPClassifier as nn
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import pickle

pg.init()


class Car:
    stepSize = 32
    x_steps = 15
    y_steps = 20
    WIDTH = x_steps * stepSize
    HEIGHT = y_steps * stepSize
    boundary = 35

    x_step_half = x_steps - (x_steps - int(x_steps/2))
    y_step_half = y_steps - (y_steps - int(y_steps / 2))

    X = stepSize*x_step_half
    Y = stepSize*(y_step_half+4)

    road1_Y = 0
    road2_Y = -HEIGHT

    hole1_x = stepSize*np.random.randint(0, x_step_half)
    hole1_y = -stepSize

    hole2_x = stepSize*np.random.randint(x_step_half, x_steps)
    hole2_y = 0

    score = 0

    car_rect = None
    hole1_rect = None
    hole2_rect = None

    def __init__(self):
        pg.font.init()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.text = pg.font.Font('Font/HoltwoodOneSC-Regular.ttf', 24)
        self.car = pg.transform.scale(pg.transform.rotate(pg.image.load('Car_images/car.png'), 180), (96, 96))
        self.road1 = pg.transform.scale(pg.image.load('Car_images/road.jpg'), [self.WIDTH, self.HEIGHT])
        self.road2 = pg.transform.scale(pg.image.load('Car_images/road.jpg'), [self.WIDTH, self.HEIGHT])
        self.hole1 = pg.transform.scale(pg.image.load('Car_images/strainer.png'), (64, 64))
        self.hole2 = pg.transform.scale(pg.image.load('Car_images/strainer.png'), (64, 64))
        self.blast = pg.transform.scale(pg.image.load('Car_images/explosion.png'), (128, 128))

    def update_car(self, dir):

        if dir == 1:
            self.X = self.X + self.stepSize
            if self.X >= self.WIDTH - 64:
                self.X = self.X - self.stepSize
            self.screen.blit(self.car, [self.X, self.Y])
        if dir == -1:
            self.X = self.X - self.stepSize
            if self.X <= -32:
                self.X = self.X + self.stepSize
            self.screen.blit(self.car, [self.X, self.Y])

        self.car_rect = pg.Rect((self.X + 15, self.Y), (64, 96))
        self.screen.blit(self.car, [self.X, self.Y])

    def update_hole(self):

        self.hole1_y += self.stepSize
        self.hole1_rect = pg.Rect([self.hole1_x, self.hole1_y], [32, 32])
        self.screen.blit(self.hole1, [self.hole1_x, self.hole1_y])
        if self.hole1_y >= self.HEIGHT:
            self.hole1_x = self.stepSize*np.random.randint(1, self.x_step_half)
            self.hole1_y = self.stepSize*np.random.randint(-15, -10)

        self.hole2_y += self.stepSize
        self.hole2_rect = pg.Rect([self.hole2_x, self.hole2_y], [32, 32])
        self.screen.blit(self.hole2, [self.hole2_x, self.hole2_y])
        if self.hole2_y >= self.HEIGHT:
            self.hole2_x = self.stepSize*np.random.randint(self.x_step_half, self.x_steps-2)
            self.hole2_y = 0

    def update_road(self):

        self.road1_Y += self.stepSize
        self.screen.blit(self.road1, [0, self.road1_Y])
        if self.road1_Y >= self.HEIGHT:
            self.road1_Y = - self.HEIGHT

        self.road2_Y += self.stepSize
        self.screen.blit(self.road2, [0, self.road2_Y])
        if self.road2_Y >= self.HEIGHT:
            self.road2_Y = - self.HEIGHT

    def collision_check(self):

        if self.car_rect.colliderect(self.hole1_rect) or self.car_rect.colliderect(self.hole2_rect):
            self.screen.blit(self.blast, [self.X+15, self.Y])
            return False
        else:
            self.score += 0.1
            self.score_text(np.round(self.score, 1))
            return True

    def score_text(self, x):
        score = self.text.render(f'Distance: {x} m', False, pg.Color('white'))
        self.screen.blit(score, [10, 10])


def game_over(running, player):
    if not running:
        gameOver = pg.transform.scale(pg.image.load('Car_images/gameover.png'), [400, 240])
        player.screen.blit(gameOver, [player.WIDTH/12, player.HEIGHT/4])

car = Car()
clock = pg.time.Clock()
Play = True
while Play:
    clock.tick(60)
    car.screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        dir = 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                dir = 1
            if event.key == pg.K_LEFT:
                dir = -1

    car.update_road()
    car.update_hole()
    car.update_car(dir)

    Play = car.collision_check()
    game_over(Play, car)
    pg.display.update()
    while not Play:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    sys.exit()










