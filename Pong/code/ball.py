from settings import *
import pygame
import random
import numpy as np

class Ball(pygame.sprite.Sprite):
    def __init__(self, size, speed, pos, *groups):
        super().__init__(*groups)

        # Settings
        self.size = size
        self.speed = speed
        self.pos = pos

        # Image
        self.image = pygame.Surface(self.size,pygame.SRCALPHA)
        pygame.draw.circle(self.image,COLORS['ball'],(self.size[0]/2,self.size[1]/2),self.size[0] /2)

        # rect and movement
        self.rect = self.image.get_frect(center = self.pos)
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(0.5,random.randrange(-100,100)/100)

        # Access to other entities
        self.paddle_sprites = None


    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right > sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.bounce_ball(direction,sprite)
                if direction == 'vertical':
                    if self.rect.bottom > sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.bounce_ball(direction,sprite)


    def update (self,dt):
        self.old_rect = self.rect.copy()
        self.move(dt)

    def move(self,dt):
        self.rect.x += self.direction.x * dt * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * dt * self.speed
        self.collision('vertical')

        if self.rect.right>WINDOW_WIDTH or self.rect.left<0:
            self.rect.right = np.clip(self.rect.right,self.size[0], WINDOW_WIDTH)
            self.direction.x *= -1

        if self.rect.bottom>WINDOW_HEIGHT or self.rect.top<0:
            self.rect.bottom = np.clip(self.rect.bottom,self.size[1], WINDOW_HEIGHT)
            self.direction.y *= -1
        
    def bounce_ball(self,direction,sprite):
        if direction == 'horizontal':
            offset = (sprite.rect.centery - self.rect.centery)
            self.direction.y = -offset/(sprite.rect.height/2)
            self.direction.x *= -1
            


    def set_paddle_sprites(self,paddle_sprites):
        self.paddle_sprites = paddle_sprites
