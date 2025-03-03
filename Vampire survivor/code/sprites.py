from settings import *
import math

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.background = True

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, *groups):
        super().__init__(*groups)
        self.player = player
        self.distance_to_player = 140
        self.direction = pygame.Vector2(1,0)
        self.gun_surf = pygame.image.load(path.join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + (self.direction * self.distance_to_player))
        self.bullet_offset = 60

    def update(self,keys,keys_justpressed,dt):
        mousepos = pygame.mouse.get_pos()
        self.direction = pygame.Vector2(mousepos[0]-(WINDOW_WIDTH//2),mousepos[1]-(WINDOW_HEIGHT//2))
        if self.direction != (0,0):
            self.direction = self.direction.normalize()
        else:
            self.direction = pygame.Vector2(1,0)
        rotation = math.degrees(math.atan2(self.direction[0],self.direction[1]))+270
        if rotation>270:
            self.image = pygame.transform.rotate(self.gun_surf,rotation)
        else:
            self.image = pygame.transform.rotate(pygame.transform.flip(self.gun_surf,False,True),rotation)
        self.rect.center = self.player.rect.center + (self.direction * self.distance_to_player)

    def spawn_bullet(self,*groups):
        Bullet(self.rect.center + self.direction*self.bullet_offset,self.direction,*groups)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, *groups):
        super().__init__(*groups)
        self.direction = direction
        self.bulletspeed = 1
        self.image = pygame.image.load(path.join('images','gun','bullet.png'))
        self.rect = self.image.get_frect(center = pos)
        self.creationtime = pygame.time.get_ticks()

    def update(self,keys,keys_justpressed,dt):
        self.rect.center += self.direction*self.bulletspeed
        current_time = pygame.time.get_ticks()
        if current_time-self.creationtime > 5000:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type, animation, collision_sprites, *groups):
        super().__init__(*groups)
        self.current_animation = animation
        self.animation_iterator = 0
        self.animation_length = len(animation)
        self.animation_speed = 5
        self.image = self.current_animation[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(0,0)
        self.collision_sprites = collision_sprites

        self.enemy_type = enemy_type

    def move(self,target,dt):
        self.direction = pygame.Vector2(target)- self.rect.center
        if self.direction.magnitude() !=0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction*dt*ENEMY_SPEED

    def update(self,keys,keys_justpressed,dt):
        if pygame.sprite.spritecollide(self,self.collision_sprites,True,pygame.sprite.collide_rect):
            self.kill()
        self.animation_iterator = (self.animation_iterator + (self.animation_speed*dt))% self.animation_length
        self.image = self.current_animation[int(self.animation_iterator)]

    def get_damage(self):
        if self.enemy_type == 'bat':
            return 5
        if self.enemy_type == 'blob':
            return 1
        if self.enemy_type == 'skeleton':
            return 10
        return 3