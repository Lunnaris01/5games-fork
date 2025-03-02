from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()


    def draw(self,campos):
        self.offset.x = -campos[0] + WINDOW_WIDTH/2
        self.offset.y = -campos[1] + WINDOW_HEIGHT/2
        
        background_sprites = [sprite for sprite in self if hasattr(sprite,'background')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite,'background')]


        for sprite in background_sprites:
            self.display_surface.blit(sprite.image,sprite.rect.center + self.offset)
        for sprite in sorted(object_sprites,key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image,sprite.rect.center + self.offset)
