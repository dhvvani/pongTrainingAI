import pygame

class Paddle:
    # Paddle variables
    PADDLE_WIDTH = 20
    PADDLE_HEIGHT = 100
    PADDLE_COLOR = (255, 255, 255)
    PADDLE_VELOCITY = 4
    def __init__(self, x, y):
        self.x = self.origX = x
        self.y = self.origY = y

    def drawPaddle(self, window):
        pygame.draw.rect(window, self.PADDLE_COLOR, (self.x, self.y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT) )

    def movePaddle(self, windowHeight, up = True):
        #use min and max to prevent paddles from moving off the window
        if up:
            self.y = max(0, self.y - self.PADDLE_VELOCITY)
        else:
            self.y = min(windowHeight - self.PADDLE_HEIGHT, self.y + self.PADDLE_VELOCITY )

    def reset(self):
        self.x = self.origX
        self.y = self.origY