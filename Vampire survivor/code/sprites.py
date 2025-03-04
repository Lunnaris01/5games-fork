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
        self.bullet_sound = pygame.mixer.Sound(path.join('audio','shoot.wav'))

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
        self.bullet_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, *groups):
        super().__init__(*groups)
        self.direction = direction
        self.bulletspeed = DEFAULT_BULLET_SPEED
        self.image = pygame.image.load(path.join('images','gun','bullet.png'))
        self.rect = self.image.get_frect(center = pos)
        self.creationtime = pygame.time.get_ticks()

    def update(self,keys,keys_justpressed,dt):
        self.rect.center += self.direction*self.bulletspeed*dt
        current_time = pygame.time.get_ticks()
        if current_time-self.creationtime > 5000:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type, animation, bullet_sprites, collision_sprites, *groups):
        super().__init__(*groups)
        self.current_animation = animation
        self.animation_iterator = 0
        self.animation_length = len(animation)
        self.animation_speed = 5
        self.image = self.current_animation[0]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-20)
        self.direction = pygame.Vector2(0,0)
        self.collision_sprites = collision_sprites
        self.bullet_sprites = bullet_sprites
        self.killtime = None
        self.kill_flash_timer = 1000
        self.enemy_type = enemy_type

    def move(self,target,dt):
        if self.is_alive():
            self.direction = pygame.Vector2(target) - self.rect.center
            if self.direction.magnitude() !=0:
                self.direction = self.direction.normalize()
            self.rect.centerx += self.direction.x*dt*ENEMY_SPEED
            self.collision('horizontal',dt)
            self.rect.centery += self.direction.y*dt*ENEMY_SPEED
            self.collision('vertical',dt)


    def update(self,keys,keys_justpressed,dt):
        if self.is_alive():
            if pygame.sprite.spritecollide(self,self.bullet_sprites,True,pygame.sprite.collide_rect):
                flash_surface = pygame.mask.from_surface(self.current_animation[0]).to_surface()
                flash_surface.set_colorkey('black')
                self.image = flash_surface
                self.destroy()
                return
            self.animation_iterator = (self.animation_iterator + (self.animation_speed*dt))% self.animation_length
            self.image = self.current_animation[int(self.animation_iterator)]
        if self.killtime:
            if pygame.time.get_ticks() - self.killtime > self.kill_flash_timer:
                self.kill()

    def get_damage(self):
        if self.enemy_type == 'bat':
            return 5
        if self.enemy_type == 'blob':
            return 1
        if self.enemy_type == 'skeleton':
            return 10
        return 3
    
    def collision(self,direction,dt):
        if self.enemy_type == 'bat':
            return
        #if pygame.sprite.spritecollide(self,self.collision_sprites,False,pygame.sprite.collide_rect):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    self.rect.centerx -= self.direction.x*dt*ENEMY_SPEED
                elif direction == 'vertical':
                    self.rect.centery -= self.direction.y*dt*ENEMY_SPEED
                else:
                    raise KeyError("Unknown direction for collision")
    def destroy(self):
        flash_surface = pygame.mask.from_surface(self.current_animation[0]).to_surface().convert_alpha()
        flash_surface.set_colorkey('black')
        self.image = flash_surface
        self.killtime = pygame.time.get_ticks()


    def is_alive(self):
        return self.killtime == None