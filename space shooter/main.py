import pygame

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
player_surf = pygame.image.load('images/player.png')


running = True
while running:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game

    display_surface.fill("gray")

    display_surface.blit(surf,(x,150)) #block image transfer
    if x<500:
        x += 0.05

    display_surface.blit(player_surf,(600,300))
    pygame.display.update()


pygame.quit()