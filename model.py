import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

# Define the neural network class for Q-learning
class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # Define the first linear layer (input to hidden)
        self.linear1 = nn.Linear(input_size, hidden_size)
        # Define the second linear layer (hidden to output)
        self.linear2 = nn.Linear(hidden_size, output_size)

    # Define the forward pass of the network
    def forward(self, x):
        # Pass through the first layer and apply ReLU activation
        x = F.relu(self.linear1(x))
        # Pass through the second layer to get the output
        x = self.linear2(x)
        return x

    # Method to save the model parameters
    def save(self, file_name='model.pth'):
        # model_folder_path = './model'
        # # Create the directory if it doesn't exist
        # if not os.path.exists(model_folder_path):
        #     os.makedirs(model_folder_path)
        #
        # # Full path to save the model
        # file_name = os.path.join(model_folder_path, file_name)
        # # Save the model state dictionary
        # torch.save(self.state_dict(), file_name)
        return


# Define the QTrainer class to train the model
class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        # Use Adam optimizer with the specified learning rate
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        # Mean Squared Error loss function
        self.criterion = nn.MSELoss()

    # Method to perform a single training step
    def train_step(self, state, action, reward, next_state, done):
        # Convert states, actions, and rewards to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # Ensure tensors are 2D if they are 1D (for single experience)
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: Get the predicted Q-values for the current state
        pred = self.model(state)

        # Clone the predictions to use as the target
        target = pred.clone()
        # Update the target Q-values
        for idx in range(len(done)):
            Q_new = reward[idx]
            # Update Q_new if the episode is not done
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # Update the target value for the taken action
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # 2: Calculate the loss between target and predicted Q-values
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        # Backpropagate the loss
        loss.backward()

        # Perform an optimization step
        self.optimizer.step()
