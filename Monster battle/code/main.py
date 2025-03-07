from settings import *
from support import *
from timer import Timer
from monster import Monster, Opponent
from ui import UI
import random

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True

        # Imports
        self.import_assets()

        # groups 
        self.all_sprites = pygame.sprite.Group()

        # data
        player_monster_list = ['Sparchu','Cleaf','Jacana','Gulfin','Pouch','Larvea']
        self.player_monsters  = [Monster(name,self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = random.choice(list(self.front_surfs.keys()))
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

        # UI
        self.ui = UI(self)


    def import_assets(self):
        self.back_surfs = folder_importer('images','back')
        self.bg_surfs = folder_importer('images', 'other')
        self.front_surfs = folder_importer('images','front')
        self.simple_surfs = folder_importer('images','simple')


    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0,-10))
            self.display_surface.blit(self.bg_surfs['floor'],floor_rect)

    def switch_monster(self,monster):
        self.all_sprites.remove(self.monster)
        self.all_sprites.add(monster)
        self.monster = monster


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            # update
            self.all_sprites.update(dt)
            keeprunning = self.ui.update()
            if not keeprunning:
                self.running = False
            # draw  
            self.display_surface.blit(self.bg_surfs['bg'],(0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Game()
    game.run()