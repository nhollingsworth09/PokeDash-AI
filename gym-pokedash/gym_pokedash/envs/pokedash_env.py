import os

path = '.'
os.chdir(path)

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
from numpy import random
from gameObjects import Scoreboard, Player, Background, Cactus
from gameFunctions import gym_collided, collided, gameOver_msg, jumped, gym_jumped
import pygame
import numpy as np

pygame.init()

gameover_image = pygame.image.load('./assets/game_over.png')
subtitle_image = pygame.image.load('./assets/subtitle_over.png')

def GameWindow(win, backg, backg2): 
    win.fill((255,255,255))
    
    #-- Drawing backgrounds for infinite run illusion
    backg.bg_draw(win)
    backg.x -= backg.vel
    backg.rightx -= backg.vel

    backg2.bg_draw(win)
    backg2.x -= backg2.vel
    backg2.rightx -= backg2.vel

class PokeDashEnv(gym.Env):

    metadata = {'render.modes': ['human', 'console']}

    def __init__(self):
          
          self.gameSpeed = 20
          self.screen = (self.win_width, self.win_height) = (1000, 380)
          self.win = pygame.display.set_mode(self.screen)
          self.collision = None
          self.max_cacti = 3
          self.score = None
          self.pika = None
          self.playerCenter = [0, 271]
          self.cacts = None
          self.noi_pika = 4
          self.frames_per_second_pika = 14
          self.bg1 = Background('./sprites/background.png', 0, 280, self.gameSpeed)
          self.bg2 = Background('./sprites/background.png', 1200, 280, self.gameSpeed)
          self.clock = pygame.time.Clock()
          self.start_frame = time.time()
          self.last_cactus = time.time()
          self.action_space = spaces.Discrete(2)
         


    def step(self, action):
          
            #-- Lock player FPS
            self.action = action
            self.current_image_pika = int((time.time() - self.start_frame) * self.frames_per_second_pika % self.noi_pika)
            #-- Managing Cactus Production
            #- Randomly select initial x value to vary cactus distances
            rand_dist = random.choice([1005, 1035, 1055, 1155, 1175], 1, p = [0.20, 0.20, 0.20, 0.20, 0.20])
            
            #-- Game will learn only one cactus for now
            idx = 0
            #idx = random.randint(0,3)
            
            if len(self.cacts) < self.max_cacti and (time.time() - self.last_cactus) >= 1.25:
                self.cacts.append(Cactus(path, rand_dist, 175, self.gameSpeed, idx))
                
                self.last_cactus = time.time()
            
            for cact in self.cacts:
                if cact.onScreen == False:
                    self.cacts.pop(self.cacts.index(cact))
                elif cact.rightx <= 0:
                    cact.onScreen = False
                else:
                    cact.x -= cact.vel
                    cact.rightx -= cact.vel 
            
            reward = 0
            self.playerCenter = [int(self.pika.x+(self.pika.width/2)), int(self.pika.y+(self.pika.height/2))]
            
            if len(self.cacts) > 0:
                if self.cacts[0].rect[3] > self.pika.rect[0]:
                    #-- Collison
                    self.collision = gym_collided(self.pika.rect, self.cacts[0].rect)
                
                    if self.collision == True:      
                        self.pika.isDead = self.collision
                        
                    #- Reward Function: If player center is above obstacle AND between region of edges
                    condition_InRegion = self.playerCenter[0] > self.cacts[0].rect[0] - 20 and self.playerCenter[0] < self.cacts[0].rect[2] + 20
                    condition_Above = self.playerCenter[1] < self.cacts[0].rect[1]
                    
                    if self.playerCenter[1] < 271 and condition_InRegion[0] and condition_Above:
                        reward = 10
                    elif self.pika.isDead == True:
                        reward = -10
                    elif self.pika.isJump == False and self.playerCenter[1] == 271:
                        reward = 5
                    elif self.playerCenter[1] < 271 and not (condition_InRegion[0] and condition_Above):
                        reward = -5
                    else:
                        reward = 0
                else:
                    #-- Repeat above for the next obstacle
                    self.collision = gym_collided(self.pika.rect, self.cacts[1].rect)
                
                    if self.collision == True:      
                        self.pika.isDead = self.collision

                    condition_InRegion = self.playerCenter[0] > self.cacts[1].rect[0]  and self.playerCenter[0] < self.cacts[1].rect[2]
                    condition_Above = self.playerCenter[1] < self.cacts[1].rect[1]
                    
                    if self.pika.isJump and condition_InRegion[0] and condition_Above:
                        reward = 10
                    elif self.pika.isDead == True:
                        reward = -10
                    elif self.pika.isJump == False and self.playerCenter[1] == 271:
                        reward = 1
                    elif self.pika.isJump == True and not (condition_InRegion[0] and condition_Above):
                        reward = -5
                    else:
                        reward = 0
            
            self.pika.score += 1
            self.score.value = self.pika.score
                
            return self.game_state(), reward, self.pika.isDead
    	
    def reset(self):
            self.bg1 = Background('./sprites/background.png', 0, 280, self.gameSpeed)  
            self.bg2 = Background('./sprites/background.png', 1200, 280, self.gameSpeed)
            
            self.cacts = []
            self.score = Scoreboard(5,5)
            self.pika = Player(25, 255)
            
            self.start_frame = time.time()
            self.last_cactus = time.time()
            
            return self.game_state()
            

    def render(self, mode='console', close=False):
        if mode == 'console':            
            print(self.game_state())
            
            
        elif mode == 'human':
            
            if close:
                pygame.quit()
            else:
                GameWindow(self.win, self.bg1, self.bg2)
                self.win.blit(self.score.font.render('Score: %s' %self.score.value, 1, (0,0,0)), (self.score.x, self.score.y))
                self.clock.tick(30)
                
                gym_jumped(self.pika, self.win, self.current_image_pika, self.action)
                
                for cact in self.cacts:
                    if cact.onScreen == True:
                        cact.draw(self.win)       
                        
                pygame.display.update()
        
    def game_state(self):
