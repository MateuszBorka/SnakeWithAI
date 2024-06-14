import torch
import random
import numpy as np
from collections import deque
from Snake import SnakeGame
from model import Linear_QNet, QTrainer
from helper import plot

# Constants
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class SnakeAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # Randomness factor
        self.gamma = 0.9  # Discount rate for future rewards
        self.memory = deque(maxlen=MAX_MEMORY)  # Memory buffer
        self.model = Linear_QNet(11, 256, 3) # input, hidden, output layers
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake_head_position
        # Define points around the snake head
        point_l = (head[0] - 20, head[1])
        point_r = (head[0] + 20, head[1])
        point_u = (head[0], head[1] - 20)
        point_d = (head[0], head[1] + 20)

        # Check snake direction
        dir_l = game.direction == "LEFT"
        dir_r = game.direction == "RIGHT"
        dir_u = game.direction == "UP"
        dir_d = game.direction == "DOWN"

        # Create state representation
        state = [
            # Danger straight
            (dir_l and game.check_collision(point_l)) or
            (dir_u and game.check_collision(point_u)) or
            (dir_d and game.check_collision(point_d)),

            # Danger right
            (dir_u and game.check_collision(point_r)) or
            (dir_d and game.check_collision(point_l)) or
            (dir_l and game.check_collision(point_u)) or
            (dir_r and game.check_collision(point_d)),

            # Danger left
            (dir_d and game.check_collision(point_r)) or
            (dir_u and game.check_collision(point_l)) or
            (dir_r and game.check_collision(point_u)) or
            (dir_l and game.check_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.fruit_position[0] < head[0],  # Food left
            game.fruit_position[0] > head[0],  # Food right
            game.fruit_position[1] < head[1],  # Food up
            game.fruit_position[1] > head[1]  # Food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # Add experience to memory

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # Sample a mini-batch
        else:
            mini_sample = list(self.memory)

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = max(0, 80 - self.n_games)  # Decrease epsilon over time
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train_agent():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = SnakeAgent()
    game = SnakeGame()

    while True:
        state_old = agent.get_state(game)  # Get current state
        final_move = agent.get_action(state_old)  # Decide action

        reward, done, score = game.play_step(final_move)  # Perform action
        state_new = agent.get_state(game)  # Get new state

        agent.train_short_memory(state_old, final_move, reward, state_new, done)  # Train short term
        agent.remember(state_old, final_move, reward, state_new, done)  # Store experience

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()  # Train long term memory

            if score > record:
                record = score
                agent.model.save()

            print(f'Game {agent.n_games} | Score: {score} | Record: {record}')

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train_agent()
