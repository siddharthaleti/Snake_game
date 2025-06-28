import pygame
import time
import random

pygame.init()

# Screen size
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game with Levels & Through Walls')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red   = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

block_size = 20
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 25)

def your_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    screen.blit(value, [0, 0])

def our_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], block_size, block_size])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(width/2, height/2 + y_offset))
    screen.blit(mesg, text_rect)

def choose_difficulty():
    choosing = True
    while choosing:
        screen.fill(black)
        message("Choose difficulty:", yellow, -60)
        message("E - Easy", white, -20)
        message("M - Medium", white, 20)
        message("H - Hard", white, 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 10
                elif event.key == pygame.K_m:
                    return 15
                elif event.key == pygame.K_h:
                    return 25

def game_loop(snake_speed):
    game_over = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0

        # Move snake head
        x1 += x1_change
        y1 += y1_change

        # Through walls: wrap coordinates if out of bounds
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - block_size
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - block_size

        screen.fill(black)
        pygame.draw.rect(screen, red, [foodx, foody, block_size, block_size])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check self collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

        our_snake(block_size, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            length_of_snake += 1

        clock.tick(snake_speed)

    # Game over screen
    screen.fill(black)
    message("You Lost! Press C to Play Again or Q to Quit", red, -20)
    your_score(length_of_snake - 1)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    main()

def main():
    snake_speed = choose_difficulty()
    game_loop(snake_speed)

main()
