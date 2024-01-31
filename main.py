# Import necessary modules and classes
import pygame
import sys
from player import Player
from chicken import Chicken
from random import choice

# Game class that manages the overall game state
class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set up the game window
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Chicken Invaders')

        # Load the game background
        self.background = pygame.image.load('background.png').convert()

        # Create the player sprite and group
        player_sprite = Player((self.screen_width / 2, self.screen_height -80), self.screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Initialize lives, score, and fonts
        self.lives = 3
        self.live_surf = pygame.image.load('player.png').convert_alpha()
        self.live_x_start_pos = self.screen_width - (self.live_surf.get_size()[0] * 3 + 20)
        self.score = 0
        self.font = pygame.font.Font('Pixeled.ttf', 20)

        # Create the chickens sprite group and set initial direction
        self.chickens = pygame.sprite.Group()
        self.chicken_setup(rows=6, cols=8)
        self.chicken_direction = 1

        # Game over setup
        self.game_over = False
        self.game_over_font = pygame.font.Font('Pixeled.ttf', 40)
        self.play_again_font = pygame.font.Font('Pixeled.ttf', 20)

        # Audio setup
        music = pygame.mixer.Sound('music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('explosion.wav')
        self.explosion_sound.set_volume(0.3)

    # Method to set up the initial positions of the chickens
    def chicken_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + 65
                y = row_index * y_distance + 65

                chicken_sprite = Chicken(x, y)
                self.chickens.add(chicken_sprite)

    # Method to check and update the position of chickens based on screen boundaries
    def chicken_position_checker(self):
        all_chickens = self.chickens.sprites()
        for chicken in all_chickens:
            if chicken.rect.right >= self.screen_width:
                self.chicken_direction = -1
                self.chicken_move_down(2)
            elif chicken.rect.left <= 0:
                self.chicken_direction = 1
                self.chicken_move_down(2)

    # Method to move all chickens down by a specified distance
    def chicken_move_down(self, distance):
        if self.chickens:
            for chicken in self.chickens.sprites():
                chicken.rect.y += distance

    # Method to handle collision checks between player lasers and chickens
    def collision_checks(self):

        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                chickens_hit = pygame.sprite.spritecollide(laser, self.chickens, True)
                if chickens_hit:
                    for chicken in chickens_hit:
                        self.score += chicken.value
                    laser.kill()
                    self.explosion_sound.play()


                    if not self.chickens.sprites():
                        self.reset_chickens()


        player_hit = pygame.sprite.spritecollide(self.player.sprite, self.chickens, True)
        if player_hit:
            self.player_hit()

    # Method to reset the position and direction of chickens
    def reset_chickens(self):
        self.chickens.empty()
        self.chicken_setup(rows=6, cols=8)
        self.chicken_direction *= 3

    # Method to handle player getting hit by chickens
    def player_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    # Method to display the remaining lives
    def display_lives(self):
        for live in range(self.lives ):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            self.screen.blit(self.live_surf, (x, 8))

    # Method to display the current score
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        self.screen.blit(score_surf, score_rect)

    # Method to display victory message if all chickens are defeated
    def victory_message(self):
        if not self.chickens.sprites():
            victory_surf = self.font.render('You won', False, 'white')
            victory_rect = victory_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            self.screen.blit(victory_surf, victory_rect)

    # Method to display the game over screen
    def display_game_over(self):
        game_over_surf = self.game_over_font.render('Game Over', False, 'blue')
        game_over_rect = game_over_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 30))
        self.screen.blit(game_over_surf, game_over_rect)

        play_again_surf = self.play_again_font.render('Play Again? (Y/N)', False, 'blue')
        play_again_rect = play_again_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 30))
        self.screen.blit(play_again_surf, play_again_rect)

        pygame.display.flip()
        # Wait for user input after game over
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.reset_game()
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

    # Method to reset the game state
    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.player.sprite.rect.x = self.screen_width / 2
        self.player.sprite.rect.y = self.screen_height - 80
        self.chickens.empty()
        self.chicken_setup(rows=6, cols=8)

    # Main game loop
    def run(self):
        if not self.game_over:

            self.screen.blit(self.background, (0, 0))

            self.player.update()
            self.chickens.update(self.chicken_direction)
            self.chicken_position_checker()
            self.collision_checks()

            self.player.sprite.lasers.draw(self.screen)
            self.player.draw(self.screen)
            self.chickens.draw(self.screen)
            self.display_lives()
            self.display_score()
            self.victory_message()
        else:
            self.display_game_over()


if __name__ == '__main__':
    game = Game()



    clock = pygame.time.Clock()
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        game.run()

        pygame.display.flip()
        clock.tick(60)
