import random
import pygame
from pygame import mixer


class Snake:
    def __init__(self, color):
        self.color = color
        self.x1 = self.y1 = 300
        self.change_x1 = self.change_y1 = 0
        self.length = 1
        self.snake_list = []
        self.snake_head = []


    def drawSnake(self, screen):
        self.x1 += self.change_x1
        self.y1 += self.change_y1

        self.snake_head = [self.x1, self.y1]
        self.snake_list.append(self.snake_head)

        if len(self.snake_list) > self.length:
            del self.snake_list[0]

        # actually draw the snake
        for x in self.snake_list:
            pygame.draw.rect(screen, self.color, [x[0], x[1], 10.0, 10.0])

    def move(self, screen):
        # tracking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # tracking keyboard events
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.change_x1 = -10
                    self.change_y1 = 0
                elif keys[pygame.K_RIGHT]:
                    self.change_x1 = 10
                    self.change_y1 = 0
                elif keys[pygame.K_UP]:
                    self.change_x1 = 0
                    self.change_y1 = -10
                elif keys[pygame.K_DOWN]:
                    self.change_x1 = 0
                    self.change_y1 = 10
                elif keys[pygame.K_ESCAPE]:
                    return "quit"

        # if the snake hits the edge
        if self.x1 >= 500 or self.x1 < 0 or self.y1 >= 500 or self.y1 < 0:
            my_font = pygame.font.SysFont("monospace", 30)
            lose = my_font.render("GAME OVER", 1, RED)
            screen.blit(lose, (100, 100))
            # stop snake from moving
            self.change_x1 = 0
            self.change_y1 = 0

        if len(self.snake_list) > 1:
            for x in self.snake_list[:-1]:
                if x == self.snake_head:
                    my_font = pygame.font.SysFont("monospace", 30)
                    lose = my_font.render("GAME OVER", 1, RED)
                    screen.blit(lose, (100, 100))
                    # stop snake from moving
                    self.change_x1 = 0
                    self.change_y1 = 0
        return None


class Apple:
    def __init__(self, color):
        self.color = color
        self.food_x = round(random.randrange(0, 500 - 10) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, 500 - 10) / 10.0) * 10.0
        self.food_eaten = 0

    def drawApple(self, screen, eaten):
        if eaten:
            self.food_x = round(random.randrange(0, 500 - 10) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, 500 - 10) / 10.0) * 10.0
        pygame.draw.rect(screen, self.color, [self.food_x, self.food_y, 10, 10])

    def foodEaten(self):
        return self.food_eaten


def drawScore(numSnakes, screen):
    # initialize font
    my_font = pygame.font.SysFont("monospace", 30)
    # render text
    label = my_font.render("Score: " + str(numSnakes), 1, BLUE)
    screen.blit(label, (10, 10))


def displayScreen():
    screen = pygame.display.set_mode((500, 500))
    screen.fill(BLACK)
    pygame.display.set_caption('Snake Game')
    return screen


def main():
    # mixer init
    mixer.init()

    # set up pygame
    pygame.init()
    clock = pygame.time.Clock()

    # define global colors
    global BLACK, RED, GREEN, BLUE
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # set up screen
    screen = displayScreen()

    # create snake and apple objects
    snake = Snake(GREEN)
    apple = Apple(RED)

    # boolean to determine if apple has been eaten
    eaten = False

    while True:
        # allows us to redraw with updates screen
        screen.fill(BLACK)

        # get snake movements with keyboard clicks
        move = snake.move(screen)
        # if the esc button was pushed
        if move == 'quit':
            break

        # draw snake
        snake.drawSnake(screen)

        # draw apple
        apple.drawApple(screen, eaten)
        # set eaten back to false
        eaten = False
        # check if the apple has been eaten
        if snake.x1 == apple.food_x and snake.y1 == apple.food_y:
            eaten = True
            apple.food_eaten += 1  # increase food eaten
            snake.length += 1  # increase snake length
            mixer.music.load('Chomp.mp3')
            mixer.music.play()

        # display the score
        drawScore(apple.food_eaten, screen)

        # update the screen
        clock.tick(30)
        pygame.display.update()

    pygame.quit()
    quit()


main()
