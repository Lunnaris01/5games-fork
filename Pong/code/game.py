from settings import * 
from player import Player
from ball import Ball

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
        self.player = Player(SIZE['paddle'],SPEED['player'],POS['player'], self.all_sprites,self.paddle_sprites)
        self.ball = Ball(SIZE['ball'], SPEED['ball'], POS['ball'], self.all_sprites)
        self.ball.set_paddle_sprites(self.paddle_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick()/1000

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False


            self.update(dt)
            self.draw()

            pygame.display.update()


    def update(self,dt):
        for sprite in self.all_sprites:
            sprite.update(dt)

    def draw(self):
        self.display_surface.fill(COLORS['bg'])
        self.all_sprites.draw(self.display_surface)
