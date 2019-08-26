"""
This game was developed with the intention of training a Deep Reinforcement Learning model using Q-Learning

@author: Nykosi Hollingsworth
@date: May 6, 2019
"""
#------------------------------------------------------------------------------
#       Imports and Environment
#------------------------------------------------------------------------------

import pygame 
import os
import time
from numpy import random

path = 'C:/Users/nholl/Dropbox/2019 SPRING/Personal Projects/PyGame/Pokemon'
os.chdir(path)

from gameObjects import Scoreboard, Player, Background, Cactus
from gameFunctions import collided, gameOver_msg, jumped, gym_jumped

pygame.init()
screen = (win_width, win_height) = (1000, 380)
win = pygame.display.set_mode(screen)
pygame.display.set_caption("PokéRun")
clock = pygame.time.Clock()

#------------------------------------------------------------------------------
#       Game Window
#------------------------------------------------------------------------------

def GameWindow(backg, backg2):    
    win.fill((255,255,255))
    
    #-- Drawing backgrounds for infinite run illusion
    backg.bg_draw(win)
    backg.x -= backg.vel
    backg.rightx -= backg.vel

    backg2.bg_draw(win)
    backg2.x -= backg2.vel
    backg2.rightx -= backg2.vel  

#------------------------------------------------------------------------------
#       Main Loop
#------------------------------------------------------------------------------
gameSpeed = 12 
    
background_1 = Background('./sprites/background.png', 0, 280, gameSpeed)  
background_2 = Background('./sprites/background.png', 1200, 280, gameSpeed) 

gameover_image = pygame.image.load('./assets/game_over.png')
subtitle_image = pygame.image.load('./assets/subtitle_over.png')

def main():
    
    #-- Initalize Game Variables
    max_cacti = 3
    cacts = []
    
    score = Scoreboard(5,5)
    pika = Player(win, 25, 255)        
    
    start_frame = time.time()
    last_cactus = time.time() 
    
    running = True
    


    while running:        
        
        GameWindow(background_1, background_2)
        win.blit(score.font.render('Score: %s' %score.value, 1, (0,0,0)), (score.x, score.y))
        
        clock.tick(30)       
        
        #-- Lock player FPS
        noi_pika = 4
        frames_per_second_pika = 14
        current_image_pika = int((time.time() - start_frame) * frames_per_second_pika % noi_pika)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        keys = pygame.key.get_pressed()   
        
                    
        #-- Managing Cactus Production
            
            #- Randomly select initial x value to vary cactus distances
        rand_dist = random.choice([1000, 1025, 1050, 1150, 1175], 1, p = [0.20, 0.20, 0.20, 0.20, 0.20])
        idx = random.randint(0,3)
        
        if len(cacts) < max_cacti and (time.time() - last_cactus) >= 1.5:
            cacts.append(Cactus(path, rand_dist, 175, gameSpeed, idx))
            
            last_cactus = time.time()
        
        for cact in cacts:
            if cact.onScreen == False:
                cacts.pop(cacts.index(cact))
            elif cact.rightx <= 0:
                cact.onScreen = False
            else:
                cact.draw(win)
                cact.x -= cact.vel
                cact.rightx -= cact.vel 
                      
        #-- Collison
        for cact in cacts:
            collision = collided(pika.rect, cact.rect)
            
            if collision == True:      
                pika.isDead = collision
                        
        pika.score += 1
        score.value = pika.score
        
        #-- Jumping
        jumped(pika, win, current_image_pika, keys)
     
        pygame.display.update()
        
        #-- Check for Player Death
        while pika.isDead:
            clock.tick(60)
            gameOver_msg(subtitle_image, gameover_image, win, win_width, win_height)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pika.isDead = False
                    running = False
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pika.isDead = False                        
                        main()
            
    pygame.quit()
    
if __name__ == '__main__':
     main()