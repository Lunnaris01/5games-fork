from settings import *
from random import sample

class Creature:
    def get_data(self, name):
        self.element = MONSTER_DATA[name]['element']
        self.health = self.max_health = MONSTER_DATA[name]['health']
        self.abilities = sample(list(ABILITIES_DATA.keys()),4)
        self.name = name
        print(self.abilities)


class Monster(pygame.sprite.Sprite,Creature):
    def __init__(self,name,surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(bottomleft = (100, WINDOW_HEIGHT))
        self.get_data(name)


class Opponent(pygame.sprite.Sprite,Creature):
    def __init__(self, name, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = (WINDOW_WIDTH -250,300))
        self.get_data(name)