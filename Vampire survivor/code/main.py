from settings import *
import pygame
from game import Game

# Init
game = Game()

while game.running:
    dt = game.clock.tick()/1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.keys[pygame.K_ESCAPE]:
            game.running = False

    # Update Entities
    game.refresh_keys()
    game.update(dt)

    # Drawing
    game.draw()

    pygame.display.update()