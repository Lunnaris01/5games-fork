from settings import *
import pygame
from os import path, listdir
from sprites import Sprite, CollisionSprite
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption("Vampire Survivor")
		self.clock = pygame.time.Clock()
		self.running = True

		# Load Assets
		player_animations = {}
		for animation in ['down','left','right','up']:
			player_animations[animation]= [pygame.image.load(path.join('images','player',animation,x)) for x in listdir(path.join('images','player',animation))]

		# Groups
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()

		self.player_starting_pos = PLAYER_DEFAULT_POS
		self.setup()

		# Player creation should happen after the Setup!
		self.player = Player(player_animations,self.player_starting_pos,self.collision_sprites,self.all_sprites)

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
				self.player_starting_pos = (obj.x,obj.y)

	def update(self,dt):
		self.all_sprites.update(self.keys,self.keys_justpressed,dt)

	def draw(self):
		self.display_surface.fill(BACKGROUND_COLOR)
		self.all_sprites.draw(self.player.rect.center)

	def refresh_keys(self):
		self.keys = pygame.key.get_pressed()
		self.keys_justpressed = pygame.key.get_just_pressed()


class Player(pygame.sprite.Sprite):
	def __init__(self, animations, pos, collision_sprites, *groups):
		super().__init__(*groups)
		self.animations = animations
		self.current_animation = self.animations['down']
		self.image = self.current_animation[0]
		self.rect = self.image.get_frect(center = pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.hitbox_rect = self.rect.inflate(-60,-100)

		self.direction = pygame.Vector2()
		self.last_dir_string = 'down'
		self.animation_index = 0
		self.collision_sprites = collision_sprites

	def update(self,keys,keys_just_pressed,dt):
		self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
		self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
		self.set_current_animation()
		if self.direction.magnitude() != 0:
			self.animation_index = (self.animation_index + (dt * 8))%(len(self.current_animation)-1)
			self.image = self.current_animation[int(self.animation_index)]
		else:
			self.image = self.current_animation[3]
		self.hitbox_rect.x += (self.direction.normalize().x if self.direction else self.direction.x)*dt*PLAYER_SPEED
		self.collision('horizontal',dt)
		self.hitbox_rect.y += (self.direction.normalize().y if self.direction else self.direction.y)*dt*PLAYER_SPEED
		self.collision('vertical',dt)
		self.rect.center = self.hitbox_rect.center

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

	def collision(self,direction,dt):
		#if pygame.sprite.spritecollide(self,self.collision_sprites,False,pygame.sprite.collide_rect):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.hitbox_rect):
				if direction == 'horizontal':
					self.hitbox_rect.x -= (self.direction.normalize().x if self.direction else self.direction.x)*dt*PLAYER_SPEED
				elif direction == 'vertical':
					self.hitbox_rect.y -= (self.direction.normalize().y if self.direction else self.direction.y)*dt*PLAYER_SPEED
				else:
					raise KeyError("Unknown direction for collision")

# Init
game = Game()

while game.running:
	dt = game.clock.tick()/1000
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