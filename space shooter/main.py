import pygame

# CONSTS

WIN_WIDTH, WIN_HEIGHT = 1280,720

# general setup
pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooter")

running = True
while running:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game

    display_surface.fill("green")
    pygame.display.update()


pygame.quit()