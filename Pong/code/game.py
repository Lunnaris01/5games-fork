from settings import * 
from paddle import Player, Bot
from ball import Ball
import random

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        # Entities
        self.ball = Ball(SIZE['ball'], SPEED['ball'], POS['ball'],self, self.all_sprites)
        self.ball.set_paddle_sprites(self.paddle_sprites)

        self.player = Player(SIZE['paddle'],SPEED['player'],POS['player'], self.all_sprites,self.paddle_sprites)
        self.bot_opponent =  Bot(SIZE['paddle'],SPEED['opponent'],POS['opponent'],self.ball,self.all_sprites,self.paddle_sprites)

        # Score
        self.score = (0,0)
        self.score_pos = (WINDOW_WIDTH/2,50)
        self.font = pygame.font.Font(path.join('fonts','Oxanium-Bold.ttf'))
        self.score_surface = self.font.render(f"{self.score[0]} : {self.score[1]}",True,'#FAFAFA')
        self.score_rect = self.score_surface.get_frect(midtop = self.score_pos)
        self.display_surface.blit(self.score_surface,self.score_rect)

    def display_score(self):
        self.score_surface = self.font.render(f"{self.score[0]} : {self.score[1]}",True,'#FAFAFA')
        self.score_rect = self.score_surface.get_frect(midtop = self.score_pos)
        text_surrounder = pygame.Surface((self.score_rect.width+10,self.score_rect.height+5)).convert_alpha()
        text_surrounder.fill((0,0,0,0))
        pygame.draw.rect(text_surrounder, '#FAFAFA', text_surrounder.get_rect(), 2,5)
        self.display_surface.blit(text_surrounder,text_surrounder.get_frect(center = self.score_rect.center).inflate(5,5).move(3,0))
        self.display_surface.blit(self.score_surface,self.score_rect)


    def run(self):
        while self.running:
            dt = self.clock.tick()/1000

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False


            self.update(dt)
            self.draw()
            self.display_score()

            pygame.display.update()


    def update(self,dt):
        for sprite in self.all_sprites:
            sprite.update(dt)

    def draw(self):
        self.display_surface.fill(COLORS['bg'])
        self.all_sprites.draw(self.display_surface)
    
    def reset_ball(self):
        self.ball.rect.center = POS['ball']
        self.ball.direction = pygame.Vector2(random.choice([1,-1]),random.randrange(-100,100)/100)
        
