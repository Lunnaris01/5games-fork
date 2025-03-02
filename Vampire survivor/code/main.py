from settings import *
import pygame
from os import path, listdir
from sprites import CollisionSprite
from random import randint
from pytmx.util_pygame import load_pygame

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
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# Keys
		self.keys = pygame.key.get_pressed()
		self.keys_justpressed = pygame.key.get_just_pressed()

		# Entities - Note that collision_sprites is just given to the player as argument, it is NOT part of the groups!
		self.player = Player(player_animations,WIN_CENTER,self.collision_sprites,self.all_sprites)

		for i in range(6):
			pos = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT))
			size = (randint(60,100),randint(40,60))
			CollisionSprite(pos, size, self.all_sprites, self.collision_sprites)

	def update(self,dt):
		self.all_sprites.update(self.keys,self.keys_justpressed,dt)

	def draw(self):
		self.display_surface.fill(BACKGROUND_COLOR)
		self.all_sprites.draw(game.display_surface)

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
		self.hitbox_rect = self.rect.inflate(-50,0)

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
		self.hitbox_rect.x += self.direction.normalize().x if self.direction else self.direction.x
		self.collision('horizontal')
		self.hitbox_rect.y += self.direction.normalize().y if self.direction else self.direction.y
		self.collision('vertical')
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

	def collision(self,direction):
		#if pygame.sprite.spritecollide(self,self.collision_sprites,False,pygame.sprite.collide_rect):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.hitbox_rect):
				print('collision')
				if direction == 'horizontal':
					self.hitbox_rect.x -= self.direction.normalize().x if self.direction else self.direction.x
				elif direction == 'vertical':
					self.hitbox_rect.y -= self.direction.normalize().y if self.direction else self.direction.y
				else:
					raise KeyError("Unknown direction for collision")

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