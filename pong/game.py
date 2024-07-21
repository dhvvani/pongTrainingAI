import pygame
from .paddle import Paddle
from .pingBall import PingBall

pygame.init()

#global variables
WIDTH = 700
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ping pong!")

FRAMES_PER_SEC = 60

WINNING_SCORE = 10



class GameInfo:
    def __init__(self, lHits, rHits, lScore, rScore):
        self.lHits = lHits
        self.rHits = rHits

        self.lScore = lScore
        self.rScore = rScore


class Game:
    # color variables:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PINK = (255, 182, 193)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Text Variables
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WIN_FONT = pygame.font.SysFont("comicsans", 75)

    def __init__(self, window, windWidth, windHeight):
        self.window = window

        self.windowWidth = windWidth
        self.windowHeight = windHeight

        self.leftPaddle = Paddle(10, windHeight // 2 - Paddle.PADDLE_HEIGHT // 2)
        self.rightPaddle = Paddle(windWidth - 10 - Paddle.PADDLE_WIDTH, windHeight // 2 - Paddle.PADDLE_HEIGHT // 2)

        self.ball = PingBall(windWidth // 2, windHeight // 2)

        self.lScore = 0
        self.rScore = 0

        self.lHits = 0
        self.rHits = 0

    def drawScore(self):
        lScoreText = self.SCORE_FONT.render(f"{self.lScore}", 1, self.WHITE)
        rScoreText = self.SCORE_FONT.render(f"{self.rScore}", 1, self.WHITE)

        self.window.blit(lScoreText, (WIDTH // 4 - lScoreText.get_width() // 2, 20))
        self.window.blit(rScoreText, (WIDTH - WIDTH // 4 - rScoreText.get_width() // 2, 20))


    def drawHits(self):
        hitTexts = self.SCORE_FONT.render(f"{self.lHits + self.rHits}", 1, self.RED)
        self.window.blit(hitTexts, (self.windowWidth //2 - hitTexts.get_width() // 2, 10))

    def drawDivider(self):
        # draw a line every 20 pixels to draw a dotted line
        rectWidth = 10
        for i in range(10, HEIGHT, HEIGHT // 20):
            if (i % 2 == 0):
                pygame.draw.rect(self.window, self.WHITE, (self.windowWidth / 2 - rectWidth // 2, i, rectWidth, self.windowHeight // 20))


    # to handle paddle-ball collicion, the the angle of bounce of the ball after it hits the paddle
    # depends on the distance between the point of collision on the paddle and the center of the
    # paddle. Want max velocity when we have maximum distance (when the ball hits the edge of the paddle = PADDLE_HEIGHT /2).
    # Let thereduction factor =  distance / max velocity of ball
    def handleCollision(self):

        ball = self.ball
        lPaddle = self.leftPaddle
        rPaddle = self.rightPaddle

        # handling collision with the ceiling and floor (not left/right since that is how a player looses
        if (ball.y + ball.radius // 2 >= HEIGHT) or (ball.y - ball.radius // 2 <= 0):
            ball.yVel *= -1

        # handling collision w ball
        # if velocity is negative, then moving in the left direction, hence,collision w lpaddle

        redFact = (lPaddle.PADDLE_HEIGHT / 2) / ball.MAX_VELOCITY

        if (ball.xVel < 0
                and ball.y - ball.radius // 2 >= lPaddle.y
                and ball.y + ball.radius // 2 <= lPaddle.y + lPaddle.PADDLE_HEIGHT
                and ball.x - ball.radius // 2 <= lPaddle.x + lPaddle.PADDLE_WIDTH):

            ball.xVel *= -1

            middle_y = lPaddle.y + lPaddle.PADDLE_HEIGHT / 2
            distanceInY = middle_y - ball.y

            ball.yVel = distanceInY / redFact * -1

        elif (ball.xVel > 0
              and ball.y - ball.radius // 2 >= rPaddle.y
              and ball.y + ball.radius // 2 <= rPaddle.y + rPaddle.PADDLE_HEIGHT
              and ball.x + ball.radius // 2 >= rPaddle.x):

            ball.xVel *= -1

            middle_y = rPaddle.y + rPaddle.PADDLE_HEIGHT / 2
            distanceInY = middle_y - ball.y

            ball.yVel = distanceInY / redFact * -1

    def draw(self, drawScr = True, drawHits = False):
        self.window.fill(self.BLACK)

        self.drawDivider()
        self.drawScore()
        self.drawHits()

        for paddle in [self.leftPaddle, self.rightPaddle]:
            paddle.drawPaddle(self.window)

        self.ball.drawBall(self.window)

    def handlePaddleMovement(self, left = True, up = True):

        """
        moves the left or right paddle.

        Returns a boolean to represent valid paddle movement.
        Movement is invalid if the paddle goes off the screen
        """

        if left:
            if up and self.leftPaddle.y - Paddle.PADDLE_VELOCITY < 0:
                return False
            if not up and self.leftPaddle.y + Paddle.PADDLE_HEIGHT > self.windowHeight:
                return False

            self.leftPaddle.movePaddle(self.windowHeight, up)
        else:
            if up and self.rightPaddle.y - Paddle.PADDLE_VELOCITY < 0:
                return False
            if not up and self.rightPaddle.y + Paddle.PADDLE_HEIGHT > self.windowHeight:
                return False

            self.rightPaddle.movePaddle(self.windowHeight, up)

        return True

    def loop(self):
        """
        executes a single game loop
        :return: game info instance stating score and hits of each paddle
        """

        self.ball.moveBall()
        self.handleCollision()

        if self.ball.x < 0:
            self.ball.reset()
            self.rScore += 1
        elif self.ball.x > self.windowWidth:
            self.ball.reset()
            self.lScore += 1

        gameInfo =  GameInfo(self.lHits, self.rHits, self.lScore, self.rScore)

        return gameInfo
    def reset(self):
        self.ball.reset()
        self.leftPaddle.reset()
        self.rightPaddle.reset()

        self.lScore = 0
        self.rScore = 0

        self.lHits = 0
        self.rHits = 0