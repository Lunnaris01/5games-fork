from settings import *
from pytmx.util_pygame import load_pygame
from player import Player
from sprites import Sprite, CollisionSprite, Gun, Bullet, Enemy
from groups import AllSprites
import random

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load Assets
        self.player_animations = {}
        for animation in ['down','left','right','up']:
            self.player_animations[animation]= [pygame.image.load(path.join('images','player',animation,frame)) for frame in listdir(path.join('images','player',animation))]
        self.enemy_animations = {}
        for enemy in ['bat','blob','skeleton']:
            self.enemy_animations[enemy] = [pygame.image.load(path.join('images','enemies',enemy,frame)) for frame in listdir(path.join('images','enemies',enemy))]
        self.enemy_spawnpoints = []
        self.enemy_spawntimer = 0
        self.game_music = pygame.mixer.Sound(path.join('audio','music.wav'))
        self.game_music.play(loops=-1)
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.player_starting_pos = PLAYER_DEFAULT_POS
        self.setup()


        # Keys
        self.keys = pygame.key.get_pressed()
        self.keys_justpressed = pygame.key.get_just_pressed()

    def setup(self):
        map = load_pygame(path.join('data','maps','world.tmx'))
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y),obj.image,self.all_sprites,self.collision_sprites)
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)).convert_alpha(),self.collision_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(self.player_animations,(obj.x,obj.y),self.collision_sprites,self.all_sprites)
                self.gun = Gun(self.player,self.all_sprites)
            if obj.name == 'Enemy':
                self.enemy_spawnpoints.append((obj.x,obj.y))

    def update(self,dt):
        self.refresh_keys()
        if pygame.mouse.get_just_pressed()[0]:
            self.gun.spawn_bullet(self.all_sprites,self.bullet_sprites)
        self.all_sprites.update(self.keys,self.keys_justpressed,dt)
        if self.enemy_spawntimer // ENEMY_SPAWNCOOLDOWN >0:
            self.enemy_spawntimer %= ENEMY_SPAWNCOOLDOWN
            
            enemy_type = random.sample(list(self.enemy_animations.keys()),1)[0]
            enemy_surf = self.enemy_animations[enemy_type]
            enemy_spawnpoint = random.sample(self.enemy_spawnpoints,1)[0]
            Enemy(enemy_spawnpoint,enemy_type,enemy_surf,self.bullet_sprites,self.collision_sprites,self.enemy_sprites,self.all_sprites)
        self.enemy_spawntimer += dt
        for enemy in self.enemy_sprites:
            enemy.move(self.player.rect.center,dt)
        player_alive = self.player.enemy_collision(self.enemy_sprites,dt)
        if not player_alive:
            self.running = False
    
    def draw(self):
        self.display_surface.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.player.rect.bottomright)

    def refresh_keys(self):
        self.keys = pygame.key.get_pressed()
        self.keys_justpressed = pygame.key.get_just_pressed()
