import secrets
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Alien management"""

    def __init__(self, ai_game):
        """Initialize alien and set its starting position"""
        # Copy some stuff over
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Image loading + rectangle
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Top left placement
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Exact position
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
