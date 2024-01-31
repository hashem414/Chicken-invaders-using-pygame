# Import necessary modules and classes
import pygame
#We give it dimensions and use it with fungshins ready
class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,speed,screen_height):
		super().__init__()
		# Create a surface for the laser with dimensions 4x20 and fill it with an orange color
		self.image = pygame.Surface((4,20))
		self.image.fill('orange')
		# Set the initial position of the laser sprite and Set laser speed and height constraint (screen height)
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = screen_height

	def destroy(self):
		# Destroy (remove) the laser sprite if it goes beyond specified y-axis constraints
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		# Update the position of the laser sprite based on its speed
		self.rect.y += self.speed
		self.destroy()
