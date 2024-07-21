#fitness of a node is the number of times it touches the paddle
from pong import Game
import pygame

class pongGame:
    def _init(self, window, width, height):
        self.game = Game(window, width, height)
        self.lPaddle = self.game.leftPaddle
        self.rPaddle = self.game.rightPaddle
        self.ball = self.game.ball

    def test_ai(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            # run the while loop 60 times per second
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.game.handlePaddleMovement(True, True)
            if keys[pygame.K_s]:
                self.game.handlePaddleMovement(True, False)

            gameInfo = self.game.loop()
            print(gameInfo.lScore, gameInfo.rScore)
            self.game.draw(True, False)

            pygame.display.update()

        pygame.quit()
