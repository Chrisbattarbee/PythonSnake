import pygame
import sys
import random


class Node:
    def __init__(self, init_position, image_location, screen_to_render_on):
        self.position = init_position
        self.nodeBody = pygame.image.load(image_location)
        self.nodeBodyRect = self.nodeBody.get_rect()
        self.screen = screen_to_render_on
        self.speed = [0, 0]

    def update_position(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.nodeBodyRect.left = self.position[0]
        self.nodeBodyRect.top = self.position[1]

    def render(self):
        screen.blit(self.nodeBody, self.nodeBodyRect)


class SnakeBody:
    def __init__(self, init_position, image_loc, screen_to_render_on):
        self.imageLocation = image_loc
        self.screen = screen_to_render_on
        self.nodes = [Node(init_position, self.imageLocation, self.screen)]

    def render(self):
        for node in self.nodes:
            node.render()

    def update_speed(self, speed_of_first):

        # We change the speed of the first node and then all of the rest of the nodes
        # take the speed of the node one before them in the list
        if len(self.nodes) != 1:
            for x in range(len(self.nodes) - 1, -1, -1):
                self.nodes[x].speed = self.nodes[x - 1].speed
        self.nodes[0].speed = speed_of_first

    def update_positions(self):

        # Update the position of all of the nodes using the speed that we have just changed
        for node in self.nodes:
            node.update_position()

    def add_node(self, position):
        self.nodes.append(Node(position, self.imageLocation, self.screen))

    def is_inside_self_or_outside_region(self, wid, heigh):

        is_inside = False

        if self.nodes[0].position[0] > wid - 12 or self.nodes[0].position[1] > heigh - 12 or \
                self.nodes[0].position[0] < 0 or self.nodes[0].position[1] < 0:
            is_inside = True

        for x in range(1, len(self.nodes)):
            if self.nodes[0].position == self.nodes[x].position:
                is_inside = True

        return is_inside


class Food:
    def __init__(self, pos, image_loc, screen_to_render_on):
        self.foodBody = pygame.image.load(image_loc)
        self.position = pos
        self.foodBodyRect = self.foodBody.get_rect()
        self.foodBodyRect.x = pos[0]
        self.foodBodyRect.y = pos[1]
        self.screen = screen_to_render_on

    def render(self):
        self.screen.blit(self.foodBody, self.foodBodyRect)


class FoodManager:
    def __init__(self, image_loc, screen_to_render_on, snake_object):
        self.imageLocation = image_loc
        self.screen = screen_to_render_on
        self.foodList = []
        self.create_food(snake_object)

    def create_food(self, snake_object):

        x = random.randint(1, 13) * 24  # X 24 to make it fit exactly to the grid
        y = random.randint(1, 9) * 24
        pos = [x, y]

        while self.is_inside(snake_object, pos) is True:
            x = random.randint(1, 13) * 24  # X 24 to make it fit exactly to the grid
            y = random.randint(1, 9) * 24
            pos = [x, y]

        self.foodList.append(Food(pos, self.imageLocation, self.screen))

    def is_inside(self, snake_object, pos):

        is_inside_something = False
        for node in snake_object.nodes:
            if node.position == pos:
                is_inside_something = True

        for food in self.foodList:
            if food.position == pos:
                is_inside_something = True

        return is_inside_something

    def remove_food_by_pos(self, pos):

        # Find the food we need and delete
        for food in self.foodList:
            if pos == food.position:
                self.foodList.remove(food)

    def remove_food_by_ref(self, food):
        self.foodList.remove(food)

    def render(self):
        for food in self.foodList:
            food.render()


class GameManager:
    def __init__(self, snake_object, screen_object, food_manager, font_object, wid, hig):
        self.gameTick = 0
        self.addQueue = [0, 0]
        self.addQueueGameTick = 999999999
        self.snake = snake_object
        self.screen = screen_object
        self.speed = [0, 0]
        self.state = 'right'
        self.prevState = 'up'
        self.fm = food_manager
        self.isAlive = True
        self.score = 0
        self.font = font_object
        self.width = wid
        self.height = hig

    def game_cycle(self):
        if self.isAlive is True:
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
            current_speed = self.speed

            self.screen.fill([0, 0, 0])
            self.snake.update_positions()
            self.set_speed(current_speed)
            if self.gameTick % 12 == 0:
                self.check_if_food_has_been_eaten()

                # Check if the game should end
                if self.snake.is_inside_self_or_outside_region(width, height) is True:
                    self.isAlive = False

            if self.gameTick % 100 == 0:
                self.fm.create_food(self.snake)
            self.fm.render()
            self.snake.render()
            self.spawn_new_nodes()

            pygame.display.flip()

            self.gameTick += 1
        else:
            self.render_score()

    def set_speed(self, current_speed):

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
                self.speed = current_speed
            self.snake.update_speed(self.speed)
        else:
            self.speed = current_speed

    def spawn_new_nodes(self):
        if self.gameTick == self.addQueueGameTick + 10:
            self.snake.add_node(self.addQueue)
            self.addQueueGameTick = 0

    def add_node_to_queue(self, position, gt):
        self.addQueue = position
        self.addQueueGameTick = gt

    def check_if_food_has_been_eaten(self):
        for food in self.fm.foodList:
            if food.position == self.snake.nodes[0].position:
                self.add_node_to_queue(self.snake.nodes[len(self.snake.nodes) - 1].position[:], self.gameTick)
                self.fm.remove_food_by_ref(food)
                self.score += 1

    def render_score(self):
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
        death_text = font.render("Oh no you died!", 1, (255, 255, 255))
        score_text = font.render("Score: " + str(self.score), 1, (255, 255, 255))
        restart_text = font.render("SPACE to retry.", 1, (255, 255, 255))
        self.screen.blit(death_text, (50, 50))
        self.screen.blit(score_text, (50, 100))
        self.screen.blit(restart_text, (50, 150))
        pygame.display.flip()


pygame.init()
font = pygame.font.Font("Resources/SanFran.ttf", 30)

size = width, height = 312, 240

screen = pygame.display.set_mode(size)

snake = SnakeBody([0, 0], 'Resources/square_white_24_ns.bmp', screen)

foodManager = FoodManager('Resources/square_green.bmp', screen, snake)

gm = GameManager(snake, screen, foodManager, font, width, height)

while 1:
    gm.game_cycle()
