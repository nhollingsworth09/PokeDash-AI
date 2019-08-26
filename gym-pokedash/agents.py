import gym
import gym_pokedash
import numpy as np
import matplotlib as plt
import seaborn as sns
import pandas as pd
import pygame

from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam, Adagrad
 
 
 
 # Deep Q-learning Agent
class DQNAgent:
     def __init__(self, state_size, action_size):
         self.state_size = state_size
         self.action_size = action_size
         self.memory = deque(maxlen=1000000)
         self.gamma = 0.95    # discount rate
         self.epsilon = 0.1  # exploration rate
         self.epsilon_min = 0.01
         self.epsilon_decay = 0.995
         self.learning_rate = 0.001
         self.model = self._build_model()
         
     def _build_model(self):
         # Neural Net for Deep-Q learning Model
         model = Sequential()
         model.add(Dense(18, input_dim=self.state_size, activation='relu'))
         model.add(Dense(9, activation='relu'))
         model.add(Dense(self.action_size, activation='linear'))
         model.compile(loss='mse',
                       optimizer=Adagrad(lr=self.learning_rate))
         return model
     
     def remember(self, state, action, reward, next_state, done):
         self.memory.append((state, action, reward, next_state, done))
         
     def act(self, env, state):
         if np.random.rand() <= self.epsilon:
             return env.action_space.sample()
         act_values = self.model.predict(np.array(state).reshape([1,self.state_size]))
         return np.argmax(act_values[0])  # returns action
     
     def replay(self, batch_size):
         minibatch = deque([self.memory[i] for i in np.random.choice(range(len(self.memory)), batch_size)])
         
         states = np.zeros((batch_size, self.state_size))
         actions, rewards, dones = [], [], []
         
         for i in range(batch_size):
             states[i] = minibatch[i][0]
             actions.append(minibatch[i][1])
             rewards.append(minibatch[i][2])
             dones.append(minibatch[i][4])
             
         target = self.model.predict(states)
         
         for i in range(batch_size):
             if dones[i]:
                 target[i][actions[i]] = rewards[i]
             else:
                 target[i][actions[i]] = rewards[i] + self.gamma * np.amax(target[i])
                 
         self.model.fit(states, target, batch_size = batch_size, epochs=1, verbose=0)
                                        
# =============================================================================
#          for state, action, reward, next_state, done in minibatch:
#              target = reward
#              if not done:
#                target = reward + self.gamma * np.amax(self.model.predict(np.array(state).reshape([1,4])))
#              target_f = self.model.predict(np.array(state).reshape([1,4]))
#              target_f[0][action] = target
#          self.model.fit(np.array(state).reshape([1,4]), target_f, epochs=1, verbose=0)
# =============================================================================
         
         if self.epsilon > self.epsilon_min:
             self.epsilon *= self.epsilon_decay


class ModelAgent:
     def __init__(self, state_size, action_size):
         self.state_size = state_size
         self.action_size = action_size
         self.memory = deque(maxlen=100000)
         self.gamma = 0.95    # discount rate
         self.epsilon = 0.1  # exploration rate
         self.epsilon_min = 0.01
         self.epsilon_decay = 0.995
         self.learning_rate = 0.001
         self.model = self._build_model()
         
     def _build_model(self):
         '''
         Use to load a saved model from the DQN process
         '''
         # Neural Net for Deep-Q learning Model
         from keras.models import load_model
         
         model = load_model('./best_player_3031.h5')
         
         return model
     
     def remember(self, state, action, reward, next_state, done):
         self.memory.append((state, action, reward, next_state, done))
         
     def act(self, env, state):
         if np.random.rand() <= self.epsilon:
             return env.action_space.sample()
         act_values = self.model.predict(np.array(state).reshape([1,3]))
         return np.argmax(act_values[0])  # returns action
     
     def replay(self, batch_size):
         minibatch = deque([self.memory[i] for i in np.random.choice(range(len(self.memory)), batch_size)])
         
         states = np.zeros((batch_size, self.state_size))
         actions, rewards, dones = [], [], []
         
         for i in range(batch_size):
             states[i] = minibatch[i][0]
             actions.append(minibatch[i][1])
             rewards.append(minibatch[i][2])
             dones.append(minibatch[i][4])
             
         target = self.model.predict(states)
         
         for i in range(batch_size):
             if dones[i]:
                 target[i][actions[i]] = rewards[i]
             else:
                 target[i][actions[i]] = rewards[i] + self.gamma * np.amax(target[i])
                 
         self.model.fit(states, target, batch_size = batch_size, epochs=1, verbose=0)
                                        
         
         if self.epsilon > self.epsilon_min:
             self.epsilon *= self.epsilon_decay

def model_agent(games = 10, frames = 5000):
    global history
    history = []
    agent = ModelAgent(4,2)
    
    for __ in range(games):
        
        env = gym.make("PokeDash-v0")
        state = env.reset()
        
        for e in range(frames):
            action = agent.act(env, state)
            
            next_state, reward, done = env.step(action)
            env.render(mode = 'human')
            
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:
                print('Game: {}/{}, Score: {}'.format(__+1, games, env.pika.score))
                break
                   
    pygame.quit()

def random_agent(games = 20, episodes = 800):
    for __ in range(games):
        env = gym.make("PokeDash-v0")
        state = env.reset()
        for e in range(episodes):
            action = env.action_space.sample()
            next_state, reward, done = env.step(action)
            env.render(mode = 'human')
        
            state = next_state
            if done:
                print('Game: {}/{}, Score: {}'.format(__+1, games, env.pika.score))
                break

def manual_agent(games = 2, episodes = 800):
    for __ in range(games):
        env = gym.make("PokeDash-v0")
        state = env.reset()
        for e in range(episodes):
            print(state[0])
            if state[0] <= 20  and env.pika.isJump == False:
                action = 1
            else:
                action = 0
            next_state, reward, done = env.step(action)
            env.render(mode = 'human')
        
            state = next_state

            if done:
                print('Game: {}/{}, Score: {}'.format(__+1, games, env.pika.score))
                break
    pygame.quit()

def dqn_agent(games = 1000, frames = 5000):
    global history
    history = []
    agent = DQNAgent(3,2)
    
    for __ in range(games):
        
        env = gym.make("PokeDash-v0")
        state = env.reset()
        
        for e in range(frames):
            action = agent.act(env, state)
            
            next_state, reward, done = env.step(action)
            env.render(mode = 'human')
            # Only remember frames after initial run up and passing the first obstacle
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            
            if done:
                print('Game: {}/{}, Score: {}'.format(__+1, games, env.pika.score))
                break
            
        history.append((__, env.pika.score))
        
        model_breakThrough = history[-1][1] == np.max([score for game, score in history])
        
        if model_breakThrough:
            agent.model.save('./best_player_{}.h5'.format(env.pika.score))
        else:
            pass
            
        agent.replay(np.min([len(agent.memory), 100]))
    pygame.quit()

if __name__ == "__main__":
    '''
    Uncomment the model you would like to run and comment all others. 
    Optionally, you can uncomment the Seaborn plot DQN model results at each iteration.
    '''
    #random_agent()
    #dqn_agent()
    model_agent()
    #manual_agent()
    
    #ax = sns.lineplot(pd.DataFrame(history).iloc[:,0], pd.DataFrame(history).iloc[:,1])
