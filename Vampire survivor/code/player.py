from settings import * 

class Player(pygame.sprite.Sprite):
	def __init__(self, animations, pos, collision_sprites, *groups):
		super().__init__(*groups)
		self.animations = animations
		self.current_animation = self.animations['down']
		self.animation_index = 0
		self.image = self.current_animation[0]
		self.rect = self.image.get_frect(center = pos)
		self.mask = pygame.mask.from_surface(self.image)
		self.hitbox_rect = self.rect.inflate(-60,-30)

		self.direction = pygame.Vector2()
		self.last_dir_string = 'down'
		self.collision_sprites = collision_sprites
		
        # Game Logik:
		self.health = 100

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
    
	def enemy_collision(self,enemies,dt):
		collided =  pygame.sprite.spritecollide(self,enemies,False,pygame.sprite.collide_mask)
		for enemy in collided:
			self.health -= dt * enemy.get_damage()
			print("Player is taking damage. New Health: " + str(self.health))
			if self.health <=0:
				return False
		return True