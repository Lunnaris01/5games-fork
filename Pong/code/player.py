from settings import *
import pygame
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, size, speed, pos, *groups):
        super().__init__(*groups)
        # Settings
        self.size = size
        self.speed = speed
        
        # Image
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(self.image,COLORS['paddle'], pygame.FRect((0,0),self.size),0,10)
        
        # rect & movement
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(0,0)


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)

    def move(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.rect.center += self.direction *dt * self.speed
        if self.rect.bottom>WINDOW_HEIGHT or self.rect.top<0:
            self.rect.bottom = np.clip(self.rect.bottom,self.size[1], WINDOW_HEIGHT)
