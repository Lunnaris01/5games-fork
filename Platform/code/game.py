from settings import *
from pytmx.util_pygame import load_pygame
from os import path, listdir
from sprite import Sprite, Player, Worm, Bee, Bullet
from group import AllSprites
from custom_timer import Timer
import random
from utils import load_animations

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # Load Assets
        self.load_assets()


        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.worm_sprites = pygame.sprite.Group()
        self.bee_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


        self.beespawns = []

        self.setup()


        # timers

        self.bee_timer = Timer(1000, func = self.create_bee ,repeat=True,autostart=True)
        self.bee_anger_timers = []



    def setup(self):
        map = load_pygame(path.join('data','maps','world.tmx'))
        for x,y,image in map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), image, True, self.all_sprites,self.collision_sprites)
        for x,y,image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image, True, self.all_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.player_animation, self.create_bullet, self.all_sprites)
                self.player.set_collision_sprites(self.collision_sprites)
            if obj.name == 'Worm':
                worm = Worm((obj.x,obj.y),(obj.width,obj.height),self.worm_animation,self.all_sprites,self.worm_sprites,self.enemy_sprites)
            if obj.name == 'Bee':
                self.beespawns.append(((obj.x,obj.y),(obj.width,obj.height)))
                print(self.beespawns)

    def load_assets(self):
        self.player_animation = [pygame.image.load(path.join('images','player',frame)) for frame in sorted(listdir(path.join('images','player')))]
        self.worm_animation = [pygame.image.load(path.join('images','enemies','worm',frame)) for frame in sorted(listdir(path.join('images','enemies','worm')))]
        self.bee_animations = load_animations(path.join('images','enemies','bee'))
        self.gun_bullet_image = pygame.image.load(path.join('images','gun','bullet.png'))
        self.gun_fire_image = pygame.image.load(path.join('images','gun','fire.png'))

        self.sound_impact = pygame.mixer.Sound(path.join('audio','impact.ogg'))
        self.sound_game_music = pygame.mixer.Sound(path.join('audio','music.wav'))
        self.sound_shoot = pygame.mixer.Sound(path.join('audio','shoot.wav'))
        self.sound_game_music.play(loops=-1)

    def create_bee(self):
        spawnpoint, move_area = random.choice(self.beespawns)
        Bee(spawnpoint,move_area,self.bee_animations,self.all_sprites,self.bee_sprites, self.enemy_sprites)

    def create_bullet(self,pos,direction):
        Bullet(pos,direction,self.gun_bullet_image,self.all_sprites,self.bullet_sprites)
        

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            for anger_timer in list(self.bee_anger_timers):
                anger_timer.update()
                if not anger_timer:
                    self.bee_anger_timers.remove(anger_timer)
            self.all_sprites.update(dt)
            if not self.player.groups():
                break
            
            # collisions
            self.collisions()

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.topleft)
            pygame.display.update()
        
        pygame.quit()


    def collisions(self):
        collided = pygame.sprite.groupcollide(self.bullet_sprites,self.enemy_sprites,True,True)
        if collided:
            for sprite in self.bee_sprites:
                if pygame.sprite.collide_circle(self.player,sprite):
                    sprite.get_angry(self.player)
                    self.bee_anger_timers.append(Timer(5000,func = sprite.calm_down,repeat=False,autostart=True))

        for sprite in self.enemy_sprites:
            if pygame.FRect.colliderect(sprite.rect,self.player.rect):
                self.player.health -=1
                if self.player.health <0:
                    self.running = False
