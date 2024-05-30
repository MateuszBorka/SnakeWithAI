import pygame
import time
import random

class SnakeGame:
    def __init__(self):
        self.game_speed = 15
        self.window_size_x = 800
        self.window_size_y = 600
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
        self.snake_head_position = [300, 300]
        self.snake_body = [[300, 300], [290, 300], [280, 300]]
        self.fruit_position = self.random_fruit_position()
        self.fruit_alive = True
        self.direction = 'RIGHT'
        self.next_direction = self.direction
        self.score = 0

    def random_fruit_position(self):
        return [random.randrange(1, (self.window_size_x // 10)) * 10,
                random.randrange(1, (self.window_size_y // 10)) * 10]

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

    def move_snake(self):
        if self.next_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.next_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.next_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.next_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_head_position[1] -= 10
        if self.direction == 'DOWN':
            self.snake_head_position[1] += 10
        if self.direction == 'LEFT':
            self.snake_head_position[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_head_position[0] += 10

    def update_snake_body(self):
        self.snake_body.insert(0, list(self.snake_head_position))
        if self.snake_head_position[0] == self.fruit_position[0] and self.snake_head_position[1] == self.fruit_position[1]:
            self.score += 1
            self.fruit_alive = False
        else:
            self.snake_body.pop()

    def check_fruit_status(self):
        if not self.fruit_alive:
            self.fruit_position = self.random_fruit_position()
        self.fruit_alive = True

    def check_collision(self):
        if self.snake_head_position[0] < 0 or self.snake_head_position[0] > self.window_size_x - 10:
            return True
        if self.snake_head_position[1] < 0 or self.snake_head_position[1] > self.window_size_y - 10:
            return True

        for block in self.snake_body[1:]:
            if self.snake_head_position[0] == block[0] and self.snake_head_position[1] == block[1]:
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

    def play_step(self):
        self.update_direction()
        self.move_snake()
        self.update_snake_body()
        self.check_fruit_status()

        game_over = self.check_collision()
        self.draw_elements()
        self.speed.tick(self.game_speed)

        return game_over, self.score

if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        if game_over:
            game.reset()
