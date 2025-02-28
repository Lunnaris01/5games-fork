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

# surface from image
player_surf = pygame.image.load(path.join('images','player.png')).convert_alpha()
player_rect = player_surf.get_frect(midbottom = (WIN_WIDTH //2 , WIN_HEIGHT-10))

star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
star_positions = [(random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)) for _ in range(20)]


running = True
while running:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game

    display_surface.fill("gray")
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    if (player_rect.right < WIN_WIDTH):
        player_rect.right +=  0.1

    display_surface.blit(surf,(x,150)) #block image transfer

    display_surface.blit(player_surf,player_rect)
    pygame.display.update()


pygame.quit()