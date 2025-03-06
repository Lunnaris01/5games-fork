import pygame.freetype
from settings import *
import numpy as np
from custom_timer import Timer

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
        self.animation = frames
        self.animation_speed = 10
        self.animation_length = len(self.animation)
        self.animation_index = 0
        self.image = self.animation[0]
        # Movement and Logic
        self.rect = self.image.get_frect(topleft = pos)
        self.is_background = is_background

class MultiAnimationSprite(pygame.sprite.Sprite):
    def __init__(self, pos, animations, is_background, *groups):
        super().__init__(*groups)
        self.animations = animations
        self.set_animation('default')
        self.image = self.current_animation[self.animation_index]
        self.animation_speed = 10

        self.rect = self.image.get_frect(topleft = pos)
        self.is_background = is_background

    def set_animation(self,animation_name):
        self.current_animation = self.animations[animation_name]
        self.animation_index = 0
        self.animation_length = len(self.current_animation)

class BackgroundSprite(Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(pos, surf, True, *groups)

class Player(AnimatedSprite):
    def __init__(self, pos, frames, bullet_func, *groups):
        super().__init__(pos, frames, False, *groups)
        self.animation = frames[:2]
        self.jump_animation = frames[-2]
        self.in_air_animation = frames[-1]
        self.animation_length = len(self.animation)
        self.x_speed = PLAYER_SPEED
        self.y_acceleration = 0
        self.direction = pygame.Vector2(0,0)
        self.flipanimation = False
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.can_doublejump = True
        self.bullet_func = bullet_func

        self.health = 100

        # Timers
        self.timer_shoot = Timer(500)

    def update(self, dt):
        self.move(dt)
        self.input()
        self.timer_shoot.update()



    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and not self.timer_shoot.active:
            self.bullet_func(self.rect.center,-1 if self.flipanimation else 1)
            self.timer_shoot.activate()

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

        if not self.can_jump():
            self.image = pygame.transform.flip(self.in_air_animation,self.flipanimation,False)


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


class Bullet(Sprite):
    def __init__(self, pos, direction, surf, *groups):
        super().__init__(pos, surf, False, *groups)
        self.direction = direction
        self.speed = 850

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt


class Worm(AnimatedSprite):
    def __init__(self, pos, movement_area, surf, *groups):
        super().__init__(pos, surf, False, *groups)
        self.direction = pygame.Vector2(1,0)
        self.speed = WORM_SPEED
        self.movement_area = pygame.rect.FRect(pos[0],pos[1],movement_area[0],movement_area[1])

    def update(self, dt):
        self.move(dt)

    def move(self,dt):

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



class Bee(MultiAnimationSprite):
    def __init__(self, pos, movement_area, animations, *groups):
        super().__init__(pos, animations, False, *groups)
        self.direction = pygame.Vector2(1,1)
        self.speed = BEE_SPEED
        self.yspeed = BEE_SPEED/3
        self.movement_area = pygame.rect.FRect(pos[0],pos[1],movement_area[0],movement_area[1])
        self.radius = 300
        self.angry = False

    def update(self, dt):
        self.move(dt)

    def move(self,dt):
        if self.angry:
            self.direction = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)
            self.direction = self.direction.normalize() if self.direction else self.direction
                            
        self.rect.x += self.direction.x*dt*self.speed
        self.check_boundaries('horizontal')
        self.rect.y += self.direction.y*dt*self.yspeed
        self.check_boundaries('vertical')

        self.animation_index = (self.animation_index + dt*self.animation_speed) % self.animation_length
        if self.direction.x < 0:
            self.image = self.current_animation[int(self.animation_index)]
        if self.direction.x > 0:
            self.image = pygame.transform.flip(self.current_animation[int(self.animation_index)],True,False)
    

    def check_boundaries(self,direction):
        if not self.angry:
            if not pygame.FRect.contains(self.movement_area,self.rect):
                if not pygame.FRect.collidepoint(self.movement_area,self.rect.centerx,self.rect.centery):
                    
                    self.direction = pygame.Vector2(self.movement_area.center) - pygame.Vector2(self.rect.center)
                    self.direction = self.direction.normalize() if self.direction else self.direction

                    return
                
                if direction == 'horizontal':
                    if self.rect.left<self.movement_area.left or self.rect.right>self.movement_area.right:
                        self.direction.x *=-1
                        self.rect.left = np.clip(self.rect.left,self.movement_area.left,self.movement_area.right-self.rect.width)
                if direction == 'vertical':
                    if self.rect.top<self.movement_area.top or self.rect.bottom>self.movement_area.bottom:
                        self.direction.y *=-1
                        self.rect.top = np.clip(self.rect.top,self.movement_area.top,self.movement_area.bottom-self.rect.height)

    def get_angry (self,target):
        if not self.angry:
            self.angry = True
            self.target = target
            self.yspeed *=3
            self.set_animation('angry')

    def calm_down(self):
        self.angry = False
        self.yspeed /=3
        self.set_animation('default')