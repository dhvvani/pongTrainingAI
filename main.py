#fitness of a node is the number of times it touches the paddle
import time

from pong import Game
import pygame
import neat
import os
import pickle

class pongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.lPaddle = self.game.leftPaddle
        self.rPaddle = self.game.rightPaddle
        self.ball = self.game.ball


#plays the AI
    def test_ai(self, genome, config):

        network = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        clock = pygame.time.Clock()

        while run:
            # run the while loop 60 times per second
            clock.tick(60)
            gameInfo = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # the right paddle is the AI
            op = network.activate((self.rPaddle.y, self.ball.y, abs(self.rPaddle.x - self.ball.x)))
            decision = op.index(max(op))

            # the AI will move upwards
            if decision == 1:
                self.game.handlePaddleMovement(True, True)
            # the AI moves down
            elif decision == 2:
                self.game.handlePaddleMovement(False, False)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.game.handlePaddleMovement(True, True)
            if keys[pygame.K_s]:
                self.game.handlePaddleMovement(True, False)


            print(gameInfo.lScore, gameInfo.rScore)
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()

    def trainAI(self, genome1, genome2, config):
        network1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        network2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        run = True
        startTime = time.time()
        maxHits = 50

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()          #ends the entire program when we click exit

            gameInfo = self.game.loop()
            self.moveAIPaddles(network1, network2)

            self.game.draw(drawScr=False, drawHits=True)
            pygame.display.update()
            duration = time.time() -startTime

            # if either (you or the opponent) paddle misses the ball once, end the game since it will most likely miss again
            # or stop the game once the left player hits 50 so the AI doesnt play infinitely
            if gameInfo.lScore >= 1 or gameInfo.rScore >= 1 or gameInfo.lHits > maxHits:
                self.calFitness(gameInfo, duration)
                break

        return False

    def moveAIPaddles(self, net1, net2):

        players = [(self.genome1, net1, self.lPaddle), (self.genome2, net2, self.rPaddle)]

        for (genome, network, paddle) in players:
            # output from neural network that will be used to move the paddles
            output = network.activate(
                (paddle.y, abs(paddle.x - self.ball.x), self.ball.y)
            )

            valid = True
            #0 = stay in place, 1 = move up 2 = move down
            decision = output.index(max(output))
            if decision == 0:
                genome.fitness -=0.01

            elif decision == 1:
                valid = self.game.handlePaddleMovement(True, True)

            elif decision == 2:
                valid = self.game.handlePaddleMovement(False, False)

            if not valid:
                genome.fitness -= 1

    def calFitness(self, gameInfo, duration):
        self.genome1.fitness += gameInfo.lHits + duration
        self.genome2.fitness += gameInfo.rHits + duration

def runNeat(config):
    #to load from a checkpoint, comment out the command below (where x is the desired checkpoint) and comment the NEXT command
    #pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-x')
    pop =neat.Population(config)

    #from neat website
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # saves a checkpoint after every x = 1 generation(s) -> allows us to restart the algorithm after a certain point
    pop.add_reporter(neat.Checkpointer(1))

    #the winning node
    winner = pop.run(evalGenomes, 1)

    #use pickle (allows us to save an entire python object) to save and load the nn
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def testAI(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winnerNetwork = neat.nn.FeedForwardNetwork.create(winner, config)

    windWidth = 700
    windHeight = 500

    window = pygame.display.set_mode((windWidth, windHeight))

    game = pongGame(window, windWidth, windHeight)
    game.test_ai(winnerNetwork)

#goal is to try train each AI with the remaining other AIs - better training if better opponents
def evalGenomes(genomes, config):
    windWidth = 700
    windHeight = 500

    window = pygame.display.set_mode((windWidth, windHeight))

    #for each i train against remaining genomes ahead of it
    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes)*100), end=" ")
        #starting fitness
        genome1.fitness = 0

        for genome_id2, genome2 in genomes[min(i+1, len(genomes)-1):]:

            #set to 0 is starting genome, otherwise it should stay the same
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = pongGame(window, windWidth, windHeight)
            game.trainAI(genome1, genome2, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    configPath = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configPath)

    runNeat(config)
    testAI(config)
