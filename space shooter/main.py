import pygame
from os import path
import random

# CONSTS

WIN_WIDTH, WIN_HEIGHT = 1280,720

# general setup
pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
dt = 16/1000

running = True


# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100
display_surface.blit(surf,(x,150)) # moved outside the loop thus will be overwritten. Just here as reminder.

# surfaces and rectangles from imagefiles
player_surf = pygame.image.load(path.join('images','player.png')).convert_alpha()
player_rect = player_surf.get_frect(midbottom = (WIN_WIDTH //2-50 , WIN_HEIGHT-5))
player_direction = pygame.math.Vector2((0,0))
player_speed = 50.0

star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
star_positions = [(random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)) for _ in range(20)]

meteor_surf = pygame.image.load(path.join('images','meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WIN_WIDTH //2 , WIN_HEIGHT //2))

laser_surf = pygame.image.load(path.join('images','laser.png')).convert_alpha()
lasers = []
# We can create plain (F)rects as well.


while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player_direction.x = 1
            if event.key == pygame.K_a:
                player_direction.x = -1
            if event.key == pygame.K_w:
                player_direction.y = -1
        # The outcommented parts are implemented outside the event loop instead!
        #    if event.key == pygame.K_s:
        #        player_direction.y = 1
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    laser_rect = laser_surf.get_frect(bottomleft = (20,WIN_HEIGHT-20))
        #    laser_rect.midbottom = event.pos
        #    lasers.append(laser_rect)
        if event.type == pygame.MOUSEMOTION:
            player_rect.center = event.pos
    #draw the game


    # inputs without the event loop!
    if (pygame.mouse.get_just_pressed()[0]):
        laser_rect = laser_surf.get_frect(bottomleft = (20,WIN_HEIGHT-20))
        laser_rect.midbottom = pygame.mouse.get_pos()
        lasers.append(laser_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        player_direction.y = 1

    display_surface.fill("gray")
    # Stars in Background
    for pos in star_positions:
        display_surface.blit(star_surf,pos)

    # Player Movement
    if (player_rect.right > WIN_WIDTH or player_rect.left<0):
        player_direction.x *= -1
    if (player_rect.bottom > WIN_HEIGHT or player_rect.top<0):
        player_direction.y *= -1
    player_rect.center += player_direction*player_speed*dt

    display_surface.blit(meteor_surf,meteor_rect)
    #display lasers and remove them. Use duplicate list to savely remove items from the original list
    for laser_rect in list(lasers):
        if laser_rect.bottom < 0:
            lasers.remove(laser_rect)
        else:
            laser_rect.top -= 100*dt
            display_surface.blit(laser_surf,laser_rect)

    display_surface.blit(player_surf,player_rect)
    pygame.display.update()
    dt = clock.tick() / 1000



pygame.quit()