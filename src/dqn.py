"""
The DQN class defines the neural network architecture.
The ReplayBuffer class is used to store and sample experiences for training.
The DQNAgent class implements the DQN algorithm, including the training procedure and experience replay.
The agent interacts with the environment, collects experiences, and updates the neural network parameters to learn the Q-values.
"""
import numpy as np
import tensorflow as tf
from collections import deque
import interface
import config



class DQN(tf.keras.Model):
    """ Define the neural network architecture """
    def __init__(self, num_actions): 
        """ No. of actions the agent can take """
        super(DQN, self).__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(64, activation='relu')
        self.dense3 = tf.keras.layers.Dense(num_actions) 

    def call(self, state):
        """ Forward pass of the NN """
        x = self.dense1(state)
        x = self.dense2(x)
        return self.dense3(x)

class ReplayBuffer: 
    """ To store sample experiences for training --> [S,A,R,N,D] -- experience """
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        """ Adds new experiences to the buffer """
        self.buffer.append(experience)

    def sample(self, batch_size):
        """Retrives random batch of experiences for the training"""
        idx = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in idx]

class DQNAgent:
    """ Define the Deep Q-Network algorithm"""
    def __init__(self, num_actions, state_dim):
        """Initialize set of parameters for the NN model"""
        self.num_actions = num_actions
        self.state_dim = state_dim
        self.model = DQN(num_actions)
        self.target_model = DQN(num_actions)
        self.target_model.set_weights(self.model.get_weights())
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
        self.replay_buffer = ReplayBuffer(max_size=10000)
        self.gamma = 0.99 # Discount factor
        self.epsilon = 1.0 # Exploration factor vs exploitation- initially 1 coz it has to fully explore!
        self.epsilon_decay = 0.999 # Reduce exploration rate over time, allows exploration for longer time
        self.epsilon_min = 0.01 # Min. exploration rate at which the decay should stop, to avoid becoming overly greedy
        self.batch_size = 32 # No. of experiences it needs to process at same time, larger is better but will cost computation power
    
    def act(self, state): 
        """Chooses action based on epsilon greedy policy - Explore & Exploit"""
        if np.random.rand() < self.epsilon: # Explore
            return np.random.choice(self.num_actions) # Random action chosen for prob. epsilon
        else: # Exploit
            q_values = self.model.predict(np.array([state]))
            return np.argmax(q_values[0]) # Or action with highest Q-Value is chosen

    def update_target_model(self):
        """Updates weights of target n/w from the main n/w"""
        self.target_model.set_weights(self.model.get_weights())

    def train(self):
        """1 training cycle"""
        if len(self.replay_buffer.buffer) < self.batch_size:
            return

        minibatch = self.replay_buffer.sample(self.batch_size)
        states = np.array([experience[0] for experience in minibatch])
        actions = np.array([experience[1] for experience in minibatch])
        rewards = np.array([experience[2] for experience in minibatch])
        next_states = np.array([experience[3] for experience in minibatch])
        dones = np.array([experience[4] for experience in minibatch])

        # Q-Values from the target(to-be-finalized) model
        predicted_value = self.target_model.predict(next_states)
        print(predicted_value)
        target = rewards + (1 - dones) * self.gamma * np.amax( predicted_value, axis=1)

        target_f = self.model.predict(states) # Actions from main model (latest trained)
        target_f[np.arange(self.batch_size), actions] = target # Maps the experiences with 

        self.model.train_on_batch(states, target_f)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

###########################################################################
# Initialize the DQN agent
#tf.debugging.set_log_device_placement(True) #To fetch GPU automatically
agent = DQNAgent(num_actions = 435, state_dim = 30)

data = interface.collect_data()

# Train the DQN agent
for episode in range(20): # No. of episodes
    
    
    # Initial state - To be initialized
    state =  config.layout.alphabetical
    print(state)

    keyboard = interface.KeyboardConfig(state, 
                                        config.coordinate_grid.standard, 
                                        config.hand_placement.home_row_us)

    env = interface.Environment(keyboard_config = keyboard, max_iterations = 500, data=data)
    done = False
    epoch = 1
    while not done:
        action = agent.act(state)
        next_state, reward, done, stats = env.step(action) 
        agent.replay_buffer.add((state, action, reward, next_state, done))
        state = next_state
        agent.train()
        print("------------EPOCH - ",epoch,"------------")
        
        epoch += 1
    agent.update_target_model()
###########################################################################