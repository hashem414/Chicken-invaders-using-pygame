# Import necessary modules and classes
import pygame
from laser import Laser
#We give it dimensions and use it with fungshins ready
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed):
		super().__init__()
		# Load player image from the file 'player.png'
		self.image = pygame.image.load('player.png').convert_alpha()
		# Set the initial position of the player sprite
		self.rect = self.image.get_rect(midbottom = pos)
		# Set player movement speed, constraints, and laser cooldown properties
		self.speed = speed
		self.max_x_constraint = constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 450
		# Create a sprite group to manage player laser
		self.lasers = pygame.sprite.Group()
		# Load laser sound and set volume
		self.laser_sound = pygame.mixer.Sound('laser.wav')
		self.laser_sound.set_volume(0.5)

	def get_input(self):
		keys = pygame.key.get_pressed()
		# Move player based on right and left arrow key input
		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		# Shoot laser when the spacebar is pressed and the player is ready
		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	# Recharge the player's ability to shoot lasers after the cooldown period
	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	# Keep the player within the specified x-axis constraints
	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint

	# Create a new laser sprite and add it to the player's laser group
	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

	# Update player based on user input and manage lasers
	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()
