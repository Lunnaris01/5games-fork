import pygame
from os import path
import random
import numpy as np

# CONSTS

WIN_WIDTH, WIN_HEIGHT = 1280,720

# CLASSES

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(path.join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(midbottom = (WIN_WIDTH //2-50 , WIN_HEIGHT-5))
        self.player_speed = 250
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
        # clip position to remain in game window
        self.rect.left = np.clip(self.rect.left,0,WIN_WIDTH-self.rect.width)
        self.rect.top = np.clip(self.rect.top,0,WIN_HEIGHT-self.rect.height)


        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop,all_sprites,laser_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        if pos == None:
            pos = (random.randint(100,WIN_WIDTH-100),random.randint(-200,0))
        self.rect = self.image.get_frect(center = pos)
        self.creationtime = pygame.time.get_ticks()
        self.direction = pygame.Vector2(random.randint(-500,500)/1000,1)
        self.speed = random.randint(250,550)
        
    
    def update(self, key, keys_justpressed,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks()-self.creationtime>2500:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.direction = pygame.Vector2(0,-1)
        self.shootingspeed = 1000

    def update(self,keys,keys_justpressed,dt):
        self.rect.center += self.direction*self.shootingspeed*dt
        if self.rect.bottom < 0:
            self.kill()

def collisions():
    if (pygame.sprite.spritecollide(player,meteor_sprites,False)):
        return False
    pygame.sprite.groupcollide(laser_sprites,meteor_sprites,True,True)
    return True

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
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

stars = [Star(star_surf,all_sprites) for _ in range(20)]
player = Player(all_sprites)


# custom events -> meteor spawning
meteor_event = pygame.event.custom_type()
meteor_spawn_cooldown = 500
pygame.time.set_timer(meteor_event,meteor_spawn_cooldown)

while running:

    keys = pygame.key.get_pressed()
    keys_justpressed = pygame.key.get_just_pressed()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, None ,all_sprites, meteor_sprites)



    # Update all the sprites at once
    all_sprites.update(keys,keys_justpressed,dt)


    # Use draw function for our sprites and groups!
    #draw the game
    display_surface.fill("gray")
    # Sprites will be drawn in order they were inserted!
    all_sprites.draw(display_surface)


    # Check Collisions
    running = collisions()
    #for l_sprite in laser_sprites:
    #    collided_sprites = pygame.sprite.spritecollide(l_sprite,meteor_spritesd,True)
    #    if collided_sprites:
    #        l_sprite.kill()

    pygame.display.update()
    dt = clock.tick() / 1000

    # Preparations for next run

    if pygame.time.get_ticks()%1000 == 0:
        meteor_spawn_cooldown = meteor_spawn_cooldown*0.99
        pygame.time.set_timer(meteor_event,int(meteor_spawn_cooldown))

print(f"Score: {pygame.time.get_ticks()//1000}")

pygame.quit()