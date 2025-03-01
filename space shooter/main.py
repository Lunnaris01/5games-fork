import pygame
from os import path
import random


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

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(path.join('images','laser.png')).convert_alpha()  
        self.rect = self.image.get_frect(midbottom = (pos))
        self.direction = pygame.Vector2()

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

# surfaces and rectangles from imagefiles as plain way to load a surface!
# self.image = pygame.image.load(path.join('images','player.png')).convert_alpha()
# self.rect = self.image.get_frect(midbottom = (WIN_WIDTH //2-50 , WIN_HEIGHT-5))

# Improved way to handle surfaces/rect with sprites!
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

# player_direction = pygame.math.Vector2((0,0))
# player_speed = 50.0

star_surf = pygame.image.load(path.join('images','star.png')).convert_alpha()
star_positions = [(random.randint(0,WIN_WIDTH-1),random.randint(0,WIN_HEIGHT-1)) for _ in range(20)]

meteor_surf = pygame.image.load(path.join('images','meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WIN_WIDTH //2 , WIN_HEIGHT //2))

laser_surf = pygame.image.load(path.join('images','laser.png')).convert_alpha()
lasers = []
# We can create plain (F)rects as well.


while running:

    keys = pygame.key.get_pressed()
    keys_justpressed = pygame.key.get_just_pressed()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_d:
        #         player_direction.x = 1
        #     if event.key == pygame.K_a:
        #         player_direction.x = -1
        #     if event.key == pygame.K_w:
        #         player_direction.y = -1
        # The outcommented parts are implemented outside the event loop instead!
        #    if event.key == pygame.K_s:
        #        player_direction.y = 1
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    laser_rect = laser_surf.get_frect(bottomleft = (20,WIN_HEIGHT-20))
        #    laser_rect.midbottom = event.pos
        #    lasers.append(laser_rect)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
    #draw the game


    # inputs without the event loop! Let's spawn a laser with a click!
    # the same functionality is implemented for the spacebar outside the event loop below!
    # if (pygame.mouse.get_just_pressed()[0]):
    #     laser_rect = laser_surf.get_frect(bottomleft = (20,WIN_HEIGHT-20))
    #     laser_rect.midbottom = pygame.mouse.get_pos()
    #     lasers.append(laser_rect)
    # # this works but is chunky
    # if keys[pygame.K_s]:
    #     player_direction.y = 1
    # elif keys[pygame.K_w]:
    #     player_direction.y = -1
    # else:
    #     player_direction.y = 0
    # # Smart solution in one line! Bonus: If we press both we automatically have 0 movement which would need an extra elif for the other approach!
    # player_direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    # We can normalize the speed e.g. if the game is not a platformer and we dont want to have a higher diagonal speed compared to the horizontal/vertical speed.
    #player_direction = player_direction.normalize() if player_direction else player_direction
    # player_rect.center += player_direction*player_speed*dt

    # laser with spacebar outside the event loop!
    # if keys_justpressed[pygame.K_SPACE]:
    #     laser_rect = laser_surf.get_frect(bottomleft = (20,WIN_HEIGHT-20))
    #     laser_rect.midbottom = player_rect.midtop
    #     lasers.append(laser_rect)


    all_sprites.update(keys,keys_justpressed,dt)

    display_surface.fill("gray")
    # Stars in Background
    for pos in star_positions:
        display_surface.blit(star_surf,pos)

    # Player Movement
    # if (player_rect.right > WIN_WIDTH or player_rect.left<0):
    #     player_direction.x *= -1
    # if (player_rect.bottom > WIN_HEIGHT or player_rect.top<0):
    #     player_direction.y *= -1

    display_surface.blit(meteor_surf,meteor_rect)



    #display lasers and remove them. Use duplicate list to savely remove items from the original list
    for laser_rect in list(lasers):
        if laser_rect.bottom < 0:
            lasers.remove(laser_rect)
        else:
            laser_rect.top -= 100*dt
            display_surface.blit(laser_surf,laser_rect)


    # Dont do this! Create draw functions with pygame groups instead!
    #display_surface.blit(player.image,player.rect)

    all_sprites.draw(display_surface)

    pygame.display.update()
    dt = clock.tick() / 1000



pygame.quit()