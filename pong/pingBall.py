import pygame
import math
import random

class PingBall:
    # Ping-pong ball variables
    BALL_RADIUS = 10
    MAX_VELOCITY = 5
    BALL_COLOR = (255, 182, 193)

    def __init__(self, x, y):
        self.x = self.origX = x
        self.y = self.origY = y

        angle = self.randAngle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.xVel = pos * abs(math.cos(angle) * self.MAX_VELOCITY)
        self.yVel = math.sin(angle) * self.MAX_VELOCITY

        self.radius = self.BALL_RADIUS

    def randAngle(self, minAngle, maxAngle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(minAngle, maxAngle))

        return angle

    def drawBall(self, window):
        pygame.draw.circle(window, self.BALL_COLOR, (self.x, self.y), self.radius)

    def moveBall(self):
        self.x += self.xVel
        self.y += self.yVel

    def reset(self):
        self.x = self.origX
        self.y = self.origY

        #SHOOTS BALL TO OPPONENT
        angle = self.randAngle(-30, 30, [0])
        self.xVel *= -1
        self.yVel = math.sin(angle) * self.MAX_VELOCITY
