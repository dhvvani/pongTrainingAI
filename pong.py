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
    PADDLE_VELOCITY = 4
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def drawPaddle(self, window):
        pygame.draw.rect(window, self.PADDLE_COLOR, (self.x, self.y, self.width, self.height) )

    def movePaddle(self, up = True):
        #use min and max to prevent paddles from moving off the window
        if up:
            self.y = max(0, self.y - self.PADDLE_VELOCITY)
        else:
            self.y = min(HEIGHT - PADDLE_HEIGHT, self.y + self.PADDLE_VELOCITY )

#functions
def draw(window, paddles):
    window.fill(BLACK)

    for paddle in paddles:
        paddle.drawPaddle(window)

    #draw a line every 20 pixels to draw a dotted line
    rectWidth = 10
    for i in range(10, HEIGHT, HEIGHT//20):
        if( i % 2 == 0):
            pygame.draw.rect(window, WHITE, (WIDTH/2 - rectWidth//2, i, rectWidth, HEIGHT//20))


    pygame.display.update()

def handlePaddleMovement(keys, lPaddle, rPaddle):
    if keys[pygame.K_w]:
        lPaddle.movePaddle(up=True)
    if keys[pygame.K_s]:
        lPaddle.movePaddle(up = False)

    if keys[pygame.K_UP]:
        rPaddle.movePaddle(up=True)
    if keys[pygame.K_DOWN]:
        rPaddle.movePaddle(up = False)



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

        keysUsed = pygame.key.get_pressed()
        handlePaddleMovement(keysUsed, leftPaddle, rightPaddle)

    pygame.quit()

#this only allows the game to start by running this file only: not if the file is imported
if __name__ == '__main__':
    main()