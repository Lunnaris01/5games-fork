from settings import *
import pygame
from os import path, listdir


class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption("Vampire Survivor")
		self.clock = pygame.time.Clock()

		# Load Assets
		player_animations = {}
		for animation in ['down','left','right','up']:
			player_animations[animation]= [pygame.image.load(path.join('images','player',animation,x)) for x in listdir(path.join('images','player',animation))]

		self.all_sprites = pygame.sprite.Group()
		self.player = Player(player_animations,WIN_CENTER,self.all_sprites)
		self.running = True

		self.keys = pygame.key.get_pressed()
		self.keys_justpressed = pygame.key.get_just_pressed()

	def update(self,dt):
		self.all_sprites.update(self.keys,self.keys_justpressed,dt)

	def draw(self):
		self.display_surface.fill(BACKGROUND_COLOR)
		self.all_sprites.draw(game.display_surface)

	def refresh_keys(self):
		self.keys = pygame.key.get_pressed()
		self.keys_justpressed = pygame.key.get_just_pressed()





class Player(pygame.sprite.Sprite):
	def __init__(self, animations, pos, *groups):
		super().__init__(*groups)
		self.animations = animations
		self.current_animation = self.animations['down']
		self.image = self.current_animation[0]
		self.rect = self.image.get_frect(center = pos)
		self.direction = pygame.Vector2()
		self.last_dir_string = 'down'
		self.animation_index = 0

	def update(self,keys,keys_just_pressed,dt):
		self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
		self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
		self.set_current_animation()
		if self.direction.magnitude() != 0:
			self.animation_index = (self.animation_index + (dt * 8))%(len(self.current_animation)-1)
			self.image = self.current_animation[int(self.animation_index)]
		else:
			self.image = self.current_animation[2]
		self.rect.center += self.direction
	
	def set_current_animation(self):
		if self.direction.y>0:
			self._set_current_animation_helper('down')
		elif self.direction.y<0:
			self._set_current_animation_helper('up')
		elif self.direction.x>0:
			self._set_current_animation_helper('right')
		elif self.direction.x<0:
			self._set_current_animation_helper('left')
		
	def _set_current_animation_helper(self,direction):
		self.current_animation = self.animations[direction]
		if self.last_dir_string != direction:
			self.last_dir_string = direction
			self.animation_index = 0

# Init
game = Game()

while game.running:
	dt = game.clock.tick(200)/1000
	# Event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT or game.keys[pygame.K_ESCAPE]:
			game.running = False

	# Update Entities
	game.refresh_keys()
	game.update(dt)

	# Drawing
	game.draw()

	pygame.display.update()