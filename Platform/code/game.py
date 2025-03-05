from settings import *
from pytmx.util_pygame import load_pygame
from os import path, listdir
from sprite import Sprite, Player, Worm
from group import AllSprites

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

        self.setup()

    def setup(self):
        map = load_pygame(path.join('data','maps','world.tmx'))
        for x,y,image in map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), image, True, self.all_sprites,self.collision_sprites)
        for x,y,image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image, True, self.all_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.player_animations,self.all_sprites)
                self.player.set_collision_sprites(self.collision_sprites)
            if obj.name == 'Worm':
                worm = Worm((obj.x,obj.y),(obj.width,obj.height),self.worm_animations,self.all_sprites,self.worm_sprites)

    def load_assets(self):
        self.player_animations = [pygame.image.load(path.join('images','player',frame)) for frame in sorted(listdir(path.join('images','player')))]
        self.worm_animations = [pygame.image.load(path.join('images','enemies','worm',frame)) for frame in sorted(listdir(path.join('images','enemies','worm')))]
        self.bee_animations = [pygame.image.load(path.join('images','enemies','bee',frame)) for frame in listdir(path.join('images','enemies','bee'))]
        self.gun_bullet_image = pygame.image.load(path.join('images','gun','bullet.png'))
        self.gun_fire_image = pygame.image.load(path.join('images','gun','fire.png'))

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)
            if not self.player.groups():
                break

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.topleft)
            pygame.display.update()
        
        pygame.quit()
