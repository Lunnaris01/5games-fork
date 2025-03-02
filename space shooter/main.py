import pygame
from os import path, listdir
import random
import numpy as np

# CONSTS

WIN_WIDTH, WIN_HEIGHT = 1280,720
PLAYER_STARTING_HEALTH = 3
# CLASSES

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(path.join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(midbottom = (WIN_WIDTH //2-50 , WIN_HEIGHT-5))
        self.player_speed = 250
        self.health = PLAYER_STARTING_HEALTH
        self.direction = pygame.Vector2()

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # laser cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks()-self.laser_shoot_time > self.cooldown_duration:
                self.can_shoot = True
            
    def lose_health(self):
        self.health -=1

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
        self.original_surf = surf
        self.image = surf
        if pos == None:
            pos = (random.randint(100,WIN_WIDTH-100),random.randint(-200,0))
        self.rect = self.image.get_frect(center = pos)
        self.creationtime = pygame.time.get_ticks()
        self.direction = pygame.Vector2(random.randint(-500,500)/1000,1)
        self.speed = random.randint(250,550)
        self.rotation = random.randint(-50,50)
        self.alignment = self.rotation

        self.mask = pygame.mask.from_surface(self.image)    
    
    def update(self, key, keys_justpressed,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks()-self.creationtime>2500:
            self.kill()
        self.alignment += self.rotation*dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.alignment,1)
        self.rect = self.image.get_frect(center = self.rect.center)


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.direction = pygame.Vector2(0,-1)
        self.shootingspeed = 1000
        self.mask = pygame.mask.from_surface(self.image)
        laser_sound.play()    

    def update(self,keys,keys_justpressed,dt):
        self.rect.center += self.direction*self.shootingspeed*dt
        if self.rect.bottom < 0:
            self.kill()


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, *groups):
        super().__init__(*groups)
        self.frames = list(frames)
        self.image = frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.animation_index = 0.0
        explosion_sound.play()

    def update(self,keys,keys_justpresse,dt):
            if self.animation_index<len(self.frames):
                self.image = self.frames[int(self.animation_index)]
                self.animation_index += dt*35
            else:
                self.kill()


def collisions():
    print(player.health)
    if (pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask)):
        damage_sound.play()
        player.lose_health()
        print(player.health)
        if player.health<1:
            return False
    for laser in laser_sprites:
        collision_list = pygame.sprite.spritecollide(laser,meteor_sprites,True)
        for collision in collision_list:
            AnimatedExplosion(explosion_frames,collision.rect.center,all_sprites)

    #collided_elems = pygame.sprite.groupcollide(laser_sprites,meteor_sprites,True,True,pygame.sprite.collide_mask)
    return True

def display_score():
    current_time = str(int(pygame.time.get_ticks()/100))
    text_surf = font.render(current_time,True,'#FAFAFA')
    text_rect = text_surf.get_frect(midbottom = (WIN_WIDTH/2,WIN_HEIGHT-50))
    text_surrounder = pygame.Surface((text_rect.width+10,text_rect.height+5)).convert_alpha()
    text_surrounder.fill((0,0,0,0))
    pygame.draw.rect(text_surrounder, '#FAFAFA', text_surrounder.get_rect(), 2,5)
    display_surface.blit(text_surrounder,text_surrounder.get_frect(center = text_rect.center).inflate(5,5).move(3,-5))
    display_surface.blit(text_surf,text_rect)


# general setup
pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
dt = 16/1000

running = True

# Improved way to handle surfaces/rect with sprites!

# Import assets:
# Sprite Objects 
star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
laser_surf = pygame.image.load(path.join('images','laser.png')).convert_alpha()  
meteor_surf = pygame.image.load(path.join('images','meteor.png')).convert_alpha()
# Fonts/text
font = pygame.font.Font(path.join('images','Oxanium-Bold.ttf'), 40)
text_surf = font.render('text',True,'#FAFAFA')
# Animations
explosion_frames = [pygame.image.load(path.join('images','explosion',x)).convert_alpha() for x in listdir(path.join('images','explosion'))]
# Sounds
laser_sound = pygame.mixer.Sound(path.join('audio','laser.wav'))
explosion_sound = pygame.mixer.Sound(path.join('audio','explosion.wav'))
game_music = pygame.mixer.Sound(path.join('audio','game_music.wav'))
damage_sound = pygame.mixer.Sound(path.join('audio','damage.ogg'))

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

stars = [Star(star_surf,all_sprites) for _ in range(20)]
player = Player(all_sprites)

# custom events -> meteor spawning
meteor_event = pygame.event.custom_type()
meteor_spawn_cooldown = 500
pygame.time.set_timer(meteor_event,meteor_spawn_cooldown)
game_music.play(loops = -1)
while running:

    keys = pygame.key.get_pressed()
    keys_justpressed = pygame.key.get_just_pressed()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, None ,all_sprites, meteor_sprites)

    # Update all the sprites at once
    all_sprites.update(keys,keys_justpressed,dt)


    # Use draw function for our sprites and groups!
    #draw the game
    display_surface.fill("#3a2e3f")
    # Sprites will be drawn in order they were inserted!
    all_sprites.draw(display_surface)
    display_score()
    # Check Collisions
    running = running and collisions()
    #for l_sprite in laser_sprites:
    #    collided_sprites = pygame.sprite.spritecollide(l_sprite,meteor_spritesd,True)
    #    if collided_sprites:
    #        l_sprite.kill()

    pygame.display.update()
    dt = clock.tick(200) / 1000

    # Preparations for next run

    if pygame.time.get_ticks()%1000 == 0:
        meteor_spawn_cooldown = meteor_spawn_cooldown*0.99
        pygame.time.set_timer(meteor_event,int(meteor_spawn_cooldown))

print(f"Score: {pygame.time.get_ticks()//100}")

pygame.quit()