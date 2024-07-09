import pygame
pygame.init()

#global variables
WIDTH = 700
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ping pong!")

FRAMES_PER_SEC = 60

WINNING_SCORE = 10

#color variables:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)
GREEN = (0, 255, 0)

#Paddle variables
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

#PING PONG BALL VARIABLES
BALL_RADIUS = 10

#Text Variables
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WIN_FONT = pygame.font.SysFont("comicsans", 75)

#classes
class Paddle:
    PADDLE_COLOR = WHITE
    PADDLE_VELOCITY = 4
    def __init__(self, x, y, width, height):
        self.x = self.origX = x
        self.y = self.origY = y
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

    def reset(self):
        self.x = self.origX
        self.y = self.origY

class PingBall:
    MAX_VELOCITY = 5
    BALL_COLOR = PINK
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

#functions
def draw(window, paddles, ball, lScore, rScore):
    window.fill(BLACK)

    lScoreText = SCORE_FONT.render(f"{lScore}", 1 ,WHITE)
    rScoreText = SCORE_FONT.render(f"{rScore}", 1, WHITE)

    window.blit(lScoreText, (WIDTH//4 - lScoreText.get_width() // 2, 20))
    window.blit(rScoreText, (WIDTH -WIDTH // 4 - rScoreText.get_width() // 2, 20))

    for paddle in paddles:
        paddle.drawPaddle(window)

    #draw a line every 20 pixels to draw a dotted line
    rectWidth = 10
    for i in range(10, HEIGHT, HEIGHT//20):
        if( i % 2 == 0):
            pygame.draw.rect(window, WHITE, (WIDTH/2 - rectWidth//2, i, rectWidth, HEIGHT//20))

    ball.drawBall(window)

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



#to handle paddle-ball collicion, the the angle of bounce of the ball after it hits the paddle
#depends on the distance between the point of collision on the paddle and the center of the
#paddle. Want max velocity when we have maximum distance (when the ball hits the edge of the paddle = PADDLE_HEIGHT /2).
#Let thereduction factor =  distance / max velocity of ball
def handleCollision(rPaddle, lPaddle, ball):
    #handling collision with the ceiling and floor (not left/right since that is how a player looses
    if( ball.y + ball.radius//2 >= HEIGHT ) or ( ball.y - ball.radius //2 <= 0 ):
        ball.yVel *= -1

    #handling collision w ball
    #if velocity is negative, then moving in the left direction, hence,collision w lpaddle

    redFact = (PADDLE_HEIGHT / 2) / ball.MAX_VELOCITY

    if(ball.xVel < 0
    and ball.y - BALL_RADIUS//2 >= lPaddle.y
    and ball.y + BALL_RADIUS//2 <= lPaddle.y + PADDLE_HEIGHT
    and ball.x - BALL_RADIUS//2  <= lPaddle.x + PADDLE_WIDTH ):

        ball.xVel *= -1

        middle_y = lPaddle.y + PADDLE_HEIGHT/2
        distanceInY = middle_y - ball.y

        ball.yVel = distanceInY / redFact * -1

    elif (ball.xVel > 0
    and ball.y - BALL_RADIUS//2 >= rPaddle.y
    and ball.y + BALL_RADIUS//2 <= rPaddle.y + PADDLE_HEIGHT
    and ball.x + BALL_RADIUS//2  >= rPaddle.x ):

        ball.xVel *= -1

        middle_y = rPaddle.y + PADDLE_HEIGHT / 2
        distanceInY = middle_y - ball.y

        ball.yVel = distanceInY / redFact * -1




def main():
    gameRunning = True
    clock = pygame.time.Clock()

    leftPaddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    rightPaddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = PingBall(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    lScore = 0
    rScore = 0

    while gameRunning:
        #this forces all computers to run at the same FPS
        clock.tick(FRAMES_PER_SEC)
        draw(WINDOW, [leftPaddle, rightPaddle], ball, lScore, rScore)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                break

        keysUsed = pygame.key.get_pressed()
        handlePaddleMovement(keysUsed, leftPaddle, rightPaddle)

        ball.moveBall()
        handleCollision(rightPaddle,leftPaddle, ball)

        if ball.x < 0:
            rScore += 1
            ball.reset()

        if ball.x > WIDTH:
            lScore += 1
            ball.reset()

        if(lScore >= WINNING_SCORE):
            lText = WIN_FONT.render("Left player won!", 1, GREEN)
            WINDOW.blit(lText, (WIDTH//2 - lText.get_width()//2, HEIGHT//2 - lText.get_height()//2))
            pygame.display.update()
            pygame.time.delay(2500)
        if(rScore >= WINNING_SCORE):
            rText = WIN_FONT.render("Right player won!", 1, GREEN)
            WINDOW.blit(rText, (WIDTH // 2 - rText.get_width() // 2, HEIGHT // 2 - rText.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2500)

        if (lScore >= WINNING_SCORE or rScore >= WINNING_SCORE):
            leftPaddle.reset()
            rightPaddle.reset()
            ball.reset()
            lScore = 0
            rScore = 0

    pygame.quit()

#this only allows the game to start by running this file only: not if the file is imported
if __name__ == '__main__':
    main()