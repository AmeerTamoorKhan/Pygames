import pygame as pg
import sys
import numpy as np
pg.init()

Width = 588
Height = 400
step = 12
screen = pg.display.set_mode([Width, Height])
floorY = Height/1.5
floor = pg.image.load('Dino Images/floor-1.png')
bg = pg.transform.scale2x(pg.image.load('Dino Images/1x-cloud.png'))
obs = [pg.image.load('Dino Images/CACTUS4.png'), pg.image.load('Dino Images/CACTUS5.png')]
dino = pg.image.load('Dino Images/Idle.png')
enemy = [pg.transform.scale(pg.image.load('Dino Images/enemy2.png'), [44, 33]),
         pg.transform.scale(pg.image.load('Dino Images/enemy1.png'), [44, 33])]


enemyReact = None
enemyPos = [[Width, 1], [Height/3, Height/3.5, Height/4]]
obsRect = [None, None]
floorX = [0, Width]
bgPos = [[Width, 1], [Height/3, Height/4, Height/5, Height/6]]
obsX = [Width/1.1, 3*Width]


class Dino:

    def __init__(self):
        self.jump = 0
        self.jumpFlag = False
        # Force (v) up and mass m.
        self.v = 5
        self.m = 1
        self.dino_react = None
        self.dinoPos = [50, floorY - 45]
        self.score_text = pg.font.Font('Dino Images/font/pixelmix.ttf', 20)
        self.score = 0

    def dino_update(self):

        self.dino_react = pg.Rect(self.dinoPos, [44, 47])
        #pg.draw.rect(screen, pg.Color('red'), self.dino_react, 1)
        screen.blit(dino, self.dinoPos)

        if player.jumpFlag:
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
            F = (1 / 2) * self.m * (self.v ** 2)

            # change in the y co-ordinate
            self.dinoPos[1] -= 5*F

            # decreasing velocity while going up and become negative while coming down
            self.v = self.v - 1

            # object reached its maximum height
            if self.v < 0:
                # negative sign is added to counter negative velocity
                self.m = -1

            # objected reaches its original state
            if self.v == - 6:
                # making isjump equal to false
                self.jumpFlag = False

                # setting original values to v and m
                self.v = 5
                self.m = 1

    def collision_check(self):
        flag = True
        # if self.dino_react.colliderect(enemyReact):
        #     flag = False

        if self.dino_react.colliderect(obsRect[0]) or self.dino_react.colliderect(obsRect[1]):
            flag = False

        return flag

    def score_update(self):

        if self.collision_check():
            self.score += 1
            text = self.score_text.render(f'Score: {self.score}', False, pg.Color('black'))
            screen.blit(text, [10, 10])



def floor_update():
    # For Floor 1
    floorX[0] -= step
    obsRect[0] = pg.Rect([floorX[0], Height/1.5], [Width, 10])
    #pg.draw.rect(screen, pg.Color('red'), rect1)
    screen.blit(floor, [floorX[0], floorY])
    if floorX[0] <= -Width:
        floorX[0] = Width

    # For Floor 2
    floorX[1] -= step
    obsRect[1] = pg.Rect([floorX[1], Height/1.5], [Width, 10])
    #pg.draw.rect(screen, pg.Color('blue'), rect2)
    screen.blit(floor, [floorX[1], floorY])

    if floorX[1] <= -Width:
        floorX[1] = Width


def background_update():
    bgPos[0][0] -= 2
    if bgPos[0][0] <= -70:
        bgPos[0][0] = Width
        bgPos[0][1] = np.random.randint(low=0, high=3)

    i = bgPos[0][1]
    screen.blit(bg, [bgPos[0][0], bgPos[1][i]])


def obstacle_update():
    obsX[0] -= step

    obsRect[0] = pg.Rect([obsX[0], floorY-40], [24, 50])
    #pg.draw.rect(screen, pg.Color('red'), obsRect[0], 1)
    if obsX[0] <= 0:
        obsX[0] = 2*Width + np.random.randint(low=10, high=100)

    screen.blit(obs[0], [obsX[0], floorY-40])

    obsX[1] -= step

    obsRect[1] = pg.Rect([obsX[1], floorY - 40], [51, 50])
    #pg.draw.rect(screen, pg.Color('red'), obsRect[1], 1)
    if obsX[1] <= 0:
        obsX[1] = 2*Width + np.random.randint(low=500, high=Width)

    screen.blit(obs[1], [obsX[1], floorY - 40])


def enemy_update():
    global enemyReact
    enemyPos[0][0] -= step

    if enemyPos[0][0] <= -50:
        enemyPos[0][0] = 2*Width + np.random.randint(low=300, high=591)
        enemyPos[0][1] = np.random.randint(low=0, high=2)

    i = enemyPos[0][1]
    enemyReact = pg.Rect([enemyPos[0][0], enemyPos[1][i]], [48, 32])
    #pg.draw.rect(screen, pg.Color('red'), enemyReact, 1)
    screen.blit(enemy[0], [enemyPos[0][0], enemyPos[1][i]])


def scene_update(player):

    screen.fill([240, 240, 240])
    floor_update()
    background_update()
    obstacle_update()
    #enemy_update()
    player.dino_update()
    running = player.collision_check()
    player.score_update()
    pg.display.update()

    return running


clock = pg.time.Clock()
player = Dino()
running = True
while running:
    clock.tick(90)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            sys.exit()

        keys = pg.key.get_pressed()

        if not player.jumpFlag:
            # if space bar is pressed
            if keys[pg.K_SPACE]:
                # make isjump equal to True
                player.jumpFlag = True

    running = scene_update(player)

