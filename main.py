import pygame
import random

# snake game snake game

# initialize game
pygame.init()

# sets display window bounds and title
displayWindow_width = 600
displayWindow_height = 600
displayWindow = pygame.display.set_mode((displayWindow_width, displayWindow_height))

pygame.display.set_caption("me when I'm playing snake")

# game colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# game over image
img = pygame.image.load('cover10.jpeg')     # loads the game over image from files
img = pygame.transform.scale(img, (displayWindow_width, displayWindow_height))      # scales the image so it fits the screen

# the game

# snake stuff
snake_block = 10    # length of each square that makes the snake
snake_speed = 30    # vroom

clock = pygame.time.Clock()     # creates a frame rate for game

# message stuff
font_size = int(displayWindow_height / 12)
font_style = pygame.font.SysFont(None, font_size)       # Game over font --- None makes it the default font, size adjusts to screen size
score_font = pygame.font.SysFont(None, int(font_size * 0.7))      # Score font --- None makes it the default font, size adjusts to screen size

# definitions of gameplay functions

def your_score(score):
    value = score_font.render("Your Score: " + str(score - 3), True, red)    # Your score minus starting snake length
    displayWindow.blit(value, [0, 0])

def message(msg, color):     # renders the message
    max_width = displayWindow_width * 0.8    # max width of the message is 80% of screen size
    font_size = int(displayWindow_height / 12)
    font_style = pygame.font.SysFont(None, font_size)
    mesg = font_style.render(msg, True, color)
    text_width = mesg.get_rect().width   # gets the width of the message

    while text_width > max_width:   # while the width of the message is greater than the max width
        font_size -= 1
        font_style = pygame.font.SysFont(None, font_size)
        mesg = font_style.render(msg, True, color)
        text_width = mesg.get_rect().width

    # centers the text
    text_height = mesg.get_rect().height
    text_x = (displayWindow_width - text_width) / 2
    text_y = (displayWindow_height - text_height) / 2

    displayWindow.blit(mesg, [text_x, text_y])

def our_snake(snake_block, snake_list):  # puts the snake on the screen
    for x in snake_list:
        pygame.draw.rect(displayWindow, blue, [x[0], x[1], snake_block, snake_block])

def our_food(snake_block , food_list):  # puts the food on the screen
    for x in food_list:
        pygame.draw.rect(displayWindow, green, [x[0], x[1], snake_block, snake_block])

def game_loop():    # main game loop
    game_over = False
    game_close = False

    # position stuff
    x1 = displayWindow_width / 2     # starting/current positions, dividing both by 2 puts you in the middle
    y1 = displayWindow_height / 2
    x1_change = 0     # adds to the current position to move location
    y1_change = 0
    prev_x1 = x1      # previous x1 and y1 makes it so you cannot go backwards and instantly end the game
    prev_y1 = y1

    length_of_snake = 5
    snake_list = [[x1, y1]]    # spawns the snake head
    direction_changes = []  # list of direction changes

    tail_added = False   # prevents snake from killing itself at the start of the game

    # random food spawner
    foodx = round(random.randrange(0, displayWindow_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, displayWindow_height - snake_block) / 10.0) * 10.0

    frame_count = 0    # increments so snake cannot instantly die in first 5 frames

    # gameplay loop
    while not game_over:
        input_taken = False      # one input per frame

        for event in pygame.event.get():

            if event.type == pygame.QUIT:   # makes the close button work, ends the game
                game_over = True

            if event.type == pygame.KEYDOWN and not input_taken:
                if (x1 != prev_x1 or y1 != prev_y1) and not tail_added:
                    for i in range(1, length_of_snake):
                        snake_list.insert(0, [x1 + i * snake_block, y1])
                tail_added = True

                if event.key == pygame.K_LEFT and x1_change == 0:     # applies values to add to current position based on direction you want to go
                    direction_changes.append((-snake_block, 0))     # adds to the direction changes list

                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    direction_changes.append((snake_block, 0))     # adds to the direction changes list

                elif event.key == pygame.K_UP and y1_change == 0:
                    direction_changes.append((0, -snake_block))     # adds to the direction changes list

                elif event.key == pygame.K_DOWN and y1_change == 0:
                    direction_changes.append((0, snake_block))     # adds to the direction changes list

                input_taken = True

            prev_x1 = x1
            prev_y1 = y1

            if direction_changes:
                x1_change, y1_change = direction_changes.pop()     # pops the first element of the direction changes list to update the direction (get rid of if breaking)

        if x1 + x1_change >= displayWindow_width or x1 + x1_change < 0 or y1 + y1_change >= displayWindow_height or y1 + y1_change < 0:
            game_close = True

        x1 += x1_change    # adds direction you want to go to current to update position
        y1 += y1_change

        if frame_count > 5 and (x1_change != 0 or y1_change != 0) and length_of_snake > 5:
            for x in snake_list[:-1]:
                if x == [x1, y1]:
                    game_close = True

        snake_list.append([x1, y1])

        if len(snake_list) > length_of_snake and not (x1 == foodx and y1 == foody):
            del snake_list[0]   # deletes the first element of the snake list, which is the tail

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, displayWindow_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, displayWindow_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        food_list = [[foodx, foody]]

        while game_close == True:
            displayWindow.fill(white)
            displayWindow.blit(img, (0, 0))
            message("skill issue     C - go again     Q - quit", red)
            your_score(length_of_snake - 1)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # if press Q, game closes
                        game_over = True
                        game_close = False

                    if event.key == pygame.K_c:   # if press C, game starts again
                        game_loop()

        displayWindow.fill(white)     # backgrounds white now

        our_snake(snake_block, snake_list)  # puts the snake on the screen

        our_food(snake_block, food_list)    # puts the food on the screen

        your_score(length_of_snake - 1)     # shows the score

        pygame.display.update()       # update the game's screen to show changes

        frame_count += 1

        clock.tick(snake_speed)     # makes the frame rate go as fast as the snake is moving

    # ends the game, closes window
    pygame.quit()
    quit()

game_loop()


game_loop()
