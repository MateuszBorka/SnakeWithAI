import pygame
import time
import random

game_speed = 15
window_size_x = 800
window_size_y = 600

BACKGROUND_COLOR = pygame.Color(50, 51, 50)
FINAL_SCORE_COLOR = pygame.Color(255, 255, 255)
SCORE_COLOR = pygame.Color(255, 255, 255)
FRUIT_COLOR = pygame.Color(255, 0, 0)
SNAKE_COLOR = pygame.Color(50, 205, 50)

pygame.init()
pygame.display.set_caption('Snake')
main_window = pygame.display.set_mode((window_size_x, window_size_y))

speed = pygame.time.Clock()

snake_head_position = [300, 300]

snake_body = [[300, 300],
              [290, 300],
              [280, 300],
              ]
fruit_position = [random.randrange(1, (window_size_x // 10)) * 10,
                  random.randrange(1, (window_size_y // 10)) * 10]

fruit_alive = True

direction = 'RIGHT'
next_direction = direction

score = 0


def show_score(color, font, size):

    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)

    score_rect = score_surface.get_rect(center=(window_size_x // 2, 20))

    main_window.blit(score_surface, score_rect)


def game_over():
    game_loss_score_font = pygame.font.SysFont('impact', 60)

    game_over_surface = game_loss_score_font.render(
        'Final Score is : ' + str(score) + "!", True, FINAL_SCORE_COLOR)

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (window_size_x / 2, window_size_y / 4)

    main_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(5)

    pygame.quit()
    quit()


while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                next_direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                next_direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                next_direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                next_direction = 'RIGHT'

    if next_direction == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if next_direction == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if next_direction == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if next_direction == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_head_position[1] -= 10
    if direction == 'DOWN':
        snake_head_position[1] += 10
    if direction == 'LEFT':
        snake_head_position[0] -= 10
    if direction == 'RIGHT':
        snake_head_position[0] += 10

    snake_body.insert(0, list(snake_head_position))
    if snake_head_position[0] == fruit_position[0] and snake_head_position[1] == fruit_position[1]:
        score += 1
        fruit_alive = False
    else:
        snake_body.pop()

    if not fruit_alive:
        fruit_position = [random.randrange(1, (window_size_x // 10)) * 10,
                          random.randrange(1, (window_size_y // 10)) * 10]

    fruit_alive = True
    main_window.fill(BACKGROUND_COLOR)

    for snake_block in snake_body:
        pygame.draw.rect(main_window, SNAKE_COLOR,
                         pygame.Rect(snake_block[0], snake_block[1], 10, 10))
    pygame.draw.rect(main_window, FRUIT_COLOR, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    if snake_head_position[0] < 0 or snake_head_position[0] > window_size_x - 10:
        game_over()
    if snake_head_position[1] < 0 or snake_head_position[1] > window_size_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_head_position[0] == block[0] and snake_head_position[1] == block[1]:
            game_over()

    show_score(SCORE_COLOR, 'impact', 20)

    pygame.display.update()

    speed.tick(game_speed)