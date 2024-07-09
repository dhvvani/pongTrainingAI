import pygame

class Paddle:
    PADDLE_COLOR = (255, 255, 255)
    PADDLE_VELOCITY = 4
    def __init__(self, x, y, width, height):
        self.x = self.origX = x
        self.y = self.origY = y
        self.width = width
        self.height = height

    def drawPaddle(self, window):
        pygame.draw.rect(window, self.PADDLE_COLOR, (self.x, self.y, self.width, self.height) )

    def movePaddle(self, windowHeight, paddleHeight, up = True):
        #use min and max to prevent paddles from moving off the window
        if up:
            self.y = max(0, self.y - self.PADDLE_VELOCITY)
        else:
            self.y = min(windowHeight - paddleHeight, self.y + self.PADDLE_VELOCITY )

    def reset(self):
        self.x = self.origX
        self.y = self.origY