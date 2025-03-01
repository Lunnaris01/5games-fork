import pygame
from os import path
import random

# CONSTS

WIN_WIDTH, WIN_HEIGHT = 1280,720

# CLASSES

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(path.join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(midbottom = (WIN_WIDTH //2-50 , WIN_HEIGHT-5))
        self.player_speed = 100
        self.direction = pygame.Vector2()

    def update(self,keys,keys_justpressed,dt):
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.rect.center += self.direction *dt*self.player_speed
        if keys_justpressed[pygame.K_SPACE]:
            print("Play shooting animation!!")

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(path.join('images','meteor.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WIN_WIDTH //2 , WIN_HEIGHT //2))


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(path.join('images','laser.png')).convert_alpha()  
        self.rect = self.image.get_frect(midbottom = (pos))
        self.direction = pygame.Vector2()


# general setup
pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
dt = 16/1000

running = True

# Improved way to handle surfaces/rect with sprites!
all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
stars = [Star(star_surf,all_sprites) for _ in range(20)]
meteor = Meteor(all_sprites)
player = Player(all_sprites)

while running:

    keys = pygame.key.get_pressed()
    keys_justpressed = pygame.key.get_just_pressed()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game


    all_sprites.update(keys,keys_justpressed,dt)

    display_surface.fill("gray")

    # Use draw function for our sprites and groups!

    all_sprites.draw(display_surface)

    pygame.display.update()
    dt = clock.tick() / 1000



pygame.quit()