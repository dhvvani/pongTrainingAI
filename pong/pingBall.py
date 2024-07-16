import pygame
class PingBall:
    # Ping-pong ball variables
    BALL_RADIUS = 10
    MAX_VELOCITY = 5
    BALL_COLOR = (255, 182, 193)

    def __init__(self, x, y):
        self.x = self.origX = x
        self.y = self.origY = y

        self.radius = self.BALL_RADIUS

        self.xVel = self.MAX_VELOCITY
        self.yVel = 0


    def drawBall(self, window):
        pygame.draw.circle(window, self.BALL_COLOR, (self.x, self.y), self.radius)

    def moveBall(self):
        self.x +=self.xVel
        self.y += self.yVel

    def reset(self):
        self.x = self.origX
        self.y = self.origY

        #SHOOTS BALL TO OPPONENT
        self.xVel *= -1
        self.yVel = 0