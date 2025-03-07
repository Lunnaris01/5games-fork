from settings import *

class UI:
    def __init__(self, game):
        self.display_surface = pygame.display.get_surface()
        self.game = game
        self.font = pygame.font.Font(None,30)
        self.left = WINDOW_WIDTH / 2 - 100
        self.top = WINDOW_HEIGHT /2 + 50
        self.monster = game.monster
        self.available_monsters = self.get_available_monsters()
        self.currentmenu = 'general'
        self.general_options = ['attack','bag','switch','escape']
        self.general_options_func = {'attack':self.attack,'bag':self.bag,'switch':self.switch,'escape':self.escape}
        self.bag_options = ['heal','superpotion','pokeball','superball']
        self.bag_options_func = {'heal': self.heal, 'superpotion': self.superpotion, 'pokeball': self.pokeball,'superball': self.superball}
        self.menu_index = {'col': 0, 'row': 0}
        self.cols, self.rows = 2,2
        self.monster_menu_limit = 4
        self.monster_menu_index = 0


    def get_available_monsters(self):
        return [monster for monster in self.game.player_monsters if monster !=self.monster and monster.health>0]

    def menu(self,options):
        # bg
        rect = pygame.FRect(self.left + 40, self.top + 60, 400, 200)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0,4)
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4,4)
        # menu

        for col in range(self.cols):
            for row in range(self.rows):
                color = COLORS['black'] if col == self.menu_index['col'] and row == self.menu_index['row'] else COLORS['gray']
                x = rect.left + rect.width / (self.cols*2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows*2) + (rect.height / self.rows) * row
                text_surf = self.font.render(options[col*self.rows+row],True,color)
                text_rect = text_surf.get_frect(center = (x,y))
                self.display_surface.blit(text_surf,text_rect)

    def attack(self):
        self.menu(self.monster.abilities)

    def general(self):
        self.menu(self.general_options)
    
    def bag(self):
        self.menu(self.bag_options)

    def switch(self):
        # bg
        rect = pygame.FRect(self.left +40, self.top-100, 400, 400)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0,4)
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4,4)
        
        # menu
        player_monsters = self.available_monsters
        firstmonster = max(0,self.monster_menu_index-self.monster_menu_limit+1)
        lastmonster = min(len(player_monsters),firstmonster+self.monster_menu_limit)
        offset = firstmonster
        for i, monster in enumerate(player_monsters[firstmonster:lastmonster]):
            color = COLORS['black'] if i+offset == self.monster_menu_index else COLORS['gray']
            x = rect.centerx
            y = rect.top + rect.height / (self.monster_menu_limit * 2) + rect.height / self.monster_menu_limit *i
            text_surf = self.font.render(monster.name,True,color)
            text_rect = text_surf.get_frect(center = (x,y))
            self.display_surface.blit(text_surf,text_rect)
            simple_surf = self.game.simple_surfs[monster.name]
            simple_rect = simple_surf.get_frect(center = (x-150,y))
            self.display_surface.blit(simple_surf,simple_rect)

    def switch_monster(self):
        self.monster = self.available_monsters[self.monster_menu_index]
        self.game.switch_monster(self.monster)
        self.available_monsters = self.get_available_monsters()
        #self.currentmenu = 'general'




    def escape(self):
        self.game.running = False

    def heal(self):
        self.monster.health = min(self.monster.health + 20, 100)

    def superpotion(self):
        self.monster.health = min(self.monster.health + 50, 100)
    
    def superball(self):
        self.catch('superball')
    
    def pokeball(self):
        self.catch('pokeball')

    def catch(self, ball):
        print(f"Try to catch opponent with a {ball}")



    def draw(self):
        match self.currentmenu:
            case 'general':
                self.general()
            case 'attack':
                self.attack()
            case 'bag':
                self.bag()
            case 'switch':
                self.switch()
            case _:
                self.currentmenu = 'general'

    def update(self):
        return self.input()

    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.currentmenu == 'general':
            self.menu_index['row'] = (self.menu_index['row'] +int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))%self.rows
            self.menu_index['col'] = ( self.menu_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))%self.cols
        elif self.currentmenu == 'switch':
            self.monster_menu_index = (self.monster_menu_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))%len(self.available_monsters)


        if keys[pygame.K_SPACE]:
            index = self.menu_index['col']*self.rows+self.menu_index['row']
            if self.currentmenu == 'general':
                self.general_options_func[self.general_options[index]]()
                self.currentmenu = self.general_options[index]
            
            elif self.currentmenu == 'bag':
                self.bag_options_func[self.bag_options[index]]()
            elif self.currentmenu == 'switch':
                self.switch_monster()
        if keys[pygame.K_ESCAPE]:
            if self.currentmenu == 'general':
                return False
            else:
                self.currentmenu = 'general'
            
        return True
                
