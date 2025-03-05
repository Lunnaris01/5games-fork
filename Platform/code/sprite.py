import pygame.freetype
from settings import *
import numpy as np
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos:tuple,surf:pygame.Surface, is_background:bool, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect( midleft = pos)
        self.is_background = is_background

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, frames:list[pygame.Surface], is_background:bool, *groups):
        super().__init__(*groups)
        # Animation Setup
        self.animation = frames[:2]
        self.jump_animation = frames[-1]
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.animation_length = len(self.animation)
        self.animation_index = 0
        self.image = self.animation[0]
        print (self.animation_length)
        # Movement and Logic
        self.rect = self.image.get_frect(topleft = pos)
        self.is_background = is_background

class BackgroundSprite(Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(pos, surf, True, *groups)

class Player(AnimatedSprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(pos, surf, False, *groups)
        self.x_speed = PLAYER_SPEED
        self.y_acceleration = 0
        self.direction = pygame.Vector2(0,0)
        self.flipanimation = False

        self.can_doublejump = True

    def update(self, dt):
        self.move(dt)


    def move(self,dt):
        keys = pygame.key.get_pressed()
        keys_just = pygame.key.get_just_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        if self.can_jump():
            self.direction.y = 0
        if keys_just[pygame.K_SPACE]:
            if keys[pygame.K_LCTRL] and self.can_jump():
                print("superjump")
                self.y_acceleration = (-PLAYER_JUMP_ACCELERATION*1.3)
                self.direction.y = 0
                self.can_doublejump = True
            elif self.can_jump():
                print("normal jump")
                self.y_acceleration = (-PLAYER_JUMP_ACCELERATION)
                self.can_doublejump = True
                self.direction.y = 0
            elif self.can_doublejump:
                print("double jump")
                self.y_acceleration = (-PLAYER_JUMP_ACCELERATION)
                self.can_doublejump = False
                self.direction.y = 0
        self.y_acceleration += GRAVITY * dt
        self.y_acceleration = np.clip(self.y_acceleration,-5000,1000)
        self.direction.y += self.y_acceleration * dt 
        self.rect.y += self.direction.y*dt
        self.collision('vertical')


        self.rect.x += self.direction.x*dt*self.x_speed
        self.collision('horizontal')
        self.animation_index = (self.animation_index + dt*self.animation_speed) % self.animation_length
        if self.direction.x == 0:
            self.animation_index = 0
        if self.direction.x > 0:
            self.flipanimation = False
        elif self.direction.x < 0:
            self.flipanimation = True
        
        self.image = pygame.transform.flip(self.animation[int(self.animation_index)],self.flipanimation,False)

        if keys[pygame.K_LCTRL] and self.can_jump():
            self.image = pygame.transform.flip(self.jump_animation,self.flipanimation,False)

        if self.rect.bottom>50000:
            self.kill()

    def can_jump(self):
        for sprite in self.collision_sprites:
            x,y = self.rect.midbottom
            if pygame.FRect.collidepoint(sprite.rect,x,y):
                return True
        return False

    def set_collision_sprites(self,collision_sprites):
        self.collision_sprites = collision_sprites

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0 : self.rect.right = sprite.rect.left
                    if self.direction.x < 0 : self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0



class Worm(AnimatedSprite):
    def __init__(self, pos, movement_area, surf, *groups):
        super().__init__(pos, surf, False, *groups)
        self.direction = pygame.Vector2(1,0)
        self.speed = WORM_SPEED
        self.movement_area = pygame.rect.FRect(pos[0],pos[1],movement_area[0],movement_area[1])

    def update(self, dt):
        self.move(dt)

    def move(self,dt):
        keys = pygame.key.get_pressed()

        self.rect.x += self.direction.x*dt*self.speed

        self.animation_index = (self.animation_index + dt*self.animation_speed) % self.animation_length
        self.check_boundaries()
        if self.direction.x > 0:
            self.image = self.animation[int(self.animation_index)]
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.animation[int(self.animation_index)],True,False)
        

    def check_boundaries(self):
        if not pygame.FRect.contains(self.movement_area,self.rect):
            self.direction.x *=-1
            self.rect.left = np.clip(self.rect.left,self.movement_area.left,self.movement_area.right-self.rect.width)