# =============================================================================
              import collections
              state = {}
      
              def flatten(x):
                  if isinstance(x, collections.Iterable):
                      return [a for i in x for a in flatten(i)]
                  else:
                      return [x]
              
              if len(self.cacts) > 0:
                  '''
                  Below are tests for what to include in the domain space. Currently, object distance, player center location, and wether the player is jumping is included. Other variables considered is the gap between objects, and object information (for various objects).
                  '''
                  if self.cacts[0].rect[0] > self.pika.rect[3]:
                      state['dist_to_obstacle'] = flatten(self.cacts[0].rect[0] - self.pika.rect[3])
                      #state['dist_gap_obstacle'] = flatten(1200 - self.cacts[0].rect[2])
                      #state['obstacle_width'] = flatten(self.cacts[0].hitbox[2])
                      #state['obstacle_height'] = flatten(self.cacts[0].hitbox[3])
                  elif len(self.cacts) > 1 and self.cacts[0].rect[0] < self.pika.rect[3]:
                      state['dist_to_obstacle'  ] = flatten(self.cacts[1].rect[0] - self.pika.rect[3])
                      #state['dist_gap_obstacle'] = flatten(self.cacts[1].rect[2] - self.cacts[1].rect[0])
                      #state['obstacle_width'] = flatten(self.cacts[1].hitbox[2])
                      #state['obstacle_height'] = flatten(self.cacts[1].hitbox[3])
                  else:
                      state['dist_to_obstacle'] = [1200]
                      #state['dist_gap_obstacle'] = [1200]
                      #state['obstacle_width'] = [0]
                      #state['obstacle_height'] = [0]
              else:
                      state['dist_to_obstacle'] = [1200]
                      #state['dist_gap_obstacle'] = [1200]
                      #state['obstacle_width'] = [0]
                      #state['obstacle_height'] = [0]
            
              state['player_y_center'] = [self.playerCenter[1]]
              state['player_Jumping'] = [self.pika.isJump]
                      
              state_flattened = [state[key] for key in state.keys()]
              state_flattened = flatten(state_flattened)
              
              return state_flattened



