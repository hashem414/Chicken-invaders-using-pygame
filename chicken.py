# Import necessary modules and classes
import pygame
from laser import Laser

#We give it dimensions and use it with fungshins ready
class Chicken(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load chicken image from the file 'enemy.png' and
        file_path = 'enemy.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = 1

    # Update the position of the chicken based on the specified direction
    def update(self, direction):
        self.rect.x += direction
