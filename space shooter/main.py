import pygame
from os import path
import random

# CONSTS

WIN_WIDTH, WIN_HEIGHT = 1280,720

# general setup
pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100
display_surface.blit(surf,(x,150)) # moved outside the loop thus will be overwritten. Just here as reminder.

# surface from image
player_surf = pygame.image.load(path.join('images','player.png')).convert_alpha()
player_rect = player_surf.get_frect(midbottom = (WIN_WIDTH //2 , WIN_HEIGHT-10))

star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
star_positions = [(random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)) for _ in range(20)]

meteor_surf = pygame.image.load(path.join('images','meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WIN_WIDTH //2 , WIN_HEIGHT //2))

laser_surf = pygame.image.load(path.join('images','laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20,WIN_HEIGHT-20))



running = True
player_movement = 0.25
while running:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game

    display_surface.fill("gray")
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    if (player_rect.right > WIN_WIDTH or player_rect.left<0):
        player_movement *= -1
    player_rect.right += player_movement

    display_surface.blit(meteor_surf,meteor_rect)
    display_surface.blit(laser_surf,laser_rect)
    display_surface.blit(player_surf,player_rect)
    pygame.display.update()


pygame.quit()