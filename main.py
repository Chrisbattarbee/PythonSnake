import pygame
import sys
import random

class Node:
    def __init__(self, initPosition, imageLocation, screenToRenderOn):
        self.position = initPosition
        self.nodeBody = pygame.image.load(imageLocation)
        self.nodeBodyRect = self.nodeBody.get_rect()
        self.screen = screenToRenderOn
        self.speed = [0, 0]

    def updatePosition(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.nodeBodyRect.left = self.position[0]
        self.nodeBodyRect.top = self.position[1]

    def render(self):
        screen.blit(self.nodeBody, self.nodeBodyRect)

class SnakeBody:
    def __init__(self, initPosition, imageLoc, screenToRenderOn):
        self.imageLocation = imageLoc
        self.screen = screenToRenderOn
        self.nodes = [Node(initPosition, self.imageLocation, self.screen)]

    def render(self):
        for node in self.nodes:
            node.render()

    def updateSpeed(self, speedOfFirst):

        # We change the speed of the first node and then all of the rest of the nodes
        # take the speed of the node one before them in the list
        if len(self.nodes) != 1:
            for x in range(len(self.nodes) - 1, -1, -1):
                self.nodes[x].speed = self.nodes[x - 1].speed
        self.nodes[0].speed = speedOfFirst

    def updatePositions(self):

        # Update the position of all of the nodes using the speed that we have just changed
        for node in self.nodes:
            node.updatePosition()

    def addNode(self, position):
        self.nodes.append(Node(position, self.imageLocation, self.screen))

    def isInsideSelfOrOutsideRegion(self, width, height):

        isInside = False

        if self.nodes[0].position[0] > width - 12 or self.nodes[0].position[1] > height - 12 or self.nodes[0].position[0] < 0 or self.nodes[0].position[1] < 0:
            isInside = True

        for x in range(1, len(self.nodes)):
            if self.nodes[0].position == self.nodes[x].position:
                isInside = True

        return isInside

class Food:

    def __init__(self, pos, imageLoc, screenToRenderOn):
        self.foodBody = pygame.image.load(imageLoc)
        self.position = pos
        self.foodBodyRect = self.foodBody.get_rect()
        self.foodBodyRect.x = pos[0]
        self.foodBodyRect.y = pos[1]
        self.screen = screenToRenderOn

    def render(self):
        self.screen.blit(self.foodBody, self.foodBodyRect)

class FoodManager:

    def __init__(self, imageLoc, screenToRenderOn, snakeObject):
        self.imageLocation = imageLoc
        self.screen = screenToRenderOn
        self.foodList = []
        self.createFood(snakeObject)

    def createFood(self, snake):

        isInsideSomething = True
        x = random.randint(1, 13) * 24  # X 24 to make it fit exactly to the grid
        y = random.randint(1, 9) * 24
        pos = [x, y]

        while self.isInside(snake, pos) is True:
            x = random.randint(1,13) * 24 # X 24 to make it fit exactly to the grid
            y = random.randint(1,9) * 24
            pos = [x,y]

        self.foodList.append(Food(pos, self.imageLocation, self.screen))

    def isInside(self, snake, pos):

        isInsideSomething = False
        for node in snake.nodes:
            if node.position == pos:
                isInsideSomething= True

        for food in self.foodList:
            if food.position == pos:
                isInsideSomething = True

        return isInsideSomething

    def removeFoodByPos(self, pos):

        # Find the food we need and delete
        for food in self.foodList:
            if pos == food.position:
                self.foodList.remove(food)

    def removeFoodByRef(self, food):
        self.foodList.remove(food)

    def render(self):
        for food in self.foodList:
            food.render()

class GameManager:
    def __init__(self, snakeObject, screenObject, foodManager, fontObject, wid, hig):
        self.gameTick = 0
        self.addQueue = [0, 0]
        self.addQueueGameTick = 999999999
        self.snake = snakeObject
        self.screen = screenObject
        self.speed = [0, 0]
        self.state = 'right'
        self.prevState = 'up'
        self.fm = foodManager
        self.isAlive = True
        self.score = 0
        self.font = fontObject
        self.width = wid
        self.height = hig

    def GameCycle(self):
        if self.isAlive == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    # Handling key presses
                if event.type == pygame.KEYDOWN:
                    self.prevState = self.state
                    if event.key == pygame.K_w:
                        self.state = 'up'
                    if event.key == pygame.K_s:
                        self.state = 'down'
                    if event.key == pygame.K_a:
                        self.state = 'left'
                    if event.key == pygame.K_d:
                        self.state = 'right'

            # Handles speed logic
            currentSpeed = self.speed


            self.screen.fill(black)
            self.snake.updatePositions()
            self.SetSpeed(currentSpeed)
            if self.gameTick % 12 == 0:
                self.checkIfFoodHasBeenEaten()

                #Check if the game should end
                if self.snake.isInsideSelfOrOutsideRegion(width, height) is True:
                    self.isAlive = False

            if self.gameTick % 100 == 0:
                self.fm.createFood(self.snake)
            self.fm.render()
            self.snake.render()
            self.spawnNewNodes()

            pygame.display.flip()

            self.gameTick += 1
        else:
            self.renderScore()

    def SetSpeed(self, currentSpeed):

        speed = [0, 0]
        if self.gameTick % 12 == 0:

            # Add all the new nodes

            if self.state == 'left' and self.prevState != 'right':
                self.speed = [-2, 0]
            elif self.state == 'right' and self.prevState != 'left':
                self.speed = [2, 0]
            elif self.state == 'up' and self.prevState != 'down':
                self.speed = [0, -2]
            elif self.state == 'down' and self.prevState != 'up':
                self.speed = [0, 2]
            else:
                self.speed = currentSpeed
            self.snake.updateSpeed(self.speed)
        else:
            self.speed = currentSpeed

    def spawnNewNodes(self):
        if self.gameTick == self.addQueueGameTick + 10:
            self.snake.addNode(self.addQueue)
            self.addQueueGameTick = 0

    def AddNodeToQueue(self, position, gt):
        self.addQueue = position
        self.addQueueGameTick = gt

    def checkIfFoodHasBeenEaten(self):
        for food in self.fm.foodList:
            if food.position == self.snake.nodes[0].position:

                self.AddNodeToQueue(self.snake.nodes[len(self.snake.nodes) - 1].position[:], self.gameTick)
                self.fm.removeFoodByRef(food)
                self.score += 1

    def renderScore(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    # Reinitialize all variables that we need to
                    self.snake = SnakeBody([0, 0], "Resources/square_white_24_ns.bmp", screen)
                    self.isAlive = True
                    self.score = 0
                    self.state = 'right'
                    self.prevState = 'up'

        self.screen.fill(black)
        deathText = font.render("Oh no you died!", 1, (255,255,255))
        scoreText = font.render("Score: " + str(self.score), 1, (255,255,255))
        restartText = font.render("SPACE to retry.", 1, (255,255,255))
        self.screen.blit(deathText, (50, 50))
        self.screen.blit(scoreText, (50, 100))
        self.screen.blit(restartText, (50, 150))
        pygame.display.flip()


pygame.init()
font = pygame.font.Font("Resources/SanFran.ttf", 30)

size = width, height = 312, 240

screen = pygame.display.set_mode(size)

snake = SnakeBody([0,0], 'Resources/square_white_24_ns.bmp', screen)

black = [0, 0, 0]

foodManager = FoodManager('Resources/square_green.bmp', screen, snake)

gm = GameManager(snake, screen, foodManager, font, width, height)

while 1:
    gm.GameCycle()
