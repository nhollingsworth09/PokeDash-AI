"""
This module primarily houses functions that test game states
"""
import pygame 

def collided(player, obs):
    #If one is left of the other
    if player[2] <= obs[0] or obs[2] <= player[0]:
        return False
    #If one is right of the other
    elif player[0] >= obs[2] or obs[0] >= player[2]:
        return False
    #If one is above the other
    elif player[3] <= obs[1] or obs[3] <= player[1]:
        return False
    #If one is below the other
    elif player[1] >= obs[3] or obs[1] >= player[3]:
        return False
    else:
        return True

def gameOver_msg(subtile_image, gameover_image, win, win_width, win_height):
    subtitle_rect = subtile_image.get_rect()
    subtitle_rect.centerx = win_width / 2
    subtitle_rect.top = win_height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = win_width / 2
    gameover_rect.centery = win_height*0.35

    win.blit(subtile_image, subtitle_rect)
    win.blit(gameover_image, gameover_rect)

def gym_jumped(player, win, current_image_pika, action):
    if not player.isJump:
        player.draw(win, current_image_pika)
        if action == 1:
            player.isJump = True
            
    else:       
        player.draw(win, 1)
        
    #-- Jumping is simulated using a quadratic formula creating a parabola
        if player.jumpCount >= -9:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount**2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 9

    
def jumped(player, win, current_image_pika, keys):
    
    if not player.isJump:
        player.draw(win, current_image_pika)
        if keys[pygame.K_UP]:
            player.isJump = True
            
    else:       
        player.draw(win, 1)
        
    #-- Jumping is simulated using a quadratic formula creating a parabola
        if player.jumpCount >= -9:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount**2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 9