from settings import *
import pygame
import numpy as np

class Paddle(pygame.sprite.Sprite):
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

class Player(Paddle):
    def __init__(self, size, speed, pos, *groups):
        super().__init__(size, speed, pos, *groups)


class Bot(Paddle):
    def __init__(self, size, speed, pos, ball, *groups):
        super().__init__(size, speed, pos, *groups)
        self.ball = ball

    def move(self,dt):
        self.direction.y = -1 if self.rect.centery>self.ball.rect.centery else 1
        self.rect.center += self.direction *dt * self.speed

