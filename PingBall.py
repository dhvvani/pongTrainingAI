import pygame
class PingBall:
    MAX_VELOCITY = 5
    BALL_COLOR = (255, 182, 193)
    def __init__(self, x, y, radius):
        self.x = self.origX = x
        self.y = self.origY = y
        self.radius = radius
        self.yVel = 0
        self.xVel = self.MAX_VELOCITY

    def drawBall(self, window):
        pygame.draw.circle(window, self.BALL_COLOR, (self.x, self.y), self.radius)

    def moveBall(self):
        self.x +=self.xVel
        self.y += self.yVel

    def reset(self):
        self.x = self.origX
        self.y = self.origY

        #SHOOTS BALL TO OPPONENT
        self.yVel = 0
        self.xVel *= -1