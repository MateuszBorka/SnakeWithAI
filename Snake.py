import pygame
import time
import random
import numpy as np


class SnakeGame:
    def __init__(self):
        self.frame_iteration = 0
        self.game_speed = 50
        self.window_size_x = 320
        self.window_size_y = 240
        self.BACKGROUND_COLOR = pygame.Color(50, 51, 50)
        self.FINAL_SCORE_COLOR = pygame.Color(255, 255, 255)
        self.SCORE_COLOR = pygame.Color(255, 255, 255)
        self.FRUIT_COLOR = pygame.Color(255, 0, 0)
        self.SNAKE_COLOR = pygame.Color(50, 205, 50)

        pygame.init()
        pygame.display.set_caption('Snake')
        self.main_window = pygame.display.set_mode((self.window_size_x, self.window_size_y))
        self.speed = pygame.time.Clock()

        self.reset()

    def reset(self):
        # self.snake_head_position = [300, 300]
        # self.snake_body = [[300, 300], [290, 300], [280, 300]]
        self.frame_iteration = 0
        self.snake_head_position = [40, 40]
        self.snake_body = [[40, 40], [30, 40], [20, 40]]
        self.fruit_position = self.random_fruit_position()
        self.fruit_alive = True
        self.direction = 'RIGHT'
        self.next_direction = self.direction
        self.score = 0

    def random_fruit_position(self):
        while True:
            fruit_position = [random.randrange(2, (self.window_size_x // 10 - 1)) * 10, random.randrange(2, (self.window_size_y // 10 - 1)) * 10]
            if fruit_position not in self.snake_body:
                return fruit_position


    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect(center=(self.window_size_x // 2, 20))
        self.main_window.blit(score_surface, score_rect)

    def game_over(self):
        game_loss_score_font = pygame.font.SysFont('impact', 60)
        game_over_surface = game_loss_score_font.render(
            'Final Score is : ' + str(self.score) + "!", True, self.FINAL_SCORE_COLOR)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_size_x / 2, self.window_size_y / 4)
        self.main_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        quit()

    def update_direction(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.next_direction = 'UP'
                if event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.next_direction = 'DOWN'
                if event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.next_direction = 'LEFT'
                if event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.next_direction = 'RIGHT'

    def move_snake(self, action):
        # [straight, right, left]

        # clock_wise = [1, 4, 2, 3]
        clock_wise = ["RIGHT", "DOWN", "LEFT", "UP"]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        if self.direction == "UP":
            self.snake_head_position[1] -= 10
        if self.direction == "DOWN":
            self.snake_head_position[1] += 10
        if self.direction == "LEFT":
            self.snake_head_position[0] -= 10
        if self.direction == "RIGHT":
            self.snake_head_position[0] += 10

        # if self.next_direction == 'UP' and self.direction != 'DOWN':
        #     self.direction = 'UP'
        # if self.next_direction == 'DOWN' and self.direction != 'UP':
        #     self.direction = 'DOWN'
        # if self.next_direction == 'LEFT' and self.direction != 'RIGHT':
        #     self.direction = 'LEFT'
        # if self.next_direction == 'RIGHT' and self.direction != 'LEFT':
        #     self.direction = 'RIGHT'

        # if self.direction == 'UP':
        #     self.snake_head_position[1] -= 10
        # if self.direction == 'DOWN':
        #     self.snake_head_position[1] += 10
        # if self.direction == 'LEFT':
        #     self.snake_head_position[0] -= 10
        # if self.direction == 'RIGHT':
        #     self.snake_head_position[0] += 10

    def update_snake_body(self):
        self.snake_body.insert(0, list(self.snake_head_position))
        if self.snake_head_position[0] == self.fruit_position[0] and self.snake_head_position[1] == self.fruit_position[
            1]:
            self.score += 1
            self.fruit_alive = False
        else:
            self.snake_body.pop()

    def check_fruit_status(self):
        if not self.fruit_alive:
            self.fruit_position = self.random_fruit_position()
        self.fruit_alive = True

    def check_collision(self, pt = None):

        if pt is None:
            pt = self.snake_head_position
        if pt[0] < 0 or pt[0] > self.window_size_x - 10:
            return True
        if pt[1] < 0 or pt[1] > self.window_size_y - 10:
            return True

        for block in self.snake_body[1:]:
            if pt[0] == block[0] and pt[1] == block[1]:
                return True
        return False

    def draw_elements(self):
        self.main_window.fill(self.BACKGROUND_COLOR)
        for snake_block in self.snake_body:
            pygame.draw.rect(self.main_window, self.SNAKE_COLOR,
                             pygame.Rect(snake_block[0], snake_block[1], 10, 10))
        pygame.draw.rect(self.main_window, self.FRUIT_COLOR, pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], 10, 10))
        self.show_score(self.SCORE_COLOR, 'impact', 20)
        pygame.display.update()

    def play_step(self, action):
        self.frame_iteration += 1
        self.update_direction()
        self.move_snake(action)
        self.update_snake_body()
        reward = 0
        if self.fruit_alive == False:
            reward = 10
        self.check_fruit_status()

        self.draw_elements()
        self.speed.tick(self.game_speed)

        game_over = False
        if self.check_collision() or self.frame_iteration > 100*len(self.snake_body):
            game_over = True;
            reward = -10

        return reward, game_over, self.score


if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        if game_over:
            game.reset()
