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

        # gun cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks()-self.laser_shoot_time > self.cooldown_duration:
                self.can_shoot = True
            
            

    def update(self,keys,keys_justpressed,dt):
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.rect.center += self.direction *dt*self.player_speed
        if keys_justpressed[pygame.K_SPACE] and self.can_shoot:
            print("Play shooting animation!!")
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.direction = pygame.Vector2()


# general setup
pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
dt = 16/1000

running = True

# Improved way to handle surfaces/rect with sprites!

# Import sprites we want to reuse:
star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
laser_surf = pygame.image.load(path.join('images','laser.png')).convert_alpha()  
meteor_surf = pygame.image.load(path.join('images','meteor.png')).convert_alpha()

all_sprites = pygame.sprite.Group()
stars = [Star(star_surf,all_sprites) for _ in range(20)]
meteor = Meteor((WIN_WIDTH //2 , WIN_HEIGHT //2),meteor_surf,all_sprites)
player = Player(all_sprites)


# custom events -> meteor spawning
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)

while running:

    keys = pygame.key.get_pressed()
    keys_justpressed = pygame.key.get_just_pressed()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            print('create meteor')
    #draw the game


    all_sprites.update(keys,keys_justpressed,dt)

    display_surface.fill("gray")

    # Use draw function for our sprites and groups!

    all_sprites.draw(display_surface)

    pygame.display.update()
    dt = clock.tick() / 1000



pygame.quit()