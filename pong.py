import pygame
pygame.init()

#global variables
WIDTH = 700
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ping pong!")

FRAMES_PER_SEC = 60

#color variables:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)

#Paddle variables
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100


#classes
class Paddle:
    PADDLE_COLOR = WHITE
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def drawPaddle(self, window):
        pygame.draw.rect(window, self.PADDLE_COLOR, (self.x, self.y, self.width, self.height) )

#functions
def draw(window, paddles):
    window.fill(BLACK)

    for paddle in paddles:
        paddle.drawPaddle(window)

    pygame.display.update()

def main():
    gameRunning = True
    clock = pygame.time.Clock()

    leftPaddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    rightPaddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while gameRunning:
        #this forces all computers to run at the same FPS
        clock.tick(FRAMES_PER_SEC)
        draw(WINDOW, [leftPaddle, rightPaddle])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                break

    pygame.quit()

#this only allows the game to start by running this file only: not if the file is imported
if __name__ == '__main__':
    main()